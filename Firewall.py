#!/usr/bin/python3
import subprocess
import os
import time

ips = []

subprocess.Popen(f'echo "[[ Report ]]\n\n"> report_checking_actions', shell=True, stdin=subprocess.PIPE,
                 stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def app_():
    subprocess.Popen('sudo netstat -atup  > netstate_log.txt', shell=True, stdin=subprocess.PIPE,
                     stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    with open('netstate_log.txt', 'r') as f:
        f = f.readlines()
        lines = []
        for line in f[2:]:
            line_list = line.split(" ")
            line_list = [i for i in line_list if i != '']
            lines.append(line_list)

    print("************\nChecked ips : ", ips)

    counter = 0
    for i in lines:
        if len(i) == 8 and '[::]' not in i[4]:
            x = i[4].split(":")
            if x[0] not in ips and x[0] != "0.0.0.0" and x[0] != 'localhost':
                counter += 1
                ips.append(x[0])

    if counter > 0:
        print("\n**********\nChecking Ips : ", ips[-counter:])
    else:
        print('None new ip interact to check ...')
        return
    for i in range(1, counter + 1):
        ip = ips[-i]
        print(f"Checking {ip}")
        try:
            check_output = subprocess.check_output(f"amispammer -d {ip}", shell=True, stdin=subprocess.PIPE,
                                                   stderr=subprocess.PIPE)
        except subprocess.CalledProcessError:
            check_output = subprocess.check_output(f"amispammer -i {ip}", shell=True, stdin=subprocess.PIPE,
                                                   stderr=subprocess.PIPE)
        for line_o in check_output.decode().split('\n'):
            subprocess.Popen(f'echo "{line_o}" >> report_checking_actions', shell=True, stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            lines = check_output.decode().split('\n')

        if 'REASON' in check_output.decode():
            spam_ip = lines[2].split(":")[1]

            subprocess.Popen(f"sudo iptables -A INPUT -s {spam_ip} -j DROP", shell=True, stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            subprocess.Popen(
                f'echo "---------------->> IP (blacklisted) : {spam_ip} DROPPED IN iptables " >> report_checking_actions',
                shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            print("----------> Blocked IP : ", spam_ip)
        else:
            subprocess.Popen(
                f'echo "{lines[2].split(":")[1][1:]} .. is Safe" >> report_checking_actions',
                shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        subprocess.Popen('echo " \n              **********************************'
                         '************************ \n" >> report_checking_actions', shell=True, stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)


while True:
    app_()
    print("SLEEPING ....")
    time.sleep(1)
