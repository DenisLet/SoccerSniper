from bs4 import BeautifulSoup
from time import sleep


def current_moment(time):
    if time[0].isdigit():
        moment = int(time[0])
    elif time[0] == "Half" or time[0] == "45+":
        moment = 45
    elif "Fin" in time:
        moment = -1
    else:
        moment = 0
    print(moment)
    return moment

def get_link(match):
    link = match.get_attribute("id")
    url = f"https://www.soccer24.com/match/{link[4:]}"
    return url

def handling(game):
    match = game.get_attribute("innerHTML")
    soup = BeautifulSoup(match, "html.parser")
    time = soup.select_one("div.event__stage--block").text.strip().split()
    if soup.select_one("div.event__score.event__score--home").text.strip().isdigit() and \
        soup.select_one("div.event__score.event__score--away").text.strip().isdigit():
        score_one = int(soup.select_one("div.event__score.event__score--home").text.strip())
        score_two = int(soup.select_one("div.event__score.event__score--away").text.strip())
    else:
        score_one = 99
        score_two = 99
    if "Finished" in time or "Overtime" in time or "Postponed" in time \
            or "Interrupted" in time or "Awaitingupdates" in time or "Awarded" in time:
        time = ["Fin", "Fin"]
    print(time, score_one,":",score_two)
    return time,score_one,score_two


