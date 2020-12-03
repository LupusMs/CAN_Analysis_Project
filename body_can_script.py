import pandas as pd
import glob
import csv
import os
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
    time_list = []


##########################################################################################
identifier_dict = {}  # a container for all the identifier objects

# create and specify the necessary paths/folders
if not os.path.exists("Output_CSVs"):
    os.mkdir("Output_CSVs")
    print("Output_CSVs directory has been created")
else:
    print("Output_CSVs directory already exists")

if not os.path.exists("Makeshift_DB"):
    os.mkdir("Makeshift_DB")
    print("Makeshift_DB, the directory for persisted storage has been created.")
else:
    print("Makeshift_DB directory already exists")

input_path = os.path.join(".", "Input_CSVs", "*.csv")
output_path = os.path.join(".", "Output_CSVs")
db_path = os.path.join(".", "Makeshift_DB")

# get the files and create a dataframe df
ixxat_csv_filenames = glob.glob(input_path)
ixxat_csv_filenames.sort()
frame_list = []

for filename in ixxat_csv_filenames:
    single_frame = pd.read_csv(filename, header=0, index_col=None)
    frame_list.append(single_frame)

df = pd.concat(frame_list, ignore_index=True)
#print(df.iloc[84780:84790])  # making sure that the concatenation worked ok

# group the ids by the frequency of occurrences
# create an extra helper column and populate it with '1's to achieve this
df['Count'] = 1
grouped_df = df.groupby(df['ID (hex)']).count()['Count'].reset_index()

# add the ids and occurrences to instances of the data class and add the instances to a dictionary
for index, row in grouped_df.iterrows():
    identifier = Identifier(row["ID (hex)"], row["Count"])
    identifier_dict[row["ID (hex)"]] = identifier

# convert hex string to int and save to id_int # useful later when plotting graphs and histograms
for id in identifier_dict:
    identifier_dict[id].id_int = int(id, 16)
    # print(identifier.id_hex + "\t" + str(identifier.occurrences) + "\t\t" + str(identifier.id_int))

# iterate over the dataframe rows and:
# (a)check how often the datafield changes
# (b)see how many different messages an id is used for (it could be in (a) that only the same few messages keep getting changed over and over)

#df_head = df.head(30)
for index, row in df.iterrows():
    identifier = identifier_dict[row["ID (hex)"]]
    if row["Data (hex)"] in identifier.unique_payloads.keys():
        if row["Data (hex)"] != identifier.last_payload:
            identifier.last_payload = row["Data (hex)"]
            identifier.payload_changes += 1
            identifier.time_list.append(row["Adjusted_Time"])
        identifier.unique_payloads[row["Data (hex)"]] += 1

    else:
        identifier.unique_payloads[row["Data (hex)"]] = 1
        identifier.last_payload = row["Data (hex)"]
        identifier.payload_changes += 1
        identifier.time_list.append(row["Adjusted_Time"])

# REMEMBER TO PERSIST THE IDENTIFIER OBJECTS in a database

######INSERT CODE HERE########

# Some printing for debugging purposes
# print("0x303 unique payloads are:")
# print(identifier_dict["303"].unique_payloads)
#
# print("0x108 unique payloads are:")
# print(identifier_dict["108"].unique_payloads)

print(df.iloc[0:30])

# go through the dictionary, check the payload changes and the size of the unique_payloads dict
# write this data in a csv file
with open(os.path.join(output_path, "Filtered_Sorted(by_ID).csv"), 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["ID_(dec)", "ID_(hex)", "Occurrences", "Payload_Changes", "Total_Unique_Payloads"])
    for key in identifier_dict:
        writer.writerow(
            [identifier_dict[key].id_int, key, identifier_dict[key].occurrences, identifier_dict[key].payload_changes,
             len(identifier_dict[key].unique_payloads)])

# generate a csv of the output sorted by size of the payload changes
# read in the previously output csv file to do this
filtered_df = pd.read_csv(os.path.join(output_path, "Filtered_Sorted(by_ID).csv"), header=0, index_col=None)
filtered_df = filtered_df.sort_values(["Payload_Changes", "Occurrences"], ascending=[1, 0])
filtered_df.drop(columns="Total_Unique_Payloads", inplace=True)
filtered_df.reset_index(drop=True, inplace=True)
filtered_df.to_csv(os.path.join(output_path, "Filtered_Sorted(by_PayloadChanges).csv"))

# generate additional different csv files based on the number of changes
# create 3 different csv files for this
f1 = open(os.path.join(output_path, "Filtered(No_Change).csv"),"w")
f2 = open(os.path.join(output_path, "Filtered(Analysable_Changes).csv"),"w")
f3 = open(os.path.join(output_path, "Filtered(Many_Changes).csv"),"w")

writer1 = csv.writer(f1)
writer1.writerow(["ID_(dec)", "ID_(hex)", "Occurrences", "Payload_Changes"])
writer2 = csv.writer(f2)
writer2.writerow(["ID_(dec)", "ID_(hex)", "Occurrences", "Payload_Changes"])
writer3 = csv.writer(f3)
writer3.writerow(["ID_(dec)", "ID_(hex)", "Occurrences", "Payload_Changes"])

for identifier in identifier_dict.values():
    if identifier.payload_changes == 0 and identifier.occurrences > 25:
        writer1.writerow([identifier.id_int,identifier.id_hex,identifier.occurrences,identifier.payload_changes])

    elif (identifier.payload_changes == 0 and identifier.occurrences <= 25) or (1 <= identifier.payload_changes <= 25):
        writer2.writerow([identifier.id_int,identifier.id_hex,identifier.occurrences,identifier.payload_changes])

    else:
        writer3.writerow([identifier.id_int, identifier.id_hex, identifier.occurrences, identifier.payload_changes])

f1.close()
f2.close()
f3.close()





