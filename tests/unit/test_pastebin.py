"""
This file contains the unit tests for the pastebin model
"""
from web.models.pastebin import Pastebin
from datetime import datetime

def test_new_pastebin():
    """
    GIVEN a Pastebin model
    WHEN a new Pastebin is created
    THEN check that title, content and paste_type are correct
    """

    pastebin = Pastebin("test user", "text", None, "test title", None, None)

    assert pastebin.content == "test user"
    assert pastebin.title == "test title"
    assert pastebin.paste_type == "text"
    assert pastebin.is_valid()
    assert pastebin.date == datetime.utcnow().replace(microsecond=0)
    
