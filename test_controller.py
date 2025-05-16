from PySide6.QtCore import QObject, Signal
import constants
from device import Device
from arduino import AIODevice
from constants import KEY_DEBUG, KEY_TESTING_SPEED, DEFAULT_SETTINGS
from typing import Dict, Any, List, Callable  # Added Callable
from globals import logger as log  # Use the global logger instance
from settings import get_instance  # Use the global settings instance accessor
import config_loader  # Keep for get_instance()
import asyncio
import enum


class TestState(enum.Enum):
    """
    Enum representing the internal states of the TestController during test execution.
    """

    IDLE = enum.auto()  # Controller is inactive, ready for a test.
    RUNNING = enum.auto()  # Test sequence is actively executing steps.
    AWAITING_RELAY = enum.auto()  # Paused, waiting for a specific input signal (historically relay). Renamed to AWAITING_INPUT in newer constants.
    AWAITING_BUTTON = enum.auto()  # Paused, waiting for user confirmation via button press.
    FINISHED = enum.auto()  # Test sequence completed (pass or fail determined later).
    ERROR = enum.auto()  # An unexpected error occurred during the test.


class MessageType(enum.Enum):
    INFO = enum.auto()  # General informational message.
    WARNING = enum.auto()  # Warning message.
    ERROR = enum.auto()  # Error message (often non-fatal to test sequence).
    NOTICE = enum.auto()  # Notable event or status update.
    DEBUG = enum.auto()  # Debugging information.
    TEST_STARTED = enum.auto()  # Signals the beginning of a test run. Data: model name (str).
    TEST_FINISHED = enum.auto()  # Signals the end of a test run. Data: success (bool).
    TEST_PROGRESS = enum.auto()  # General progress message during the test. Data: message (str). Deprecated, use APPEND_TEXT.
    TEST_PASSED = enum.auto()  # Signals the test completed successfully. Data: final message (str).
    TEST_FAILED = enum.auto()  # Signals the test failed. Data: failure reason (str).
    TEST_ERROR = enum.auto()  # Signals an unexpected error during the test. Data: error details (str).
    WAITING_FOR_INPUT = enum.auto()  # Signals the controller is waiting for hardware input. Data: pin function (str).
    WAITING_FOR_BUTTON = enum.auto()  # Signals the controller is waiting for user button press. Data: prompt text (str).
    APPEND_TEXT = enum.auto()  # Instructs the UI to append text to the main display. Data: text (str).
    INPUT_OK = enum.auto()  # Signals that the expected input was received. Data: pin function (str).
    INPUT_FAIL = enum.auto()  # Signals that input was received but didn't match expected, or timed out. Data: pin function (str).


class ControllerMessage:
    """
    Class representing a message emitted by the TestController to the UI or other components.
    Contains a type (ControllerMessageType) and an optional payload (object).
    """

    def __init__(self, msg_type: MessageType, payload: str = ""):
        self.type = msg_type  # Type of message (ControllerMessageType)
        self.data = payload  # Optional payload (str)


class TestController(QObject):
    """
    Manages and executes the automated test sequence for a selected V40Device.

    This class reads the test steps from `config.yaml`, interacts with the
    `AIODevice` to control the test fixture hardware, and communicates
    progress, results, and required user interactions back to the `MainWindow`
    via Qt signals.
    """

    # --- Signals ---
    # @Deprecated: Use sendMessage with specific ControllerMessage types instead. Kept for potential compatibility if needed.
    testStarted = Signal(str)
    updateText = Signal(str)
    testProgress = Signal(str, int)
    testFinished = Signal(bool, str)
    waitingForInput = Signal(str, str)
    waitingForButton = Signal(str)
    errorOccurred = Signal(str)

    # Consolidated signal for all communication with the UI.
    sendMessage = Signal(ControllerMessage)  # Emits messages with type (ControllerMessage) and payload (object).

    def __init__(self, aio_device: AIODevice, settings=None, parent: QObject = None):
        """
        Initializes the TestController.

        Args:
            aio_device: An instance of AIODevice for hardware interaction.
            settings: An optional ApplicationSettings instance. If None, uses globals.get_settings().
            parent: The parent QObject, typically the MainWindow.
        """
        super().__init__(parent)

        # Assign settings instance
        self.settings = settings or get_instance()

        self._aio_device = aio_device
        self.debug = self.settings.get_bool(KEY_DEBUG, False)  # Get debug flag from settings

        # Load configuration using the global singleton accessor
        self._config_loader = config_loader.get_instance()
        print(self._config_loader)
        self._test_sequence: List[Dict[str, Any]] = []  # Initialize empty
        self._load_config()  # Load initial config

        # State variables
        self._current_device: Device | None = None
        self._state: TestState = TestState.IDLE
        self._input_event = asyncio.Event()  # Event for synchronizing waits

        # Variables for tracking the current 'wait_for_input' step
        self._current_wait_step: Dict[str, Any] | None = None
        self._input_received_value: Any | None = None

        # Mapping from configuration action strings to handler methods
        self._action_handlers: Dict[str, Callable] = {
            "message": self._handle_message,
            "write_pin": self._handle_write_pin,
            "write_pin_direct": self._handle_write_pin_direct,
            "delay": self._handle_delay,
            "wait_for_input": self._handle_wait_for_input,
            "wait_for_button": self._handle_wait_for_button,
        }

        # Log if test sequence is initially empty
        if not self._test_sequence:
            log.warning("No test sequence found in config.yaml on initialization!")

    def _load_config(self) -> bool:
        """Loads or reloads the test sequence configuration. Returns True on success."""
        try:
            loaded = self._config_loader.reload()  # Use reload method from ConfigLoader
            if loaded:
                self._test_sequence = self._config_loader.test_sequence  # Get the test sequence from the config loader
            if not self._test_sequence:
                log.warning("Test sequence loaded but is empty.")
            else:
                log.info(f"Successfully loaded test sequence with {len(self._test_sequence)} steps.")
            return True
            # else:
            #     log.error("ConfigLoader failed to reload configuration.")
            #     self._test_sequence = []
            #     return False
        except Exception as e:
            log.exception("Exception during configuration loading.")
            self._test_sequence = []
            return False

    # --- Properties ---
    @property
    def state(self) -> TestState:
        """Returns the current state of the test controller."""
        return self._state

    @property
    def is_busy(self) -> bool:
        """Returns True if the controller is currently running a test or waiting."""
        return self._state not in [TestState.IDLE, TestState.FINISHED, TestState.ERROR]

    def _reset_state(self):
        """Resets the controller's internal state variables after a test run or error."""
        if self.debug:
            log.debug("Resetting TestController state.")
        self._state = TestState.IDLE
        self._input_event.clear()
        # Don't clear _current_device here, keep it until the next run starts
        self._current_wait_step = None
        self._input_received_value = None
        # Detach any potentially lingering callbacks (defensive)
        # Note: This assumes only one input callback can be active at a time.
        # If multiple simultaneous waits were needed, this logic would need adjustment.
        if hasattr(self, '_last_attached_pin') and self._last_attached_pin is not None:
            try:
                self._aio_device.detach_callback(self._last_attached_pin)
                log.debug(f"Detached lingering callback from pin {self._last_attached_pin}")
            except Exception as e:
                log.warning(f"Error detaching lingering callback from pin {self._last_attached_pin}: {e}")
            self._last_attached_pin = None  # Reset tracker

    async def _cleanup_pins(self):
        """Executes the 'cleanup' sequence defined in the configuration file."""
        if self.debug:
            log.debug("Executing configured cleanup sequence...")
        cleanup_sequence = self._config_loader.get_cleanup_sequence()  # Assumes method exists in ConfigLoader
        if not cleanup_sequence:
            log.warning("No cleanup sequence found in configuration.")
            return

        # Ensure _current_device is set for condition checking during cleanup
        if not self._current_device:
            log.warning("Cannot execute cleanup sequence: No current device context.")
            # Fallback: try setting all known output pins low? Less ideal.
            # await self._aio_device.set_all_pins_to_value(0) # Example fallback
            return

        for step in cleanup_sequence:
            # Check conditions based on the device model used in the *last* test run
            if self._should_execute_step(step):
                try:
                    action_type = step.get("action")
                    if action_type in self._action_handlers:
                        handler = self._action_handlers[action_type]
                        if self.debug:
                            log.debug(f"Running cleanup step: {step}")
                        await handler(step)  # Execute the cleanup action
                    else:
                        log.warning(f"Unknown action type '{action_type}' in cleanup step: {step}")
                except Exception as e:
                    # Log errors during cleanup but don't stop other cleanup steps
                    log.error(f"Error during configured cleanup step {step}: {e}")
        if self.debug:
            log.debug("Cleanup sequence finished.")

    # --- Main Test Execution Logic ---
    async def async_run_test(self, device: Device):
        """
        Starts and executes the configured test sequence asynchronously for the given device.

        Args:
            device: The Device instance representing the selected model and program.
        """
        self.debug = self.settings.get_bool(KEY_DEBUG, False)

        # 1. Pre-checks
        if self.is_busy:
            log.warning("TestController.async_run_test called while busy.")
            self.sendMessage.emit(ControllerMessage(MessageType.WARNING, "TestController.async_run_test called while busy."))
            return

        # Reload config and ensure sequence exists
        if not self._load_config() or not self._test_sequence:
            log.error("Cannot run test: Test sequence missing or failed to load.")
            self.sendMessage.emit(ControllerMessage(MessageType.ERROR, "Test sequence missing or failed to load."))
            return

        # 2. Initialization
        self._current_device = device  # Set the device for this run
        self._reset_state()  # Reset state variables from previous runs
        self._state = TestState.RUNNING
        # model = self._current_device.model
        log.info(f"Starting test sequence for {device}")
        # self.testStarted.emit(device)  # Emit legacy signal if needed
        self.sendMessage.emit(ControllerMessage(MessageType.TEST_STARTED))

        try:
            # --- 3. Execute Test Steps ---
            for i, step in enumerate(self._test_sequence, 1):
                if self.debug:
                    log.debug(f"Processing Step {i}/{len(self._test_sequence)}: {step}")

                progress = i / len(self._test_sequence) * 100
                self.testProgress.emit(f"Executing step {i}/{len(self._test_sequence)}", int(progress))  # Legacy signal

                # Check conditional execution flags (if_has, if_missing)
                if not self._should_execute_step(step):
                    if self.debug:
                        log.debug(f"Skipping step {i} due to condition.")
                    continue

                # Find and execute the handler for the step's action
                action_type = step.get("action")
                if action_type in self._action_handlers:
                    handler = self._action_handlers[action_type]
                    await handler(step)  # Await the handler's completion
                else:
                    log.warning(f"Unknown action type '{action_type}' in step {i}: {step}")
                    # Optionally emit an error or warning message
                    self.sendMessage.emit(ControllerMessage(MessageType.WARNING, f"Unknown test action: {action_type}"))

            # --- 4. Test Completion (Success) ---
            log.info(f"Test sequence completed successfully for {self._current_device}.")
            self._state = TestState.FINISHED
            success_message = f"Test for {self._current_device} Passed"
            self.testFinished.emit(True, success_message)  # Legacy signal
            self.sendMessage.emit(ControllerMessage(MessageType.TEST_PASSED, success_message))  # Consolidated signal

        # --- 5. Error Handling ---
        except asyncio.TimeoutError as e:
            # Specific handling for timeouts during waits
            step_info = f" during step: {self._current_wait_step}" if self._current_wait_step else ""
            log.error(f"Timeout occurred{step_info}")
            fail_msg = (
                self._current_wait_step.get("message_on_fail", f"Timeout waiting for {self.state.name}")
                if self._current_wait_step
                else "Operation timed out"
            )
            self.errorOccurred.emit(fail_msg)  # Legacy signal
            self._state = TestState.ERROR
            self.testFinished.emit(False, f"Test Failed: {fail_msg}")  # Legacy signal
            self.sendMessage.emit(ControllerMessage(MessageType.TEST_ERROR, fail_msg))  # Consolidated signal
        except Exception as e:
            # General exception handling for errors during step execution
            log.exception(f"Unexpected error during test for {self._current_device}: {e}")
            error_details = f"Unexpected error: {e}"
            self.errorOccurred.emit(error_details)  # Legacy signal
            self._state = TestState.ERROR
            self.testFinished.emit(False, f"Test Failed: {error_details}")  # Legacy signal
            self.sendMessage.emit(ControllerMessage(MessageType.TEST_ERROR, error_details))  # Consolidated signal
        except asyncio.CancelledError:
            log.info("Test interrupted by user")
            self.sendMessage.emit(ControllerMessage(MessageType.NOTICE, "Test interrupted by user."))
            self._state = TestState.ERROR

        finally:
            # --- 6. Cleanup ---
            if self.debug:
                log.debug("Entering test cleanup phase.")
            await self._cleanup_pins()  # Execute cleanup actions
            # Reset state *after* cleanup, emit final finished message based on outcome
            final_state = self._state  # Capture state before reset
            self._reset_state()
            # Emit the final overall finished signal *after* cleanup and reset
            self.sendMessage.emit(
                ControllerMessage(MessageType.TEST_FINISHED, f"Test finished with state: {final_state.name}")
            )  # Consolidated signal

    def _should_execute_step(self, step: Dict[str, Any]) -> bool:
        """
        Determines if a given test step should be executed based on the
        `if_has` and `if_missing` conditions in the step definition and the
        features of the `_current_device`.

        Args:
            step: The test step dictionary from the configuration.

        Returns:
            True if the step should be executed, False otherwise.
        """

        return True  # Not implemented with this version

        if self._current_device is None:
            log.warning("Cannot check step condition: No current device set.")
            return False  # Cannot execute without device context

        model = self._current_device
        execute = True

        # Check 'if_has' condition: Step runs only if ALL specified features are True on the model.
        if "if_has" in step:
            required_features = step["if_has"]
            if not isinstance(required_features, list):
                required_features = [required_features]
            # Check if all required features exist and are True on the model object
            execute = all(hasattr(model, feature) and getattr(model, feature, False) for feature in required_features)
            if not execute:
                if self.debug:
                    log.debug(f"Step skipped: Missing required feature(s) {required_features}")
                return False  # Skip early if 'if_has' fails

        # Check 'if_missing' condition: Step runs only if ALL specified features are False on the model.
        # This check only happens if the 'if_has' condition (if present) passed.
        if "if_missing" in step:  # No need for 'execute and' because if 'if_has' failed, we returned False already
            missing_features = step["if_missing"]
            if not isinstance(missing_features, list):
                missing_features = [missing_features]
            # Check if any of the specified features exist and are True on the model object
            # If *any* are True, the condition fails (step is skipped).
            if any(hasattr(model, feature) and getattr(model, feature, False) for feature in missing_features):
                execute = False
                log.debug(f"Step skipped: Found disallowed feature(s) {missing_features}")

        return execute

    # --- Action Handler Methods ---

    async def _handle_message(self, step: Dict[str, Any]):
        """Handles the 'message' action: formats and emits text to the UI."""
        text = step.get("text", "")
        if self._current_device:
            try:
                # Format the message using the current device's model name
                text = text.format(model_name=self._current_device.name)
            except KeyError as e:
                log.warning(f"Placeholder key error in message '{text}': {e}. Leaving as is.")
        # Emit the formatted text for UI display
        print(f"Message: {text}")
        self.updateText.emit(text)  # Legacy
        self.sendMessage.emit(ControllerMessage(MessageType.APPEND_TEXT, text))

    async def _handle_write_pin(self, step: Dict[str, Any]):
        """Handles the 'write_pin' action: writes a value to a pin identified by its function."""
        pin_function = step.get("function")
        value_str = step.get("value")  # Value from YAML might be int or str representation
        if pin_function is None or value_str is None:
            log.warning(f"Missing 'function' or 'value' in write_pin step: {step}")
            return
        try:
            value = int(value_str)  # Ensure value is an integer (0 or 1)
            if value not in [0, 1]:
                raise ValueError("Pin value must be 0 or 1")
            if self.debug:
                log.debug(f"Writing pin func '{pin_function}' to {value}")
            await self._aio_device.write_pin_by_func(pin_function, value)
        except ValueError as e:
            log.error(f"Invalid value '{value_str}' for pin function '{pin_function}': {e}")
        except Exception as e:
            log.error(f"Failed to write pin function '{pin_function}': {e}")
            raise  # Re-raise hardware errors to potentially stop the test

    async def _handle_write_pin_direct(self, step: Dict[str, Any]):
        """Handles the 'write_pin_direct' action: writes a value to a specific pin number."""
        pin_number_str = step.get("pin")
        value_str = step.get("value")
        if pin_number_str is None or value_str is None:
            log.warning(f"Missing 'pin' or 'value' in write_pin_direct step: {step}")
            return
        try:
            pin_number = int(pin_number_str)
            value = int(value_str)
            if value not in [0, 1]:
                raise ValueError("Pin value must be 0 or 1")
            if self.debug:
                log.debug(f"Writing direct pin {pin_number} to {value}")
            await self._aio_device.digital_write(pin_number, value)
        except ValueError as e:
            log.error(f"Invalid pin number '{pin_number_str}' or value '{value_str}': {e}")
        except Exception as e:
            log.error(f"Failed to write direct pin {pin_number_str}: {e}")
            raise  # Re-raise hardware errors

    async def _handle_delay(self, step: Dict[str, Any]):
        """Handles the 'delay' action: pauses execution for a specified duration."""
        # Get default delay from settings, fallback to constants if not found
        default_speed_ms = self.settings.get_int(KEY_TESTING_SPEED, DEFAULT_SETTINGS[KEY_TESTING_SPEED])
        # Get specific duration from step, or use default
        duration_ms = step.get("duration_ms", default_speed_ms)
        try:
            duration_s = int(duration_ms) / 1000.0
            if duration_s < 0:
                log.warning(f"Negative delay requested ({duration_ms}ms), using 0s.")
                duration_s = 0
            if self.debug:
                log.debug(f"Delaying for {duration_s:.3f} seconds")
            await asyncio.sleep(duration_s)
        except (ValueError, TypeError):
            log.error(f"Invalid duration '{duration_ms}' specified for delay step: {step}. Using default.")
            # Fallback to default delay in case of error
            await asyncio.sleep(default_speed_ms / 1000.0)

    async def _handle_wait_for_input(self, step: Dict[str, Any]):
        """Handles the 'wait_for_input' action: waits for a specific input pin to reach an expected state."""
        # --- 1. Extract Parameters ---
        pin_function = step.get("function")
        expected_value = step.get("expected_value")  # Value can be int (0, 1) or None (any change)
        timeout_key = step.get("timeout_key")
        message_on_fail = step.get("message_on_fail", f"Timeout waiting for {pin_function}.")
        message_on_pass = step.get("message_on_pass", f"Input received on {pin_function}.")
        fail_on_timeout = step.get("fail_on_timeout", False)
        fail_on_mismatch = step.get("fail_on_mismatch", False)

        # --- 2. Validate Parameters ---
        if pin_function is None or timeout_key is None:  # expected_value can be None
            log.error(f"Missing 'function' or 'timeout_key' in wait_for_input step: {step}")
            raise ValueError(f"Invalid wait_for_input step config: {step}")

        pin_number = self._aio_device.get_pin_by_function(pin_function)
        if pin_number is None:
            log.error(f"Pin function '{pin_function}' not found in device configuration.")
            raise ValueError(f"Pin function '{pin_function}' not found")

        try:  # Validate expected_value if not None
            if expected_value is not None:
                expected_value = int(expected_value)
        except ValueError:
            log.error(f"Invalid 'expected_value' in wait_for_input step: {step}")
            raise ValueError(f"Invalid expected_value for {pin_function}")

        timeout_sec = self.settings.get_int(timeout_key, DEFAULT_SETTINGS.get(timeout_key, 10))
        if self.debug:
            log.debug(f"Wait timeout set to {timeout_sec}s for {pin_function} (from key: {timeout_key})")

        # --- 3. Setup Wait ---
        prompt = step.get("text", f"Waiting for input on {pin_function}...")
        if "text" in step:
            await self._handle_message(step)  # Show initial prompt if provided
        self.waitingForInput.emit(pin_function, prompt)  # Legacy signal
        self.sendMessage.emit(ControllerMessage(MessageType.WAITING_FOR_INPUT, prompt))
        self._input_event.clear()
        self._state = TestState.AWAITING_RELAY  # Consider renaming state to AWAITING_INPUT
        self._current_wait_step = step  # Store step details for the callback
        self._input_received_value = None  # Reset received value
        input_match = False  # Track if received value matched expectation
        self._last_attached_pin = pin_number  # Track for defensive detachment

        self._aio_device.attach_callback(self._generic_input_handler, pin_number)
        log.info(f"Waiting for input on pin {pin_number} (func: {pin_function}), expecting: {expected_value}, timeout: {timeout_sec}s")

        # --- 4. Execute Wait ---
        try:
            await asyncio.wait_for(self._input_event.wait(), timeout=timeout_sec)
            # --- Input Received ---
            log.info(f"Input event triggered for {pin_function}. Received value: {self._input_received_value}")
            # Check if the received value matches the expectation (if expectation is set)
            if expected_value is None or self._input_received_value == expected_value:
                input_match = True
                log.info(f"Input value matched expectation ({expected_value}).")
                self.updateText.emit(message_on_pass)  # Legacy
                self.sendMessage.emit(ControllerMessage(MessageType.INPUT_OK, pin_function))
                # self.sendMessage.emit(ControllerMessage.APPEND_TEXT, message_on_pass)
            else:
                # Value received but did not match expectation
                input_match = False
                mismatch_msg = f"Input value mismatch on {pin_function}: received {self._input_received_value}, expected {expected_value}."
                log.warning(mismatch_msg)
                self.updateText.emit(mismatch_msg)  # Legacy
                self.sendMessage.emit(ControllerMessage(MessageType.INPUT_FAIL, pin_function))  # Signal failure type
                # self.sendMessage.emit(ControllerMessage.APPEND_TEXT, mismatch_msg)
                if fail_on_mismatch:
                    log.error("Failing test due to input value mismatch.")
                    raise ValueError(mismatch_msg)  # Raise error to fail the test run

        # --- 5. Handle Timeout ---
        except asyncio.TimeoutError:
            log.warning(f"Timeout occurred while waiting for input on {pin_function}.")
            self.updateText.emit(message_on_fail)  # Legacy
            self.sendMessage.emit(ControllerMessage(MessageType.INPUT_FAIL, pin_function))  # Signal failure type
            # self.sendMessage.emit(ControllerMessage(MessageType.APPEND_TEXT, message_on_fail))
            if fail_on_timeout:
                log.error("Failing test due to input timeout.")
                raise  # Re-raise the TimeoutError to fail the test run

        # --- 6. Cleanup Wait ---
        finally:
            if self.debug:
                log.debug(f"Detaching input handler from pin {pin_number} for {pin_function}")
            self._aio_device.detach_callback(pin_number)
            self._last_attached_pin = None
            self._state = TestState.RUNNING  # Transition back to running state
            self._current_wait_step = None
            self._input_received_value = None
            # self._input_event.clear() # Already cleared or handled by wait_for

    def _generic_input_handler(self, data: list):
        """
        Internal callback attached to AIODevice for input pins during 'wait_for_input'.
        It receives data from AIODevice, extracts pin and value, checks if it's the
        pin currently being waited for, stores the value, and sets the asyncio event.

        Args:
            data: The data list received from AIODevice (expected: [pin_number, value]).
        """
        # Ignore callbacks if not in the correct state or if step info is missing
        if self._state != TestState.AWAITING_RELAY:
            return
        if not self._current_wait_step:
            return

        try:
            # --- Extract data based on AIODevice callback format ---
            if not data or len(data) < 2:
                log.warning(f"Received malformed input data in _generic_input_handler: {data}")
                return
            pin_number = data[0]
            value = data[1]  # Assume format [pin_number, value]
            # ---

            # Check if this input corresponds to the pin we are currently waiting for
            expected_pin = self._aio_device.get_pin_by_function(self._current_wait_step["function"])

            if pin_number == expected_pin:
                if self.debug:
                    log.debug(f"Input handler received: Pin={pin_number}, Value={value} (Waiting step: {self._current_wait_step.get('function')})")
                self._input_received_value = value  # Store the received value

                # Signal the asyncio event that *some* input was received on the target pin.
                # The value check happens *after* the wait_for completes.
                if not self._input_event.is_set():
                    self._input_event.set()
            # else: # Optional: Log input on other pins while waiting? Can be noisy.
            #     log.debug(f"Input handler received data for non-waiting pin {pin_number} while waiting for {expected_pin}")

        except Exception as e:
            log.exception(f"Error in _generic_input_handler: {e}")

    async def _handle_wait_for_button(self, step: Dict[str, Any]):
        """Handles the 'wait_for_button' action: pauses execution until notified by the UI."""

        # --- 1. Extract Parameters ---
        timeout_ms = step.get("timeout_ms")
        timeout_key = step.get("timeout_key")  # Takes precedence over timeout_ms

        if timeout_key:
            timeout_sec = self.settings.get_int(timeout_key, DEFAULT_SETTINGS.get(timeout_key, 20))
            if timeout_ms:
                log.warning("Both 'timeout_ms' and 'timeout_key' specified in wait_for_button step. Using 'timeout_key'.")
        elif timeout_ms and timeout_key is None:
            timeout_sec = timeout_ms / 1000.0
        else:  # No timeout specified
            log.warning("No timeout specified for wait_for_button step. Using default.")
            timeout_sec = DEFAULT_SETTINGS.get(constants.KEY_BUTTON_TIMEOUT, 20)  # Default to 20 seconds

        if self.debug:
            log.debug(f"Wait for button timeout set to {timeout_sec}s (from key: {timeout_key})")

        message_on_fail = step.get("message_on_fail", "Timeout waiting for user confirmation.")
        fail_on_timeout = step.get("fail_on_timeout", False)  # If true, timeout fails the test

        # --- 2. Validate Parameters ---
        # if timeout_key is None:
        #     log.error(f"Missing 'timeout_key' in wait_for_button step: {step}")
        #     raise ValueError(f"Invalid wait_for_button step config: {step}")

        # timeout_sec = self.settings.get_int(timeout_key, DEFAULT_SETTINGS.get(timeout_key, 20))

        # --- 3. Setup Wait ---
        prompt = step.get("text", "Waiting for user confirmation...")
        if "text" in step:
            await self._handle_message(step)  # Display prompt message
        # self.waitingForButton.emit(prompt)  # Legacy signal
        self.sendMessage.emit(ControllerMessage(MessageType.WAITING_FOR_BUTTON, prompt))

        self._input_event.clear()
        self._state = TestState.AWAITING_BUTTON
        log.info(f"Waiting for user button press confirmation (timeout: {timeout_sec}s)")

        # --- 4. Execute Wait ---
        try:
            await asyncio.wait_for(self._input_event.wait(), timeout=timeout_sec)
            # --- Button Pressed ---
            log.info("Button press confirmed by UI.")
            self.updateText.emit("Testing complete.")
            self.sendMessage.emit(ControllerMessage(MessageType.APPEND_TEXT, "Testing complete."))

        # --- 5. Handle Timeout ---
        except asyncio.TimeoutError:
            log.warning("Timeout occurred while waiting for button confirmation.")
            self.updateText.emit(message_on_fail)  # Legacy
            self.sendMessage.emit(ControllerMessage(MessageType.APPEND_TEXT, message_on_fail))
            if fail_on_timeout:
                log.error("Failing test due to button confirmation timeout.")
                raise  # Re-raise the TimeoutError to fail the test run

        # --- 6. Cleanup Wait ---
        finally:
            self._state = TestState.RUNNING  # Resume running state
            # self._input_event.clear() # Already cleared or handled by wait_for

    # --- UI Interaction Method ---
    def notify_button_pressed(self):
        """
        Public method called by the MainWindow when the user clicks the
        'Continue' button while the controller is in AWAITING_BUTTON state.
        """
        # Check if controller is actually waiting for the button
        if self._state == TestState.AWAITING_BUTTON:
            # Check if event hasn't already been set (e.g., by timeout)
            if not self._input_event.is_set():
                if self.debug:
                    log.debug("notify_button_pressed: Setting button confirmation event.")
                self._input_event.set()  # Set the event to release the wait
            else:
                if self.debug:
                    log.debug("notify_button_pressed: Event already set, likely timeout occurred.")
        else:
            log.warning(f"notify_button_pressed called but controller not in AWAITING_BUTTON state (State: {self._state.name})")

    def dump_test_config(self) -> str:
        """
        Returns a string representation of the loaded test sequence for debugging.
        """
        if not self._test_sequence:
            return "No test sequence loaded."

        config_str = f"Loaded Test Sequence ({len(self._test_sequence)} steps from {self._config_loader}):"
        for i, step in enumerate(self._test_sequence, start=1):
            # Basic formatting, could use pprint or json.dumps for better structure
            config_str += f"\n Step {i:02d}: {step}"
        return config_str


# --- Main block for testing ---
if __name__ == "__main__":
    # This block is for testing the TestController in isolation if needed.
    # It requires mocking or providing dummy AIODevice and Settings instances.
    print("Testing TestController standalone...")

    # Example: Create dummy instances (replace with actual mocks if needed)
    class DummySettings:
        def get_int(self, key, default=None):
            return DEFAULT_SETTINGS.get(key, default)

        def get_bool(self, key, default=None):
            return DEFAULT_SETTINGS.get(key, default)

    class DummyAIODevice:
        async def write_pin_by_func(self, func, val):
            print(f"MOCK WRITE: Func={func}, Val={val}")

        async def digital_write(self, pin, val):
            print(f"MOCK WRITE: Pin={pin}, Val={val}")

        def get_pin_by_function(self, func):
            return {'relay in': 7}.get(func)  # Example

        def attach_callback(self, cb, pin):
            print(f"MOCK ATTACH: Pin={pin}")

        def detach_callback(self, pin):
            print(f"MOCK DETACH: Pin={pin}")

    settings_inst = DummySettings()
    aio_dev_inst = DummyAIODevice()

    try:
        controller = TestController(aio_dev_inst, settings_inst)
        print(controller.dump_test_config())

        # Example: Simulating a test run (requires an event loop)
        # async def run():
        #     # Need a V40Device instance
        #     model_enum = Model.EA # Example model
        #     program_code = "01" # Example program
        #     device_inst = V40Device(model_enum, program_code)
        #     await controller.async_run_test(device_inst)
        # asyncio.run(run())

    except Exception as main_e:
        print(f"Error during TestController standalone test: {main_e}")
