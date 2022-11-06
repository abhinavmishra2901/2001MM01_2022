# Assignment 06 CS384 -     Attendance Report Generator.
# By Abhinav Mishra - 2001MM01

# Libraries
from platform import python_version
import os
import csv

import numpy as np
import pandas as pd

from datetime import datetime
import calendar
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import warnings


# To remove any unnecessary warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# Code

start_time = datetime.now()
os.system("cls")

# Defining a Function to Find the day corresponding to the given date


def findDay(date):
    born = datetime.strptime(date, '%d-%m-%Y').weekday()
    return (calendar.day_name[born])

# Defining a function to mail the consolidate attendance report


def email(sender_address, sender_pass):
    try:
        mail_content = '''Hello Sir,
        Please find attached the consolidated attendance report.
        Thank You
        Abhinav Mishra
        2001MM01
        '''
        # The mail addresses and password
        receiver_address = 'cs3842022@gmail.com'
        cc = 'abhinavmishra2901@gmail.com'

        # Setup the MIME
        message = MIMEMultipart()
        message['From'] = sender_address
        message['To'] = receiver_address
        message['CC'] = cc

        # The subject line
        message['Subject'] = 'Consolidated Attendance Report sent by Python. It has an attachment.'

        # The body and the attachments for the mail
        message.attach(MIMEText(mail_content, 'plain'))
        os.chdir(os.getcwd().replace('\\', "/")+"/output/")
        attach_file_name = 'attendance_report_consolidated.xlsx'

        # Open the file as binary mode
        attach_file = open(attach_file_name, 'rb')
        payload = MIMEBase('application', 'octate-stream')
        payload.set_payload((attach_file).read())
        encoders.encode_base64(payload)  # encode the attachment

        # add payload header with filename
        payload.add_header('Content-Disposition',
                           "attachment; filename= %s" % attach_file_name)
        message.attach(payload)

        # Create SMTP session for sending the mail
        session = smtplib.SMTP('smtp.gmail.com', 587,
                               timeout=120)  # use gmail with port

        session.starttls()  # enable security

        # login with mail_id and password
        session.login(sender_address, sender_pass)
        text = message.as_string()
        session.sendmail(sender_address, receiver_address, text)
        print('Mail Sent')  # Confirmation that the mail is sent
        session.quit()  # Quitting the session
    except:
        print("There was some error in mailing the consolidate attendance report.")

# Attendance Report Function


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

    total_dates = []
    for i in timestamp:
        # Checking the condition if the attendance were marked on class dates and on Monday and Thursday or not
        if i[:10] not in total_dates and (findDay(i[:10]) == 'Monday' or findDay(i[:10]) == 'Thursday'):
            total_dates.append(i[:10])

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

    # The main part of the function
    # Storing all students attendance report in all_students_data
    all_students_data = []
    # Defining a list to store consolidated data
    consolidated_data = []
    # Iterating through the list of registered students
    for i in range(len(reg_students)):
        # Defining the sublist report which is the row wise data of consolidated report
        report = [reg_students[i][:8], reg_students[i][9:]]
        # Defining a variable to store the total real count
        total_real = 0
        # Attendance report of a particular student stored in individual_student_data
        individual_student_data = []
        for j in range(len(total_dates)):
            # Creating a unique list to store unqiue timestamps of a student
            unique = []
            # Each row of individual student's attendance report
            row_data = [0, '', '', 0, 0, 0, 0, 0]
            for k in range(len(student_timestamps[i])):
                datestamp = student_timestamps[i][k][:10]
                row_data[0] = total_dates[j]
                # If the student has marked the attendance on a valid date
                if datestamp == total_dates[j]:
                    # Total Attendance Count increased
                    row_data[3] += 1
                    # If the student has marked the attendance on a valid time
                    if student_timestamps[i][k][11:13] == '14' or student_timestamps[i][k][11:] == '15:00:00':
                        # Real Count increased
                        row_data[4] += 1
                        # Total Real Count also increased
                        total_real += 1
                        # Subtracting the Absent Count
                        row_data[7] -= 1
                        # If datestamp is not present in unique, adding it to the list
                        if datestamp not in unique:
                            unique.append(datestamp)
                        # If datestamp is present in unique, the datestamp is a duplicate
                        elif datestamp in unique:
                            # Increasing Duplicate Count
                            row_data[5] += 1
                            # Decreasing Real Count
                            row_data[4] -= 1
                    # If the student has not marked the attendance on a valid time, it is a FAKE
                    else:
                        row_data[6] += 1
            # If the absent count is negative, the student is present and hence absent count is 0 and P is appended to report
            if row_data[7] < 0:
                row_data[7] = 0
                report.append('P')
            # Else Absent count is 1 and 'A' is appended to Report
            else:
                row_data[7] = 1
                report.append('A')
            individual_student_data.append(row_data)

        # Appending the total_dates, total_real count and attendance percentage to report
        report.append(len(total_dates))
        report.append(total_real)
        report.append(round(total_real*100/len(total_dates), 2))
        # Appending the report to consolidated_data and individual_student_data to all_students_data
        consolidated_data.append(report)
        all_students_data.append(individual_student_data)

    try:

        # OUTPUT - 1

        # Creating individual roll number files
        i = 0
        for student in all_students_data:
            # 2nd Row of Roll No. and Name of the student
            student.insert(0, ['', reg_students[i][:8],
                               reg_students[i][9:], '', '', '', '', ''])
            # Saving the file as roll.csv
            np.savetxt("output/"+reg_students[i][:8]+".csv", student, header="Date,Roll,Name,Total Attendance Count,Real,Duplicate,Invalid,Absent", delimiter=",",
                       fmt='%s', comments='')

            # Reading the csv file
            df_new = pd.read_csv("output/"+reg_students[i][:8]+".csv")

            # saving xlsx file
            roll_output = pd.ExcelWriter("output/"+reg_students[i][:8]+".xlsx")
            df_new.to_excel(roll_output, index=False,
                            sheet_name=reg_students[i][:8])

            # Adjusting the Column Widths
            for column in df_new:
                column_width = max(df_new[column].astype(
                    str).map(len).max(), len(column))
                col_idx = df_new.columns.get_loc(column)
                roll_output.sheets[reg_students[i][:8]].set_column(
                    col_idx, col_idx, column_width)
            roll_output.save()  # Saving the Excel File

            # Deleting the csv File
            os.remove("output/"+reg_students[i][:8]+".csv")
            i += 1

        # OUTPUT - 2

        # Creating consolidated report file

        # Defining the header
        consolidated_header = 'Roll,Name'
        for date in total_dates:
            consolidated_header += ','+str(date)
        consolidated_header += ',Actual Lecture Taken,Total Real,%Attendance'

        # Saving the file as attendance_report_consolidated.csv
        np.savetxt("output/attendance_report_consolidated.csv", consolidated_data, header=consolidated_header, delimiter=",",
                   fmt='%s', comments='')

        # Reading the csv file
        df_new = pd.read_csv("output/attendance_report_consolidated.csv")

        # Saving xlsx file
        roll_output = pd.ExcelWriter(
            "output/attendance_report_consolidated.xlsx")
        df_new.to_excel(roll_output, index=False,
                        sheet_name="Consolidated Report")

        # Adjusting the column widths
        for column in df_new:
            column_width = max(df_new[column].astype(
                str).map(len).max(), len(column))
            col_idx = df_new.columns.get_loc(column)
            roll_output.sheets['Consolidated Report'].set_column(
                col_idx, col_idx, column_width)

        roll_output.save()  # Saving the Excel File

        # Deleting the csv File
        os.remove("output/attendance_report_consolidated.csv")

        # OUTPUT - 3

        # Asking the User for the option to mail the consolidated Attendance Report
        x_check = 0
        while (x_check == 0):
            x = input(
                "Do you wish to email the consolidated Attendance Report to cs3842022@gmail.com? (YES/NO)")
            if x.upper() == "YES":
                print("You need to generate an app password by following the steps mentioned in: https://support.google.com/accounts/answer/185833?hl=en")
                emailid = input("Enter Your Email ID: ")
                password = input("Enter Your Password: ")
                email(emailid, password)
                x_check = 1

            elif x.upper() == "NO":
                print("Ok!")
                x_check = 1
            else:
                print("Please enter either YES or NO!")

    except:
        print("Something went wrong while writing to octant_output.csv")
        exit()


# Version Check
ver = python_version()

if ver == "3.8.10":
    print("Correct Version Installed")
else:
    print("Please install 3.8.10. Instruction are present in the GitHub Repo/Webmail. Url: https://pastebin.com/nvibxmjw")

# Calling the attendance report function
attendance_report()


# This shall be the last lines of the code.
end_time = datetime.now()
print('Duration of Program Execution: {}'.format(end_time - start_time))
print("Files Created Successfully")
