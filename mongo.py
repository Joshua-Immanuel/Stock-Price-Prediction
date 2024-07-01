from pymongo import MongoClient
import gridfs

# Connection URI
uri = "mongodb+srv://admin:admin@cluster0.iuabg.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri)
db = client['stock_models']
fs = gridfs.GridFS(db)

# # Specify the path to the model file
# model_file_path = 'artifacts/model.h5'

# # Open the model file in binary mode and store it in GridFS
# with open(model_file_path, 'rb') as file:
#     fs.put(file, filename='model.h5')

model_filename = 'model.h5'

# Find the model file in GridFS
model_file = fs.find_one({'filename': model_filename})

if model_file:
    # Open the file and read its contents
    model_data = model_file.read()
    
    # Write the contents to a local file
    with open(model_filename, 'wb') as f:
        f.write(model_data)
    
    print(f"Model file '{model_filename}' retrieved successfully.")
else:
    print(f"Model file '{model_filename}' not found.")


# Close the connection
client.close()
