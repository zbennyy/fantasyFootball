import math

from espn_api.football import League


# returns the following score data as a list, in order:
# [number of games played, total points scored, minimum score, maximum score, average score, standard deviation,
# week of minimum score, week of maximum score]
def compute_score_data(team):
    games_played = 0
    sum_scores = 0
    min_score = 1000
    max_score = 0
    min_week = 0
    max_week = 0

    for week in range(len(team.scores)):
        score = team.scores[week - 1]
        if score != 0:
            sum_scores += score
            if score < min_score:
                min_score = score
                min_week = week
            if score > max_score:
                max_score = score
                max_week = week
            games_played += 1

    average_score = sum_scores / games_played - 1
    variance = 0

    for score in team.scores:
        if score != 0:
            variance += math.pow(score - average_score, 2)

    variance /= games_played
    standard_deviation = math.sqrt(variance)

    return [games_played, sum_scores, min_score, max_score, average_score, standard_deviation, min_week, max_week]


# gets current standings position of a team
def sort_key_teams_standings(team):
    return team.standing


# gets position of a player
def sort_key_players_position(player):
    return player.position


def print_team_data(output_file, team):

    # compute relevant data
    data = compute_score_data(team)
    max_score = data[3]
    max_week = data[7]
    max_opp = team.schedule[max_week - 1].team_name
    max_opp_id = team.schedule[max_week - 1].team_id
    max_opp_string = "<a href=\"" + str(max_opp_id) + ".html\">" + max_opp + "</a>"
    min_score = data[2]
    min_week = data[6]
    min_opp = team.schedule[min_week - 1].team_name
    min_opp_id = team.schedule[min_week - 1].team_id
    min_opp_string = "<a href=\"" + str(min_opp_id) + ".html\">" + min_opp + "</a>"
    max_score_string = str(max_score) + " Points in Week " + str(max_week) + " vs " + max_opp_string
    min_score_string = str(min_score) + " Points in Week " + str(min_week) + " vs " + min_opp_string
    improvement_since_draft = team.draft_projected_rank - team.standing
    if improvement_since_draft == 0:
        improvement_string = "EVEN"
    elif improvement_since_draft > 0:
        improvement_string = "+" + str(improvement_since_draft)
    else:
        improvement_string = str(improvement_since_draft)
    projection_string = str(team.draft_projected_rank) + " (" + improvement_string + ")"

    output_file.write("\t\t<h2>Stats</h2>\n")
    output_file.write("\t\t<p><b>Current Streak:</b> " + team.streak_type + " " + str(team.streak_length) + "</p>\n")
    output_file.write("\t\t<p><b>Total Points Scored This Season:</b> " + str(round(team.points_for, 2)) + "</p>\n")
    output_file.write("\t\t<p><b>Average Points Per Game:</b> " + str(round(data[4], 2)) + "</p>\n")
    output_file.write("\t\t<p><b>Best Score:</b> " + max_score_string + "</p>\n")
    output_file.write("\t\t<p><b>Worst Score:</b> " + min_score_string + "</p>\n")
    output_file.write("\t\t<p><b>Draft Day Projected Position:</b> " + projection_string + "</p>\n")
    output_file.write("\t\t<p><b>Chance to Make Playoffs:</b> " + str(round(team.playoff_pct, 2)) + "%</p>\n")


def print_team_scoreboard(output_file, team):

    # initial table setup
    output_file.write("\t\t<h3>Scoreboard</h3>\n")
    output_file.write("\t\t<table>\n")
    output_file.write("\t\t\t<tr>\n")
    output_file.write("\t\t\t\t<th>Week</th>\n")
    output_file.write("\t\t\t\t<th>Opponent</th>\n")
    output_file.write("\t\t\t\t<th>Result</th>\n")
    output_file.write("\t\t\t</tr>\n")

    # create row for each completed week
    for week in range(len(team.schedule)):
        if team.outcomes[week - 1] != "U":
            opponent_name = team.schedule[week - 1].team_name
            opponent_link = str(team.schedule[week - 1].team_id) + ".html"
            outcome = team.outcomes[week - 1]
            score = team.scores[week - 1]
            opp_score = team.schedule[week - 1].scores[week - 1]
            score_string = outcome + " " + str(score) + " - " + str(opp_score)
            output_file.write("\t\t\t<tr>\n")
            output_file.write("\t\t\t\t<td>Week " + str(week) + "</td>\n")
            output_file.write("\t\t\t\t<td><a href=\"" + opponent_link + "\">" + opponent_name + "</a></td>\n")
            output_file.write("\t\t\t\t<td>" + score_string + "</td>\n")
            output_file.write("\t\t\t</tr>\n")

    # close table
    output_file.write("\t\t</table>\n")


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
        team_header_string = ("#" + str(team.standing) + " " + team.team_name + " (" + str(team.wins) + "-" +
                              str(team.losses) + ")")

        # initial HTML setup
        output_file.write("<!DOCTYPE html>\n")
        output_file.write("<html lang=en>\n\n")
        output_file.write("\t<head>\n")
        output_file.write("\t\t<link rel=\"stylesheet\" href=\"teams_stuff.css\">\n")
        output_file.write("\t\t<title>" + team.team_name + "</title>\n")
        output_file.write("\t</head>\n\n")
        output_file.write("\t<body>\n")
        output_file.write("\t\t<h1>" + team_header_string + "</h1>\n")
        output_file.write("\t\t<h2>Owner: " + team.owner + "</h2>\n")

        print_team_data(output_file, team)
        output_file.write("\n")
        print_team_scoreboard(output_file, team)
        output_file.write("\n")
        print_roster(output_file, team.roster)

        # close HTML file
        output_file.write("<p><a href=\"/fantasyFootball\">Return to Home</a></p>\n")
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