# Assignment 08 - Cricket Scorecard Generator
# By Abhinav Mishra - 2001MM01

# Libraries
import re
import math
from platform import python_version
from datetime import datetime
import os
start_time = datetime.now()

# Code
os.system("cls")

# Scorecard Function


def pakistan_inn():
    # Defining a Fall of Wickets list
    fallofwickets = []

    # Defining a pakistan inning list
    pakistan_inn = []

    # Defining variables to store the runs and wickets of the team
    runs = 0
    wickets = 0
    byes=0
    legbyes=0
    wides=0
    nb=0
    p=0

    # Powerplay Runs
    powerplay = 0

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

            if run[2:5] == 'out':
                ballwise_stats.append('out')
                wickets += 1
                # Updating the Fall of Wickets information
                fallofwickets.append(
                    "{}-{} ({}, {})".format(math.ceil(runs/2), math.ceil(wickets/2), batsman, line[0:4]))
                out_reason.append(run[6:])
            elif run[2:] == 'wide':
                ballwise_stats.append('wide')
                runs += 1
                wides+=1
                out_reason.append("")
            elif run[4:] == 'wides':
                ballwise_stats.append(run[2]+' wides')
                runs += int(run[2])
                wides+=int(run[2])
                out_reason.append("")

            elif run[2:] == 'byes' or run[2:] == 'leg byes':
                ballwise_stats.append(run[2:])
                inilist = [m.start() for m in re.finditer(r", ", line)]
                occ = 2
                if len(inilist) >= 2:
                    x = (line[inilist[occ-1]+2])
                if x == 'F':
                    runs += 4
                    if line[0] == "\n":
                        pass
                    elif float(line[0]) < 6:
                        powerplay += 4
                    if run[2:]=='byes':
                        byes+=4
                    elif run[2:]=='leg byes':
                        legbyes+=4
                elif x == 'S':
                    runs += 6
                    if line[0] == "\n":
                        pass
                    elif float(line[0]) < 6:
                        powerplay += 6
                    if run[2:]=='byes':
                        byes+=6
                    elif run[2:]=='leg byes':
                        legbyes+=6
                else:
                    runs += int(x)
                    if line[0] == "\n":
                        pass
                    elif float(line[0]) <= 5:
                        powerplay += int(x)
                    if run[2:]=='byes':
                        byes+=int(x)
                    elif run[2:]=='leg byes':
                        legbyes+=int(x)
                out_reason.append("")

            else:
                runs_mapping = {'no run': 0, '1 run': 1,
                                '2 runs': 2, '3 runs': 3, 'FOUR': 4, 'SIX': 6}
                ballwise_stats.append(runs_mapping[run[2:]])
                runs += runs_mapping[run[2:]]
                out_reason.append("")
            pakistan_inn.append(ballwise_stats)
        extras=byes+legbyes+nb+p+wides
        # Runs and wickets are read twice due to a gap between two lines. Hence dividing by 2 and taking the ceil
        runs = math.ceil(runs/2)
        wickets = math.ceil(wickets/2)

        # Deleting the double data due to space between two lines
        del fallofwickets[1::2]
        del pakistan_inn[1::2]
        del out_reason[1::2]

        # Powerplay Runs calculation
        for i in range(38):
            if pakistan_inn[i][3] == 'wide' or pakistan_inn[i][3] == 'byes' or pakistan_inn[i][3] == 'leg byes':
                powerplay += 1
            elif pakistan_inn[i][3] == 'out':
                continue
            else:
                powerplay += int(pakistan_inn[i][3])

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

        # Defining a bowling order based on the given information
        india_bowling = []
        bowling_order = []
        for i in pakistan_inn:
            india_bowling.append(i[1])
        for i in india_bowling:
            if i.strip() not in bowling_order:
                bowling_order.append(i)
        india_bowling = bowling_order.copy()

        # Defining the list to store various information for each bowler
        india_bowling_overs = [0]*len(bowling_order)
        india_bowling_maidens = [0]*len(bowling_order)
        india_bowling_runs = [0]*len(bowling_order)
        india_bowling_wickets = [0]*len(bowling_order)
        india_bowling_NB = [0]*len(bowling_order)
        india_bowling_WD = [0]*len(bowling_order)
        india_bowling_ECO = [0]*len(bowling_order)
        # Updating the information by calculating it for each batsman
        index = 0
        for i in india_bowling:
            maiden_check = 0
            for j in pakistan_inn:
                if j[1].strip() == i:
                    india_bowling_overs[index] += 1
                    if j[3] != 'out' and j[3] != 'wide' and j[3] != 'byes':
                        india_bowling_runs[index] += int(j[3])
                    if j[3] == 'wide':
                        india_bowling_runs[index] += 1
                        india_bowling_WD[index] += 1
                        india_bowling_overs[index] -= 1
                    if j[3] == 'byes':
                        pass
                    if j[3] == 'leg byes':
                        pass
                    if j[3] == 'out':
                        india_bowling_wickets[index] += 1
                    if j[3] == 0:
                        maiden_check += 1
                    else:
                        maiden_check = 0
                    if maiden_check == 6:
                        india_bowling_maidens += 1

            # Calculating Economy = Number of runs/Number of overs and overs from the balls count
            india_bowling_ECO[index] = round(
                india_bowling_runs[index]*6/india_bowling_overs[index], 1)
            india_bowling_overs[index] = ((india_bowling_overs[index]/6)-math.floor(
                india_bowling_overs[index]/6))*0.6 + math.floor(india_bowling_overs[index]/6)
            index += 1

    # Writing the Information to Scorecard.txt
    with open("Scorecard.txt", 'w') as scorecard:
        scorecard.writelines(
            f"{'Pakistan Innings' : <25}{'' : <35}{'' : ^10}{'' : ^10}{'' : ^10}{'' : ^10}{str(runs)+'-'+str(wickets)+'('+pakistan_inn[-1][0]+')' : ^10}\n")
        scorecard.writelines(
            f"\n{'Batter' : <25}{'' : <35}{'R' : ^10}{'B' : ^10}{'4s' : ^10}{'6s' : ^10}{'SR' : >10}\n")
        for i in range(11):
            for j in range(len(out_batsman)):
                if pakistan_batting[i] not in out_batsman:
                    scorecard.writelines(
                        f"{pakistan_batting[i] : <25}{'Not Out' : <35}{pakistan_batting_runs[i] : ^10}{pakistan_batting_balls[i] : ^10}{pakistan_batting_fours[i] : ^10}{pakistan_batting_sixes[i] : ^10}{pakistan_batting_SR[i] : >10}\n")
                    break
                elif out_batsman[j] == pakistan_batting[i]:
                    scorecard.writelines(
                        f"{pakistan_batting[i] : <25}{out_reason[j] : <35}{pakistan_batting_runs[i] : ^10}{pakistan_batting_balls[i] : ^10}{pakistan_batting_fours[i] : ^10}{pakistan_batting_sixes[i] : ^10}{pakistan_batting_SR[i] : >10}\n")
        scorecard.writelines(
            f"{'Extras' : <25}{'' : <35}{'{}(b {}, lb {}, w {}, nb {}, p {})'.format(int(extras/2),int(byes/2),int(legbyes/2),int(wides/2),int(nb/2),int(p/2)) : ^10}{'' : ^10}{'' : ^10}{'' : ^10}{'' : >10}\n")        
        scorecard.writelines(
            f"{'Total' : <25}{'' : <35}{'{}({} wkts, {} Ov)'.format(runs,wickets,pakistan_inn[-1][0]) : ^10}{'' : ^10}{'' : ^10}{'' : ^10}{'' : >10}\n")
        scorecard.writelines(f"\n{'Fall of Wickets':<25}\n")
        fow = fallofwickets[0]
        for i in range(1, len(fallofwickets)):
            fow += ", " + fallofwickets[i]
        scorecard.writelines(f"{fow:<25}\n")
        scorecard.writelines(
            f"\n{'Bowler' : <40}{'O' : ^10}{'M' : ^10}{'R' : ^10}{'W' : ^10}{'NB' : ^10}{'WD' : ^10}{'ECO' : >10}\n")
        for i in range(len(bowling_order)):
            scorecard.writelines(
                f"{bowling_order[i] : <40}{india_bowling_overs[i] : ^10}{india_bowling_maidens[i] : ^10}{india_bowling_runs[i] : ^10}{india_bowling_wickets[i] : ^10}{india_bowling_NB[i] : ^10}{india_bowling_WD[i] : ^10}{india_bowling_ECO[i] : >10}\n")
        scorecard.writelines(
            f"\n{'Powerplays' : <40}{'' : ^10}{'Overs' : ^10}{'' : ^10}{'Runs' : >10}\n")
        scorecard.writelines(
            f"{'Mandatory' : <40}{'' : ^10}{'0.1-6' : ^10}{'' : ^10}{powerplay : >10}\n")


def india_inn():
    # Defining a Fall of Wickets list
    fallofwickets = []

    # Defining a India inning list
    india_inn = []

    # Defining variables to store the runs and wickets of the team
    runs = 0
    wickets = 0
    byes=0
    legbyes=0
    wides=0
    nb=0
    p=0

    # Powerplay Runs
    powerplay = 0

    # Opening the india Innings File
    with open("india_inns2.txt", 'r') as ind:
        # Reading the lines
        lines = ind.readlines()
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
                
            if run[2:5] == 'out':
                ballwise_stats.append('out')
                wickets += 1
                # Updating the Fall of Wickets information
                fallofwickets.append(
                    "{}-{} ({}, {})".format(math.ceil(runs/2), math.ceil(wickets/2), batsman, line[0:4]))
                out_reason.append(run[6:])
            elif run[2:] == 'wide':
                ballwise_stats.append('wide')
                runs += 1
                wides+=1
                out_reason.append("")
            elif run[4:] == 'wides':
                ballwise_stats.append(run[2]+' wides')
                runs += int(run[2])
                wides+=int(run[2])
                out_reason.append("")

            elif run[2:] == 'byes' or run[2:] == 'leg byes':
                ballwise_stats.append(run[2:])
                inilist = [m.start() for m in re.finditer(r", ", line)]
                occ = 2
                if len(inilist) >= 2:
                    x = (line[inilist[occ-1]+2])
                if x == 'F':
                    runs += 4
                    if line[0] == "\n":
                        pass
                    elif float(line[0]) < 6:
                        powerplay += 4
                    if run[2:]=='byes':
                        byes+=4
                    elif run[2:]=='leg byes':
                        legbyes+=4
                elif x == 'S':
                    runs += 6
                    if line[0] == "\n":
                        pass
                    elif float(line[0]) < 6:
                        powerplay += 6
                    if run[2:]=='byes':
                        byes+=6
                    elif run[2:]=='leg byes':
                        legbyes+=6
                else:
                    runs += int(x)
                    if line[0] == "\n":
                        pass
                    elif float(line[0]) <= 5:
                        powerplay += int(x)
                    if run[2:]=='byes':
                        byes+=int(x)
                    elif run[2:]=='leg byes':
                        legbyes+=int(x)
                out_reason.append("")

            else:
                runs_mapping = {'no run': 0, '1 run': 1,
                                '2 runs': 2, '3 runs': 3, 'FOUR': 4, 'SIX': 6}
                ballwise_stats.append(runs_mapping[run[2:]])
                runs += runs_mapping[run[2:]]
                out_reason.append("")
            # Appending the ballwise lists to the master list of india_inn
            india_inn.append(ballwise_stats)

        # Runs and wickets are read twice due to a gap between two lines. Hence dividing by 2 and taking the ceil
        runs = math.ceil(runs/2)
        wickets = math.ceil(wickets/2)
        extras=byes+legbyes+nb+p+wides

        # for i in india_inn:
        #     print(i)
        # Deleting the double data due to space between two lines
        del fallofwickets[1::2]
        del india_inn[1::2]
        del out_reason[1::2]

        # Powerplay Runs calculation
        for i in range(38):
            if india_inn[i][3] == 'wide':
                powerplay += 1
            elif india_inn[i][3] == '2 wides':
                powerplay += 2
            elif india_inn[i][3] == '3 wides':
                powerplay += 3
            elif india_inn[i][3] == 'byes' or india_inn[i][3] == 'leg byes' or india_inn[i][3] == 'out':
                continue
            else:
                powerplay += int(india_inn[i][3])

        # Creating a template to define which batsman was out and how he was out
        out_batsman = []
        for i in range(len(out_reason)):
            if out_reason[i][0:6] == 'Caught':
                c, d = out_reason[i].find('by '), out_reason[i].find('!!')
                catcher = out_reason[i][c+3:d]
                out_reason[i] = "c "+catcher+" b "+india_inn[i][1]
                out_batsman.append(india_inn[i][2])
            elif out_reason[i][0:3] == 'Lbw':
                out_reason[i] = "lbw b "+india_inn[i][1]
                out_batsman.append(india_inn[i][2])
            elif out_reason[i][0:6] == 'Bowled':
                out_reason[i] = "b "+india_inn[i][1]
                out_batsman.append(india_inn[i][2])
            else:
                out_batsman.append("")

        # Defining a batting order based on the given information
        india_batting = []
        batting_order = []
        for i in india_inn:
            india_batting.append(i[2])
        for i in india_batting:
            if i not in batting_order:
                batting_order.append(i)
        india_batting = batting_order.copy()

        # Defining the list to store various information for each batsman
        india_batting_runs = [0]*len(india_batting)
        india_batting_balls = [0]*len(india_batting)
        india_batting_fours = [0]*len(india_batting)
        india_batting_sixes = [0]*len(india_batting)
        india_batting_SR = [0]*len(india_batting)

        # Updating the information by calculating it for each batsman
        index = 0
        for i in india_batting:
            for j in india_inn:
                if j[2] == i:
                    if j[3] != 'out' and j[3] != 'wide' and j[3] != '3 wides' and j[3] != '2 wides' and j[3] != 'byes' and j[3] != 'leg byes':
                        india_batting_runs[index] += int(j[3])
                    if j[3] != 'wide' and j[3] != 'byes' and j[3] != '3 wides' and j[3] != '2 wides':
                        india_batting_balls[index] += 1
                    if j[3] == 4:
                        india_batting_fours[index] += 1
                    if j[3] == 6:
                        india_batting_sixes[index] += 1
                if india_batting_balls[index] != 0:
                    india_batting_SR[index] = round(
                        india_batting_runs[index]*100/india_batting_balls[index], 2)
            index += 1

        # Defining a bowling order based on the given information
        pakistan_bowling = []
        bowling_order = []
        for i in india_inn:
            pakistan_bowling.append(i[1])
        for i in pakistan_bowling:
            if i.strip() not in bowling_order:
                bowling_order.append(i)
        pakistan_bowling = bowling_order.copy()

        # Defining the list to store various information for each bowler
        pakistan_bowling_overs = [0]*len(bowling_order)
        pakistan_bowling_maidens = [0]*len(bowling_order)
        pakistan_bowling_runs = [0]*len(bowling_order)
        pakistan_bowling_wickets = [0]*len(bowling_order)
        pakistan_bowling_NB = [0]*len(bowling_order)
        pakistan_bowling_WD = [0]*len(bowling_order)
        pakistan_bowling_ECO = [0]*len(bowling_order)
        # Updating the information by calculating it for each batsman
        index = 0
        for i in pakistan_bowling:
            maiden_check = 0
            for j in india_inn:
                if j[1].strip() == i:
                    pakistan_bowling_overs[index] += 1
                    if j[3] != 'out' and j[3] != 'wide' and j[3] != '3 wides' and j[3] != '2 wides' and j[3] != 'byes' and j[3] != 'leg byes':
                        pakistan_bowling_runs[index] += int(j[3])
                    if j[3] == 'wide':
                        pakistan_bowling_runs[index] += 1
                        pakistan_bowling_WD[index] += 1
                        pakistan_bowling_overs[index] -= 1
                    if j[3] == '2 wides':
                        pakistan_bowling_runs[index] += 2
                        pakistan_bowling_WD[index] += 2
                        pakistan_bowling_overs[index] -= 1
                    if j[3] == '3 wides':
                        pakistan_bowling_runs[index] += 3
                        pakistan_bowling_WD[index] += 3
                        pakistan_bowling_overs[index] -= 1
                    if j[3] == 'byes':
                        pass
                    if j[3] == 'leg byes':
                        pass
                    if j[3] == 'out':
                        pakistan_bowling_wickets[index] += 1
                    if j[3] == 0:
                        maiden_check += 1
                    else:
                        maiden_check = 0
                    if maiden_check == 6:
                        pakistan_bowling_maidens += 1

            # Calculating Economy = Number of runs/Number of overs and overs from the balls count
            pakistan_bowling_ECO[index] = round(
                pakistan_bowling_runs[index]*6/pakistan_bowling_overs[index], 1)
            pakistan_bowling_overs[index] = ((pakistan_bowling_overs[index]/6)-math.floor(
                pakistan_bowling_overs[index]/6))*0.6 + math.floor(pakistan_bowling_overs[index]/6)
            index += 1

    # Writing the Information to Scorecard.txt
    with open("Scorecard.txt", 'a') as scorecard:
        scorecard.writelines(
            f"\n{'India Innings' : <25}{'' : <35}{'' : ^10}{'' : ^10}{'' : ^10}{'' : ^10}{str(runs)+'-'+str(wickets)+'('+india_inn[-1][0]+')' : ^10}\n")
        scorecard.writelines(
            f"\n{'Batter' : <25}{'' : <35}{'R' : ^10}{'B' : ^10}{'4s' : ^10}{'6s' : ^10}{'SR' : >10}\n")
        for i in range(len(india_batting)):
            for j in range(len(out_batsman)):
                if india_batting[i] not in out_batsman:
                    scorecard.writelines(
                        f"{india_batting[i] : <25}{'Not Out' : <35}{india_batting_runs[i] : ^10}{india_batting_balls[i] : ^10}{india_batting_fours[i] : ^10}{india_batting_sixes[i] : ^10}{india_batting_SR[i] : >10}\n")
                    break
                elif out_batsman[j] == india_batting[i]:
                    scorecard.writelines(
                        f"{india_batting[i] : <25}{out_reason[j] : <35}{india_batting_runs[i] : ^10}{india_batting_balls[i] : ^10}{india_batting_fours[i] : ^10}{india_batting_sixes[i] : ^10}{india_batting_SR[i] : >10}\n")
        scorecard.writelines(
            f"{'Extras' : <25}{'' : <35}{'{}(b {}, lb {}, w {}, nb {}, p {})'.format(int(extras/2),int(byes/2),int(legbyes/2),int(wides/2),int(nb/2),int(p/2)) : ^10}{'' : ^10}{'' : ^10}{'' : ^10}{'' : >10}\n")        
        scorecard.writelines(
            f"{'Total' : <25}{'' : <35}{'{}({} wkts, {} Ov)'.format(runs,wickets,india_inn[-1][0]) : ^10}{'' : ^10}{'' : ^10}{'' : ^10}{'' : >10}\n")

        scorecard.writelines(f"\n{'Fall of Wickets':<25}\n")
        fow = fallofwickets[0]
        for i in range(1, len(fallofwickets)):
            fow += ", " + fallofwickets[i]
        scorecard.writelines(f"{fow:<25}\n")
        scorecard.writelines(
            f"\n{'Bowler' : <40}{'O' : ^10}{'M' : ^10}{'R' : ^10}{'W' : ^10}{'NB' : ^10}{'WD' : ^10}{'ECO' : >10}\n")
        for i in range(len(bowling_order)):
            scorecard.writelines(
                f"{bowling_order[i] : <40}{pakistan_bowling_overs[i] : ^10}{pakistan_bowling_maidens[i] : ^10}{pakistan_bowling_runs[i] : ^10}{pakistan_bowling_wickets[i] : ^10}{pakistan_bowling_NB[i] : ^10}{pakistan_bowling_WD[i] : ^10}{pakistan_bowling_ECO[i] : >10}\n")
        scorecard.writelines(
            f"\n{'Powerplays' : <40}{'' : ^10}{'Overs' : ^10}{'' : ^10}{'Runs' : >10}\n")
        scorecard.writelines(
            f"{'Mandatory' : <40}{'' : ^10}{'0.1-6' : ^10}{'' : ^10}{powerplay : >10}\n")


def scorecard():
    pakistan_inn()
    india_inn()


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
