import pickle
def create_database():
    with open("free_tire_database.csv","r") as f:
        data = f.readlines()

    key_headers = data[0].replace('"',"").strip("\n").split(",")
    result = [dict(zip(key_headers,item.replace('"',"").strip("\n").split(","))) for item in data[1:]]

    with open("Database.pickle","wb") as f:
        pickle.dump(result,f)
    return "Done!"

print(create_database())


def load_database():
    with open("Database.pickle","rb") as f:
        data = pickle.load(f)
    return data
