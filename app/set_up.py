from pymongo import MongoClient


# Connect to MongoDB locally
client = MongoClient('mongodb://localhost:27017/')
db = client.im  # Connect to the database