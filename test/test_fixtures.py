
import viagee


def test_config_fixture(config_fxt):
    config = viagee.GgConfig(
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

    assert viagee.GgConfig.save.called


def test_keyring_fixture(keyring_fxt):
    keyring = viagee.Oauth2Keyring("scope")

    assert keyring.getTokens("user") == ('atoken', 'rtoken')

    keyring.setTokens('user', 'atoken', 'rtoken')
    assert viagee.Secret.password_store_sync.called
    assert viagee.Secret.password_store_sync.call_args[0][4] == \
        "access:atoken;refresh:rtoken"


def test_default_mailer_fixture(default_mailer_fxt):
    assert viagee.is_default_mailer() == True
    assert viagee.is_default_mailer.called


def test_notify_fixture(notify_fxt):
    viagee.Notify.init("scope")
    assert viagee.Notify.init.called

    viagee.Notify.Notification.new('args')
    assert viagee.Notify.Notification.new.called


def test_oauth_fixture(oauth_fxt):
    assert viagee.Wnck.tag == 'wnck'

    screen = viagee.Wnck.Screen.get_default()
    assert screen.tag == 'screen'

    win = screen.get_windows()[0]
    assert win.tag == 'win'

    assert win.get_name() == 'state=abcdefghij.code=thecode'
