from typing import Text
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
from random import randint

class instagramBot:
    def __init__(self,username,password):
        self.username = username
        self.password = password
        self.bot = webdriver.Chrome(executable_path="E:\code\python\instabot\chromedriver.exe")

    def login(self):
        bot = self.bot
        bot.get('https://www.instagram.com/accounts/login/')
        time.sleep(randint(2,4))

        email=bot.find_element_by_name('username').send_keys(self.username)
        time.sleep(randint(1,2))
        password = bot.find_element_by_name('password').send_keys(self.password)

        time.sleep(randint(1,3))
        bot.find_element_by_name('password').send_keys(Keys.RETURN)
        time.sleep(randint(3,4))

    def findMyFollowers(self):
        bot = self.bot
        
        bot.get('https://instagram.com/'+self.username)
        time.sleep(randint(2,3))
        
        total_follower = bot.find_elements_by_class_name('g47SY')
        # print('total followers >>>>>>>>>>>>>>>>',)
        
        bot.find_element_by_xpath('//*[@href="/'+ self.username+ '/followers/"]').click()
        time.sleep(randint(1,2))

        popup = bot.find_element_by_class_name('isgrP')

        followers_array=[]

        i=1
        while i <= int(total_follower[1].text):
            bot.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight',popup)
            time.sleep(randint(1,2))

            followers = bot.find_elements_by_class_name('FPmhX')
            # print('here is the output >>>>>>>>>>>',followers)
            for follower in followers:
                if follower not in followers_array:
                    followers_array.append(follower.text)
                    i+=1
                if i> int(total_follower[1].text):
                    break
        try:
            prev_follower_df = pd.read_csv('file/follower_list.csv')
            today_followers_df = pd.DataFrame({'followers':followers_array})
            # print('Following earlier >>>>>>>>>>>',prev_follower_df)
            prev_follower_df = prev_follower_df[~prev_follower_df['followers'].isin(today_followers_df['followers'])]
            
            if not prev_follower_df.empty:
                prev_follower_df['followers'].to_csv('file/unfollowers.csv',mode='w')
                print('Unfollowed You >>>>>>>>>>>',prev_follower_df)

            today_followers_df.to_csv('file/follower_list.csv',mode='w')
            print('Updated csv file in /file folder')

        except FileNotFoundError as fnf_error:
            print('check for csv file in /file folder')
            pd.DataFrame({'followers':followers_array}).to_csv('file/follower_list.csv',mode='w')

  

    def unfollow(self):
        bot = self.bot
        try:
            i=0
            tmp_list = []
            follower_df = pd.read_csv('file/unfollowers.csv')
            if not follower_df.empty:
                for item in follower_df['followers']:
                    if item == 'followers':
                        continue
                    bot.get('https://inst:agram.com/'+item)
                    tmp_list.append(item)
                    
                    bot.find_element_by_class_name('_6VtSN').click()
                    time.sleep(randint(1,3))
                    bot.find_element_by_class_name('-Cab_').click()
                    time.sleep(randint(6,7))
                    i+=1
                    if i >=50:
                        break

            unfollowed_df = pd.DataFrame({'followers':tmp_list})
            follower_df = follower_df[~follower_df['followers'].isin(unfollowed_df['followers'])]
            follower_df['followers'].to_csv('file/unfollowers.csv',mode='w')
            if not unfollowed_df['followers'].empty:
                print('Unfollowed {} people in list below',i+1)
                print(unfollowed_df['followers'])
            else:
                print('No unfollowers')
        except FileNotFoundError as err:
            print('Unfollower file missing >>>>',err)



insta = instagramBot('Your_username','YOUR_PASSWORD')
insta.login()
time.sleep(randint(3,4))
insta.findMyFollowers()
if input('want to unfollow who unfollowed you.--> yes/no') == 'yes':
    insta.unfollow()
else:
    print('Why you wasted my time')

insta.bot.close()
