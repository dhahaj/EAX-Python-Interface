---
presentation:
  width: 1800
  height: 1200
  theme: black.css
  autoSlide: 5000
---

<!-- slide -->

# Testing

The test process is designed to be completely modular and it is defined in the `config.yaml` file. Each entry under the `testing` key is broken into four parts: `description`, `command`, `params` and `delay`.

<!-- @import "README.pdf"
@import "config.yaml"  {class="line-numbers"} -->
<!-- slide -->

- [Testing](#testing)
  - [Description](#description)
  - [Command](#command)
  - [Params](#params)
  - [Delay](#delay)

<!-- slide -->

## Description

The `description` key is a string that describes the command. This is used for logging purposes.

<!-- slide -->

## Command

The `command` key is a string that contains the command to be executed. The available commands are:

| Command | Description | Params |
| ------- | ----------- | ------ |
| `digital_write` | Sets the value of a pin. | `pin_number`, `pin_value` |
| `insert_text` | Displays text on the screen. | `text` |
| `load_instructions` | Clears the screen and displays the instructions. | `filename` (optional) |
| `wait_for_button` | Waits for a button to be pressed. | `timeout` (optional) |
| `wait_for_input` | Waits for a pin to be set. | `pin_number`, `pin_value`, `timeout` (optional) |
| `set_indicator` | Sets the value of the indicator. | `indicator_value` |
| `indicator_on` | Turns on the indicator. | None |
| `indicator_off` | Turns off the indicator. | None |
| `set_test_indicator` | Sets the value of the test indicator. | `indicator_value` |
| `test_indicator_on` | Turns on the test indicator. | None |
| `test_indicator_off` | Turns off the test indicator. | None |
| `set_battery` | Sets the value of the battery. | `battery_value` |
| `battery_on` | Turns on the battery output. | None |
| `battery_off` | Turns off the battery output. | None |
| `set_low_battery` | Sets the value of the low battery. | `low_battery_value`|
| `low_battery_on` | Turns on the low battery output. | None |
| `low_battery_off` | Turns off the low battery output. | None |
| `set_remote` | Sets the value of the remote. | `remote_value` |
| `set_pad` | Sets the value of the pad. | `pad_value` |
| `set_relay1` | Sets the value of relay 1. | `relay1_value` |
| `set_relay2` | Sets the value of relay 2. | `relay2_value` |
| `set_all_pins_to_value` | Sets all pins to a value. | `pin_value` |

<!-- slide -->

## Params

The `params` key is a list of parameters to be passed to the command. Some commands require parameters, while others do not. Refer to the table above for the list of parameters for each command.

<!-- slide -->

## Delay

The `delay` key is a float that specifies the delay in milliseconds before the next command is executed.
