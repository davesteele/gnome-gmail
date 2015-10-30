

from gi.repository import Gio


def test_gio_get_app():
    app = Gio.app_info_get_default_for_type('x-scheme-handler/https', True)
    assert type(app.get_filename()) is str

def test_gio_get_all():
    apps = [x for x in Gio.app_info_get_all_for_type("x-scheme-handler/mailto")]
    assert len(apps) > 0
    assert all([type(x.get_id()) is str for x in apps])
    assert all(['desktop' in x.get_id() for x in apps])

def test_gio_set_default():
    app = Gio.app_info_get_default_for_type('x-scheme-handler/https', True)
    app.set_as_default_for_type('x-scheme-handler/https')
