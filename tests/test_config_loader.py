import os
import sys
import types

import pytest

from constants import KEY_CHIP_PART

SAMPLE_YAML = """
version: 1.0
logging:
  log_file: test.log
  database_file: {db}
programmer_config:
  executable: prog
  arguments:
    - -p {{chip_part}}
    - -f {{firmware_name}}
    - -s {{serial_number}}
    - -c {{programmer}}
  programmer: pickit
  usb_vendor_id: "0xAAAA"
  usb_product_id: "0xBBBB"
devices:
  label_styles: ""
  label_size: "font-size:14pt;"
  firmware_path: {fwdir}
  firmware_files:
    - device_name: TEST
      firmware_name: fw.hex
      color: '#abcdef'
testing:
  sequence:
    - action: message
      text: Hello
cleanup:
  - action: message
    text: Clean
"""

def stub_qt(monkeypatch):
    qtcore = types.SimpleNamespace(QFile=object, QDir=object, QIODevice=object)
    qtpy = types.SimpleNamespace(QtCore=qtcore)
    monkeypatch.setitem(sys.modules, 'qtpy', qtpy)
    monkeypatch.setitem(sys.modules, 'qtpy.QtCore', qtcore)

def import_modules(monkeypatch):
    stub_qt(monkeypatch)
    import importlib
    if 'config_loader' in sys.modules:
        importlib.reload(sys.modules['config_loader'])
    else:
        import config_loader
    if 'device' in sys.modules:
        importlib.reload(sys.modules['device'])
    else:
        import device
    return sys.modules['config_loader'], sys.modules['device']

def make_config(tmp_path, monkeypatch):
    cfg_mod, _ = import_modules(monkeypatch)
    fwdir = tmp_path / "fw"
    fwdir.mkdir()
    config_text = SAMPLE_YAML.format(db=tmp_path/"db.sqlite", fwdir=fwdir)
    cfg_file = tmp_path / "config.yaml"
    cfg_file.write_text(config_text)
    return cfg_mod.ConfigLoader(str(cfg_file))

def test_device_names_and_sequence(tmp_path, monkeypatch):
    cfg = make_config(tmp_path, monkeypatch)
    assert cfg.device_names == ["TEST"]
    assert cfg.get_test_sequence()[0]["text"] == "Hello"

def test_find_programmer_serial_number(tmp_path, monkeypatch):
    cfg_mod, _ = import_modules(monkeypatch)
    cfg = make_config(tmp_path, monkeypatch)
    monkeypatch.setattr(cfg_mod, "find_device", lambda vid, pid: {"device_id": "USB\\VID_AAAA&PID_BBBB#123456"})
    assert cfg.find_programmer_serial_number() == "123456"


def test_generate_program_arguments(tmp_path, monkeypatch):
    cfg_mod, _ = import_modules(monkeypatch)
    cfg = make_config(tmp_path, monkeypatch)
    monkeypatch.setattr(cfg_mod, "find_device", lambda vid, pid: {"device_id": "ID012345"})
    dummy_settings = types.SimpleNamespace(get=lambda key, default=None: "PIC" if key==KEY_CHIP_PART else default)
    dummy_device = types.SimpleNamespace(firmware_path="/path/fw.hex")
    args = cfg.generate_program_arguments(settings=dummy_settings, device=dummy_device)
    assert args[0] == "prog"
    assert "PIC" in args[1]
    assert "/path/fw.hex" in args[2]
    assert "012345" in args[3]


def test_load_devices(tmp_path, monkeypatch):
    cfg_mod, device_mod = import_modules(monkeypatch)
    cfg = make_config(tmp_path, monkeypatch)
    monkeypatch.setattr(cfg_mod, "get_config", lambda **kwargs: cfg)
    devices = device_mod.load_devices()
    assert len(devices) == 1
    dev = devices[0]
    assert isinstance(dev, device_mod.Device)
    assert dev.name == "TEST"
    assert dev.firmware_path.endswith("fw.hex")

