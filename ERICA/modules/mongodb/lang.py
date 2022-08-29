from ERICA import db
collection = db["Zaid"]["language"]

def save_welcome(chat_id, msg_id):
    doc = {"_id": 1, "welcomes": {chat_id: msg_id}}
    result = collection.find_one({"_id": 1})
    if result:
        collection.update_one(
            {"_id": 1}, {"$set": {f"welcomes.{chat_id}": msg_id}}
        )
    else:
        collection.insert_one(doc)


def get_welcome(chat_id):
    result = collection.find_one({"_id": 1})
    if result is not None:
        try:
            msg_id = result["welcomes"][chat_id]
            return msg_id
        except KeyError:
            return None
    else:
        return None
