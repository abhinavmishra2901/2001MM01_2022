# Help https://youtu.be/H37f_x4wAC0

# Assignment 03 CS384 -    Identify Octant’s Longest Subsequence Count From XLSX File
# By Abhinav Mishra - 2001MM01

# Libraries
from platform import python_version
import os
import openpyxl_dictreader
from openpyxl import Workbook
import math
os.system("cls")


# Code
def octant_longest_subsequence_count():

    # Declaring the lists to store the values
    time = []
    u = []
    v = []
    w = []
    u_prime = []
    v_prime = []
    w_prime = []
    octant = []

    # Opening the input_octant_transition_identify.xlsx file in read mode
    try:
        reader = openpyxl_dictreader.DictReader(
            "input_octant_longest_subsequence.xlsx", "Sheet1")

        # Storing the values of each key in the corresponding lists
        for row in reader:
            time.append(float(row['Time']))
            u.append(float(row['U']))
            v.append(float(row['V']))
            w.append(float(row['W']))

        # Calculating the average of U, V, W
        u_avg = sum(u)/len(u)
        v_avg = sum(v)/len(v)
        w_avg = sum(w)/len(w)

        # Data Preprocessing - Calculating the difference between the velocities and their respective average values and storing in the respective lists.
        for u_value in u:
            u_prime.append(u_value-u_avg)
        for v_value in v:
            v_prime.append(v_value-v_avg)
        for w_value in w:
            w_prime.append(w_value-w_avg)
    # FileNotFound Error
    except FileNotFoundError:
        print("Input File not found!")
        exit()
    # Other errors if any
    except:
        print("Some error occured while reading the input file")
        exit()

    # Declaring List to store the count of each Octant ID
    count = [0]*8

    # Tagging the octants by help of the video provided in the assignment
    for i in range(0, len(time)):
        if (u_prime[i] >= 0 and v_prime[i] >= 0):
            if w_prime[i] >= 0:
                octant.append("+1")
                count[0] += 1
            else:
                octant.append("-1")
                count[1] += 1
        if (u_prime[i] < 0 and v_prime[i] >= 0):
            if w_prime[i] >= 0:
                octant.append("+2")
                count[2] += 1
            else:
                octant.append("-2")
                count[3] += 1
        if (u_prime[i] < 0 and v_prime[i] < 0):
            if w_prime[i] >= 0:
                octant.append("+3")
                count[4] += 1
            else:
                octant.append("-3")
                count[5] += 1
        if (u_prime[i] >= 0 and v_prime[i] < 0):
            if w_prime[i] >= 0:
                octant.append("+4")
                count[6] += 1
            else:
                octant.append("-4")
                count[7] += 1

    try:
        # Output the file to output_octant_transition_identify.xlsx
        wb = Workbook()
        sheet = wb.active

        # Header line
        header_line = ["Time", "U", "V", "W", "U Avg", "V Avg", "W Avg", "U'=U-U avg", "V'=V-V avg",
                       "W'=W-W avg", "Octant", " ", "Count", "Longest Subsequence Length", "Count"]

        # Loop to print the header line
        for i in range(1, 16):
            # The Cell Address. Converting integer to the corresponding character by ascii conversion
            cell = chr(i+64)+'1'
            sheet[cell] = header_line[i-1]

        # Declaring a list to store the output of lines/rows
        output_row = []

        # Declaring a list to store the octants
        octant_ids = ["+1", "-1", "+2", "-2", "+3", "-3", "+4", "-4"]

        # Loop to check the maximum consecutive subsequence as well as the count or repetition of the subsequence
        # Iterating through octant_ids
        for j in octant_ids:
            # Declaring variables to show the current maximum length of the subsequence and the previous maximum length of the subsequence
            previous_count = 0
            max_count = 0
            # Iterating through the octant list and checking the maximum length of a subsequence
            for i in range(len(time)):
                if octant[i] == j:
                    previous_count += 1
                else:
                    if previous_count > max_count:
                        max_count = previous_count
                    previous_count = 0
            # Next I am declaring variables to show the count of repetition of the subsequence in the octant list
            range_count = 0
            count_check = 0
            # Again iterating through the octant list to find the count
            for i in range(len(time)):
                if octant[i] != j:
                    count_check = 0
                else:
                    count_check += 1
                    if count_check == max_count:
                        range_count += 1
                        count_check = 0
            print(max_count, "", range_count)

        for i in range(8, len(time)):
            octant_ids.append(" ")
        for i in range(0, len(time)):
            if i == 0:
                output_row.append([time[0], u[0], v[0], w[0], u_avg, v_avg, w_avg, u_prime[0], v_prime[0],
                                   w_prime[0], octant[0], "", octant_ids[0]])
            else:
                output_row.append([time[i], u[i], v[i], w[i], " ", " ",
                                  " ", u_prime[i], v_prime[i], w_prime[i], octant[i], "", octant_ids[i]])

        # Writing the remaining values to the output_octant_transition_identify.xlsx file
        # Here i is the range of columns and j is the range of rows. By combinations of characters we are storing the data to the corresponding cells.
        for i in range(1, 14):
            for j in range(2, len(time)+2):
                cell = chr(i+64)+str(j)
                sheet[cell] = output_row[j-2][i-1]

    except:
        print("Something went wrong while writing to octant_output.csv")
        exit()

    finally:
        # Saving the workbook.
        wb.save("output_octant_longest_subsequence.xlsx")
        wb.close()  # Closing the workbook.


# Version Check
ver = python_version()

if ver == "3.8.10":
    print("Correct Version Installed")
else:
    print("Please install 3.8.10. Instruction are present in the GitHub Repo/Webmail. Url: https://pastebin.com/nvibxmjw")

# Calling the function octant_longest_subsequence_count()
octant_longest_subsequence_count()
# Finally a message to show that all the steps have been completed successfully
print("Output Success")
