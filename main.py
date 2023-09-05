from typing import List, Optional
import csv
import pandas as pd
import os
from tqdm import tqdm

def seperately_or_summed_up() -> str:
    while True:
        answer = input(" How do you want to calculate data?(SEPARATELY or SUMMED): ").strip().upper()
        if answer not in ["SEPARATELY", "SUMMED"]:
            print("Type correct answer")
            continue
        return answer

def get_yes_no_answer() -> str:
    while True:
        answer = input("Y/N: ").strip().upper()
        if answer not in ["Y", "N"]:
            print("wrong input")
            continue
        return answer
        
def get_correct_phase() -> str:
    while True:
        phase = input("Enter phase letter (A, B, C): ").strip().upper()
        if phase not in ["A", "B", "C"]:
            print("Wrong input, try again)")
        return phase

def get_file_amount() -> int:
    while True:
        try:
            amount = int(input("How many files do you want to split? (Enter exact number): "))
            return amount
        except Exception as e:
            print(f"Error occured while getting number: {e}")
            print("Try again, check your typing....")
            continue


def retrieve_data_from_csv(full_file_name: str) -> Optional[List[str]]:
    try:
        os.chdir(os.path.abspath(os.path.dirname(__file__)))
        with open(full_file_name, "r") as file:
            lines = file.readlines()
            data = [line.strip().split(",") for line in lines]
            return data
    except Exception as e:
        print(f"Error occured while retrieving data: {e}")
        print("Try again, if problem persists that means an error has been made....")

def get_folder_dir(phase: str) -> Optional[str]:
    try:
        base_dir = os.path.abspath(os.path.dirname(__file__))
        directory_path = os.path.join(base_dir, f"Sorted data({phase})")
        return directory_path
    except Exception as e:
        print(f"Error occured while getting folder dir: {e}")
        print("Try again, if problem persists that means an error has been made....")

def sort_csv_files(full_file_name: str) -> None:
    try:
        os.chdir(os.path.abspath(os.path.dirname(__file__)))
        file = pd.read_csv(full_file_name)
        file.sort_values("Date/time UTC", axis=0, ascending=True,inplace=True, na_position='first')
        file.to_csv(full_file_name, index=False)
    except Exception as e:
        print(f"Error occured while sorting files: {e}")
        print("Try again, if problem persists that means an error has been made....")
        
def make_new_folder(phase: str) -> Optional[bool]:
    try:
        os.mkdir(os.path.join(os.path.abspath(os.path.dirname(__file__)), f"Sorted data({phase})"))
        return True
    except Exception as e:
        print(f"Error occured while creating a new folder: {e}")
        print("Try again, if problem persists that means an error has been made....")

    
def create_file(year:str, month: str, day:str, data: List[str], one_day_data: List[str], phase: str) -> bool:
    try:
        with open(f"{year}-{month}-{day}_em_data({phase}).csv", "w", newline='') as file:
            writer = csv.writer(file)
            writer.writerow(data[0])
            for one_hour in one_day_data:
                writer.writerow(one_hour)
        return True
    except  Exception as e:
        print(f"Error occured while creating a new file: {e}")
        print("Try again, if problem persists that means an error has been made....")
        return False

        
def call_date_rearangement() -> Optional[bool]:
    counter = 0
    file_count = get_file_amount()
    while file_count > counter:
        print(" Is your files date format like this DD/MM/YYYY?: ")
        print()
        answer = get_yes_no_answer()
        print()
        if answer == "Y":
            full_file_name = input("Enter full file name(instead of PHASE type the correct letter): ")
            phase = get_correct_phase()
            data = (retrieve_data_from_csv(full_file_name))
            rearange_dates(data, phase)
            print("dates rearanged successfully")
            print()
            counter += 1
        else:
            return file_count
    return file_count
        
def rearange_dates(data: List[str], phase: str) -> None:
    
    
    pbar = tqdm(total=len(data))
    print("      rearanging dates......")
    with open(f"em_data({phase}).csv", "w", newline='') as file:
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
            pbar.update(1)
        pbar.close()


def call_file_splitting(file_count: int) -> bool:
    counter = 0 
    while file_count > counter:
        full_file_name = input("Enter full file name(instead of PHASE type the correct letter): ")
        phase = get_correct_phase()
        print()
        data = (retrieve_data_from_csv(full_file_name))
        
        print()
        sort_csv_files(full_file_name) 
        data = (retrieve_data_from_csv(full_file_name))
        if split_separate_phase_data_to_days(data, phase):
            print("Files split succesfully")
            counter += 1
        else:
            print("Error occured try again")
            return False


def split_separate_phase_data_to_days(data: List[str], phase: str, dts_start: str, dts_stop:str) -> bool:
    try:
        print("     splitting phase data to days..........")
        pbar = tqdm(total=len(data))
        one_day_data = []
        total_daily_active_wh = 0 
        total_daily_returned_wh = 0
        day = 0
        hour = 0
        month = 0
        year = 0
        one_hour_active_wh = 0
        one_hour_returned_wh = 0
        total = 0 
        daily_total = 0
        for line in data[1:]:
            active_wh = line[1]
            returned_wh = line[2]
            total += float(active_wh)

            if month == 0:
                month == line[0][5:7]
            if month != line[0][5:7]:
                month = line[0][5:7]
            
            if day == 0:
                day = line[0][8:10]
            if day != line[0][8:10]:
                one_day_data.append(["Total", f"active = {round(total_daily_active_wh, 2)}", f" returned = {round(total_daily_returned_wh, 2)}"])
                
                directory_path = get_folder_dir(phase)
                if os.path.exists(directory_path):
                    os.chdir(directory_path)
                else:
                    make_new_folder(phase)
                    os.chdir(directory_path)
                create_file(year,month,day,data,one_day_data,phase)
                
                one_day_data = []
                total_daily_active_wh = 0
                total_daily_returned_wh = 0
                day = line[0][8:10]
            
            if hour == 0:
                hour = line[0][11:13]
                one_hour_active_wh += float(active_wh)
                one_hour_returned_wh += float(returned_wh)
            
            elif hour != line[0][11:13]:
                if
                
                one_hour_active_wh += float(active_wh)
                one_hour_returned_wh += float(returned_wh)
                one_day_data.append([f"{year}-{month}-{day} {hour}:00",f"{round(one_hour_active_wh, 2)}",f"{one_hour_returned_wh}"])
                daily_total += one_hour_active_wh
                total_daily_returned_wh += one_hour_returned_wh
                total_daily_active_wh += one_hour_active_wh
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
            pbar.update(1)
        pbar.close()
        with open(f"total.txt", "w", newline='') as file:
            file.write(f"Total wh: {total}")
        print("Files created successfully")
        return True
    except Exception as e:
        print(f"Error occured while splitting data: {e}")
        print("Try again, if problem persists that means an error has been made....")
        return False

def sort_data_hourly(data: List[str]) -> List[str]:
        try:
            pbar = tqdm(total=len(data))
            print("        sorting data hourly......")
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
                pbar.update(1)
            pbar.close()
            return hourly_data
        except Exception as e:
            print(f"Error occured while sorting data hourly: {e}")
            print("Try again, if problem persists that means an error has been made....")
            return False
    
def split_data_to_days(data: List[str]) -> bool:
    try:
        pbar = tqdm(total=len(data))
        print("       splitting days......")
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
        
        # Create the last file after processing all data
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
        
        with open(f"total.txt", "w", newline='') as file:
            file.write(f"Total wh: {total}")
        pbar.close()
        print("Files created successfully")
        return True
    except Exception as e:
        print(f"Error occured while splitting data to days: {e}")
        print("Try again, if problem persists that means an error has been made....")
        return False

def sum_up_values(phase_one: List[str], phase_two: List[str], phase_three: List[str]) -> List[str]:
    try:
        daily_data = []
        pbar = tqdm(total=len(phase_one))
        print("       Summing up values.... This may take a while")
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
    except Exception as e:
        print(f"Error occured while summing up values: {e}")
        print(" It might because of date structure")
        print(" Try again, if problem persists that means an error has been made....")
        return False

def launch_application() -> None:
    print()
    print(" You can only split one document at the time")
    print(" Data files MUST be in the same directory as the application ")
    print(" Data files MUST be identical to example 'em_data(PHASE).csv', Phases are - A, B, C")
    print(" If program fails it is highly likely that you entered wrong information")
    print()
    print(" These files usually come in UTC+0 format" )
    print(" So you need to specify the dates when daylight saving starts and ends" )
    
    daylight_saving_start = input("Enter starting date (MM/DD): ").strip()
    daylight_saving_stop = input("Enter ending date (MM/DD): ").strip()
    
    
    choice = seperately_or_summed_up()
    files_count = call_date_rearangement()
    sort_csv_files("em_data(A).csv")
    sort_csv_files("em_data(B).csv")
    sort_csv_files("em_data(C).csv")
    if choice == "SUMMED":
        phase_a = retrieve_data_from_csv("em_data(A).csv")
        phase_b = retrieve_data_from_csv("em_data(B).csv")
        phase_c = retrieve_data_from_csv("em_data(C).csv")
        one_hour_a = sort_data_hourly(phase_a)
        one_hour_b = sort_data_hourly(phase_b)
        one_hour_c = sort_data_hourly(phase_c)
        daily_data = sum_up_values(one_hour_a, one_hour_b,one_hour_c)
        split_data_to_days(daily_data)
    else:
        call_file_splitting(files_count)
    
    
if __name__ == "__main__":
    launch_application()