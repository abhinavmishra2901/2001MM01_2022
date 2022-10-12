# Assignment 05 CS384 -    Octant Ranking and ID
# By Abhinav Mishra - 2001MM01

# Libraries
from datetime import datetime
from platform import python_version
import os
import openpyxl_dictreader
from openpyxl import Workbook
import math
os.system("cls")
start_time = datetime.now()

# Help https://youtu.be/N6PBd4XdnEw


def octant_range_names(mod=5000):
    octant_name_id_mapping = {"1": "Internal outward interaction", "-1": "External outward interaction", "2": "External Ejection",
                              "-2": "Internal Ejection", "3": "External inward interaction", "-3": "Internal inward interaction", "4": "Internal sweep", "-4": "External sweep"}
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
            "octant_input.xlsx", "Sheet1")

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
                octant.append(1)
                count[0] += 1
            else:
                octant.append(-1)
                count[1] += 1
        if (u_prime[i] < 0 and v_prime[i] >= 0):
            if w_prime[i] >= 0:
                octant.append(2)
                count[2] += 1
            else:
                octant.append(-2)
                count[3] += 1
        if (u_prime[i] < 0 and v_prime[i] < 0):
            if w_prime[i] >= 0:
                octant.append(3)
                count[4] += 1
            else:
                octant.append(-3)
                count[5] += 1
        if (u_prime[i] >= 0 and v_prime[i] < 0):
            if w_prime[i] >= 0:
                octant.append(4)
                count[6] += 1
            else:
                octant.append(-4)
                count[7] += 1

    # Defining Ranges with help of mod
    range1 = []

    # Also defining a list called label to store some label texts for column L in the excel sheet
    label = [" "]
    range_count = 0

    # With each step in the loop, if the condition is satisfied we increase the range count by 1 and also append a blank space in label for convenience in later steps
    for x in range(0, len(time), mod):
        if x == 0:
            range1.append(".0000-{}".format(mod-1))
            range_count = range_count+1
            label.append("")
        elif x+mod > len(time):
            range1.append("{}-{}".format(x, len(time)-1))
            range_count = range_count+1
            label.append("")
        else:
            range1.append("{}-{}".format(x, x+mod-1))
            range_count = range_count+1
            label.append("")


    # Declaring Lists to store the count of each octant ID in the given mod
    mod_c1 = []
    mod_cm1 = []
    mod_c2 = []
    mod_cm2 = []
    mod_c3 = []
    mod_cm3 = []
    mod_c4 = []
    mod_cm4 = []
    # Here cmi refers to -ith octant

    # Overall Transition Count
    overall_transition_list = []

    # Counting the octant values in each mod using a loop method for a particular range in the octant list
    z = 0
    y = mod
    while y-mod < 30000:
        mod_c1.append(octant[z:y].count(1))
        mod_cm1.append(octant[z:y].count(-1))
        mod_c2.append(octant[z:y].count(2))
        mod_cm2.append(octant[z:y].count(-2))
        mod_c3.append(octant[z:y].count(3))
        mod_cm3.append(octant[z:y].count(-3))
        mod_c4.append(octant[z:y].count(4))
        mod_cm4.append(octant[z:y].count(-4))
        z = y
        y = y+mod

    # Appending the remaining length of the lists with a blank string for convenience in later steps
    for x in range(int(30000/mod)+2, len(time)):
        mod_c1.append("")
        mod_cm1.append("")
        mod_c2.append("")
        mod_cm2.append("")
        mod_c3.append("")
        mod_cm3.append("")
        mod_c4.append("")
        mod_cm4.append("")
        range1.append("")

    # try:
    # Output the file to output_octant_transition_identify.xlsx
    wb = Workbook()
    sheet = wb.active

    # Header line
    header_line = ["Time", "U", "V", "W", "U Avg", "V Avg", "W Avg", "U'=U-U avg", "V'=V-V avg",
                    "W'=W-W avg", "Octant", " ", "Octant ID", "1", "-1", "2", "-2", "3", "-3", "4", "-4"]

    # Loop to print the header line
    for i in range(1, 22):
        # The Cell Address. Converting integer to the corresponding character by ascii conversion
        cell = chr(i+64)+'1'
        sheet[cell] = header_line[i-1]

    # Writing the first two lines separately due to difference in the data length
    output_row_1 = [time[0], u[0], v[0], w[0], u_avg, v_avg, w_avg, u_prime[0], v_prime[0],
                    w_prime[0], octant[0], " ", "Overall Count", count[0], count[1], count[2], count[3], count[4], count[5], count[6], count[7]]
    output_row_2 = [time[1], u[1], v[1], w[1], " ", " ", " ", u_prime[1], v_prime[1], w_prime[1],
                    octant[1], "User Input", "Mod {}".format(mod), " ", " ", " ", " ", " ", " ", " ", " "]

    # Declaring a list to store the output of remaining lines/rows
    output_row = []
    for i in range(2, len(time)):
        output_row.append([time[i], u[i], v[i], w[i], " ", " ", " ", u_prime[i], v_prime[i], w_prime[i], octant[i], " ", range1[i-2],
                            mod_c1[i-2], mod_cm1[i-2], mod_c2[i-2], mod_cm2[i-2], mod_c3[i-2], mod_cm3[i-2], mod_c4[i-2], mod_cm4[i-2]])

    # Loop to print the remaining lines/rows into the cells
    for i in range(1, 22):
        # The Cell Address. Converting integer to the corresponding character by ascii conversion
        cell = chr(i+64)+'2'
        sheet[cell] = output_row_1[i-1]
        # The Cell Address. Converting integer to the corresponding character by ascii conversion
        cell = chr(i+64)+'3'
        sheet[cell] = output_row_2[i-1]

    # Writing the remaining values to the output_octant_transition_identify.xlsx file
    # Here i is the range of columns and j is the range of rows. By combinations of characters we are storing the data to the corresponding cells.
    for i in range(1, 22):
        for j in range(4, len(time)+2):
            cell = chr(i+64)+str(j)
            sheet[cell] = output_row[j-4][i-1]

# except:
#     print("Something went wrong while writing to octant_output.csv")
#     exit()

# finally:
    # Saving the workbook.
    wb.save("octant_output_ranking_excel.xlsx")
    wb.close()  # Closing the workbook.


# Code

ver = python_version()

if ver == "3.8.10":
    print("Correct Version Installed")
else:
    print("Please install 3.8.10. Instruction are present in the GitHub Repo/Webmail. Url: https://pastebin.com/nvibxmjw")


mod = 5000
octant_range_names(mod)


# This shall be the last lines of the code.
end_time = datetime.now()
print('Duration of Program Execution: {}'.format(end_time - start_time))
