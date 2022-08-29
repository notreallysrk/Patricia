
from pymongo import MongoClient
MONGO_DB_URI = "mongodb+srv://Anmol:Anmol@cluster0.icc3g.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(MONGO_DB_URI)
db = client["Melody"]
