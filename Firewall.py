#!/usr/bin/python3
import subprocess
import os
import time
import json


def start_():
    """it's create the log file, or read it if existed the """
    ips_ = {"checked ips": [],
            "checking ips": [],
            "blacklisted": []}
    if os.path.isfile("Ips_log.json"):
        with open("Ips_log.json", "r") as f:
            ips = json.load(f)
            if not ips:
                ips = ips_
    else:
        with open("Ips_log.json", "w") as f:
            ips = ips_
            json.dump(ips, f)

    return ips


def app_():
    """It blocks the server's ip , not the host name, so may block some domains if they are attached to poisoned ip """
    ips = start_()
    f = subprocess.check_output('sudo netstat -atupn ', shell=True,
                                stdin=subprocess.PIPE, stderr=subprocess.PIPE).decode()

    lines = []
    for line in f.split("\n")[2:]:
        line_list = line.split(" ")
        line_list = [i for i in line_list if i != '']
        lines.append(line_list)

    for i in lines:
        if len(i) == 8 and '[::]' not in i[4]:
            x = i[4].split(":")
            if x[0] not in ips['checked ips'] + ips["checking ips"] + ips["blacklisted"] + ["0.0.0.0", 'localhost']:
                ips["checking ips"].append(x[0])

    if ips["checking ips"]:
        print("\n**********\nChecking Ips : ", ips["checking ips"])
        with open('Ips_log.json', 'w') as f:
            json.dump(ips, f)
    else:
        print('None new ip interact to check ...')
        return

    for ip in ips["checking ips"]:
        print(f"Checking {ip}")

        check_output = subprocess.check_output(f"amispammer -i {ip}", shell=True, stdin=subprocess.PIPE,
                                               stderr=subprocess.PIPE)

        lines = check_output.decode().split('\n')
        ips["checked ips"].append(ip)

        if 'REASON' in check_output.decode():
            spam_ip = lines[2].split(":")[1]
            # the change in iptables not permanent, so save it or ignore before rebooting the system .. it's up to you
            subprocess.Popen(f"sudo iptables -A INPUT -s {spam_ip} -j DROP", shell=True, stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            print("----------> Blocked IP : ", spam_ip)
            ips["blacklisted"].append(spam_ip)
    ips["checking ips"] = []
    with open("Ips_log.json", "w") as f:
        json.dump(ips, f)


while True:
    app_()
    print("SLEEPING ....")
    time.sleep(1)
