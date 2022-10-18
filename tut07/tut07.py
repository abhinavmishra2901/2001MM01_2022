
# Libraries
from datetime import datetime
from platform import python_version
import os
import openpyxl_dictreader
from openpyxl import Workbook
os.system("cls")
start_time = datetime.now()

# Help

# Read all the excel files in a batch format from the input/ folder. Only xlsx to be allowed
# Save all the excel files in a the output/ folder. Only xlsx to be allowed
# output filename = input_filename[_octant_analysis_mod_5000].xlsx , ie, append _octant_analysis_mod_5000 to the original filename.

# Code

# Function - 1 to count the octant ranks


def octant_rank_count(count):
    # Overall Rank
    overall_rank = []
    # Creating a copy of the attribute list
    count_copy = count.copy()
    # Reversing the copy of the attribute list
    count_copy.sort(reverse=True)
    # Checking and appending the index of the sorted list's elements in the original list
    for i in count_copy:
        overall_rank.append(count.index(i))

    # Storing the ranks to an octant_rank_list by mapping the indexes
    octant_rank_list = [0]*8
    rank = 1
    for j in range(8):
        check = overall_rank[j]
        octant_rank_list[check] = rank
        rank += 1
    for j in range(8):
        if octant_rank_list[j] == 0:
            for x in range(1, 9):
                if x not in octant_rank_list:
                    octant_rank_list[j] = x

    return octant_rank_list

# Function - 2 to write the octant range names


def octant_range_names(inputfile, mod=5000):
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

    # Opening the octant_input.xlsx file in read mode
    try:
        reader = openpyxl_dictreader.DictReader(
            inputfile, "Sheet1")

        # Storing the values of each key in the corresponding lists
        for row in reader:
            time.append(float(row['T']))
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

    # Defining a list to store the ranks
    rank_list = []
    rank_list.append(octant_rank_count(count))
    rank_list.append([""]*8)

    # With each step in the loop, if the condition is satisfied we increase the range count by 1 and also append a blank space in label for convenience in later steps
    for x in range(0, len(time), mod):
        if x == 0:
            range1.append(".0000-{}".format(mod-1))
        elif x+mod > len(time):
            range1.append("{}-{}".format(x, len(time)-1))
        else:
            range1.append("{}-{}".format(x, x+mod-1))

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
    while y-mod < len(time):
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

    # Storing the ranks of the mod ranges in the rank_list variable. Here the elements are initially row-wise and I am changing it to column-wise to print later.
    for i in range(len(mod_c1)):
        mod_list = []
        mod_list.append(mod_c1[i])
        mod_list.append(mod_cm1[i])
        mod_list.append(mod_c2[i])
        mod_list.append(mod_cm2[i])
        mod_list.append(mod_c3[i])
        mod_list.append(mod_cm3[i])
        mod_list.append(mod_c4[i])
        mod_list.append(mod_cm4[i])
        rank_list.append(octant_rank_count(mod_list))

    # Creating column-wise list to store the ranks in the designated order
    rank1 = []
    rank2 = []
    rank3 = []
    rank4 = []
    rank5 = []
    rank6 = []
    rank7 = []
    rank8 = []

    # Creating lists to store the index of the first rank, the first rank octant id and first rank octant name
    first_rank_index = []
    first_rank = []
    first_rank_name = []
    octant_id_list = [1, -1, 2, -2, 3, -3, 4, -4]

    # Running a loop to map the index of rank 1 to the corresponding lists and then map the octant id to the octant name by using the octant_name_id_mapping dictionary
    for i in range(len(rank_list)):
        if 1 in rank_list[i]:
            first_rank_index.append(rank_list[i].index(1))
    for i in range(len(first_rank_index)):
        first_rank.append(octant_id_list[first_rank_index[i]])
    for i in range(len(first_rank)):
        first_rank_name.append(octant_name_id_mapping[str(first_rank[i])])
    for i in range(len(rank_list)):
        rank1.append(rank_list[i][0])
        rank2.append(rank_list[i][1])
        rank3.append(rank_list[i][2])
        rank4.append(rank_list[i][3])
        rank5.append(rank_list[i][4])
        rank6.append(rank_list[i][5])
        rank7.append(rank_list[i][6])
        rank8.append(rank_list[i][7])

    # Extending the 3 columns to store the rank1 mod values count
    rank7.extend(("", "", "", "Octant ID"))
    rank7.extend(octant_id_list)
    rank8.extend(("", "", "", "Octant Name"))
    octant_name_list = []
    for i in range(8):
        octant_name_list.append(octant_name_id_mapping[str(octant_id_list[i])])
    rank8.extend(octant_name_list)
    first_rank.extend(("", "", "", "Count of Rank 1 Mod Values"))
    rank1_mod_values = []
    # Here we are slicing the rank1 list to exclude the overall rank1 count
    rank1_mod_values.append(rank1[2:].count(1))
    rank1_mod_values.append(rank2[2:].count(1))
    rank1_mod_values.append(rank3[2:].count(1))
    rank1_mod_values.append(rank4[2:].count(1))
    rank1_mod_values.append(rank5[2:].count(1))
    rank1_mod_values.append(rank6[2:].count(1))
    rank1_mod_values.append(rank7[2:].count(1))
    rank1_mod_values.append(rank8[2:].count(1))
    first_rank.extend(rank1_mod_values)

    # Appending the remaining length of the lists with a blank string for convenience in later steps
    for x in range(int(len(time)/mod)+2, len(time)):
        mod_c1.append("")
        mod_cm1.append("")
        mod_c2.append("")
        mod_cm2.append("")
        mod_c3.append("")
        mod_cm3.append("")
        mod_c4.append("")
        mod_cm4.append("")
        range1.append("")
        rank1.append("")
        rank2.append("")
        rank3.append("")
        rank4.append("")
        rank5.append("")
        rank6.append("")
        rank7.append("")
        rank8.append("")
        first_rank.append("")
        first_rank_name.append("")

    try:
        # Output the file to output_octant_transition_identify.xlsx
        wb = Workbook()
        sheet = wb.active

        # Header line1
        header_line1 = ["", "", "", "", "", "", "", "", "",
                        "", "", " ", " ", "Overall Octant Count", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]
        # Header line2
        header_line2 = ["Time", "U", "V", "W", "U Avg", "V Avg", "W Avg", "U'=U-U avg", "V'=V-V avg",
                        "W'=W-W avg", "Octant", " ", " ", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]
        # Loop to print the header line1
        for i in range(1, 27):
            # The Cell Address. Converting integer to the corresponding character by ascii conversion
            cell = chr(i+64)+'1'
            sheet[cell] = header_line1[i-1]
        for i in range(1, 7):
            # The Cell Address for AA to AF. Converting integer to the corresponding character by ascii conversion
            cell = 'A'+chr(i+64)+'1'
            sheet[cell] = header_line1[i+25]

        # Loop to print the header line2
        for i in range(1, 27):
            # The Cell Address. Converting integer to the corresponding character by ascii conversion
            cell = chr(i+64)+'2'
            sheet[cell] = header_line2[i-1]
        for i in range(1, 7):
            # The Cell Address for AA to AF. Converting integer to the corresponding character by ascii conversion
            cell = 'A'+chr(i+64)+'2'
            sheet[cell] = header_line2[i+25]

        # Writing the first two line separately due to difference in the data length
        output_row_1 = [time[0], u[0], v[0], w[0], u_avg, v_avg, w_avg, u_prime[0], v_prime[0],
                        w_prime[0], octant[0], "", "Octant ID", "1", "-1", "2", "-2", "3", "-3", "4", "-4", "Rank of 1", "Rank of -1", "Rank of 2", "Rank of -2", "Rank of 3", "Rank of -3", "Rank of 4", "Rank of -4", "Rank 1 Octant ID", "Rank 1 Octant Name"]
        output_row_2 = [time[1], u[1], v[1], w[1], "", "", "", u_prime[1], v_prime[1],
                        w_prime[1], octant[1], "Mod {}".format(mod), "Overall Count", count[0], count[1], count[2], count[3], count[4], count[5], count[6], count[7], rank1[0], rank2[0], rank3[0], rank4[0], rank5[0], rank6[0], rank7[0], rank8[0], first_rank[0], first_rank_name[0]]

        # Loop to print the first output line into the cells
        for i in range(1, 27):
            # Condition to leave column L empty
            if i == 12:
                continue
            # The Cell Address. Converting integer to the corresponding character by ascii conversion
            cell = chr(i+64)+'3'
            if i > 12:
                sheet[cell] = output_row_1[i-2]
            else:
                sheet[cell] = output_row_1[i-1]

        for i in range(1, 7):
            # The Cell Address for AA to AF. Converting integer to the corresponding character by ascii conversion
            cell = 'A'+chr(i+64)+'3'
            sheet[cell] = output_row_1[i+24]

        # Loop to print the second output line into the cells
        for i in range(1, 27):
            # Condition to leave column L empty
            if i == 12:
                continue
            # The Cell Address. Converting integer to the corresponding character by ascii conversion
            cell = chr(i+64)+'4'
            if i > 12:
                sheet[cell] = output_row_2[i-2]
            else:
                sheet[cell] = output_row_2[i-1]

        for i in range(1, 7):
            # The Cell Address for AA to AF. Converting integer to the corresponding character by ascii conversion
            cell = 'A'+chr(i+64)+'4'
            sheet[cell] = output_row_2[i+24]

        # Declaring a list to store the output of remaining lines/rows
        output_row = []
        for i in range(2, len(time)):
            output_row.append([time[i], u[i], v[i], w[i], " ", " ", " ", u_prime[i], v_prime[i], w_prime[i], octant[i], " ", range1[i-2],
                               mod_c1[i-2], mod_cm1[i-2], mod_c2[i-2], mod_cm2[i-2], mod_c3[i-2], mod_cm3[i-2], mod_c4[i-2], mod_cm4[i-2], rank1[i], rank2[i], rank3[i], rank4[i], rank5[i], rank6[i], rank7[i], rank8[i], first_rank[i-1], first_rank_name[i-1]])

        # Writing the remaining values to the output file
        # Here i is the range of columns and j is the range of rows. By combinations of characters we are storing the data to the corresponding cells.
        for i in range(1, 27):
            # Condition to leave column L empty
            if i == 12:
                continue
            if i > 12:
                for j in range(5, len(time)+2):
                    cell = chr(i+64)+str(j)
                    sheet[cell] = output_row[j-5][i-2]
            else:
                for j in range(5, len(time)+2):
                    cell = chr(i+64)+str(j)
                    sheet[cell] = output_row[j-5][i-1]

        # The Cell Address for AA to AF. Converting integer to the corresponding character by ascii conversion
        for i in range(1, 7):
            for j in range(5, len(time)+2):
                cell = 'A'+chr(i+64)+str(j)
                sheet[cell] = output_row[j-5][i+24]

    except:
        print("Something went wrong while writing to octant_output.csv")
        exit()

    finally:
        # Saving the workbook.
        wb.save("octant_output_ranking_excel.xlsx")
        wb.close()  # Closing the workbook.


def octant_analysis(mod=5000):
    inputfile = "input/2.0.xlsx"
    octant_range_names(inputfile, mod)


ver = python_version()

if ver == "3.8.10":
    print("Correct Version Installed")
else:
    print("Please install 3.8.10. Instruction are present in the GitHub Repo/Webmail. Url: https://pastebin.com/nvibxmjw")


mod = 5000
octant_analysis(mod)


# This shall be the last lines of the code.
end_time = datetime.now()
print('Duration of Program Execution: {}'.format(end_time - start_time))
