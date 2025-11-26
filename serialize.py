import pickle

def save(fname, data):
    """Serializes given data and saves it to a file given by fname as a path.
    The file will be overwritten if it already exists. Otherwise, a new file
    is created.
    Returns 1 if write was successful
    Returns 0 otherwise"""
    serialized_data = pickle.dumps(data)

    try:
        with open(fname, "wb") as f:
            f.write(serialized_data)

    except OSError as e:
        return 0

    return 1

def load(fname):
    """Deserializes data from file, given by fname as a path.
    Returns deserialized data if read was successful
    Returns None otherwise"""
    try:
        with open(fname, "rb") as f:
            serialized_data = f.read()

        deserialized_data = pickle.loads(serialized_data, encoding="ASCII")

    except OSError as e:
        print(f"Cannot open file; {e}")
        return

    return deserialized_data
