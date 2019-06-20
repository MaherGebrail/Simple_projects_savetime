import csv
import os


csv_files_names=[]
with open("new_excel_new.csv","w") as f :
    for file in os.listdir('.'):

        if file.endswith(".csv") and not file.endswith("new.csv"):
            csv_files_names.append(file)


    with open(csv_files_names[0]) as r :
        read = csv.reader(r)
        lines = list(read)
        writer_csv = csv.writer(f)
        writer_csv.writerows(lines)

    for file_name in csv_files_names[1::]:
        with open(file_name,"r") as r:
            read = csv.reader(r)
            lines = list(read)[1::]
            writer_csv = csv.writer(f)
            writer_csv.writerows(lines)

