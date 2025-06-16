from counter import Counter


def test_counter_operations(tmp_path, monkeypatch):
    # Redirect QSettings storage to a temporary directory
    monkeypatch.setenv('XDG_CONFIG_HOME', str(tmp_path))
    c = Counter('unit_test_counter')
    assert c.get() == 0
    c.increment()
    assert c.get() == 1
    c.value = 5
    assert c.get() == 5
    c.reset()
    assert c.get() == 0

