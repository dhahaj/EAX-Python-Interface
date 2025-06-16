import sys
import types

class DummyConfig:
    def __init__(self, db_path, log_file):
        self.data = {
            'logging': {
                'log_file': log_file,
                'database_file': db_path,
                'log_level': 'DEBUG',
                'console_log_level': 'DEBUG',
                'log_rotation': '1 day',
                'log_retention': '1 day',
                'db_log_level': 'DEBUG',
            }
        }
    def get(self, key):
        return self.data.get(key)

def stub_qt(monkeypatch):
    qtcore = types.SimpleNamespace(QFile=object, QDir=object, QIODevice=object)
    qtpy = types.SimpleNamespace(QtCore=qtcore)
    monkeypatch.setitem(sys.modules, 'qtpy', qtpy)
    monkeypatch.setitem(sys.modules, 'qtpy.QtCore', qtcore)

def test_applogger_basic(tmp_path, monkeypatch):
    stub_qt(monkeypatch)
    import importlib
    import applogger
    db = tmp_path / 'logs.sqlite'
    logf = tmp_path / 'out.log'
    monkeypatch.setattr(applogger.config_loader, 'get_config', lambda: DummyConfig(db, logf))
    importlib.reload(applogger)
    log = applogger.AppLogger(logfile=str(logf), database=str(db))
    log.clear_logs()
    log.info('hello')
    rows = log.get_logs()
    assert len(rows) >= 1
    assert rows[0]['level'] == 'INFO'

