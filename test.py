from scan import current_moment,get_link,handling
from parsing import check_link
from selenium import webdriver
from selenium.webdriver.common.by import By

from time import sleep
from datetime import datetime
from send import errormsg,any_mistakes

options = webdriver.ChromeOptions()
options.add_argument('--mute-audio')
browser = webdriver.Chrome(options=options)

browser.get("https://www.soccer24.com/")

switch_to_live = browser.find_element(By.CSS_SELECTOR, "div.filters__tab:nth-child(2) > div:nth-child(2)")
switch_to_live.click()
sleep(1)
scan_list = set()
t1_one = set()
t1_more = set()
t2_one = set()
t2_more = set()
scan_list2 = set()
try:
    while True:
        try:
            matches = browser.find_elements(By.CSS_SELECTOR,"[id^='g_1']")
            for i in matches:
                time,score_one,score_two = handling(i)
                moment = current_moment(time)
                if moment >= 55 and score_one+score_two == 0 :
                    link = get_link(i)
                    checker = 1
                    if link in scan_list:
                        continue
                    scan_list.add(link)
                    check_link(link,score_one,score_two,checker,moment)

                if moment >= 30 and score_one == 0:
                    link1 = get_link(i)
                    checker = 11
                    if link1 in t1_one:
                        continue
                    t1_one.add(link1)
                    check_link(link1,score_one,score_two,checker,moment)

                if moment >= 30 and score_two == 0:
                    link2 = get_link(i)
                    checker = 21
                    if link2 in t2_one:
                        continue
                    t2_one.add(link2)
                    check_link(link2,score_one,score_two,checker,moment)

                if moment >= 55 and score_one+score_two <= 1:
                    link3 = get_link(i)
                    checker = 15
                    if link3 in scan_list2:
                        continue
                    scan_list2.add(link3)
                    check_link(link3,score_one,score_two,checker,moment)


                if moment >= 55 and score_one == 1:
                    link4 = get_link(i)
                    checker = 12
                    if link4 in t1_more:
                        continue
                    t1_more.add(link4)
                    check_link(link4,score_one,score_two,checker,moment)

                if moment >= 55 and score_two == 1:
                    link5 = get_link(i)
                    checker = 22
                    if link5 in t2_more:
                        continue
                    t2_more.add(link5)
                    check_link(link5,score_one,score_two,checker,moment)





            print(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
            sleep(45)
        except Exception as mist:
            
            print(mist)
            sleep(1)
            pass

finally:
    errormsg()
