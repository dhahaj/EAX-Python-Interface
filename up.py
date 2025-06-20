from ctypes import (
    WinDLL, c_int, c_bool, c_char_p,
    POINTER, byref
)


class UPController:
    """Thin OO wrapper around up_control.dll / UP.exe."""

    # --- error & state codes you might check for -----------
    ERR_OK = 0
    ERR_UP_MISSING = 2          # ‘UP.exe not found’ per manual

    STATE_DONE = 0
    STATE_BUSY = 1
    # -------------------------------------------------------

    def __init__(self, dll_path: str, index: int = 0):
        """
        dll_path – absolute path to up_control.dll or up_control64.dll
        index    – programmer index (0 for first/only unit)
        """
        self.index = index
        self._dll = WinDLL(dll_path)

        # bind only what we actually use
        self._bind("UP_ProgConfig",
                   [c_int, c_char_p, c_int, c_int, c_char_p, c_char_p])
        self._bind("UP_Prog",
                   [c_int, c_bool, c_bool, c_bool, c_bool])
        self._bind("UP_ProgStateEx",
                   [c_int,
                    POINTER(c_int), POINTER(c_int), POINTER(c_int)])
        self._bind("UP_LastErrorCode", [c_int])
        self._bind("UP_Cancel",       [c_int])
        self._bind("UP_CleanUp",      [])

    # ---------- public API ---------------------------------
    def configure(self, ppr_path: str,
                  data_file: str | None = None,
                  eeprom_file: str | None = None) -> int:
        """
        Load a .PPR project and (optionally) override data/EEPROM files.
        Returns DLL error code (0 = OK).
        """
        ppr = ppr_path.encode()
        data = (data_file or "").encode()
        eeprom = (eeprom_file or "").encode()
        return self.UP_ProgConfig(self.index, ppr, 0, 0, data, eeprom)

    def program_all(self) -> int:
        """Equivalent to clicking ‘Program’ (all memories)."""
        return self.UP_Prog(self.index, True,  True,  True,  True)

    def wait_until_done(self, poll_ms: int = 100) -> tuple[int, int]:
        """
        Polls until STATE_DONE, returns (final_state, last_error_code).
        """
        from time import sleep

        main_pb = c_int()
        task_pb = c_int()
        task_id = c_int()

        while True:
            state = self.UP_ProgStateEx(self.index,
                                        byref(main_pb),
                                        byref(task_pb),
                                        byref(task_id))
            if state == self.STATE_DONE:
                break
            if state != self.STATE_BUSY:
                return state, self.last_error()  # abnormal
            sleep(poll_ms / 1000.0)
        return self.STATE_DONE, self.last_error()

    def cancel(self) -> int:
        if not callable(self.UP_Cancel):
            raise NotImplementedError("This UP DLL has no UP_Cancel()")
        return self.UP_Cancel(self.index)

    def last_error(self) -> int:
        return self.UP_LastErrorCode(self.index)

    def close(self) -> None:
        self.UP_CleanUp()
    # -------------------------------------------------------

    # ---------- private helper -----------------------------
    def _bind(self, name: str, argtypes: list) -> None:
        """
        Try to attach <name>.  If the DLL doesn’t have it, leave
        a stub that raises NotImplementedError at call time.
        """
        try:
            func = getattr(self._dll, name)
        except AttributeError:
            def _missing(*_a, **_kw):
                raise NotImplementedError(f"{name} not present in this DLL")
            setattr(self, name, _missing)
            return

        func.argtypes = argtypes
        func.restype = c_int
        setattr(self, name, func)
    # -------------------------------------------------------


# ---------------- quick usage ------------------------------
if __name__ == "__main__":
    up = UPController(r"C:\\Program Files (x86)\\ASIX\\UP\\up_control64.dll")

    assert up.configure(r"firmware\\EAX300.ppr") == UPController.ERR_OK
    assert up.program_all() == UPController.ERR_OK

    state, err = up.wait_until_done()
    print("state =", state, "err =", err)

    up.close()
