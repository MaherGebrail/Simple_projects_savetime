#!/usr/bin/python3
import subprocess
import os
import time
import json


def start_():
    if not os.path.isfile("Ips_log.json"):
        with open("Ips_log.json", "w") as f:
            ips = {"checked ips": [],
                   "checking ips": [],
                   "blacklisted": []}
            json.dump(ips, f)
    else:
        with open("Ips_log.json", "r") as f:
            ips = json.load(f)
            if not ips:
                ips = {"checked ips": [],
                       "checking ips": [],
                       "blacklisted": []}
    return ips


def app_():
    ips = start_()
    f = subprocess.check_output('sudo netstat -atup ', shell=True,
                                stdin=subprocess.PIPE, stderr=subprocess.PIPE).decode()
    # print(f)
    lines = []
    for line in f.split("\n")[2:]:
        line_list = line.split(" ")
        line_list = [i for i in line_list if i != '']
        lines.append(line_list)

    for i in lines:
        if len(i) == 8 and '[::]' not in i[4]:
            x = i[4].split(":")
            if x[0] not in ips['checked ips'] and x[0] not in ips["checking ips"] and x[0] != "0.0.0.0" \
                    and x[0] != 'localhost':
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
        try:
            check_output = subprocess.check_output(f"amispammer -d {ip}", shell=True, stdin=subprocess.PIPE,
                                                   stderr=subprocess.PIPE)
        except subprocess.CalledProcessError:
            check_output = subprocess.check_output(f"amispammer -i {ip}", shell=True, stdin=subprocess.PIPE,
                                                   stderr=subprocess.PIPE)

        lines = check_output.decode().split('\n')
        ips["checked ips"].append(ip)

        if 'REASON' in check_output.decode():
            spam_ip = lines[2].split(":")[1]
            subprocess.Popen(f"sudo iptables -A INPUT -s {spam_ip} -j DROP", shell=True, stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            subprocess.Popen(f"sudo iptables -A INPUT -d {spam_ip} -j DROP", shell=True, stdin=subprocess.PIPE,
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
