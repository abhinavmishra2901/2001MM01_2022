# Assignment 02 CS384 -   Identify Octant Transition Count From XLSX File and Provide Octant Transition Count Based on Mod Values
# By Abhinav Mishra - 2001MM01

# Libraries
from platform import python_version
import os
import openpyxl_dictreader
from openpyxl import Workbook
os.system("cls")


def octant_transition_count(mod=5000):

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
            "input_octant_transition_identify.xlsx", "Sheet1")

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
    count=[0]*8
    # Here cmi refers to -ith octant

    # Tagging the octants by help of the video provided in the assignment
    for i in range(0, len(time)):
        if (u_prime[i] >= 0 and v_prime[i] >= 0):
            if w_prime[i] >= 0:
                octant.append(1)
                count[0]+=1
            else:
                octant.append(-1)
                count[1]+=1
        if (u_prime[i] < 0 and v_prime[i] >= 0):
            if w_prime[i] >= 0:
                octant.append(2)
                count[2]+=1
            else:
                octant.append(-2)
                count[3]+=1
        if (u_prime[i] < 0 and v_prime[i] < 0):
            if w_prime[i] >= 0:
                octant.append(3)
                count[4]+=1
            else:
                octant.append(-3)
                count[5]+=1
        if (u_prime[i] >= 0 and v_prime[i] < 0):
            if w_prime[i] >= 0:
                octant.append(4)
                count[6]+=1
            else:
                octant.append(-4)
                count[7]+=1

    # Defining Ranges with help of mod 
    range1 = []

    #Also defining a list called label to store some label texts for column L in the excel sheet
    label = [" "]
    range_count = 0
    #With each step in the loop, if the condition is satisfied we increase the range count by 1 and also append a blank space in label for convenience in later steps
    for x in range(0, 30000, mod):
        if x == 0:
            range1.append(".0000-{}".format(mod))
            range_count = range_count+1
            label.append("")
        elif x+mod > 30000:
            range1.append("{}-30000".format(x+1))
            range_count = range_count+1
            label.append("")
        else:
            range1.append("{}-{}".format(x+1, x+mod))
            range_count = range_count+1
            label.append("")

    # Adding a verified row to check the sum of individual range counts, also extending the label list
    range1.extend(("Verified", " ", " ", "Overall Transition Count",
                  " ", "Count", "+1", "-1", "+2", "-2", "+3", "-3", "+4", "-4"))
    label.extend(("", "", "", "", "", "From"))
    # Appending the remaining length of the lists with a blank string for convenience in later steps
    for x in range(range_count+1, len(time)):
        range1.append("")
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

    # Counting the octant values in each mod using a loop method for a particular range in the octant list
    z = 0
    y = mod
    while y-mod < 30000:
        mod_c1.append(octant[z:y+1].count(1))
        mod_cm1.append(octant[z:y+1].count(-1))
        mod_c2.append(octant[z:y+1].count(2))
        mod_cm2.append(octant[z:y+1].count(-2))
        mod_c3.append(octant[z:y+1].count(3))
        mod_cm3.append(octant[z:y+1].count(-3))
        mod_c4.append(octant[z:y+1].count(4))
        mod_cm4.append(octant[z:y+1].count(-4))
        z = y+1
        y = y+mod

    # Also appending the sum of each mod counts in order to verify the sum
    # In this step we also extend the lists to print the column headers for overall transition count
    mod_c1.extend((sum(mod_c1), " ", " ", " ", "To", "+1"))
    mod_cm1.extend((sum(mod_cm1), " ", " ", " ", " ", "-1"))
    mod_c2.extend((sum(mod_c2), " ", " ", " ", " ", "+2"))
    mod_cm2.extend((sum(mod_cm2), " ", " ", " ", " ", "-2"))
    mod_c3.extend((sum(mod_c3), " ", " ", " ", " ", "+3"))
    mod_cm3.extend((sum(mod_cm3), " ", " ", " ", " ", "-3"))
    mod_c4.extend((sum(mod_c4), " ", " ", " ", " ", "+4"))
    mod_cm4.extend((sum(mod_cm4), " ", " ", " ", " ", "-4"))

    # Overall Transition Count
    overall_transition_list = []

    #A simple 2D loop to check the transitions. I am using two loops and then adding the count to overall_transition list
    for j in range(8):
        octant_list = [1, -1, 2, -2, 3, -3, 4, -4]
        overall_transition = [0]*8
        for i in range(len(time)):
            if octant[i-1] == octant_list[j]:
                if octant[i] == 1:
                    overall_transition[0] += 1
                elif octant[i] == -1:
                    overall_transition[1] += 1
                elif octant[i] == 2:
                    overall_transition[2] += 1
                elif octant[i] == -2:
                    overall_transition[3] += 1
                elif octant[i] == 3:
                    overall_transition[4] += 1
                elif octant[i] == -3:
                    overall_transition[5] += 1
                elif octant[i] == 4:
                    overall_transition[6] += 1
                elif octant[i] == -4:
                    overall_transition[7] += 1
        
        #overall_transition_list is the list to store the 8 lists we obtained in the above loop
        overall_transition_list.append(overall_transition)

    #To print the data to the excel file, we append the overall_transition_list's values to the respective columns using a loop
    for i in range(8):
        mod_c1.append(overall_transition_list[0][i])
        mod_cm1.append(overall_transition_list[1][i])
        mod_c2.append(overall_transition_list[2][i])
        mod_cm2.append(overall_transition_list[3][i])
        mod_c3.append(overall_transition_list[4][i])
        mod_cm3.append(overall_transition_list[5][i])
        mod_c4.append(overall_transition_list[6][i])
        mod_cm4.append(overall_transition_list[7][i])

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

    try:
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
                        w_prime[0], octant[0], " ", "Overall Count", count[0],count[1],count[2],count[3],count[4],count[5],count[6],count[7]]
        output_row_2 = [time[1], u[1], v[1], w[1], " ", " ", " ", u_prime[1], v_prime[1], w_prime[1],
                        octant[1], "User Input", "Mod {}".format(mod), " ", " ", " ", " ", " ", " ", " ", " "]

        # Declaring a list to store the output of remaining lines/rows
        output_row = []
        for i in range(2, len(time)):
            output_row.append([time[i], u[i], v[i], w[i], " ", " ", " ", u_prime[i], v_prime[i], w_prime[i], octant[i], label[i-2], range1[i-2],
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

    except:
        print("Something went wrong while writing to octant_output.csv")
        exit()

    finally:
        # Saving the workbook.
        wb.save("output_octant_transition_identify.xlsx")
        wb.close()  # Closing the workbook.


# Version Check
ver = python_version()

if ver == "3.8.10":
    print("Correct Version Installed")
else:
    print("Please install 3.8.10. Instruction are present in the GitHub Repo/Webmail. Url: https://pastebin.com/nvibxmjw")

mod = 5000
octant_transition_count(mod)
print("Output Success")
