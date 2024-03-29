from dearpygui.core import *
from dearpygui.simple import *
from platform import python_version
from ERICA.__main__ import STATS

try:
    from telegram import __version__ as pver
except ImportError:
    pver = "N/A"

with window("About"):
    add_text("Deadly telegram bot")
    add_text("Maintained with <3 by ElricX (https://t.me/WTF_BLAZE)")
    add_text("Enviroment:")
    add_text(f"Bot lib: python-telegram-bot v{pver}.", bullet=True)
    add_text(f"Python version: {python_version()}.", bullet=True)
    add_text("Source:")
    add_text("GitHub: github.com/piroxpower", bullet=True)
    add_text("GitLab: gitlab.com/piroxpower", bullet=True)

with window("stats"):
    add_text("\n*Bot statistics*:\n"+ "\n".join([mod.__stats__() for mod in STATS]))



start_dearpygui(primary_window="About")
