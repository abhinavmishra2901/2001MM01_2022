# Assignment 04 CS384 -     Identify Octant’s Longest Subsequence Count and Their Time Ranges From XLSX File
# By Abhinav Mishra - 2001MM01

# Libraries
from platform import python_version
import os
import openpyxl_dictreader
from openpyxl import Workbook
os.system("cls")

# Code
def octant_longest_subsequence_count_with_range():

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
            "input_octant_longest_subsequence_with_range.xlsx", "Sheet1")

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
    long_sub_len = []
    count_sub_len = []

    # Declaring Lists to store the count of ranges
    long_sub_len_range = []
    count_sub_len_range = []

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
                       "W'=W-W avg", "Octant", " ", "Count", "Longest Subsequence Length", "Count", "", "Count", "Longest Subsequence Length", "Count"]

        # Loop to print the header line
        for i in range(1, 20):
            # The Cell Address. Converting integer to the corresponding character by ascii conversion
            cell = chr(i+64)+'1'
            sheet[cell] = header_line[i-1]

        # Declaring a list to store the output of lines/rows
        output_row = []

        # Declaring a list to store the octants
        octant_ids = ["+1", "-1", "+2", "-2", "+3", "-3", "+4", "-4"]
        octant_ids2 = []  # Declaring octant_ids2 list for a different column with "Time" label
        # Loop to check the maximum consecutive subsequence as well as the count or repetition of the subsequence
        # Iterating through octant_ids
        for j in octant_ids:
            octant_ids2.append(j)
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
            # Also declaring variables to store the from, to and count range of longest subsequence
            from_range = []
            count_range = []
            to_range = []
            # Again iterating through the octant list to find the count
            for i in range(len(time)):
                if octant[i] != j:
                    count_check = 0
                else:
                    count_check += 1
                    if count_check == max_count:
                        range_count += 1
                        count_check = 0
                        count_range.append("")
                        # Appending the "From" and "To" time value to the from_range and to_range lists
                        from_range.append(time[i-max_count+1])
                        to_range.append(time[i])

            # Appending the values to respective lists so that the particular column can be printed
            long_sub_len.append(max_count)
            long_sub_len_range.append(max_count)
            octant_ids2.append("Time")
            octant_ids2.extend(count_range)
            long_sub_len_range.append("From")
            long_sub_len_range.extend(from_range)
            count_sub_len.append(range_count)
            count_sub_len_range.append(range_count)
            count_sub_len_range.append("To")
            count_sub_len_range.extend(to_range)

        # Appending blank spaces
        for i in range(8, len(time)):
            octant_ids.append(" ")
            octant_ids2.append(" ")
            long_sub_len.append("")
            long_sub_len_range.append(" ")
            count_sub_len.append("")
            count_sub_len_range.append(" ")

        # Running a loop to store the values to an output_row list
        for i in range(0, len(time)):
            if i == 0:
                output_row.append([time[0], u[0], v[0], w[0], u_avg, v_avg, w_avg, u_prime[0], v_prime[0],
                                   w_prime[0], octant[0], "", octant_ids[0], long_sub_len[0], count_sub_len[0], "", octant_ids[0], long_sub_len_range[0], count_sub_len_range[0]])
            else:
                output_row.append([time[i], u[i], v[i], w[i], " ", " ",
                                  " ", u_prime[i], v_prime[i], w_prime[i], octant[i], "", octant_ids[i], long_sub_len[i], count_sub_len[i], "", octant_ids2[i], long_sub_len_range[i], count_sub_len_range[i]])

        # Writing the values to the output_octant_transition_identify.xlsx file
        # Here i is the range of columns and j is the range of rows. By combinations of characters we are storing the data to the corresponding cells.
        for i in range(1, 20):
            for j in range(2, len(time)+2):
                cell = chr(i+64)+str(j)
                sheet[cell] = output_row[j-2][i-1]

    except:
        print("Something went wrong while writing to octant_output.csv")
        exit()

    finally:
        # Saving the workbook.
        wb.save("output_octant_longest_subsequence_with_range.xlsx")
        wb.close()  # Closing the workbook.


# Version Check
ver = python_version()

if ver == "3.8.10":
    print("Correct Version Installed")
else:
    print("Please install 3.8.10. Instruction are present in the GitHub Repo/Webmail. Url: https://pastebin.com/nvibxmjw")

# Calling the function octant_longest_subsequence_count()
octant_longest_subsequence_count_with_range()
# Finally a message to show that all the steps have been completed successfully
print("Output Success")
