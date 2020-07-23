import MElo
import TrueSkill_lol
import json
import scipy
from scipy import optimize
import itertools
import math
import trueskill

# This script applies the system then has a command line interface to get the ratings of the team and the players.
# The interface at the end takes as the input the team then the name of each player as is used on gamepedia and outputs the expected probability of the first team winning.
# new_team and new_player add the rating equivalents of a completely new team and player respectively.
# show_all shows either all the team ratings or all the player ratings, depending on what is being asked for, separated by semicolons. It follows the format "name;mu;sigma".


# This function was taken directly from trueskill.org, it was written by Juho Snellman, his website is snellman.net.
def win_probability(team1, team2, BETA):
    delta_mu = sum(r.mu for r in team1) - sum(r.mu for r in team2)
    sum_sigma = sum(r.sigma ** 2 for r in itertools.chain(team1, team2))
    size = len(team1) + len(team2)
    denom = math.sqrt(size * (BETA * BETA) + sum_sigma)
    ts = trueskill.global_env()
    return ts.cdf(delta_mu / denom)

# Opens the match history file.
with open("FixedMatchHistory.json", mode="r", encoding="utf8") as f:
    mh=json.load(f)

# Initializes the trueskill class.
TrueSkill_lol=TrueSkill_lol.TrueSkill_lol(mh)
# Applies the algorithm.
results=TrueSkill_lol.apply(25,3,4,0.12)
ratings=results.ratings
team_ratings=results.team_ratings
champ_ratings=results.champ_ratings

# Prints the accuracy results, MSE is the Mean Squared Error, EMSE is the expected MSE from it's own predictions,
# A is the percentage of games where it correctly guessed the winner, and EA is the expected A.
print(results.MSE, results.EMSE, results.A, results.EA)

# Initializes the TrueSkill environment to be used in this script.
ts=trueskill.TrueSkill(25,3,4,0.12, draw_probability=0)

# Implements the interface.
team=1
while 0==0:
    t1=[]
    t2=[]
    print("\nTeam1: ")
    c=0
    while c==0:
        inp=input()
        inp=inp.lower()
        if inp=="show_all":
            for j in team_ratings:
                print(j,";", team_ratings[j].mu, ";", team_ratings[j].sigma)
            break
        if inp=="new_team":
            t1.append(ts.create_rating())
            print(t1[-1])
            break
        if inp in team_ratings:
            t1.append(team_ratings[inp])
            print(team_ratings[inp])
            c=1
        else:
            print("404 team not found")


    for i in range(5):
        c=0
        while c==0:
            inp=input()
            inp=inp.lower()

            if inp=="show_all":
                for j in ratings:
                    print(j,";", ratings[j].mu, ";", ratings[j].sigma)
            if inp=="show_champs":
                for j in champ_ratings:
                    print(j,";", champ_ratings[j].mu, ";", champ_ratings[j].sigma)
            if inp=="new_player":
                t1.append(ts.create_rating())
                print(t1[-1])
                break
            if inp in ratings:
                t1.append(ratings[inp])
                print(ratings[inp])
                c=1
            else:
                print("404 player not found")
    print("\nTeam2: ")
    c=0
    while c==0:
        inp=input()
        inp=inp.lower()
        if inp=="show_all":
            for j in team_ratings:
                print(j,";", team_ratings[j].mu, ";", team_ratings[j].sigma)
        if inp=="new_team":
            t2.append(ts.create_rating())
            print(t2[-1])
            break
        if inp in team_ratings:
            t2.append(team_ratings[inp])
            print(team_ratings[inp])
            c=1
        else:
            print("404 team not found")

    for i in range(5):
        c=0
        while c==0:
            inp=input()
            inp=inp.lower()
            if inp=="show_all":
                for j in ratings:
                    print(j,";", ratings[j].mu, ";", ratings[j].sigma)
                    # print("|", j,"|", ratings[j].mu, "|", ratings[j].sigma, "|")
                    # print("|:-|:-|:-|")

            if inp=="show_champs":
                for j in champ_ratings:
                    print(j,";", champ_ratings[j].mu, ";", champ_ratings[j].sigma)

            if inp=="new_player":
                t2.append(ts.create_rating())
                print(t2[-1])
                break
            if inp in ratings:
                t2.append(ratings[inp])
                print(ratings[inp])
                c=1
            else:
                print("404 player not found")
    print("\n"+str(win_probability(t1, t2, 4)))



################################################################################



























    #
