# Assignment 01 CS384 -  Identify Octant Count FromCSV File and Provide Octant Count Based on Mod Values
# By Abhinav Mishra - 2001MM01

# Libraries
import csv
import os
os.system("cls")

def octact_identification(mod=5000):

    #Declaring the variables to store the values
    time=[]
    u=[]
    v=[]
    w=[]
    u_dash=[]
    v_dash=[]
    w_dash=[]
    octant=[]

    #Opening the octant_input.csv file in read mode
    with open("octant_input.csv",'r') as input_file:
        reader=csv.DictReader(input_file)

        #Storing the values of each key in the corresponding lists
        for row in reader:
            time.append(float(row['Time']))
            u.append(float(row['U']))
            v.append(float(row['V']))
            w.append(float(row['W']))

        #Calculating the average of U, V, W
        u_avg=sum(u)/len(u)        
        v_avg=sum(v)/len(v)
        w_avg=sum(w)/len(w)

        #Data Preprocessing - Calculating the difference between the velocities and their respective average values and storing in the respective lists.
        for u_value in u:
            u_dash.append(u_value-u_avg)
        for v_value in v:
            v_dash.append(v_value-v_avg)
        for w_value in w:
            w_dash.append(w_value-w_avg)

    #Tagging the octants by help of the video provided in the assignment
    for i in range(0,len(u_dash)):
        if(u_dash[i]>=0 and v_dash[i]>=0):
            if w_dash[i]>=0:
                octant.append(1)
            else:
                octant.append(-1)            
        if(u_dash[i]<0 and v_dash[i]>=0):
            if w_dash[i]>=0:
                octant.append(2)
            else:
                octant.append(-2)            
        if(u_dash[i]<0 and v_dash[i]<0):
            if w_dash[i]>=0:
                octant.append(3)
            else:
                octant.append(-3)            
        if(u_dash[i]>=0 and v_dash[i]<0):
            if w_dash[i]>=0:
                octant.append(4)
            else:
                octant.append(-4)

     #Output the file to octant_output.csv
    file_output=open("octant_output.csv",'w')
    file_output.writelines("Time,U,V,W,U Avg, V Avg, W Avg, U'=U-U avg, V'=V-V avg, W'=W-W avg, Octant\n")
    file_output.writelines([str(time[0]),",",str(u[0]),",",str(v[0]),",",str(w[0]),",",str(u_avg),",",str(v_avg),",",str(w_avg),",",str(u_dash[0]),",",str(v_dash[0]),",",str(w_dash[0]),",",str(octant[0]),"\n"])
    for i in range(1,len(time)):
        file_output.writelines([str(time[i]),",",str(u[i]),",",str(v[i]),",",str(w[i]),","," ",","," ",","," ",",",str(u_dash[i]),",",str(v_dash[i]),",",str(w_dash[i]),",",str(octant[i]),"\n"])
    file_output.close() #Closing the output file

mod=5000
octact_identification(mod)
print("Output File created successfully!")