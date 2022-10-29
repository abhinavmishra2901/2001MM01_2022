# Assignment 08 - Cricket Scorecard Generator
# By Abhinav Mishra - 2001MM01

import re
import math
from platform import python_version
from datetime import datetime
import os
start_time = datetime.now()

# Help


# Code
os.system("cls")

# Scorecard Function


def scorecard():
    # Defining a pakistan inning list
    pakistan_inn = []

    # Defining variables to store the runs and wickets of the team
    runs = 0
    wickets = 0

    # Opening the Pakistan Innings File
    with open("pak_inns1.txt", 'r') as pak:
        # Reading the lines
        lines = pak.readlines()
        # Defining the list to store the mode in which the batsman got out
        out_reason = []
        # Iterating through the lines
        for line in lines:
            # Defining a list to store the ballwise statistics
            ballwise_stats = []
            ballwise_stats.append(line[0:4])
            a, b = line.find('to'), line.find(', ')
            # Bowler for the particular ball
            bowler = line[4:a-1]
            ballwise_stats.append(bowler)
            # Batsman for the particular ball
            batsman = line[a+3:b]
            ballwise_stats.append(batsman)
            # Runs scored on that ball by reading the next words
            inilist = [m.start() for m in re.finditer(r", ", line)]
            occ = 2
            if len(inilist) >= 2:
                run = line[b:inilist[occ-1]]
            if run[2:] == 'no run':
                ballwise_stats.append(0)
                runs += 0
                out_reason.append("")
            elif run[2:] == '1 run':
                ballwise_stats.append(1)
                runs += 1
                out_reason.append("")
            elif run[2:] == '2 runs':
                ballwise_stats.append(2)
                runs += 2
                out_reason.append("")
            elif run[2:] == '3 runs':
                ballwise_stats.append(3)
                runs += 3
                out_reason.append("")
            elif run[2:] == 'wide':
                ballwise_stats.append('wide')
                runs += 1
                out_reason.append("")
            elif run[2:] == 'byes':
                ballwise_stats.append('byes')
                runs += 1
                out_reason.append("")
            elif run[2:] == 'leg byes':
                ballwise_stats.append('leg byes')
                runs += 1
                out_reason.append("")
            elif run[2:] == 'FOUR':
                ballwise_stats.append(4)
                runs += 4
                out_reason.append("")
            elif run[2:] == 'SIX':
                ballwise_stats.append(6)
                runs += 6
                out_reason.append("")
            elif run[2:5] == 'out':
                ballwise_stats.append('out')
                wickets += 1
                out_reason.append(run[6:])
            # Appending the ballwise lists to the master list of pakistan_inn
            pakistan_inn.append(ballwise_stats)

        # Runs and wickets are read twice due to a gap between two lines. Hence dividing by 2 and taking the ceil
        runs = math.ceil(runs/2)
        wickets = math.ceil(wickets/2)

        # Deleting the double data due to space between two lines
        del pakistan_inn[1::2]
        del out_reason[1::2]

        # Creating a template to define which batsman was out and how he was out
        out_batsman = []
        for i in range(len(out_reason)):
            if out_reason[i][0:6] == 'Caught':
                c, d = out_reason[i].find('by '), out_reason[i].find('!!')
                catcher = out_reason[i][c+3:d]
                out_reason[i] = "c "+catcher+" b "+pakistan_inn[i][1]
                out_batsman.append(pakistan_inn[i][2])
            elif out_reason[i][0:3] == 'Lbw':
                out_reason[i] = "lbw b"+pakistan_inn[i][1]
                out_batsman.append(pakistan_inn[i][2])
            elif out_reason[i][0:6] == 'Bowled':
                out_reason[i] = "b"+pakistan_inn[i][1]
                out_batsman.append(pakistan_inn[i][2])
            else:
                out_batsman.append("")

        # Defining a batting order based on the given information
        pakistan_batting = []
        batting_order = []
        for i in pakistan_inn:
            pakistan_batting.append(i[2])
        for i in pakistan_batting:
            if i not in batting_order:
                batting_order.append(i)
        pakistan_batting = batting_order.copy()

        # Defining the list to store various information for each batsman
        pakistan_batting_runs = [0]*11
        pakistan_batting_balls = [0]*11
        pakistan_batting_fours = [0]*11
        pakistan_batting_sixes = [0]*11
        pakistan_batting_SR = [0]*11

        # Updating the information by calculating it for each batsman
        index = 0
        for i in pakistan_batting:
            for j in pakistan_inn:
                if j[2] == i:
                    if j[3] != 'out' and j[3] != 'wide' and j[3] != 'byes':
                        pakistan_batting_runs[index] += int(j[3])
                    if j[3] != 'wide' and j[3] != 'byes':
                        pakistan_batting_balls[index] += 1
                    if j[3] == 4:
                        pakistan_batting_fours[index] += 1
                    if j[3] == 6:
                        pakistan_batting_sixes[index] += 1
                if pakistan_batting_balls[index] != 0:
                    pakistan_batting_SR[index] = round(
                        pakistan_batting_runs[index]*100/pakistan_batting_balls[index], 2)
            index += 1

    # Writing the Information to Scorecard.txt
    with open("Scorecard.txt", 'w') as scorecard:
        scorecard.writelines(
            f"{'Pakistan Innings' : <25}{'' : <35}{'' : ^10}{'' : ^10}{'' : ^10}{'' : ^10}{str(runs)+'-'+str(wickets)+'('+pakistan_inn[-1][0]+')' : ^10}\n")
        scorecard.writelines(
            f"{'Batter' : <25}{'' : <35}{'R' : ^10}{'B' : ^10}{'4s' : ^10}{'6s' : ^10}{'SR' : >10}\n")
        for i in range(11):
            for j in range(len(out_batsman)):
                if pakistan_batting[i] not in out_batsman:
                    scorecard.writelines(
                        f"{pakistan_batting[i] : <25}{'Not Out' : <35}{pakistan_batting_runs[i] : ^10}{pakistan_batting_balls[i] : ^10}{pakistan_batting_fours[i] : ^10}{pakistan_batting_sixes[i] : ^10}{pakistan_batting_SR[i] : >10}\n")
                    break
                elif out_batsman[j] == pakistan_batting[i]:
                    scorecard.writelines(
                        f"{pakistan_batting[i] : <25}{out_reason[j] : <35}{pakistan_batting_runs[i] : ^10}{pakistan_batting_balls[i] : ^10}{pakistan_batting_fours[i] : ^10}{pakistan_batting_sixes[i] : ^10}{pakistan_batting_SR[i] : >10}\n")


# Version Check
ver = python_version()

if ver == "3.8.10":
    print("Correct Version Installed")
else:
    print("Please install 3.8.10. Instruction are present in the GitHub Repo/Webmail. Url: https://pastebin.com/nvibxmjw")

# Calling the scorecard function
scorecard()


# This shall be the last lines of the code.
end_time = datetime.now()
print('Duration of Program Execution: {}'.format(end_time - start_time))
