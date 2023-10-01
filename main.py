#!/usr/bin/env python3

import teamfiles
import homepage
import scoreboards

from espn_api.football import League


def create_all(my_league):
    scoreboards.create(my_league)
    teamfiles.create(my_league.teams)
    homepage.create(my_league)


if __name__ == "__main__":
    cookies_file = open('venv/secret_stuff.txt', 'r')
    my_s2 = cookies_file.readline().strip()
    my_swid = cookies_file.readline().strip()
    cookies_file.close()

    print("Connecting to ESPN...")
    league = League(league_id=859158741, year=2023, espn_s2=my_s2, swid=my_swid)
    create_all(league)
