from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from functools import reduce
from time import sleep
from send import bet_siska




def check_link(url,score_one,score_two,checker,time):
    caps = DesiredCapabilities().CHROME
    caps["pageLoadStrategy"] = "eager"
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    browser = webdriver.Chrome(desired_capabilities=caps,options = options)
    browser.get(url)
    browser.implicitly_wait(1)
    team_home = browser.find_elements(By.CSS_SELECTOR, "a.participant__participantName")[0].get_attribute(
            "href") + "results/"
    sleep(1)
    team_away = browser.find_elements(By.CSS_SELECTOR, "a.participant__participantName")[1].get_attribute(
            "href") + "results/"
    sleep(1)
    title = browser.find_element(By.CSS_SELECTOR, ".tournamentHeader__country").text

    print(title)


    def separator(matches):
        match_list = list()
        for i in matches:
            line = i.text
            # print(line)
            if "Awrd" in line or "Abn" in line:
                continue
            match_list.append(line.split())
        return match_list

    def get_data(browser,link):
        browser.get(link)
        dataset = browser.find_elements(By.CSS_SELECTOR, "[id^='g_1']")
        matches = separator(dataset)
        team = browser.find_element(By.CSS_SELECTOR, "div.heading__name").get_attribute("innerHTML")
        return matches,team


    def forming(browser, link1, link2):  # NEED ADD TYPE SPORT AND FIXABLE CSS SELECTOR
        match_list_home, team1 = get_data(browser,link1)
        match_list_away, team2 = get_data(browser,link2)
        return match_list_home, match_list_away, team1, team2

    games = forming(browser, team_home, team_away)

    team1_results = games[0]
    team2_results = games[1]
    team1_name = games[2].split()
    team2_name = games[3].split()

    print(team1_name, team2_name)


    def separation_home_away(team_, all_matches):
        home_matches = list()
        away_matches = list()
        waste = ["W", "U18", "U20", "U21", "U23"]  # WASTE - U20 and another juniors and woman champs//
        for i in waste:
            if i in team_:
                team_ = [j for j in team_ if j not in waste]
        # print(team_)
        for k in all_matches:
            i = [j for j in k[:len(k) - 1] if j not in waste] + k[-1:]
            x = i.index(team_[len(team_) - 1])
            if i[x + 1].isdigit():
                away_matches.append(i)
            elif "(" in i[x + 1] and i[x + 2].isdigit():
                away_matches.append(i)
            else:
                home_matches.append(i)
        return home_matches, away_matches

    team1_home, team1_away = separation_home_away(team1_name, games[0])
    team2_home, team2_away = separation_home_away(team2_name, games[1])

    def get_scores(results):
        scorelines = []

        for match in results:
            scoreline = None
            # print(match)
            if "Pen" in match or "AET" in match:
                scoreline = match[-7:-1]
            if '(' in match[-2]:
                scoreline = match[-5:-1]
            if match[-2].isdigit() and match[-3].isdigit() and match[-4].isdigit()==False and "Pen" not in match and "AET" not in match:
                scoreline= match[-3:-1]
            if scoreline == None:
                continue
            scorelines.append(scoreline)
        return scorelines

    team1_results_home = get_scores(team1_home)
    team1_results_away = get_scores(team1_away)
    team2_results_home = get_scores(team2_home)
    team2_results_away = get_scores(team2_away)
    print("Before total")

    def total_scored(scores):
        total_one, total_more = 0, 0
        count = len(scores)

        for data in scores:

            if 2 <= len(data) <= 4:
                if (int(data[0]) + int(data[1]))>=1:
                    total_one += 1
                    if (int(data[0]) + int(data[1]))>1:
                        total_more += 1
            else:
                if (int(data[-1]) + int(data[-2])) >= 1:
                    total_one += 1
                    if (int(data[-1]) + int(data[-2])) > 1:
                        total_more += 1

        if count > 14:
            both_one = round(total_one * 100/count, 1)
            both_more = round(total_more * 100 / count, 1)
            return both_one, both_more
        else:
            return 0, 0

    def calc_team_scoring_home(scores):
        scored_one = 0
        scored_more = 0
        count = len(scores)
        for data in scores:
            if 2<=len(data) <= 4:
                if int(data[0]) >= 1:
                    scored_one += 1
                    if int(data[0]) > 1:
                        scored_more += 1

            else:
                if int(data[-2]) >= 1:
                    scored_one += 1
                    if int(data[-2]) > 1:
                        scored_more += 1

        if count > 14:
            goal_one = round(scored_one * 100/count, 1)
            goal_more = round(scored_more * 100/count, 1)
            return goal_one, goal_more
        else:
            return 0, 0

    def calc_team_scoring_away(scores):
        scored_one = 0
        scored_more = 0
        count = len(scores)
        for data in scores:
            if 2<=len(data) <= 4:
                if int(data[1]) >= 1:
                    scored_one += 1
                    if int(data[1]) > 1:
                        scored_more += 1


            else:
                if int(data[-1]) >= 1:
                    scored_one += 1
                    if int(data[-1]) > 1:
                        scored_more += 1

        if count > 14:
            goal_one = round(scored_one * 100/count, 1)
            goal_more = round(scored_more * 100/count, 1)
            return goal_one, goal_more
        else:
            return 0, 0

    def calc_team_conceded_home(scores):
        conceded_one = 0
        conceded_more = 0
        count = len(scores)
        for data in scores:
            if 2<=len(data) <= 4:
                if int(data[1]) >= 1:
                    conceded_one += 1
                    if int(data[1]) > 1:
                        conceded_more += 1

            else:
                if int(data[-1]) >= 1:
                    conceded_one += 1
                    if int(data[-1]) > 1:
                        conceded_more += 1

        if count > 14:
            goal_one = round(conceded_one * 100/count, 1)
            goal_more = round(conceded_more * 100/count, 1)
            return goal_one, goal_more
        else:
            return 0, 0

    def calc_team_conceded_away(scores):
        conceded_one = 0
        conceded_more = 0
        count = len(scores)
        for data in scores:
            if 2<=len(data) <= 4:
                if int(data[0]) >= 1:
                    conceded_one += 1
                    if int(data[0]) > 1:
                        conceded_more += 1

            else:
                if int(data[-2]) >= 1:
                    conceded_one += 1
                    if int(data[-2]) > 1:
                        conceded_more += 1

        if count > 14:
            goal_one = round(conceded_one * 100/count, 1)
            goal_more = round(conceded_more * 100/count, 1)
            return goal_one, goal_more
        else:
            return 0, 0




    team1_scoring_home = calc_team_scoring_home(team1_results_home)
    team1_scoring_away = calc_team_scoring_away(team1_results_away)
    team2_scoring_home = calc_team_scoring_home(team2_results_home)
    team2_scoring_away = calc_team_scoring_away(team2_results_away)

    team1_conceding_home = calc_team_conceded_home(team1_results_home)
    team1_conceding_away = calc_team_conceded_away(team1_results_away)
    team2_conceding_home = calc_team_conceded_home(team2_results_home)
    team2_conceding_away = calc_team_conceded_away(team2_results_away)

    team1_total_home = total_scored(team1_results_home)
    team1_total_away = total_scored(team1_results_away)
    team2_total_home = total_scored(team2_results_home)
    team2_total_away = total_scored(team2_results_away)

    info_totalOne = f'<{team1_total_home[0]}%> {team1_total_away[0]}% {team2_total_home[0]}% <{team2_total_away[0]}%>'
    info_totalMore = f'<{team1_total_home[1]}%> {team1_total_away[1]}% {team2_total_home[1]}% <{team2_total_away[1]}%>'

    info_ind_t1One = f'<{team1_scoring_home[0]}%> {team1_scoring_away[0]}% {team2_conceding_home[0]}% <{team2_conceding_away[0]}%>'
    info_ind_t1More = f'<{team1_scoring_home[1]}%> {team1_scoring_away[1]}% {team2_conceding_home[1]}% <{team2_conceding_away[1]}%>'

    info_ind_t2One = f'<{team2_scoring_away[0]}%> {team2_scoring_home[0]}% {team1_conceding_away[0]}% <{team1_conceding_home[0]}%>'
    info_ind_t2More = f'<{team2_scoring_away[1]}%> {team2_scoring_home[1]}% {team1_conceding_away[1]}% <{team1_conceding_home[1]}%>'



    def condition_ind_team1_oneGoal(data1_h,data1_a,data2_h,data2_a):
        if (data1_h[0] > 90 and data1_a[0] >80) and (data2_a[0] > 90 and data2_h[0]>80):
             return True
        if data1_h[0]>95 and data2_a[0]> 95:
            return True
        if data1_h[0] + data1_a[0] > 180 and data2_h[0] + data2_a[0] > 180:
            return True

    def condition_ind_team1_moreGoal(data1_h,data1_a,data2_h,data2_a):
        if data1_h[1] > 75 and data2_a[1] > 75:
            return True
        if data1_h[1] > 80 and data2_a[1]> 70:
            return True
        if data1_h[1]>85 and data2_a[1]> 65:
            return True
        if data1_h[1] + data1_a[1] > 160 and data2_h[1] + data2_a[1] > 150:
            return True

    def condition_ind_team2_oneGoal(data2_a, data2_h, data1_a, data1_h):
        if (data2_a[0] > 90 and data2_h[0]>80) and (data1_h[0] > 90 and data1_a >80):
            return True
        if data2_a[0] > 95 and data1_h[0] > 95:
            return True
        if data2_h[1] + data2_a[1]  > 180 and data1_h[1] + data1_a[1] > 180:
            return True

    def condition_ind_team2_moreGoal(data2_a, data2_h, data1_a, data1_h):
        if data2_a[1] > 75 and data1_h[1] > 75:
            return True
        if data2_a[1] > 80 and data1_h[1] > 70:
            return True
        if data2_a[1] > 85 and data1_h[1] > 65:
            return True
        if data2_h[1] + data2_a[1] > 160 and data1_h[1] + data1_a[1] > 150:
            return True

    def condition_total_one(data1_h,data1_a,data2_h,data2_a):
        if data1_h[0]>99 and data2_a[0]>99:
            if data1_a[0]>=95 and data2_h[0]>=95:
                return True


    def sub_condition_05(data1_h,data1_a,data2_h,data2_a):
        if data1_h[0]>=75 and data1_a[0]>=75:
            if data2_a[0]>=75 and data2_h[0]>=75:
                return True

    def condition_total_more(data1_h,data1_a,data2_h,data2_a):
        if data1_h[1]>=90 and data2_a[1]>=90:
            if data1_a[0]>=80 and data2_h[0]>=80:
                return True
        if data1_h[1] + data1_a[1]>=180:
            if data2_h[1] + data2_a[1]>=170:
                return True

    team1_scoreOne = condition_ind_team1_oneGoal(team1_scoring_home,team1_scoring_away,team2_conceding_home,team2_conceding_away)
    team1_scoreMore = condition_ind_team1_moreGoal(team1_scoring_home,team1_scoring_away,team2_conceding_home,team2_conceding_away)
    team2_scoreOne = condition_ind_team1_oneGoal(team2_scoring_away,team2_scoring_home,team1_conceding_away,team1_conceding_home)
    team2_scoreMore = condition_ind_team1_moreGoal(team2_scoring_away,team2_scoring_home,team1_conceding_away,team1_conceding_home)
    bothTotal_one = condition_total_one(team1_total_home,team1_total_away,team2_total_home,team2_total_away)
    bothTotal_more = condition_total_more(team1_total_home, team1_total_away, team2_total_home, team2_total_away)
    sub_condition_home = sub_condition_05(team1_scoring_home,team1_scoring_away,team2_conceding_home,team2_conceding_away)
    sub_condition_away = sub_condition_05(team2_scoring_home,team2_scoring_away,team1_conceding_home,team1_conceding_away)

    print("Condition1 - 1",team1_scoreOne, info_ind_t1One)
    print("Condition1 - more", team1_scoreMore, info_ind_t1More)
    print("Condition2 - 1",team2_scoreOne, info_ind_t2One)
    print("Condition2 - more", team2_scoreMore, info_ind_t2More)
    print("Condition both - 1",bothTotal_one, info_totalOne)
    print("Condition both - more", bothTotal_more,info_totalMore)
    if team1_scoreOne == True or team1_scoreMore == True or team2_scoreOne == True or team2_scoreMore == True \
        or bothTotal_one == True or bothTotal_more == True:
        print(url)

    current_score = f'{score_one}:{score_two}'

    if checker == 1 and bothTotal_one == True:
        bet = (title,"TIME: "+str(time),"SCORE: "+current_score, ' '.join(map(str,team1_name)),' '.join(map(str,team2_name)),
               "||| TOTAL OVER 0.5 NON CERTAIN |||",
               "COMMON:: " + info_totalOne,
               "1TEAM     :: " + info_ind_t1One,
               "2TEAM     :: " + info_ind_t2One
               )

        bet_siska(bet)

    if checker == 1 and bothTotal_one == True:
        if sub_condition_home == True and sub_condition_away == True:
            bet = (title,"TIME: "+str(time),"SCORE: "+current_score, ' '.join(map(str,team1_name)),' '.join(map(str,team2_name)),
                   "||| TOTAL OVER 0.5   %75% TRUE |||",
                   "COMMON:: " + info_totalOne,
                   "1TEAM     :: " + info_ind_t1One,
                   "2TEAM     :: " + info_ind_t2One
                   )

            bet_siska(bet)


    if checker == 11 and team1_scoreOne == True:
        bet = (title,"TIME: "+str(time),"SCORE: "+current_score, ' '.join(map(str,team1_name)),' '.join(map(str,team2_name)),
               "||| TEAM1 OVER 0.5 |||",
               "1TEAM 0.5 :: " + info_ind_t1One,
               "2TEAM 0.5 :: " + info_ind_t2One
               )

        bet_siska(bet)

    if checker == 21 and team2_scoreOne == True:
        bet = (title,"TIME: "+str(time),"SCORE: "+current_score, ' '.join(map(str,team1_name)),' '.join(map(str,team2_name)),
               "||| TEAM2 OVER 0.5 |||",
               "2TEAM 0.5 :: " + info_ind_t2One,
               "1TEAM 0.5 :: " + info_ind_t1One
               )

        bet_siska(bet)

    if checker == 15 and bothTotal_more == True:
        bet = (title,"TIME: "+str(time),"SCORE: "+current_score, ' '.join(map(str,team1_name)),' '.join(map(str,team2_name)),
               "||| TOTAL OVER 1.5 |||",
               "COMMON:: " + info_totalMore,
               "1TEAM 0.5 :: " + info_ind_t1One,
               "2TEAM 0.5 :: " + info_ind_t2One,
               "1TEAM 1.5 :: " + info_ind_t1More,
               "2TEAM 1.5 :: " + info_ind_t2More,
               )
        bet_siska(bet)

    if checker == 12 and team1_scoreMore == True:
        bet = (title,"TIME: "+str(time),"SCORE: "+current_score, ' '.join(map(str,team1_name)),' '.join(map(str,team2_name)),
               "||| TEAM1 OVER 1.5 |||",
               "COMMON:: " + info_totalMore,
               "1TEAM 1.5 :: " + info_ind_t1More,
               "2TEAM 1.5 :: " + info_ind_t2More,
               )
        bet_siska(bet)

    if checker == 22 and team2_scoreMore == True:
        bet = (title,"TIME: "+str(time),"SCORE: "+current_score, ' '.join(map(str,team1_name)),' '.join(map(str,team2_name)),
               "||| TEAM2 OVER 1.5 |||",
               "COMMON:: " + info_totalMore,
               "2TEAM 1.5 :: " + info_ind_t2More,
               "1TEAM 1.5 :: " + info_ind_t1More

               )
        bet_siska(bet)