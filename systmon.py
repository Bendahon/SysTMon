# <----------------->
# | python3         |
# | Bendahon 2020   |
# <----------------->
from time import time
from datetime import datetime
import os

# Global vars
LocalFolderName = f"{os.getenv('HOME')}/.bendahon/"
SysTMonFolderName = LocalFolderName + "systmon/"
StatusFileName = f"{SysTMonFolderName}Login"


# Commands to be run with the program
run_commands = \
    [
        "===========Disks===========",
        "lsblk -o NAME,SIZE,TYPE,MOUNTPOINT | grep -v loop",
        "---------------------",
        "df -h | grep -v loop | grep -v tmpfs | grep -v udev",
        "===========OS===========",
        "uname -a",
        # "cat /etc/*-release | grep PRETTY",
        "cat /etc/lsb-release | grep RELEASE",
        "id",
        "uptime",
        "===========RAID===========",
        "cat /proc/mdstat | grep -v Person | grep -v unused"
    ]


def pass_cmd_to_shell(cmd):
    # cmd is the command passed in E.G  -- "cat /foo/SecretPassword.txt"
    # print(cmd)
    stdint = os.popen(cmd)
    output = stdint.read()
    return output


def write_stats(listin):
    # listin = commands: E.G ["pinky", lsblk"]
    # Get object of date_time
    current_date = datetime.fromtimestamp(time())
    # Get a YYYY/MM/DD format
    get_date_and_time = current_date.strftime("%Y-%m-%d---%H:%M:%S")
    stat_write_file_name = f"{StatusFileName}-{get_date_and_time}"
    statfile = open(stat_write_file_name, "w", encoding="utf-8")
    statfile.write(f"Generated: {get_date_and_time}\n")
    for listi in listin:
        if listi.startswith("==="):
            statfile.write(str(f"\n{listi}\n"))
        elif listi.startswith("---"):
            statfile.write(str(f"{listi}\n"))
        else:
            stat = pass_cmd_to_shell(listi)
            statfile.write(str(stat.strip() + "\n"))
    statfile.close()
    print(pass_cmd_to_shell(f"cat '{stat_write_file_name}'"))


def check_folders_exits():
    if not os.path.exists(LocalFolderName):
        print("Default folder doesnt exit, creating")
        os.mkdir(LocalFolderName)
    if not os.path.exists(SysTMonFolderName):
        print("systmon folder doesn't exist, creating")
        os.mkdir((SysTMonFolderName))


def arg_pass():
    write_stats(run_commands)


def main():
    print("SysTMon by Bendahon 2020")
    # Check if the status file exits
    check_folders_exits()
    arg_pass()


if __name__ == "__main__":
    main()
