from pymongo import MongoClient

# Connection details
host = 'localhost'  # MongoDB server hostname or IP address
port = 27017       # MongoDB server port (default is 27017)

# Create a MongoClient instance
client = MongoClient(host, port)

# Access a database (replace 'mydatabase' with your actual database name)
db = client['mydatabase']

# Access a collection within the database (replace 'mycollection' with your actual collection name)
collection = db['mycollection']

# Example: Insert a document
document = {"name": "John", "age": 30}
collection.insert_one(document)

# Example: Find documents
results = collection.find({"age": {"$gt": 25}})
for result in results:
    print(result)

# Close the connection to MongoDB
client.close()
