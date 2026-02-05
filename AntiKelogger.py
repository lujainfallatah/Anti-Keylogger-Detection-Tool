import json
from subprocess import check_output
import os
import io
import pyfiglet
import PySimpleGUI as sg
import time
import sys
from tqdm import tqdm

os.system("cls")

# Create a popup window
sg.theme('DarkPurple2')
layout = [[sg.Text("Do you want to scan the system? Click OK to proceed.")], [sg.Button("OK"), sg.Button("Cancel")]]
window = sg.Window("Keylogger Detection Tool", layout)

# Event loop
while True:
    event, values = window.read()

    # Exit the program if the user clicks Cancel or closes the window, and run the program if the user clicks OK
    if event == "OK":
        break
    else:
        if event == "Cancel" or event == sg.WIN_CLOSED:
            exit()

window.close()


class Process(object):
    def __init__(self, proc_info):
        print(proc_info)
        self.pid = proc_info[1]
        self.cmd = proc_info[0]

    def name(self):
        return '%s' % self.cmd

    def procid(self):
        return '%s' % self.pid


# Define the action to be performed when a keylogger is detected
def kill_logger(key_pid):
    response = input("\n\nDo you want to terminate this process: Yes/No?")
    if response.lower() == "yes":
        os.system('taskkill /f /im ' + key_pid)
    # else:
    #    pass
    exit()


def get_process_list():
    process_list = []
    sub_process = str(check_output("tasklist", shell=True).decode())
    x = io.StringIO(sub_process)
    for line in x:
        line = line.split()
        if len(line) > 0:
            process_list.append(line)
    return process_list


if __name__ == "__main__":
    process_list = get_process_list()

    def loading():
        print(pyfiglet.figlet_format("Keylogger Detection Tool", justify="center", width=110))
        print("Searching for keyloggers....")
        for i in tqdm(range(100), desc="Loading....", ascii=False, ncols=95):
            time.sleep(0.1)
        print("Scan completed.")

    loading()

    process_cmd = []
    process_pid = []

    for process in process_list:
        process_cmd.append(process[0])
        process_pid.append(process[1])

    with open("ioc.json", "r") as f:
        dict1 = json.load(f)

    record = 0
    flag = 1

    for x in process_cmd:
        for y in dict1:
            if x.find(y['name']) > -1:
                print("\n Keylogger detected: \nThe following process might be a keylogger: \n\n\t" + process_pid[
                    record] + " ---> " + x)
                kill_logger(x)
                flag = 0
        record += 1

    if flag:
        print("\n Keylogger detected:..,")