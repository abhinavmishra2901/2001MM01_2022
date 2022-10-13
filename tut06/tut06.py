# Assignment 06 CS384 -     Attendance Report Generator.
# By Abhinav Mishra - 2001MM01

# Libraries
from platform import python_version
import os
import csv

from datetime import datetime
import calendar

start_time = datetime.now()
os.system("cls")

# Code

# Defining a Function to Find the day corresponding to the given date


def findDay(date):
    born = datetime.strptime(date, '%d %m %Y').weekday()
    return (calendar.day_name[born])


def attendance_report():
    try:
        # List to store the data of the registered students by taking input from input_registered_students.csv
        reg_students = []
        with open("input_registered_students.csv", 'r') as input_reg:
            read_reg = csv.DictReader(input_reg)
            for row in read_reg:
                reg_students.append(
                    row["Roll No"].upper()+" "+row["Name"].upper())

        # List to store the data of the attendance of the students by taking input from input_attendance.csv
        timestamp = []
        attendance = []
        with open("input_attendance.csv", 'r') as input_attendance:
            read_att = csv.DictReader(input_attendance)
            for row in read_att:
                timestamp.append(row["Timestamp"].upper())
                attendance.append(row["Attendance"].upper())

    # FileNotFound Error
    except FileNotFoundError:
        print("Input File not found!")
        exit()
    # Other errors if any
    except:
        print("Some error occured while reading the input file")
        exit()

    # A list to store the attendance timestamps of all the students
    student_timestamps = []
    for name in reg_students:
        # A list to store the attendance timestamp of individual students
        individual_timestamp = []
        for i in range(len(attendance)):
            # Comparing the attendance by roll numbers
            if attendance[i][:9] == name[:9]:
                individual_timestamp.append(timestamp[i])
        student_timestamps.append(individual_timestamp)

    # Creating various lists to store the corresponding data to be output later to the csv files
    fake_count = []
    actual_count = []
    absent_count = []
    total_dates = []
    total_days = []

    for i in range(len(student_timestamps)):
        fake = 0
        actual = 0
        for j in student_timestamps[i]:
            # Checking the condition if the attendance were marked within the class duration or not
            if j[:10].replace('/', ' ') not in total_dates:
                total_dates.append(j[:10].replace('/', ' '))
            if (int(j[11:13]) < 14 or int(j[11:13]) > 14) and (j[11:] != "15:00:00"):
                # Removing fake counts from the individual list
                student_timestamps[i].remove(j)
                fake += 1  # increasing the fake attendance count if any fake attendance was marked by the student
        actual = len(student_timestamps[i])
        fake_count.append(fake)
        actual_count.append(actual)

    # Checking the condition if the attendance were marked on Mondays and Thursdays or not
    # Here at the same time I am counting the total number of class days
    for i in total_dates:
        if findDay(i) == 'Monday' or findDay(i) == 'Thursday':
            total_days.append(findDay(i))
    total_days_count = len(total_days)
    for i in actual_count:
        absent_count.append(total_days_count-i)

    # Creating a final_rows list to store the rows to be output
    final_rows = []
    for i in range(len(reg_students)):
        # Creating an individual row list to be appended later to the final_rows list
        individual_row = []
        # Appending the respective values to the respective lists
        individual_row.append(reg_students[i][:8])
        individual_row.append(reg_students[i][9:])
        individual_row.append(total_days_count)
        individual_row.append(actual_count[i])
        individual_row.append(fake_count[i])
        individual_row.append(absent_count[i])
        percentage_count = round((actual_count[i]/total_days_count)*100, 2)
        individual_row.append(percentage_count)
        final_rows.append(individual_row)

    try:
        # Header File
        header_line = [
            "Roll,Name,total_lecture_taken,attendance_count_actual,attendance_count_fake,attendance_count_absent,Percentage (attendance_count_actual/total_lecture_taken) 2 digit decimal\n"]
        for row in final_rows:
            # Creating individual roll number files
            roll_output = open("output/"+row[0]+".csv", 'w')
            roll_output.writelines(header_line)
            roll_output.writelines((str(row[0]), ",", str(row[1]), ",", str(row[2]), ",", str(
                row[3]), ",", str(row[4]), ",", str(row[5]), ",", str(row[6]), "\n"))
            roll_output.close()  # Closing the output file
    except:
        print("Something went wrong while writing to octant_output.csv")
        exit()

#Version Check
ver = python_version()

if ver == "3.8.10":
    print("Correct Version Installed")
else:
    print("Please install 3.8.10. Instruction are present in the GitHub Repo/Webmail. Url: https://pastebin.com/nvibxmjw")


attendance_report()


# This shall be the last lines of the code.
end_time = datetime.now()
print('Duration of Program Execution: {}'.format(end_time - start_time))
print("Files Created Successfully")
