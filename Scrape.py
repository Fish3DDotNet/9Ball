# Python program to scrape table from website

# import libraries selenium and time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os
import csv
from time import sleep

div = ''
divno = 0

def login():

    # Create webdriver object
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    # Get the website
    driver.get("https://accounts.poolplayers.com/login")


    # Make Python sleep for some time
    sleep(2)

    email = driver.find_element(By.ID, 'email')
    pw = driver.find_element(By.ID, 'password')
    email.send_keys(".com")
    pw.send_keys("")
    pw.send_keys(Keys.RETURN)

    sleep(2)

    for i in range(3):

        if i == 0:
            np = driver.find_element(By.CLASS_NAME, 'button_button__1lvaa')
        elif i == 1:
            np = driver.find_element(By.LINK_TEXT, 'APA of Spokane')
        elif i == 2:
            np = driver.find_element(By.XPATH, '//*[@id="wrapper"]/div[3]/div[2]/div/div/div[2]/ul/li[3]/a')

        np.send_keys(Keys.RETURN)
        sleep(3)

    return driver

def navtopage(driver,pic):

    if pic == 1:
        ## tuesday double jeopardy 442
        np = driver.find_element(By.XPATH,
                                 '//*[@id="wrapper"]/div[3]/div[2]/div/div/div[2]/div/div/div/div[2]/div/a[4]')
        div = 'Tue Double Jeopardy'
        divno = 442

    elif pic == 2:
        ## Thursday double jeopardy 444
        np = driver.find_element(By.XPATH,
                                 '//*[@id="wrapper"]/div[3]/div[2]/div/div/div[2]/div/div/div/div[4]/div/a[3]')
        div = 'Thurs Double Jeopardy'
        divno = 444

    elif pic == 3:
        ## Sat double jeopardy 444
        np = driver.find_element(By.XPATH,
                                 '//*[@id="wrapper"]/div[3]/div[2]/div/div/div[2]/div/div/div/div[5]/div/a[4]')
        div = 'Sat Double Jeopardy'
        divno = 446

    np.send_keys(Keys.RETURN)

    sleep(3)

    np = driver.find_element(By.XPATH, '//*[@id="wrapper"]/div[3]/div[2]/div/div[2]/div[2]/ul/li[2]/a')

    np.send_keys(Keys.RETURN)


    return div, divno

def getdata(driver,t,div,divno):

    team = driver.find_element(By.XPATH,
                               '//*[@id="wrapper"]/div[3]/div[2]/div/div[2]/div[2]/div/div/div[' + str(
                                   t) + ']/div[1]/h3/a')
    teamname = team.accessible_name[:-5]
    teamno = team.accessible_name[-4:]
    teamno = teamno.replace('(', '').replace(')', '')

    pi = driver.find_elements(By.XPATH,
                                '//*[@id="wrapper"]/div[3]/div[2]/div/div[2]/div[2]/div/div/div['+str(t)+']/div[2]/table/tbody/tr')
    for p in range(len(pi)):

        player = driver.find_element(By.XPATH,
                                 '//*[@id="wrapper"]/div[3]/div[2]/div/div[2]/div[2]/div/div/div['+str(t)+']/div[2]/table/tbody/tr['+str(p+1)+']/td[1]/div[1]')

        playerno = driver.find_element(By.XPATH,
                                 '//*[@id="wrapper"]/div[3]/div[2]/div/div[2]/div[2]/div/div/div['+str(t)+']/div[2]/table/tbody/tr['+str(p+1)+']/td[1]/div[2][text()]')

        playersl = driver.find_element(By.XPATH,
                                 '//*[@id="wrapper"]/div[3]/div[2]/div/div[2]/div[2]/div/div/div['+str(t)+']/div[2]/table/tbody/tr['+str(p+1)+']/td[2]')

        l = str(div + " - " + str(divno)),str(teamno),str(teamname),str(player.text),str(playerno.text[-5:]),str(playersl.text)
        plist.append(l)

        print(str(div) + " - " + str(divno) + "," + str(teamno) + "," + str(teamname) + "," + str(player.text) + "," + str(playerno.text[-5:]) + "," + str(playersl.text))

def iterate(driver,div,divno):
    teams = driver.find_elements(By.XPATH, '//h3')
    for t in range(len(teams)-1):
        getdata(driver,t+1,div,divno)



def processAll(driver):

    for i in range(3):

        div, divno = navtopage(driver,i+1)
        sleep(3)
        iterate(driver,div,divno)

        np = driver.find_element(By.LINK_TEXT, 'APA of Spokane')
        np.send_keys(Keys.RETURN)
        sleep(3)
        np = driver.find_element(By.XPATH, '//*[@id="wrapper"]/div[3]/div[2]/div/div/div[2]/ul/li[3]/a')
        np.send_keys(Keys.RETURN)
        sleep(3)


plist = []

driver = login()
sleep(3)
processAll(driver)



file = open('static/data/teams.txt', 'w+', newline='')

# writing the data into the file
with file:
    write = csv.writer(file)
    write.writerows(plist)
file.close()
