
import pytest

from gi.repository import Notify


def test_notify_init():
    Notify.init("foo")

def test_notify_show():
    Notify.init("foo")

    notice = Notify.Notification.new(
        "ggtest",
        "Testing Notifications",
        "dialog-information"
    )

    notice.show()
