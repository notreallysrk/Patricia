# Copyright (c) 2021 Itz-fork

from aiohttp import ClientSession
from py_trans import Async_PyTranslator

class Yui_Affiliate():
    """
    AffiliatePlus Class of Yui

    Arguments:
        None
    
    Methods:

    """
    def __init__(self) -> None:
        self.data = {
            "age": "1",
            "birthyear": "2021",
            "birthdate": "July 14, 2021",
            "birthplace": "New Delhi, India :)",
            "location": "New Delhi",
            "build": "Zaid - v1.0 Affiliate+",
            "version": "Zaid - v1.0",
            "celebrity": "@Timesisnotwaiting",
            "company": "Yui",
            "email": "itsunknown122@gmail.com",
            "kindmusic": "Future bass"
        }
        self.bot_name = "Zaid"
        self.dev_name = "@Timesisnotwaiting"
    
    async def ask_yui(self, message, user_id):
        c_message = await self.__prepare_message(message)
        api_url = f"https://api.affiliateplus.xyz/api/chatbot?message={c_message}&botname={self.bot_name}&ownername={self.dev_name}&user={user_id}"
        for k, i in self.data.items():
            api_url += f"&{k}={i}"
        async with ClientSession() as yui_session:
            res = await yui_session.get(api_url)
            response = await res.json()
            return response["message"]
    
    async def __prepare_message(self, message):
        py_t = Async_PyTranslator()
        msg_origin = await py_t._detect_lang(message)
        if msg_origin != "en":
            return await py_t.translate(message, "en")
        else:
            return message
