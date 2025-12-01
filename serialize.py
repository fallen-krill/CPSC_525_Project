import pickle
import json
from project import Project, Page

# everything here is temporary or a placeholder
# both serializing and deserializing need to deal with a data structure
# deserializing: will have to take input and properly construct said data structure

def serialize(fname, data):
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

def json_save(fname, project: Project):
    eqn_list = []
    for i in range(len(project.pages)):
        eqn_list.append(project.pages[i].equations)
    try:
        with open(fname, "w") as f:
            json.dump(eqn_list, f)
    except OSError as e:
        return 0

    return 1

def json_load(fname):
    try:
        with open(fname, "r") as f:
            deserialized_data = json.load(f)

            project = Project()
            print(deserialized_data)
            for i in range(len(deserialized_data)):
                project.add_page()
                for j in range(len(deserialized_data[i])):
                    project.pages[i].add_equation_text(deserialized_data[i][j])
            return project

    except Exception as e:
        print(f"Bad file: {e}")
        exit(0)
                
            

def deserialize(fname):
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
