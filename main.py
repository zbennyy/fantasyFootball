import math

from espn_api.football import League


# returns the following score data as a list, in order:
# [number of games played, total points scored, minimum score, maximum score, average score, standard deviation]
def compute_score_data(team):
    games_played = 0
    sum_scores = 0
    min_score = 1000
    max_score = 0

    for score in team.scores:
        if score != 0:
            sum_scores += score
            if score < min_score:
                min_score = score
            if score > max_score:
                max_score = score
            games_played += 1

    average_score = sum_scores / games_played - 1
    variance = 0

    for score in team.scores:
        if score != 0:
            variance += math.pow(score - average_score, 2)

    variance /= games_played
    standard_deviation = math.sqrt(variance)

    return [games_played, sum_scores, min_score, max_score, average_score, standard_deviation]


# gets current standings position of a team
def sort_key_teams_standings(team):
    return team.standing


# gets position of a player
def sort_key_players_position(player):
    return player.position


def print_roster(output_file, players):

    # create table
    output_file.write("\t\t<h3>Roster</h3>\n")
    output_file.write("\t\t<table>\n")
    output_file.write("\t\t\t<tr>\n")
    output_file.write("\t\t\t\t<th>Position</th>\n")
    output_file.write("\t\t\t\t<th>Player</th>\n")
    output_file.write("\t\t\t\t<th>Team</th>\n")
    output_file.write("\t\t\t\t<th>Total Points</th>\n")
    output_file.write("\t\t\t\t<th>Projected Total Points</th>\n")
    output_file.write("\t\t\t</tr>\n")

    # add row for each player
    players.sort(key=sort_key_players_position)
    for player in players:
        output_file.write("\t\t\t<tr>\n")
        output_file.write("\t\t\t\t<td>" + player.position + "</td>\n")
        output_file.write("\t\t\t\t<td>" + player.name + "</td>\n")
        output_file.write("\t\t\t\t<td>" + player.proTeam + "</td>\n")
        output_file.write("\t\t\t\t<td>" + str(player.total_points) + "</td>\n")
        output_file.write("\t\t\t\t<td>" + str(player.projected_total_points) + "</td>\n")
        output_file.write("\t\t\t</tr>\n")

    # close table
    output_file.write("\t\t</table>")


# creates an HTML page for each team
def create_team_files(teams):
    for team in teams:
        output_file = open("teams/" + str(team.team_id) + ".html", 'w')

        # initial HTML setup
        output_file.write("<!DOCTYPE html>\n")
        output_file.write("<html lang=en>\n\n")
        output_file.write("\t<head>\n")
        output_file.write("\t\t<link rel=\"stylesheet\" href=\"stuff.css\">\n")
        output_file.write("\t\t<title>" + team.team_name + "</title>\n")
        output_file.write("\t</head>\n\n")
        output_file.write("\t<body>\n")
        output_file.write("\t\t<h1>" + team.team_name + " (" + str(team.wins) + "-" + str(team.losses) + ")</h1>\n")
        output_file.write("\t\t<h2>Owner: " + team.owner + "</h2>\n")

        print_roster(output_file, team.roster)

        # close HTML file
        output_file.write("<p><a href=\"/index.html\">Return to Home</a></p>\n")
        output_file.write("\t</body>\n\n")
        output_file.write("</html>")
        output_file.close()


# write data for each team to output file as a row of an HTML table.
def print_teams_to_index_file(output_file, teams):
    teams.sort(key=sort_key_teams_standings)
    for team in teams:
        data = compute_score_data(team)
        team_file = "teams/" + str(team.team_id) + ".html"
        output_file.write("\t\t\t<tr>\n")
        output_file.write("\t\t\t\t<td><a href=\"" + team_file + "\">" + team.team_name + "</a></td>\n")
        output_file.write("\t\t\t\t<td>" + team.owner + "</td>\n")
        output_file.write("\t\t\t\t<td>" + str(team.wins) + "</td>\n")
        output_file.write("\t\t\t\t<td>" + str(team.losses) + "</td>\n")
        if team.streak_type == "WIN":
            output_file.write("\t\t\t\t<td>W " + str(team.streak_length) + "</td>\n")
        else:
            output_file.write("\t\t\t\t<td>L " + str(team.streak_length) + "</td>\n")
        output_file.write("\t\t\t\t<td>" + str(round(data[1], 2)) + "</td>\n")
        output_file.write("\t\t\t\t<td>" + str(round(data[4], 2)) + "</td>\n")
        output_file.write("\t\t\t\t<td>" + str(round(data[2], 2)) + "</td>\n")
        output_file.write("\t\t\t\t<td>" + str(round(data[3], 2)) + "</td>\n")
        output_file.write("\t\t\t\t<td>" + str(round(data[5], 2)) + "</td>\n")
        output_file.write("\t\t\t</tr>\n")


# create and populate index file. currently only consists of a table of the league standings.
def create_index_file(teams):
    output_file = open('index.html', 'w')

    # initial HTML setup
    output_file.write("<!DOCTYPE html>\n")
    output_file.write("<html lang=en>\n\n")
    output_file.write("\t<head>\n")
    output_file.write("\t\t<link rel=\"stylesheet\" href=\"stuff.css\">\n")
    output_file.write("\t\t<title>Fantasy Football Score Data</title>\n")
    output_file.write("\t<head>\n\n")
    output_file.write("\t<body>\n")

    # data table setup
    output_file.write("\t\t<table>\n")
    output_file.write("\t\t\t<tr>\n")
    output_file.write("\t\t\t\t<th>Team Name</th>\n")
    output_file.write("\t\t\t\t<th>Owner</th>\n")
    output_file.write("\t\t\t\t<th>Wins</th>\n")
    output_file.write("\t\t\t\t<th>Losses</th>\n")
    output_file.write("\t\t\t\t<th>Streak</th>\n")
    output_file.write("\t\t\t\t<th>Total Points Scored</th>\n")
    output_file.write("\t\t\t\t<th>Average Points Scored</th>\n")
    output_file.write("\t\t\t\t<th>Worst Score</th>\n")
    output_file.write("\t\t\t\t<th>Best Score</th>\n")
    output_file.write("\t\t\t\t<th>Standard Deviation</th>\n")
    output_file.write("\t\t\t</tr>\n")

    print_teams_to_index_file(output_file, teams)

    # close HTML file
    output_file.write("\t\t</table>\n")
    output_file.write("\t</body>\n\n")
    output_file.write("</html>")
    output_file.close()


def main():
    cookies_file = open('venv/secret_stuff.txt', 'r')
    my_s2 = cookies_file.readline().strip()
    my_swid = cookies_file.readline().strip()
    cookies_file.close()

    league = League(league_id=859158741, year=2023, espn_s2=my_s2, swid=my_swid)
    create_team_files(league.teams)
    create_index_file(league.teams)


if __name__ == '__main__':
    main()
