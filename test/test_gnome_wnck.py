
import pytest

from gi.repository import Wnck

def test_wnck():
    screen = Wnck.Screen.get_default()
    screen.force_update()
    wins = [x for x in screen.get_windows()]

    assert len(wins) > 0
    assert all([type(x.get_name()) is str for x in wins])
