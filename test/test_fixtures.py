
import gnomegmail


def test_config_fixture(config_fxt):
    config = gnomegmail.GgConfig(
                fpath="~/.config/gnome-gmail/gnome-gmail.conf",
                section='gnome-gmail',
                initvals={
                    'suppress_preferred': '0',
                    'suppress_account_selection': '0',
                    'new_browser': '1',
                    'last_email': '',
                },
                header="header",
             )

    config.get_str('last_email')
    config.get_bool('new_browser')

    config.set_str('last_email', 'joe@example.com')
    config.set_bool('new_browser', True)

    assert gnomegmail.GgConfig.save.called


def test_keyring_fixture(keyring_fxt):
    keyring = gnomegmail.Oauth2Keyring("scope")

    assert keyring.getTokens("user") == ('atoken', 'rtoken')

    keyring.setTokens('user', 'atoken', 'rtoken')
    assert gnomegmail.Secret.password_store_sync.called
    assert gnomegmail.Secret.password_store_sync.call_args[0][4] == \
        "access:atoken;refresh:rtoken"


def test_default_mailer_fixture(default_mailer_fxt):
    assert gnomegmail.is_default_mailer() == True
    assert gnomegmail.is_default_mailer.called


def test_notify_fixture(notify_fxt):
    gnomegmail.Notify.init("scope")
    assert gnomegmail.Notify.init.called

    gnomegmail.Notify.Notification.new('args')
    assert gnomegmail.Notify.Notification.new.called


def test_oauth_fixture(oauth_fxt):
    assert gnomegmail.Wnck.tag == 'wnck'

    screen = gnomegmail.Wnck.Screen.get_default()
    assert screen.tag == 'screen'

    win = screen.get_windows()[0]
    assert win.tag == 'win'

    assert win.get_name() == 'state=abcdefghij.code=thecode'
