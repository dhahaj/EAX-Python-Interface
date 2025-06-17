import sys
import types
import importlib
import platform


def make_dummy_pyudev(devices):
    class DummyContext:
        def list_devices(self, subsystem=None, DEVTYPE=None):
            return devices
    return types.SimpleNamespace(Context=lambda: DummyContext())

class DummyUSBDevice:
    def __init__(self, vid, pid, path="/dev/usb1", name="USB-device", auth=b"1"):
        self._vals = {
            "ID_VENDOR_ID": vid.lower(),
            "ID_MODEL_ID": pid.lower(),
            "ID_MODEL": name,
        }
        self._path = path
        self._auth = auth

    def get(self, key, default=None):
        return self._vals.get(key, default)

    @property
    def attributes(self):
        return {"authorized": self._auth}

    @property
    def device_path(self):
        return self._path


def test_linux_find_and_list(monkeypatch):
    dev = DummyUSBDevice("1234", "5678", "/dev/hub1", "Hub1")
    monkeypatch.setitem(sys.modules, "pyudev", make_dummy_pyudev([dev]))
    monkeypatch.setattr(platform, "system", lambda: "Linux")
    usb = importlib.import_module("usbinfo")
    importlib.reload(usb)
    assert usb.find_device("1234", "5678") == {
        "name": "Hub1",
        "device_id": "/dev/hub1",
        "status": "OK",
    }
    assert usb.list_hubs() == [
        {"name": "Hub1", "device_id": "/dev/hub1", "status": "OK"}
    ]


def test_linux_no_device(monkeypatch):
    monkeypatch.setitem(sys.modules, "pyudev", make_dummy_pyudev([]))
    monkeypatch.setattr(platform, "system", lambda: "Linux")
    usb = importlib.import_module("usbinfo")
    importlib.reload(usb)
    assert usb.find_device("1234", "5678") is None
    assert usb.list_hubs() == []


def make_dummy_wmi(hubs):
    class DummyWMI:
        def Win32_USBHub(self):
            return hubs

    return types.SimpleNamespace(WMI=lambda: DummyWMI())


def test_windows_list_and_find(monkeypatch):
    hub = types.SimpleNamespace(
        Name="HubX",
        DeviceID="USB\\VID_1234&PID_ABCD#0001",
        Status="OK",
    )
    monkeypatch.setitem(sys.modules, "wmi", make_dummy_wmi([hub]))
    monkeypatch.setattr(platform, "system", lambda: "Windows")
    usb = importlib.import_module("usbinfo")
    importlib.reload(usb)
    assert usb.list_hubs() == [
        {"name": "HubX", "device_id": hub.DeviceID, "status": "OK"}
    ]
    assert usb.find_device("1234", "abcd") == {
        "name": "HubX",
        "device_id": hub.DeviceID,
        "status": "OK",
    }

