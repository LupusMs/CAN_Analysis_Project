import pandas as pd
import glob
import csv
import os
import shelve
import pickle
from dataclasses import dataclass


#########################################################################################
# The class that takes all the attributes related to a specific identifier.
@dataclass
class Identifier:
    def __init__(self, id_hex, occurrences):
        self.id_hex = id_hex
        self.occurrences = occurrences

    payload_changes = -1
    id_int = 0
    last_payload = "xyz"
    unique_payloads = {}  # or use a set instead
    time_dict = {}


##########################################################################################
identifier_dict = {}  # a container for all the identifier objects
timelog_dict = {}

# create and specify the necessary paths/folders
if not os.path.exists(os.path.join("Output_CSVs","Processed_CSVs")):
    os.mkdir(os.path.join("Output_CSVs","Processed_CSVs"))
    print("Processed_CSVs directory has been created")
else:
    print("Processed_CSVs directory already exists")

tlog_input_path = os.path.join(".", "TimeLog_CSVs", "*.csv")
output_path = os.path.join(".", "Output_CSVs", "Processed_CSVs")
db_path = os.path.join(".", "Makeshift_DB")


# Read from the makeshift database
with open(os.path.join(db_path, "Identifier_DB_pickle"), "rb") as db:
    identifier_dict = pickle.load(db)

print("0x108 unique payloads are:")
print(identifier_dict["108"].unique_payloads, end="\n")

# Write out all the identifiers processed information to individual csvs in the Processed_CSVs folder
for id in identifier_dict:
    filename = f"0x{id}.csv" 

    with open(os.path.join(output_path, filename), "w") as f:
        f_writer = csv.writer(f)
        f_writer.writerow(["Time", "Payload", "Payload_Occurrences"])

        for k in sorted(identifier_dict[id].time_dict):
            v = identifier_dict[id].time_dict[k]
            f_writer.writerow([k, v, identifier_dict[id].unique_payloads[v]])




