import pickle

def save(fname, data):
    """serializes data given to it and writes to a file
    returns 1 if write was successful
    returns 0 otherwise"""

    #convert to pickled bytes object
    serialized_data = pickle.dumps(data)

    #write serialized data to file
    try:
        with open(fname, "wb") as f:
            f.write(serialized_data)

    #failed to write data
    except OSError as e:
        return 0

    return 1

def load(fname):
    """deserializes data read from a file
    returns deserialized data if read was successful
    returns None otherwise"""

    #load file
    try:
        with open(fname, "rb") as f:
            serialized_data = f.read()

        #convert pickled data to usable object
        deserialized_data = pickle.loads(serialized_data, encoding="ASCII")

    #failed to load file data
    except OSError as e:
        print(f"Cannot open file; {e}")
        return

    return deserialized_data
