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
    last_payload = "n"
    unique_payloads = {}  # or use a set instead
    time_dict = {}


##########################################################################################
identifier_dict = {}  # a container for all the identifier objects
timelog_dict = {}
priority_ids_list = []

# create and specify the necessary paths/folders
tlog_input_path = os.path.join(".", "TimeLog_CSVs", "*.csv")
output_path = os.path.join(".", "Output_CSVs")
db_path = os.path.join(".", "Makeshift_DB")

# Read from the makeshift database
with open(os.path.join(db_path, "Identifier_DB_pickle"), "rb") as db:
    identifier_dict = pickle.load(db)

print("0x108 unique payloads are:")
print(identifier_dict["208"].unique_payloads)

print("0x108 time_dict is:")
print(identifier_dict["208"].time_dict)

with open(os.path.join(output_path, "208_sunroof.csv"), "w") as f:
    f_writer = csv.writer(f)
    f_writer.writerow(["Time", "Payload", "Payload_Frequency"])

    for k in sorted(identifier_dict["208"].time_dict):
        v = identifier_dict["208"].time_dict[k]
        f_writer.writerow([k, v, identifier_dict["208"].unique_payloads[v]])




