# Python program to scrape table from website

# import libraries selenium and time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from time import sleep

def login():

    # Create webdriver object
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    # Get the website
    driver.get("https://accounts.poolplayers.com/login")


    # Make Python sleep for some time
    sleep(2)

    email = driver.find_element(By.ID, 'email')
    pw = driver.find_element(By.ID, 'password')
    email.send_keys("@gmail.com")
    pw.send_keys("")
    pw.send_keys(Keys.RETURN)

    sleep(2)
    return driver

def navtopage(driver):

    for i in range(5):

        if i == 0:
            np = driver.find_element(By.CLASS_NAME, 'button_button__1lvaa')
        elif i == 1:
            np = driver.find_element(By.LINK_TEXT, 'APA of Spokane')
        elif i == 2:
            np = driver.find_element(By.XPATH, '//*[@id="wrapper"]/div[3]/div[2]/div/div/div[2]/ul/li[3]/a')
        elif i == 3:
            np = driver.find_element(By.XPATH,
                                     '//*[@id="wrapper"]/div[3]/div[2]/div/div/div[2]/div/div/div/div[2]/div/a[4]')
            sleep(3)
            pi = driver.find_elements(By.XPATH, '//h4')
            for i in range(len(pi)):
                print(pi[i].accessible_name)
            print("")

        elif i == 4:
            np = driver.find_element(By.XPATH, '//*[@id="wrapper"]/div[3]/div[2]/div/div[2]/div[2]/ul/li[2]/a')

        np.send_keys(Keys.RETURN)
        sleep(3)
    pi = driver.find_element(By.XPATH,  '//*[@id="wrapper"]/div[3]/div[2]/div/div[1]/div/div/h4/span[text()]')
    print("")
    print(pi.text)

def getdata(driver,t):

    # np = driver.find_elements(By.XPATH, '//h3')
    # for i in  range(len(np)):
    #     print(np[i].accessible_name)
    pi = driver.find_elements(By.XPATH,
                                '//*[@id="wrapper"]/div[3]/div[2]/div/div[2]/div[2]/div/div/div['+str(t)+']/div[2]/table/tbody/tr')
    for p in range(len(pi)):

        team = driver.find_element(By.XPATH,
                                    '//*[@id="wrapper"]/div[3]/div[2]/div/div[2]/div[2]/div/div/div['+str(t)+']/div[1]/h3/a')
        teamname = team.accessible_name[:-5]
        teamno = team.accessible_name[-4:]
        teamno = teamno.replace('(', '').replace(')','')


        player = driver.find_element(By.XPATH,
                                 '//*[@id="wrapper"]/div[3]/div[2]/div/div[2]/div[2]/div/div/div['+str(t)+']/div[2]/table/tbody/tr['+str(p+1)+']/td[1]/div[1]')
        #print(player.text)

        playerno = driver.find_element(By.XPATH,
                                 '//*[@id="wrapper"]/div[3]/div[2]/div/div[2]/div[2]/div/div/div['+str(t)+']/div[2]/table/tbody/tr['+str(p+1)+']/td[1]/div[2][text()]')
        #print(playerno.text[-5:])

        playersl = driver.find_element(By.XPATH,
                                 '//*[@id="wrapper"]/div[3]/div[2]/div/div[2]/div[2]/div/div/div['+str(t)+']/div[2]/table/tbody/tr['+str(p+1)+']/td[2]')
        #print(playersl.text)

        print(teamno + " - " + teamname + " - " + player.text + " - " + playerno.text + " - " + playersl.text)
def iterate(driver):
    teams = driver.find_elements(By.XPATH, '//h3')
    for t in range(len(teams)-1):
        getdata(driver,t+1)



driver = login()
sleep(3)
navtopage(driver)
sleep(3)
iterate(driver)
# getdata()
# sleep(10)
#
# sleep(3)
#
#
# np = driver.find_element(By.XPATH, '//*[@id="wrapper"]/div[3]/div[2]/div/div[2]/div[2]/div/div/section/select/option[13]')
# np.send_keys(Keys.RETURN)
#
# print('hold')

#
# np = driver.find_elements(By.XPATH, '//h3')
# for i in  range(len(np)):
#     print(np[i].accessible_name)
#
# APA of Spokane
# 1 Ball @ A Time�(01)
# Hit A Rail�(02)
# Rack n Roll�(03)
# No Fair Aiming�(04)
# Motley Crew�(05)
# H82LOSE�(06)
# Were Solids.... Right?�(07)
# Chevelles�(08)
# Just For The Fun�(09)
# Stick it 2 Em!�(10)
# Shameless�(11)
# Rocky Blasters�(12)
#
# np = driver.find_element(By.XPATH, '//*[@id="wrapper"]/div[3]/div[2]/div/div[2]/div[2]/div/div/div[1]/div[2]/table/tbody/tr[1]/td[1]/div[1]')
# np = driver.find_element(By.XPATH, '//*[@id="wrapper"]/div[3]/div[2]/div/div[2]/div[2]/div/div/div[1]/div[2]/table/tbody/tr[2]/td[1]/div[1]')
# Next team
# np = driver.find_element(By.XPATH, '//*[@id="wrapper"]/div[3]/div[2]/div/div[2]/div[2]/div/div/div[2]/div[2]/table/tbody/tr[1]/td[1]/div[1]')
# print(np.text)
# Mitchell Andrews
#
# np = driver.find_element(By.XPATH, '//*[@id="wrapper"]/div[3]/div[2]/div/div[2]/div[2]/div/div/div[1]/div[2]/table/tbody/tr[1]/td[1]/div[2][text()]')
# print(np.text)
# #94612717
#
# np = driver.find_element(By.XPATH, '//*[@id="wrapper"]/div[3]/div[2]/div/div[2]/div[2]/div/div/div[1]/div[2]/table/tbody/tr[1]/td[2]')
# print(np.text)
# 8
#
