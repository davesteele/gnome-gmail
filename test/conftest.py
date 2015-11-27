
import pytest
from mock import Mock
import tempfile
import os


@pytest.fixture()
def config_fxt(monkeypatch):
    monkeypatch.setattr("gnomegmail.GgConfig.save", Mock())
    return None


@pytest.fixture()
def keyring_fxt(monkeypatch):
    monkeypatch.setattr(
        "gnomegmail.Secret.password_lookup_sync",
        Mock(return_value="access:atoken;refresh:rtoken")
    )
    monkeypatch.setattr(
        "gnomegmail.Secret.password_store_sync",
        Mock()
    )
    return None


@pytest.fixture()
def default_mailer_fxt(monkeypatch):
    monkeypatch.setattr("gnomegmail.is_default_mailer",
                        Mock(return_value=True))
    return None


@pytest.fixture()
def notify_fxt(monkeypatch):
    monkeypatch.setattr("gnomegmail.Notify", Mock())
    return None


@pytest.fixture()
def web_fxt(monkeypatch):
    monkeypatch.setattr('gnomegmail.urllib.request.urlopen', Mock())
    monkeypatch.setattr('gnomegmail.urllib.request.build_opener', Mock())

    monkeypatch.setattr(
        'gnomegmail.json.loads',
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
        'gnomegmail.random.sample',
        Mock(return_value=[chr(x) for x in range(ord('a'), ord('k'))])
    )
    monkeypatch.setattr('gnomegmail.browser', Mock())
    monkeypatch.setattr(
        'gnomegmail.subprocess.check_output',
        Mock(return_value='state=abcdefghij.code=thecode')
    )

    monkeypatch.setattr('gnomegmail.Gtk.init', Mock())

    Wnck = Mock()
    Wnck.tag = 'wnck'
    monkeypatch.setattr('gnomegmail.Wnck', Wnck)

    screen = Mock()
    screen.tag = 'screen'
    Wnck.Screen.get_default.return_value = screen

    win = Mock()
    win.tag = 'win'
    screen.get_windows.return_value = [win]

    win.get_name.return_value = 'abcdefghij'
