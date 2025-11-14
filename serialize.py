import pickle

# everything here is temporary or a placeholder
# both serializing and deserializing need to deal with a data structure
# deserializing: will have to take input and properly construct said data structure

def save(fname, data):
    """serializes data given to it and writes to a file
    returns 1 if write was successful
    returns 0 otherwise"""
    serialized_data = pickle.dumps(data)

    try:
        with open(fname, "wb") as f:
            f.write(serialized_data)
        #print(f"Wrote data to {fname}")

    except OSError as e:
        return 0

    return 1

def load(fname):
    """deserializes data read from a file
    returns deserialized data if read was successful
    returns None otherwise"""
    try:
        with open(fname, "rb") as f:
            serialized_data = f.read()

        deserialized_data = pickle.loads(serialized_data, encoding="ASCII")

        #print(f"Loaded data from {fname};")
        #print(deserialized_data)

    except OSError as e:
        print(f"Cannot open file; {e}")
        return

    return deserialized_data
