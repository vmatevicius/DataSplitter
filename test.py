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
        
def make_new_folder(phase: str) -> Optional[bool]:
    try:
        os.mkdir(os.path.join(os.path.abspath(os.path.dirname(__file__)), f"Sorted data({phase})"))
        return True
    except Exception as e:
        print(f"Error occured while creating a new folder: {e}")
        print("Try again, if problem persists that means an error has been made....")

def get_folder_dir(phase: str) -> Optional[str]:
    try:
        base_dir = os.path.abspath(os.path.dirname(__file__))
        directory_path = os.path.join(base_dir, f"Sorted data({phase})")
        return directory_path
    except Exception as e:
        print(f"Error occured while getting folder dir: {e}")
        print("Try again, if problem persists that means an error has been made....")

phase_a = retrieve_data_from_csv("em_data(A).csv")
phase_b = retrieve_data_from_csv("em_data(B).csv")
phase_c = retrieve_data_from_csv("em_data(C).csv")


def sort_data_hourly(data: List[str]) -> List[str]:
        try:
            hourly_data = []
            day = 0
            hour = 0
            month = 0
            year = 0
            one_hour_active_wh = 0
            one_hour_returned_wh = 0
            for line in data[1:]:
                active_wh = line[1]
                returned_wh = line[2]

                if hour == 0:
                    hour = line[0][11:13]
                    one_hour_active_wh += float(active_wh)
                    one_hour_returned_wh += float(returned_wh)
                
                elif hour != line[0][11:13]:
                    one_hour_active_wh += float(active_wh)
                    one_hour_returned_wh += float(returned_wh)
                    hourly_data.append([f"{year}-{month}-{day} {hour}:00",f"{round(one_hour_active_wh, 2)}",f"{one_hour_returned_wh}"])
                    one_hour_active_wh = 0
                    one_hour_returned_wh = 0 
                    hour = line[0][11:13]

                elif hour == line[0][11:13]:
                    one_hour_active_wh += float(active_wh)
                    one_hour_returned_wh += float(returned_wh)


                if year == 0:
                    year = int(line[0][:4])
                if year != int(line[0][:4]):
                    year +=  1
                if month == 0:
                    month == line[0][5:7]
                if month != line[0][5:7]:
                    month = line[0][5:7]
                
                if day == 0:
                    day = line[0][8:10]
                if day != line[0][8:10]:
                    day = line[0][8:10]
            return hourly_data
        except Exception as e:
            print(f"Error occured while sorting data hourly: {e}")
            print("Try again, if problem persists that means an error has been made....")
            return False

one_hour_a = sort_data_hourly(phase_a)
one_hour_b = sort_data_hourly(phase_b)
one_hour_c = sort_data_hourly(phase_c)

def sum_up_values(phase_one: List[str], phase_two: List[str], phase_three: List[str]) -> List[str]:
        daily_data = []
        pbar = tqdm(total=len(phase_one))
        for hour_a in phase_one:
            for hour_b in phase_two:
                if hour_a[0] == hour_b[0]:
                    hour_a[1] = str(float(hour_a[1]) + float(hour_b[1]))
                else:
                    continue
            for hour_c in phase_three:
                if hour_a[0] == hour_c[0]:
                    hour_a[1] = str(float(hour_a[1]) + float(hour_c[1]))
                else:
                    continue
            daily_data.append(hour_a)
            pbar.update(1)
        pbar.close()
        return daily_data

daily_data = sum_up_values(one_hour_a, one_hour_b,one_hour_c)


def split_data_to_days(data: List[str]) -> bool:
    try:
        pbar = tqdm(total=len(data))
        header = ["Date/time UTC","Active energy Wh (C)","Returned energy Wh (C)"]
        one_day_data = []
        day = 0
        hour = 0
        month = 0
        year = 0
        total = 0

        for line in data:
            total += float(line[1])
            
            if day == 0:
                day = line[0][8:10]
            if day != line[0][8:10]:
                directory_path = get_folder_dir("summed")
                if os.path.exists(directory_path):
                    os.chdir(directory_path)
                else:
                    make_new_folder("summed")
                    os.chdir(directory_path)
                with open(f"{year}-{month}-{day}_em_data.csv", "w", newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(header)
                    for one_hour in one_day_data:
                        writer.writerow(one_hour)
                one_day_data = []
                day = line[0][8:10]

            if hour == 0:
                hour = line[0][11:13]
                one_day_data.append(line)
            
            elif hour != line[0][11:13]:
                one_day_data.append(line)
                hour = line[0][11:13]

            if year == 0:
                year = int(line[0][:4])
            if year != int(line[0][:4]):
                year +=  1
            if month == 0:
                month == line[0][5:7]
            if month != line[0][5:7]:
                month = line[0][5:7]
            
            pbar.update(1)
        with open(f"total.txt", "w", newline='') as file:
            file.write(f"Total wh: {total}")
        pbar.close()
        print("Files created successfully")
        return True
    except Exception as e:
        print(f"Error occured while splitting data to days: {e}")
        print("Try again, if problem persists that means an error has been made....")
        return False


split_data_to_days(daily_data)
