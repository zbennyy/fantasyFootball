#!/usr/bin/env python3

from espn_api.football import League


# returns the active roster for lineup given in the following order:
# [qb, rb1, rb2, wr1, wr2, te, flex, dst, k]
def get_active_lineup(lineup):

    # initialize values
    qb = None
    rb1 = None
    rb2 = None
    wr1 = None
    wr2 = None
    te = None
    flex = None
    dst = None
    k = None

    # find active players
    for player in lineup:
        if player.slot_position == 'QB':
            qb = player
        if player.slot_position == 'RB':
            if rb1 is None:
                rb1 = player
            else:
                rb2 = player
        if player.slot_position == 'WR':
            if wr1 is None:
                wr1 = player
            else:
                wr2 = player
        if player.slot_position == 'TE':
            te = player
        if player.slot_position == 'RB/WR/TE':
            flex = player
        if player.slot_position == 'D/ST':
            dst = player
        if player.slot_position == 'K':
            k = player

    # return
    return [qb, rb1, rb2, wr1, wr2, te, flex, dst, k]


def convert_index_to_position(index):
    if index == 0:
        return "QB"
    elif index == 1 or index == 2:
        return "RB"
    elif index == 3 or index == 4:
        return "WR"
    elif index == 5:
        return "TE"
    elif index == 6:
        return "FLX"
    elif index == 7:
        return "D/ST"
    else:
        return "K"


def print_week_scoreboard(output_file, my_league, week_num):
    print("\tCreating scoreboard for week " + str(week_num) + "...")
    output_file.write("<!DOCTYPE html>\n")
    output_file.write("<html lang=en>\n\n")
    output_file.write("\t<head>\n")
    output_file.write("\t\t<link rel=\"stylesheet\" href=\"weeks_stuff.css\">\n")
    output_file.write("\t\t<title>Week " + str(week_num) + " Scoreboard</title>\n")
    output_file.write("\t</head>\n\n")
    output_file.write("\t<body>\n")
    output_file.write("\t\t<header>\n")
    output_file.write("\t\t\t<h1>Week " + str(week_num) + " Scoreboard</h1>\n")
    output_file.write("\t\t\t<p id=\"return_to_home\"><a href=\"/fantasyFootball\">Return to Home</a></p>\n")
    output_file.write("\t\t</header>\n")
    output_file.write("\t\t<main>\n")

    # find the week's highest and lowest scorers
    best_team = None
    best_score = 0
    worst_team = None
    worst_score = 1000
    for game in my_league.box_scores(week=week_num):
        if game.home_score > best_score:
            best_team = game.home_team
            best_score = game.home_score
        if game.home_score < worst_score:
            worst_team = game.home_team
            worst_score = game.home_score
        if game.away_score > best_score:
            best_team = game.away_team
            best_score = game.away_score
        if game.away_score < worst_score:
            worst_team = game.away_team
            worst_score = game.away_score
    best_team_string = ("<a href=\"/fantasyFootball/teams/" + str(best_team.team_id) + ".html\">" +
                        best_team.team_name + "</a> (" + str(round(best_score, 2)) + " points)")
    worst_team_string = ("<a href=\"/fantasyFootball/teams/" + str(worst_team.team_id) + ".html\">" +
                         worst_team.team_name + "</a> (" + str(round(worst_score, 2)) + " points)")
    output_file.write("\t\t\t<div class=\"week_data\">\n")
    output_file.write("\t\t\t\t<p><b>This Week's High Scorer:</b> " + best_team_string + "</p>\n")
    output_file.write("\t\t\t\t<p><b>This Week's Lowest Scorer:</b> " + worst_team_string + "</p>\n")
    output_file.write("\t\t\t</div>\n")

    div_type = 0
    for game in my_league.box_scores(week=week_num):

        # collect data
        home_team_string = ("<a href=\"/fantasyFootball/teams/" + str(game.home_team.team_id) + ".html\">"
                            + game.home_team.team_name + "</a>")
        away_team_string = ("<a href=\"/fantasyFootball/teams/" + str(game.away_team.team_id) + ".html\">"
                            + game.away_team.team_name + "</a>")
        home_active = get_active_lineup(game.home_lineup)
        away_active = get_active_lineup(game.away_lineup)

        # teams
        output_file.write("\t\t\t<div class=\"game_" + str(div_type) + "\">\n")
        output_file.write("\t\t\t\t<table>\n")
        output_file.write("\t\t\t\t\t<thead>\n")
        output_file.write("\t\t\t\t\t\t<tr>\n")
        output_file.write("\t\t\t\t\t\t\t<th></th>\n")
        output_file.write("\t\t\t\t\t\t\t<th colspan=\"2\" class=\"team\">" + home_team_string + "</th>\n")
        output_file.write("\t\t\t\t\t\t\t<th colspan=\"2\" class=\"team\">" + away_team_string + "</th>\n")
        output_file.write("\t\t\t\t\t\t</tr>\n")

        # header row
        output_file.write("\t\t\t\t\t\t<tr>\n")
        output_file.write("\t\t\t\t\t\t\t<th class=\"pos_name\">Pos.</th>\n")
        output_file.write("\t\t\t\t\t\t\t<th class=\"player_left\">Player (Team)</th>\n")
        output_file.write("\t\t\t\t\t\t\t<th class=\"score\">Score</th>\n")
        output_file.write("\t\t\t\t\t\t\t<th class=\"score\">Score</th>\n")
        output_file.write("\t\t\t\t\t\t\t<th class=\"player_right\">Player (Team)</th>\n")
        output_file.write("\t\t\t\t\t\t</tr>\n")
        output_file.write("\t\t\t\t\t</thead>\n")

        # players
        output_file.write("\t\t\t\t\t<tbody>\n")
        for i in range(len(home_active)):
            output_file.write("\t\t\t\t\t\t<tr>\n")
            output_file.write("\t\t\t\t\t\t\t<td class=\"pos_name\">" + convert_index_to_position(i) + "</td>\n")
            output_file.write("\t\t\t\t\t\t\t<td class=\"player_left\">" + home_active[i].name + " (" +
                              home_active[i].proTeam + ")</td>\n")
            output_file.write("\t\t\t\t\t\t\t<td class=\"score\">" + str(home_active[i].points) + "</td>\n")
            output_file.write("\t\t\t\t\t\t\t<td class=\"score\">" + str(away_active[i].points) + "</td>\n")
            output_file.write("\t\t\t\t\t\t\t<td class=\"player_right\">" + away_active[i].name + " (" +
                              away_active[i].proTeam + ")</td>\n")
            output_file.write("\t\t\t\t\t\t</tr>\n")
        output_file.write("\t\t\t\t\t</tbody>\n")

        # scores
        output_file.write("\t\t\t\t\t<tfoot>\n")
        output_file.write("\t\t\t\t\t\t<tr>\n")
        output_file.write("\t\t\t\t\t\t\t<td></td>\n")
        output_file.write("\t\t\t\t\t\t\t<td class=\"player_left\"><b>TOTAL</b></td>\n")
        output_file.write("\t\t\t\t\t\t\t<td class=\"score\"><b>" + str(game.home_score) + "</b></td>\n")
        output_file.write("\t\t\t\t\t\t\t<td class=\"score\"><b>" + str(game.away_score) + "</b></td>\n")
        output_file.write("\t\t\t\t\t\t\t<td class=\"player_right\"><b>TOTAL</b></td>\n")
        output_file.write("\t\t\t\t\t\t</tr>\n")
        output_file.write("\t\t\t\t\t</tfoot>\n")

        # close table and div
        output_file.write("\t\t\t\t</table>\n")
        output_file.write("\t\t\t</div>\n\n")
        div_type = (div_type + 1) % 2

    # close remaining tags
    output_file.write("\t\t</main>\n")
    output_file.write("\t</body>\n\n")
    output_file.write("</html>\n")


def create(my_league):
    print("Creating week-by-week scoreboards...")
    for week in range(1, my_league.current_week):
        output_file = open('weeks/week_' + str(week) + '.html', 'w')
        print_week_scoreboard(output_file, my_league, week)
        output_file.close()


if __name__ == "__main__":
    cookies_file = open('venv/secret_stuff.txt', 'r')
    my_s2 = cookies_file.readline().strip()
    my_swid = cookies_file.readline().strip()
    cookies_file.close()

    print("Connecting to ESPN...")
    league = League(league_id=859158741, year=2023, espn_s2=my_s2, swid=my_swid)
    create(league)

## test comment