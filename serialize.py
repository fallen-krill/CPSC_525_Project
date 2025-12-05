import pickle
import json
from project import Project, Page


# The (intentional) bug (unsafe deserialization (CWE-502 )with pickle) ---------------------------------------

def serialize(fname, data):
    """Serializes given data and saves it to a file given by fname as a path.
    The file will be overwritten if it already exists. Otherwise, a new file
    is created. May raise.
    Returns 1 if write was successful
    Returns 0 otherwise"""
    
    #convert to pickled bytes object

    serialized_data = pickle.dumps(data)

    #write serialized data to file
    with open(fname, "wb") as f:
        f.write(serialized_data)


def deserialize(fname):
    """Deserializes data read from a file using pickle. May raise an OSError. Contains a bug allowing arbitrary code execution.
    Returns deserialized data if read was successful
    Returns None otherwise"""
    
    with open(fname, "rb") as f:
        serialized_data = f.read()

    #convert pickled data to usable object
    deserialized_data = pickle.loads(serialized_data, encoding="ASCII")

    return deserialized_data

# End bug ------------------------------------------------------------------------------------------------------



# THE FIX: (Comment out above two functions and uncomment functions below)--------------------------------------

# def serialize(fname, project: Project):
#     "Serialize project into 2D list with json.dump().
#     "
#     eqn_list = []
#     for i in range(len(project.pages)):
#         eqn_list.append(project.pages[i].equations)
#     try:
#         with open(fname, "w") as f:
#             json.dump(eqn_list, f)
#     except OSError as e:
#         exit(-1)


# def deserialize(fname):
#     """Deserialize with json.load() and parse as if it's a 2D list."""
    
#     try:
#         with open(fname, "r") as f:
#             deserialized_data = json.load(f)

#             project = Project() # Create new project
            
#             for i in range(len(deserialized_data)):
#                 project.add_page()
#                 for j in range(len(deserialized_data[i])):
#                     project.pages[i].add_equation_text(deserialized_data[i][j])
#             return project

#     except Exception as e:
#         print(f"Bad file: {e}")
#         exit(-1)

# End fix ------------------------------------------------------------------------------------------------------
            

