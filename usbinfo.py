# usbinfo.py
import platform

if platform.system() == "Windows":
    import wmi            # unchanged

    _WMI = wmi.WMI()

    def list_hubs():
        """Return list of dicts with keys: name, device_id, status"""
        return [
            {"name": hub.Name,
             "device_id": hub.DeviceID,
             "status": hub.Status}
            for hub in _WMI.Win32_USBHub()
        ]

    def find_device(vid: str, pid: str):
        """Return first matching device dict or None"""
        needle = f"USB\\VID_{vid.upper()}&PID_{pid.upper()}"
        for dev in _WMI.Win32_USBHub():
            if dev.DeviceID.startswith(needle):
                return {"name": dev.Name,
                        "device_id": dev.DeviceID,
                        "status": dev.Status}
        return None

else:                       # -------- Linux / *nix branch ----------
    # pip install pyudev
    import pyudev # type: ignore

    _CTX = pyudev.Context()

    def _fmt_status(dev):
        return "OK" if dev.attributes.get("authorized", b"1") == b"1" else "Blocked"

    def list_hubs():
        hubs = []
        for dev in _CTX.list_devices(subsystem='usb', DEVTYPE='usb_device'):
            hubs.append({
                "name": dev.get("ID_MODEL", "USB-device"),
                "device_id": dev.device_path,          # e.g. /devices/pci…/1-3
                "status": _fmt_status(dev)
            })
        return hubs

    def find_device(vid: str, pid: str):
        for dev in _CTX.list_devices(subsystem='usb', DEVTYPE='usb_device'):
            if (dev.get('ID_VENDOR_ID') == vid.lower() and
                    dev.get('ID_MODEL_ID') == pid.lower()):
                return {
                    "name": dev.get("ID_MODEL", "USB-device"),
                    "device_id": dev.device_path,
                    "status": _fmt_status(dev)
                }
        return None
