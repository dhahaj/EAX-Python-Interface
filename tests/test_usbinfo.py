import sys
import sys
import types
import importlib
import platform


def make_dummy_pyudev(devices):
    class DummyContext:
        def list_devices(self, subsystem=None, DEVTYPE=None):
            return devices
    return types.SimpleNamespace(Context=lambda: DummyContext())


def test_find_device_none(monkeypatch):
    monkeypatch.setitem(sys.modules, 'pyudev', make_dummy_pyudev([]))
    monkeypatch.setattr(platform, 'system', lambda: 'Linux')
    usb = importlib.import_module('usbinfo')
    importlib.reload(usb)
    assert usb.find_device('1234', '5678') is None
    assert usb.list_hubs() == []

