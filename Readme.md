combine_csv_files.py .. combine all the csv files into only one

simple_api_flask.py ..  run api server , with the option to get the data or changing it if you are authorized for changing it

str_hex_bin .. pyhton file that convert (str or int) val to (hex, bin) val , while using args to be used from /usr/bin/ without cd to file location 

Firewall.py .. python file(act as firewall for linux users) that checks for ips that pc interact with , and block in iptables those which are blacklisted .. [Note : (netstat , amispammer) must be installed and sudo privilage needed ...To let it works in background 'just comment every print()'], blacklisted in iptable will not be permanent to give you space to choose either save them or save them  ... 
-to save iptables ('sudo iptables-save > 'path'/'file_name')
-to restore iptables rules ('sudo iptables-restore < 'same-path'/'same-file_name')
