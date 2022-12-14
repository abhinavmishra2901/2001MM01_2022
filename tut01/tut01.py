# Assignment 01 CS384 -  Identify Octant Count FromCSV File and Provide Octant Count Based on Mod Values
# By Abhinav Mishra - 2001MM01

# Libraries
import csv
import os
os.system("cls")

# Octant Identification function with default value of mod as 5000


def octant_identification(mod=5000):

    # Declaring the lists to store the values
    time = []
    u = []
    v = []
    w = []
    u_dash = []
    v_dash = []
    w_dash = []
    octant = []

    # Opening the octant_input.csv file in read mode
    try:
        with open("octant_input.csv", 'r') as input_file:
            # Reading the input file into reader variable
            reader = csv.DictReader(input_file)

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
                u_dash.append(u_value-u_avg)
            for v_value in v:
                v_dash.append(v_value-v_avg)
            for w_value in w:
                w_dash.append(w_value-w_avg)
    # FileNotFound Error
    except FileNotFoundError:
        print("Input File not found!")
        exit()
    # Other errors if any
    except:
        print("Some error occured while reading the input file")
        exit()

# Task - 1: Find the individual count of each of the octant and write the overall count
    # Declaring Variables to store the count of each Octant ID
    c1 = 0
    cm1 = 0
    c2 = 0
    cm2 = 0
    c3 = 0
    cm3 = 0
    c4 = 0
    cm4 = 0
    # Here cmi refers to -ith octant

    # Tagging the octants by help of the video provided in the assignment
    for i in range(0, len(time)):
        if (u_dash[i] >= 0 and v_dash[i] >= 0):
            if w_dash[i] >= 0:
                octant.append(1)
                c1 = c1+1
            else:
                octant.append(-1)
                cm1 = cm1+1
        if (u_dash[i] < 0 and v_dash[i] >= 0):
            if w_dash[i] >= 0:
                octant.append(2)
                c2 = c2+1
            else:
                octant.append(-2)
                cm2 = cm2+1
        if (u_dash[i] < 0 and v_dash[i] < 0):
            if w_dash[i] >= 0:
                octant.append(3)
                c3 = c3+1
            else:
                octant.append(-3)
                cm3 = cm3+1
        if (u_dash[i] >= 0 and v_dash[i] < 0):
            if w_dash[i] >= 0:
                octant.append(4)
                c4 = c4+1
            else:
                octant.append(-4)
                cm4 = cm4+1

# Task - 2: Take a user input for the mod value. This mod value will be used to break the file into ranges. Here now you need to give the overall count of each octant in each of the mod ranges too

    range1 = []
    range_count = 0
    for x in range(0, len(time), mod):
        if x == 0:
            range1.append(".0000-{}".format(mod-1))
            range_count = range_count+1
        elif x+mod > len(time)-1:
            range1.append("{}-{}".format(x, len(time)-1))
            range_count = range_count+1
        else:
            range1.append("{}-{}".format(x, x+mod-1))
            range_count = range_count+1

    # Appending the remaining length of the list with a blank string for convenience in later steps
    for x in range(range_count, len(time)):
        range1.append("")

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
    for x in range(int(30000/mod), len(time)):
        mod_c1.append("")
        mod_cm1.append("")
        mod_c2.append("")
        mod_cm2.append("")
        mod_c3.append("")
        mod_cm3.append("")
        mod_c4.append("")
        mod_cm4.append("")

    try:
        # Output the file to octant_output.csv
        file_output = open("octant_output.csv", 'w')

        # Header line
        file_output.writelines(
            "Time,U,V,W,U Avg,V Avg,W Avg,U'=U-U avg,V'=V-V avg,W'=W-W avg,Octant, ,Octant ID,1,-1,2,-2,3,-3,4,-4\n")

        # Writing the first two lines separately due to difference in the data length
        file_output.writelines([str(time[0]), ",", str(u[0]), ",", str(v[0]), ",", str(w[0]), ",", str(u_avg), ",", str(v_avg), ",", str(w_avg), ",", str(u_dash[0]), ",", str(v_dash[0]), ",", str(
            w_dash[0]), ",", str(octant[0]), ",", " ", ",", "Overall Count", ",", str(c1), ",", str(cm1), ",", str(c2), ",", str(cm2), ",", str(c3), ",", str(cm3), ",", str(c4), ",", str(cm4), ",", "\n"])
        file_output.writelines([str(time[1]), ",", str(u[1]), ",", str(v[1]), ",", str(w[1]), ",", " ", ",", " ", ",", " ", ",", str(
            u_dash[1]), ",", str(v_dash[1]), ",", str(w_dash[1]), ",", str(octant[1]), ",", "User Input", ",", "Mod {}".format(mod), "\n"])

        # Writing the remaining values to the octant_output.csv file
        for i in range(2, len(time)):
            file_output.writelines([str(time[i]), ",", str(u[i]), ",", str(v[i]), ",", str(w[i]), ",", " ", ",", " ", ",", " ", ",", str(u_dash[i]), ",", str(v_dash[i]), ",", str(w_dash[i]), ",", str(octant[i]), ",", " ", ",", str(
                range1[i-2]), ",", str(mod_c1[i-2]), ",", str(mod_cm1[i-2]), ",", str(mod_c2[i-2]), ",", str(mod_cm2[i-2]), ",", str(mod_c3[i-2]), ",", str(mod_cm3[i-2]), ",", str(mod_c4[i-2]), ",", str(mod_cm4[i-2]), ",", "\n"])
    except:
        print("Something went wrong while writing to octant_output.csv")
        exit()

    finally:
        file_output.close()  # Closing the output file


# Calling the octant_identification function
mod = 5000
octant_identification(mod)
print("Output File created successfully!")
