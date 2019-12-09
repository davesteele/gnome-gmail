
import pytest
from mock import Mock
import tempfile
import os


@pytest.fixture()
def config_fxt(monkeypatch):
    monkeypatch.setattr("viagee.GgConfig.save", Mock())
    return None


@pytest.fixture()
def keyring_fxt(monkeypatch):
    monkeypatch.setattr(
        "viagee.Secret.password_lookup_sync",
        Mock(return_value="access:atoken;refresh:rtoken")
    )
    monkeypatch.setattr(
        "viagee.Secret.password_store_sync",
        Mock()
    )
    return None


@pytest.fixture()
def default_mailer_fxt(monkeypatch):
    monkeypatch.setattr("viagee.is_default_mailer",
                        Mock(return_value=True))
    return None


@pytest.fixture()
def notify_fxt(monkeypatch):
    monkeypatch.setattr("viagee.Notify", Mock())
    return None


@pytest.fixture()
def web_fxt(monkeypatch):
    monkeypatch.setattr('viagee.urllib.request.urlopen', Mock())
    monkeypatch.setattr('viagee.urllib.request.build_opener', Mock())

    monkeypatch.setattr(
        'viagee.json.loads',
        Mock(return_value={
                'message': {'id': '1'},
                'access_token': 'atoke',
                'refresh_token': 'rtoke',
            }
        )
    )


@pytest.fixture()
def tmpfile(request):
    fd, path = tempfile.mkstemp()

    request.addfinalizer(lambda: os.remove(path))

    return path


@pytest.fixture()
def oauth_fxt(monkeypatch, web_fxt):
    monkeypatch.setattr(
        'viagee.random.sample',
        Mock(return_value=[chr(x) for x in range(ord('a'), ord('k'))])
    )
    monkeypatch.setattr('viagee.browser', Mock())
    monkeypatch.setattr(
        'viagee.subprocess.check_output',
        Mock(return_value='state=abcdefghij.code=thecode')
    )

    monkeypatch.setattr('viagee.Gtk.main_iteration', Mock())

    Wnck = Mock()
    Wnck.tag = 'wnck'
    monkeypatch.setattr('viagee.Wnck', Wnck)

    screen = Mock()
    screen.tag = 'screen'
    Wnck.Screen.get_default.return_value = screen

    win = Mock()
    win.tag = 'win'
    screen.get_windows.return_value = [win]

    win.get_name.return_value = 'state=abcdefghij.code=thecode'
