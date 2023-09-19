import pickle
def load():
    with open("database.pickle","rb") as f:
        data = pickle.load(f)
    return data

def save(data):
    with open("database.pickle","wb") as f:
        pickle.dump(data,f)