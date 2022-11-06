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


def scorecard(input_file, inn1):

    # Defining a Fall of Wickets list
    fallofwickets = []

    # Defining a pakistan inning list
    team_inn = []

    # Defining variables to store the runs and wickets of the team
    runs = 0
    wickets = 0
    byes = 0
    legbyes = 0
    wides = 0
    nb = 0
    p = 0

    # Powerplay Runs
    powerplay = 0

    # Opening the Team Innings File
    with open(input_file, 'r') as team_commentary:
        # Reading the lines
        lines = team_commentary.readlines()
        del lines[1::2]
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
            run = line[inilist[0]:]
            if run[2:5] == 'out':
                ballwise_stats.append('out')
                wickets += 1
                # Updating the Fall of Wickets information
                fallofwickets.append(
                    "{}-{} ({}, {})".format(math.ceil(runs), math.ceil(wickets), batsman, line[0:4]))
                out_reason.append(run[6:])
            elif run[2:6] == 'wide':
                ballwise_stats.append('wide')
                if float(line[0:3]) < 6:
                    powerplay += 1
                runs += 1
                wides += 1
                out_reason.append("")
            elif run[4:9] == 'wides':
                ballwise_stats.append(run[2]+' wides')
                if float(line[0:3]) < 6:
                    powerplay += int(run[2])
                runs += int(run[2])
                wides += int(run[2])
                out_reason.append("")

            elif run[2:6] == 'byes' or run[2:10] == 'leg byes':
                if run[2:6] == 'byes':
                    ballwise_stats.append(run[2:6])
                else:
                    ballwise_stats.append(run[2:10])

                inilist = [m.start() for m in re.finditer(r", ", line)]
                occ = 2
                if len(inilist) >= 2:
                    x = (line[inilist[occ-1]+2])
                if x == 'F':
                    runs += 4
                    if float(line[0:3]) < 6:
                        powerplay += 4
                    if run[2:6] == 'byes':
                        byes += 4
                    elif run[2:10] == 'leg byes':
                        legbyes += 4
                elif x == 'S':
                    runs += 6
                    if float(line[0:3]) < 6:
                        powerplay += 6
                    if run[2:6] == 'byes':
                        byes += 6
                    elif run[2:10] == 'leg byes':
                        legbyes += 6
                else:
                    runs += int(x)
                    if float(line[0:3]) < 6:
                        powerplay += int(x)
                    if run[2:6] == 'byes':
                        byes += int(x)
                    elif run[2:10] == 'leg byes':
                        legbyes += int(x)
                out_reason.append("")

            else:
                # Searching for 2nd Occurence of a comma(,)
                occ = 2
                if len(inilist) >= 2:
                    run = line[b:inilist[occ-1]]

                # Dictionary to map the words of runs to respective numerical values
                runs_mapping = {'no run': 0, '1 run': 1,
                                '2 runs': 2, '3 runs': 3, 'FOUR': 4, 'SIX': 6}
                ballwise_stats.append(runs_mapping[run[2:]])
                runs += runs_mapping[run[2:]]
                if float(line[0:3]) < 6:
                    powerplay += runs_mapping[run[2:]]
                out_reason.append("")
            # Appending the ballwise statistics to the team innings list
            team_inn.append(ballwise_stats)

        # Calculating Extras
        extras = byes+legbyes+nb+p+wides

        # Runs and wickets are calculated by taking the ceil
        runs = math.ceil(runs)
        wickets = math.ceil(wickets)

        # Creating a template to define which batsman was out and how he was out
        out_batsman = []
        for i in range(len(out_reason)):
            if out_reason[i][0:6] == 'Caught':
                c, d = out_reason[i].find('by '), out_reason[i].find('!!')
                catcher = out_reason[i][c+3:d]
                out_reason[i] = "c "+catcher+" b "+team_inn[i][1]
                out_batsman.append(team_inn[i][2])
            elif out_reason[i][0:3] == 'Lbw':
                out_reason[i] = "lbw b "+team_inn[i][1]
                out_batsman.append(team_inn[i][2])
            elif out_reason[i][0:6] == 'Bowled':
                out_reason[i] = "b "+team_inn[i][1]
                out_batsman.append(team_inn[i][2])
            else:
                out_batsman.append("")

        # Defining a batting order based on the given information
        batting_team = []
        batting_order = []
        for i in team_inn:
            batting_team.append(i[2])
        for i in batting_team:
            if i not in batting_order:
                batting_order.append(i)
        batting_team = batting_order.copy()
        batting_team_name = ''  # Name of the innings
        if inn1 == 1:
            with open('teams.txt', 'r') as team:
                teams = team.readlines()
                m = teams[0].find('(Playing XI)')
                batting_team_name = teams[0][:m]
                batting_team_list = teams[0].split(', ')
                m = batting_team_list[0].find(':')
                batting_team_list[0] = batting_team_list[0][m+2:]
                m = batting_team_list[-1].find('\n')
                batting_team_list[-1] = batting_team_list[-1][:m]
        else:
            with open('teams.txt', 'r') as team:
                teams = team.readlines()
                m = teams[2].find('(Playing XI)')
                batting_team_name = teams[2][:m]
                batting_team_list = teams[2].split(', ')
                m = batting_team_list[0].find(':')
                batting_team_list[0] = batting_team_list[0][m+2:]
                m = batting_team_list[-1].find('\n')
                batting_team_list[-1] = batting_team_list[-1][:m]

        batting_team_batters = []
        for i in range(len(batting_team)):
            for j in batting_team_list:
                if batting_team[i] in j:
                    batting_team_batters.append(j)
        did_not_bat=''
        for i in batting_team_list:
            if i not in batting_team_batters:
                did_not_bat+=i+', '

        # Defining the list to store various information for each batsman
        batting_team_runs = [0]*11
        batting_team_balls = [0]*11
        batting_team_fours = [0]*11
        batting_team_sixes = [0]*11
        batting_team_SR = [0]*11

        # Updating the information by calculating it for each batsman
        index = 0
        for i in batting_team:
            for j in team_inn:
                if j[2] == i:
                    if j[3] != 'out' and j[3] != 'wide' and j[3] != '3 wides' and j[3] != '2 wides' and j[3] != 'byes' and j[3] != 'leg byes':
                        batting_team_runs[index] += int(j[3])
                    if j[3] != 'wide' and j[3] != '3 wides' and j[3] != '2 wides':
                        batting_team_balls[index] += 1
                    if j[3] == 4:
                        batting_team_fours[index] += 1
                    if j[3] == 6:
                        batting_team_sixes[index] += 1
                if batting_team_balls[index] != 0:
                    batting_team_SR[index] = round(
                        batting_team_runs[index]*100/batting_team_balls[index], 2)
            index += 1

        # Defining a bowling order based on the given information
        bowling_team = []
        bowling_order = []
        for i in team_inn:
            bowling_team.append(i[1])
        for i in bowling_team:
            if i.strip() not in bowling_order:
                bowling_order.append(i)
        bowling_team = bowling_order.copy()
        if inn1 == 1:
            with open('teams.txt', 'r') as team:
                teams = team.readlines()
                n = teams[2].find('(Playing XI)')
                bowling_team_list = teams[2].split(', ')
                n = bowling_team_list[0].find(':')
                bowling_team_list[0] = bowling_team_list[0][n+2:]
                n = bowling_team_list[-1].find('\n')
                bowling_team_list[-1] = bowling_team_list[-1][:n]
        else:
            with open('teams.txt', 'r') as team:
                teams = team.readlines()
                n = teams[0].find('(Playing XI)')
                bowling_team_list = teams[0].split(', ')
                n = bowling_team_list[0].find(':')
                bowling_team_list[0] = bowling_team_list[0][n+2:]
                n = bowling_team_list[-1].find('\n')
                bowling_team_list[-1] = bowling_team_list[-1][:n]

        bowling_team_bowlers = []
        for i in range(len(bowling_team)):
            for j in bowling_team_list:
                if bowling_team[i] in j:
                    bowling_team_bowlers.append(j)

        # Defining the list to store various information for each bowler
        bowling_team_overs = [0]*len(bowling_order)
        bowling_team_maidens = [0]*len(bowling_order)
        bowling_team_runs = [0]*len(bowling_order)
        bowling_team_wickets = [0]*len(bowling_order)
        bowling_team_NB = [0]*len(bowling_order)
        bowling_team_WD = [0]*len(bowling_order)
        bowling_team_ECO = [0]*len(bowling_order)

        # Updating the information by calculating it for each batsman
        index = 0
        for i in bowling_team:
            maiden_check = 0
            for j in team_inn:
                if j[1].strip() == i:
                    bowling_team_overs[index] += 1
                    if j[3] != 'out' and j[3] != 'wide' and j[3] != '3 wides' and j[3] != '2 wides' and j[3] != 'byes' and j[3] != 'leg byes':
                        bowling_team_runs[index] += int(j[3])
                    if j[3] == 'wide':
                        bowling_team_runs[index] += 1
                        bowling_team_WD[index] += 1
                        bowling_team_overs[index] -= 1
                    if j[3] == '2 wides':
                        bowling_team_runs[index] += 2
                        bowling_team_WD[index] += 2
                        bowling_team_overs[index] -= 1
                    if j[3] == '3 wides':
                        bowling_team_runs[index] += 3
                        bowling_team_WD[index] += 3
                        bowling_team_overs[index] -= 1
                    if j[3] == 'byes':
                        pass
                    if j[3] == 'leg byes':
                        pass
                    if j[3] == 'out':
                        bowling_team_wickets[index] += 1
                    if j[3] == 0:
                        maiden_check += 1
                    else:
                        maiden_check = 0
                    if maiden_check == 6:
                        bowling_team_maidens[index] += 1

            # Calculating Economy = Number of runs/Number of overs and overs from the balls count
            bowling_team_ECO[index] = round(
                bowling_team_runs[index]*6/bowling_team_overs[index], 1)
            bowling_team_overs[index] = (bowling_team_overs[index]//6)+(bowling_team_overs[index]%6)/10
            index += 1

    # Writing the Information to Scorecard.txt
    try:
        with open("Scorecard.txt", 'a') as scorecard:
            scorecard.writelines(
                f"{'{} Innings'.format(batting_team_name) : <25}{'' : <35}{'' : ^10}{'' : ^10}{'' : ^10}{'' : ^10}{str(runs)+'-'+str(wickets)+'('+team_inn[-1][0]+')' : ^10}\n")
            scorecard.writelines(
                f"\n{'Batter' : <25}{'' : <35}{'R' : ^10}{'B' : ^10}{'4s' : ^10}{'6s' : ^10}{'SR' : >10}\n")
            for i in range(len(batting_team)):
                for j in range(len(out_batsman)):
                    if batting_team[i] not in out_batsman:
                        scorecard.writelines(
                            f"{batting_team_batters[i] : <25}{'not out' : <35}{batting_team_runs[i] : ^10}{batting_team_balls[i] : ^10}{batting_team_fours[i] : ^10}{batting_team_sixes[i] : ^10}{batting_team_SR[i] : >10}\n")
                        break
                    elif out_batsman[j] == batting_team[i]:
                        scorecard.writelines(
                            f"{batting_team_batters[i] : <25}{out_reason[j] : <35}{batting_team_runs[i] : ^10}{batting_team_balls[i] : ^10}{batting_team_fours[i] : ^10}{batting_team_sixes[i] : ^10}{batting_team_SR[i] : >10}\n")
            scorecard.writelines(
                f"{'Extras' : <25}{'' : <35}{'{}(b {}, lb {}, w {}, nb {}, p {})'.format(int(extras),int(byes),int(legbyes),int(wides),int(nb),int(p)) : ^10}{'' : ^10}{'' : ^10}{'' : ^10}{'' : >10}\n")
            scorecard.writelines(
                f"{'Total' : <25}{'' : <35}{'{}({} wkts, {} Ov)'.format(runs,wickets,team_inn[-1][0]) : ^10}{'' : ^10}{'' : ^10}{'' : ^10}{'' : >10}\n")
            scorecard.writelines(
                f"{'Did Not Bat' : <25}{did_not_bat : <35}{'' : ^10}{'' : ^10}{'' : ^10}{'' : ^10}{'' : >10}\n")
            scorecard.writelines(f"\n{'Fall of Wickets':<25}\n")
            fow = fallofwickets[0]+','
            for i in range(1, len(fallofwickets)):
                fow += fallofwickets[i]+', '
                if i % 4 == 0:
                    fow += '\n'
            scorecard.writelines(f"{fow:<25}\n")
            scorecard.writelines(
                f"\n{'Bowler' : <40}{'O' : ^10}{'M' : ^10}{'R' : ^10}{'W' : ^10}{'NB' : ^10}{'WD' : ^10}{'ECO' : >10}\n")
            for i in range(len(bowling_order)):
                scorecard.writelines(
                    f"{bowling_team_bowlers[i] : <40}{bowling_team_overs[i] : ^10}{bowling_team_maidens[i] : ^10}{bowling_team_runs[i] : ^10}{bowling_team_wickets[i] : ^10}{bowling_team_NB[i] : ^10}{bowling_team_WD[i] : ^10}{bowling_team_ECO[i] : >10}\n")
            scorecard.writelines(
                f"\n{'Powerplays' : <40}{'' : ^10}{'Overs' : ^10}{'' : ^10}{'Runs' : >10}\n")
            scorecard.writelines(
                f"{'Mandatory' : <40}{'' : ^10}{'0.1-6' : ^10}{'' : ^10}{powerplay : >10}\n\n")
    except:
        print("Something went wrong writing to the output file!")
        exit()

# Version Check
ver = python_version()

if ver == "3.8.10":
    print("Correct Version Installed")
else:
    print("Please install 3.8.10. Instruction are present in the GitHub Repo/Webmail. Url: https://pastebin.com/nvibxmjw")

# Calling the scorecard function
if os.path.exists("Scorecard.txt"):
    os.remove('Scorecard.txt')
scorecard('pak_inns1.txt', 1)
scorecard('india_inns2.txt', 2)


# This shall be the last lines of the code.
end_time = datetime.now()
print('Duration of Program Execution: {}'.format(end_time - start_time))
