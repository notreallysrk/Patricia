import sys
import logging
import importlib
from ERICA import telethn as Zaid
from ERICA import OWNER_ID
from telethon import events


def Zbot(**args):
    pattern = args.get("pattern", None)
    r_pattern = r"^[/?!.]"
    if pattern is not None and not pattern.startswith("(?i)"):
        args["pattern"] = "(?i)" + pattern
    args["pattern"] = pattern.replace("^/", r_pattern, 1)

    def decorator(func):
        async def wrapper(check):
            if check.sender_id and check.sender_id != OWNER_ID:
                pass
            try:
                await func(check)
            except BaseException:
                return
            else:
                pass

        Zaid.add_event_handler(wrapper, events.NewMessage(**args))
        return wrapper

    return decorator


def Zquery(**args):
    pattern = args.get("pattern", None)

    if pattern is not None and not pattern.startswith("(?i)"):
        args["pattern"] = "(?i)" + pattern

    def decorator(func):
        Zaid.add_event_handler(func, events.InlineQuery(**args))
        return func

    return decorator


def Zinline(**args):
    def decorator(func):
        Zaid.add_event_handler(func, events.CallbackQuery(**args))
        return func

    return decorator
