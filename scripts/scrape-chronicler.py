#!bin/python3

import os
import subprocess

start_day = 9
end_day = 13
start_hour = 15
start_min = 0
end_hour = 23


def convert_num(num):
    if num < 10:
        return f'0{num}'
    else:
        return f'{num}'

cur_day = start_day
cur_hour = start_hour
count = 0
while cur_day < end_day or (cur_day == end_day and cur_hour < end_hour):
    str_day = convert_num(cur_day)
    str_hour = convert_num(cur_hour)
    cur_start_ts = f"2023-01-{str_day}T{str_hour}:00:00.000Z"
    cur_end_ts = f"2023-01-{str_day}T{str_hour}:30:00.000Z"
    cur_file = f"../data/s1/raw/game_{count}.json"
    cmd = f"curl -X GET \"https://api2.sibr.dev/chronicler/v0/game-events?after={cur_start_ts}&before={cur_end_ts}\" -H \"accept: application/json\" > {cur_file}"
    if not os.path.exists(cur_file):
        returned_value = subprocess.call(cmd, shell=True)  # returns the exit code in unix

    print("cmd = " + cmd)
    count += 1
    if cur_hour + 1 > 23:
        new_hour = convert_num(0)
        new_day = convert_num(cur_day + 1)
    else:
        new_hour = convert_num(cur_hour + 1)
        new_day = convert_num(cur_day)
    cur_start_ts = f"2023-01-{str_day}T{str_hour}:30:00.000Z"
    cur_end_ts = f"2023-01-{new_day}T{new_hour}:00:00.000Z"
    cur_file = f"../data/s1/raw/game_{count}.json"
    cmd = f"curl -X GET \"https://api2.sibr.dev/chronicler/v0/game-events?after={cur_start_ts}&before={cur_end_ts}\" -H \"accept: application/json\" > {cur_file}"
    print("cmd = " + cmd)
    if not os.path.exists(cur_file):
        returned_value = subprocess.call(cmd, shell=True)  # returns the exit code in unix
    #exit(0)
    count += 1

    if cur_hour + 1 > 23:
        cur_hour = 0
        cur_day = cur_day + 1
    else:
        cur_hour = cur_hour + 1
        cur_day = cur_day
