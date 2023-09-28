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


# gets number of wins from a team; for use in sorting list of teams by record
def sort_key(team):
    return team.standing


# write data for each team to output file as a row of an HTML table
def print_teams_to_file(output_file, teams):
    teams.sort(key=sort_key)
    for team in teams:
        data = compute_score_data(team)
        output_file.write("\t\t\t<tr>\n")
        output_file.write("\t\t\t\t<td>" + team.team_name + "</td>\n")
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


def main():
    cookies_file = open('Scripts/secret_stuff.txt', 'r')
    my_s2 = cookies_file.readline()
    my_swid = cookies_file.readline()
    cookies_file.close()

    my_league = League(league_id=859158741, year=2023, espn_s2=my_s2, swid=my_swid)
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

    print_teams_to_file(output_file, my_league.teams)

    # close HTML file
    output_file.write("\t\t</table>\n")
    output_file.write("\t</body>\n\n")
    output_file.write("</html>")
    output_file.close()


if __name__ == '__main__':
    main()
