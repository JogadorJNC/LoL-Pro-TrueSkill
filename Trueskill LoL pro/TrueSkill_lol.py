import itertools
import math
import trueskill

# This is the implementation of the TrueSkill System.
# TrueSkill(TM) was developed my Microsoft, and Mirosoft only permits Xbox Live games and non-commercial projects to use it.
# This project requires a trueskill package that was developed by Heungsub Lee, his website is subl.ee, more info on the package can be found at trueskill.org

# The results class, it just holds some values.
class results:
    def __init__(self, ratings, team_ratings, champ_ratings, ngames, A, MSE, EA, EMSE):
        self.ratings=ratings
        self.team_ratings=team_ratings
        self.champ_ratings=champ_ratings
        self.ngames=ngames
        self.A=A
        self.MSE=MSE
        self.EA=EA
        self.EMSE=EMSE



class TrueSkill_lol:
    def __init__(self, mh):
        self.mh=mh

    def apply(self, mu, sigma, beta, tau):
        ts=trueskill.TrueSkill(mu=mu, sigma=sigma, beta=beta, tau=tau, draw_probability=0)
        SE=0
        G=0
        A=0
        ESE=0
        EA=0

        player_ratings={}
        team_ratings={}
        champ_ratings={}

        # Populates the ratings.
        for match in self.mh:
            if match["Team1"].lower() not in team_ratings:
                team_ratings[match["Team1"].lower()]=ts.create_rating()
            if match["Team2"].lower() not in team_ratings:
                team_ratings[match["Team2"].lower()]=ts.create_rating()

            for player in match["Team1Players"]:
                if player not in player_ratings:
                    player_ratings[player]=ts.create_rating()
            for player in match["Team2Players"]:
                if player not in player_ratings:
                    player_ratings[player]=ts.create_rating()

        for match in self.mh:
            t1=[]
            t2=[]

            # Creates the teams.
            t1.append(team_ratings[match["Team1"].lower()])
            t2.append(team_ratings[match["Team2"].lower()])
            for player in match["Team1Players"]:
                t1.append(player_ratings[player])
            for player in match["Team2Players"]:
                t2.append(player_ratings[player])

            # Calculates the win probability of each team.
            E=win_probability(t1, t2, beta)
            t2win=int(match["Winner"])-1
            teams=[t1,t2]

            # Calculates the new ratings.
            teams=ts.rate(teams, ranks=[t2win, (1-t2win)])

            # Updates the player ratings.
            p_number=1
            for player in match["Team1Players"]:
                player_ratings[player]=teams[0][p_number]
                p_number+=1
            p_number=1
            for player in match["Team2Players"]:
                player_ratings[player]=teams[1][p_number]
                p_number+=1

            # Updates the team ratings.
            team_ratings[match["Team1"].lower()]=teams[0][0]
            team_ratings[match["Team2"].lower()]=teams[1][0]

            G+=1
            if G%5000==0:
                print(G)

            # Updates the accuracy measurements.
            SE+=pow(((1-t2win)-E), 2)
            ESE+=E-pow(E,2)
            EA+=max(E, 1-E)
            if pow(((1-t2win)-E), 2)<0.25:
                    A+=1

        # Creates the results variable and returns it.
        ret=results(player_ratings, team_ratings, champ_ratings, G, round(A/G, 6), round(SE/G, 6), round(EA/G, 6), round(ESE/G, 6))
        return ret


# This function was taken directly from trueskill.org, it was written by Juho Snellman, his website is snellman.net.
def win_probability(team1, team2, BETA):
    delta_mu = sum(r.mu for r in team1) - sum(r.mu for r in team2)
    sum_sigma = sum(r.sigma ** 2 for r in itertools.chain(team1, team2))
    size = len(team1) + len(team2)
    denom = math.sqrt(size * (BETA * BETA) + sum_sigma)
    ts = trueskill.global_env()
    return ts.cdf(delta_mu / denom)
