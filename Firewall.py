#!/usr/bin/python3
import subprocess
import os
import time
import json


def start_():
    """it creates the log file, or read it if existed  """
    ips_ = {"checked ips": [],
            "checking ips": [],
            "blacklisted": []}
    if os.path.isfile("Ips_log.json"):
        with open("Ips_log.json", "r") as f:
            ips = json.load(f)
            subprocess.Popen(f"sudo iptables -F", shell=True, stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            for bip in ips['blacklisted']:
                subprocess.Popen(f"sudo iptables -A INPUT -s {bip} -j DROP", shell=True, stdin=subprocess.PIPE,
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    else:
        with open("Ips_log.json", "w") as f:
            ips = ips_
            json.dump(ips, f)

    return ips


ips = start_()


def app_():
    """It blocks the server's ip , not the host name, so may block some domains if they are attached to poisoned ip """

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
        with open('Ips_log.json', 'w') as f:
            json.dump(ips, f)
    else:
        return

    for ip in ips["checking ips"]:
        check_output = subprocess.check_output(f"amispammer -i {ip}", shell=True, stdin=subprocess.PIPE,
                                               stderr=subprocess.PIPE)

        lines = check_output.decode().split('\n')
        ips["checked ips"].append(ip)

        if 'REASON' in check_output.decode():
            spam_ip = lines[2].split(":")[1]
            subprocess.Popen(f"sudo iptables -A INPUT -s {spam_ip} -j DROP", shell=True, stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            ips["blacklisted"].append(spam_ip)
    ips["checking ips"] = []
    with open("Ips_log.json", "w") as f:
        json.dump(ips, f)


checkIPTABLES = True


def check_iptables():
    """Check if all blocked ips in iptables at the start of the program"""
    getTables = subprocess.check_output('sudo iptables -L --line-numbers', shell=True,
                                        stderr=subprocess.PIPE, stdin=subprocess.PIPE).decode().split("\n")
    last_number = 0
    for i in getTables:
        if len(i) >= 1:
            if i[0].isdigit():
                number = ""
                for num in i:
                    if num.isdigit():
                        number = number+str(num)
                    else:
                        break
                if number:
                    if int(number) > last_number:
                        last_number = int(number)

    with open("Ips_log.json", "r") as f:
        ips = json.load(f)
        gotBlacklisted = len(ips['blacklisted'])

    if gotBlacklisted == last_number:
        return False
    else:
        start_()
        return True


while True:
    app_()
    if checkIPTABLES:
        checkIPTABLES = check_iptables()
    time.sleep(1)
