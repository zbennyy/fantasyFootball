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


def print_box_scores_to_index_file(output_file, league):

    # if this is not the first week, print last week's scores
    if league.current_week > 1:
        last_week_box_scores = league.box_scores(league.current_week - 1)
        output_file.write("\t\t\t<div class=\"last_week_scores\">\n")
        output_file.write("\t\t\t\t<h3>Last Week's Scores:</h3>\n")
        for match in last_week_box_scores:
            if match.home_score > match.away_score:
                match_string = ("<b>" + match.home_team.team_name + "</b> def. " + match.away_team.team_name + " " +
                                str(match.home_score) + " - " + str(match.away_score))
            else:
                match_string = ("<b>" + match.away_team.team_name + "</b> def. " + match.home_team.team_name + " " +
                                str(match.away_score) + " - " + str(match.home_score))
            output_file.write("\t\t\t\t<p>" + match_string + "</p>\n")
        output_file.write("\t\t\t</div>\n")

    # print this week's upcoming matchups
    this_week_games = league.box_scores(league.current_week)
    output_file.write("\t\t\t<div class=\"this_week_games\">\n")
    output_file.write("\t\t\t\t<h3>This Week's Matchups:</h3>\n")
    for match in this_week_games:
        home_string = (match.home_team.team_name + " (" + str(match.home_team.wins) + "-" +
                       str(match.home_team.losses) + ")")
        away_string = (match.away_team.team_name + " (" + str(match.away_team.wins) + "-" +
                       str(match.away_team.losses) + ")")
        match_string = home_string + " vs " + away_string
        output_file.write("\t\t\t\t<p>" + match_string + "</p>\n")
    output_file.write("\t\t\t</div>\n")


def print_recent_activity_to_index_file(output_file, league):
    print("\t\tRetrieving FA activity...")
    recent_fa = league.recent_activity(size=10, msg_type='FA', offset=0)
    print("\t\tRetrieving waiver activity...")
    recent_waivers = league.recent_activity(size=10, msg_type='WAIVER', offset=0)
    output_file.write("\t\t\t<div class=\"recent_activity\">\n")

    # free agent acquisitions
    output_file.write("\t\t\t\t<div class=\"free_agent\">\n")
    output_file.write("\t\t\t\t\t<h3 id=\"free_agent_acquisitions\">Recent Free Agent Acquisitions</h3>\n")
    for action in recent_fa:
        team = action.actions[0][0]
        player = action.actions[0][2]
        action_string = ("<a href=\"teams/" + str(team.team_id) + ".html\">" + team.team_name + "</a> acquires " +
                         player.name + " (" + player.position + ", " + player.proTeam + ")")
        output_file.write("\t\t\t\t\t<p>" + action_string + "</p>\n")
    output_file.write("\t\t\t\t</div>\n")

    # waiver wire claims
    output_file.write("\t\t\t\t<div class=\"waiver_wire\">\n")
    output_file.write("\t\t\t\t\t<h3 id=\"waiver_claims\">Recent Waiver Wire Claims</h3>\n")
    for action in recent_waivers:
        team = action.actions[0][0]
        player = action.actions[0][2]
        cost = action.actions[0][3]
        action_string = ("<a href=\"teams/" + str(team.team_id) + ".html\">" + team.team_name + "</a> claims " +
                         player.name + " (" + player.position + ", " + player.proTeam + ") for $" + str(cost))
        output_file.write("\t\t\t\t\t<p>" + action_string + "</p>\n")
    output_file.write("\t\t\t\t</div>\n")

    # close overarching activity div
    output_file.write("\t\t\t</div>\n")


# write data for each team to output file as a row of an HTML table.
def print_teams_to_index_file(output_file, teams):

    # table setup
    output_file.write("\t\t\t<div class=\"league_standings\">\n")
    output_file.write("\t\t\t\t<h3>Standings</h3>\n")
    output_file.write("\t\t\t\t<table id=\"standings\">\n")
    output_file.write("\t\t\t\t\t<thead>\n")
    output_file.write("\t\t\t\t\t\t<tr>\n")
    output_file.write("\t\t\t\t\t\t\t<th>Pos.</th>\n")
    output_file.write("\t\t\t\t\t\t\t<th>Team Name</th>\n")
    output_file.write("\t\t\t\t\t\t\t<th>Owner</th>\n")
    output_file.write("\t\t\t\t\t\t\t<th>Wins</th>\n")
    output_file.write("\t\t\t\t\t\t\t<th>Losses</th>\n")
    output_file.write("\t\t\t\t\t\t\t<th>Streak</th>\n")
    output_file.write("\t\t\t\t\t\t\t<th>Total Points Scored</th>\n")
    output_file.write("\t\t\t\t\t\t\t<th>Average Score</th>\n")
    output_file.write("\t\t\t\t\t\t\t<th>Best Score</th>\n")
    output_file.write("\t\t\t\t\t\t\t<th>Worst Score</th>\n")
    output_file.write("\t\t\t\t\t\t\t<th>Standard Deviation</th>\n")
    output_file.write("\t\t\t\t\t\t\t<th>Playoff Chances</th>\n")
    output_file.write("\t\t\t\t\t\t</tr>\n")
    output_file.write("\t\t\t\t\t</thead>\n")

    # print team data
    teams.sort(key=sort_key_teams_standings)
    output_file.write("\t\t\t\t\t<tbody>\n")
    for team in teams:
        data = compute_score_data(team)
        team_file = "teams/" + str(team.team_id) + ".html"
        output_file.write("\t\t\t\t\t\t<tr>\n")
        output_file.write("\t\t\t\t\t\t\t<td>" + str(team.standing) + "</td>\n")
        output_file.write("\t\t\t\t\t\t\t<td><a href=\"" + team_file + "\">" + team.team_name + "</a></td>\n")
        output_file.write("\t\t\t\t\t\t\t<td>" + team.owner + "</td>\n")
        output_file.write("\t\t\t\t\t\t\t<td>" + str(team.wins) + "</td>\n")
        output_file.write("\t\t\t\t\t\t\t<td>" + str(team.losses) + "</td>\n")
        if team.streak_type == "WIN":
            output_file.write("\t\t\t\t\t\t\t<td>W " + str(team.streak_length) + "</td>\n")
        else:
            output_file.write("\t\t\t\t\t\t\t<td>L " + str(team.streak_length) + "</td>\n")
        output_file.write("\t\t\t\t\t\t\t<td>" + str(round(data[1], 2)) + "</td>\n")
        output_file.write("\t\t\t\t\t\t\t<td>" + str(round(data[4], 2)) + "</td>\n")
        output_file.write("\t\t\t\t\t\t\t<td>" + str(round(data[3], 2)) + "</td>\n")
        output_file.write("\t\t\t\t\t\t\t<td>" + str(round(data[2], 2)) + "</td>\n")
        output_file.write("\t\t\t\t\t\t\t<td>" + str(round(data[5], 2)) + "</td>\n")
        output_file.write("\t\t\t\t\t\t\t<td>" + str(round(team.playoff_pct, 2)) + "%</td>\n")
        output_file.write("\t\t\t\t\t\t</tr>\n")

    # close table
    output_file.write("\t\t\t\t\t</tbody>\n")
    output_file.write("\t\t\t\t</table>\n")
    output_file.write("\t\t\t</div>\n")


# create and populate index file.
def create(league):
    print("Creating index file...")
    output_file = open('index.html', 'w')

    # initial HTML setup
    output_file.write("<!DOCTYPE html>\n")
    output_file.write("<html lang=en>\n\n")
    output_file.write("\t<head>\n")
    output_file.write("\t\t<link rel=\"stylesheet\" href=\"stuff.css\">\n")
    output_file.write("\t\t<title>Fantasy Football Score Data</title>\n")
    output_file.write("\t</head>\n\n")
    output_file.write("\t<body>\n")
    output_file.write("\t\t<header>\n")
    output_file.write("\t\t\t<h1>Fantasy Ball Z 2023</h1>\n")
    output_file.write("\t\t</header>\n")
    output_file.write("\t\t<main>\n")

    print("\tAdding box scores to index.html...")
    print_box_scores_to_index_file(output_file, league)
    output_file.write("\n")
    print("\tAdding recent activity to index file...")
    print_recent_activity_to_index_file(output_file, league)
    output_file.write("\n")
    print("\tAdding standings to index.html...")
    print_teams_to_index_file(output_file, league.teams)

    # close HTML file
    output_file.write("\t\t</main>\n")
    output_file.write("\t</body>\n\n")
    output_file.write("</html>")
    output_file.close()


if __name__ == '__main__':
    cookies_file = open('venv/secret_stuff.txt', 'r')
    my_s2 = cookies_file.readline().strip()
    my_swid = cookies_file.readline().strip()
    cookies_file.close()

    print("Connecting to ESPN...")
    my_league = League(league_id=859158741, year=2023, espn_s2=my_s2, swid=my_swid)
    create(my_league)
