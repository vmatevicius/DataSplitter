from typing import List, Optional
import csv
import pandas as pd
import os
from tqdm import tqdm

def retrieve_data_from_csv(full_file_name: str) -> Optional[List[str]]:
        with open(full_file_name, "r") as file:
            lines = file.readlines()
            data = [line.strip().split(",") for line in lines]
            return data

data = retrieve_data_from_csv("em_data(B).csv")
header = ["Date/time UTC","Active energy Wh (C)","Returned energy Wh (C)"]

with open(f"TEST.csv", "w", newline='') as file:
    writer = csv.writer(file)
    writer.writerow(data[0])
    for line in data[1:]:
        active_wh = line[1]
        returned_wh = line[2]
        hour = line[0][11:13]
        minutes = line[0][14:16]
        year = line[0][6:10]
        month = line[0][3:5]
        day = line[0][:2]
        row = [f"{year}-{month}-{day} {hour}:{minutes}", f"{active_wh}", f"{returned_wh}"]
        writer.writerow(row)

print("Files created successfully")