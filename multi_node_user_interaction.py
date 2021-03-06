from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
import sqlite3 as sq
from threading import Thread
from multiprocessing import Process
import logging

def node(userdata):
    '''simulates a users sequence of actions'''
    user=artificial_user()
    logdata={userdata[0]:dict()}
    logdata[userdata[0]]['test at']=time.ctime()
    logdata[userdata[0]]['login page load time']=user.login(userdata)
    logdata[userdata[0]]['home page load time']=user.go_home()
    logdata[userdata[0]]['writing code test time']=user.write_code_test()
    user.logout()
    logging.info(str(logdata))

def get_user_data():
    '''Fetches username and password from the database and returns as a list of tuples.'''
    f=open('namelist','r')
    userlist=list(map(lambda x:(x,'abc123'),f.read().split('\n')[:-1]))
    return userlist

class artificial_user:
    web ='a webdriver object will replace this text' 
    user=tuple()
    tests=[]
    links=set()
    def __init__(self):
        #self.web = webdriver.Chrome('/Users/ssvighnesh/chromedriver')
        self.web = webdriver.Remote(command_executor='http://127.0.0.1:4444/wd/hub',desired_capabilities={'browserName':'firefox','javascriptEnabled': True})
    def login(self,user):
        self.user=user
        start_time=time.time()
        self.web.get('http://ec2-52-66-12-101.ap-south-1.compute.amazonaws.com/student/login')
        stop_time=time.time()
        print('login page')
        username=self.web.find_element_by_xpath('//*[@id="email"]')
        username.send_keys(user[0])
        password=self.web.find_element_by_xpath('//*[@id="password"]')
        password.send_keys(user[1])
        log=self.web.find_element_by_name('student_login')
        log.click()
        return stop_time - start_time
    def get_links(self,page):
        '''Scrape all the links in the webpage'''
        self.web.get(page)
        elems = self.web.find_elements_by_xpath("//a[@href]")
        for elem in elems:
            link=elem.get_attribute("href")
            if 'Logout' not in link:
                self.links.add(link)
    def visit(self):
        ''' Visits all the links present in the links list'''

        for link in self.links:
           self.web.get(link)
    def logout(self):
        try:
            logout=self.web.find_element_by_link_text('Logout')
        except:
            self.web.close()
        else:
            logout.click()
            self.web.close()
    def go_home(self):
        start_time=time.time()
        self.web.get('http://ec2-52-66-12-101.ap-south-1.compute.amazonaws.com/student/student-home-page/')
        print('homepage')
        return time.time() - start_time
    def roam(self):
        '''Modify this to a specific users action sequence.'''
        start_time=time.time()
        try:
            self.go_home()
            self.get_links(self.web.current_url)
            self.visit()
            return time.time() - start_time
        except Exception as E:
            print(E)
            self.web.close()
    def write_code_test(self):
        self.web.get('http://ec2-52-66-12-101.ap-south-1.compute.amazonaws.com/code-test/list-code-test-sch/0/')
        self.tests=self.web.find_elements_by_link_text('Take this test')
        test=self.tests[-1]
        test.click()
        '''
        Input=self.web.find_element_by_id('input')
        Input.clear()
        Input.send_keys('input')
        Output=self.web.find_element_by_id('output')
        Output.clear()
        Output.send_keys('output')
        Processing=self.web.find_element_by_id('processing-involved')
        Processing.clear()
        Processing.send_keys('processing')
        Alternative=self.web.find_element_by_id('alternatives')
        Alternative.clear()
        Alternative.send_keys('Alternative')
        Algo=self.web.find_element_by_id('algorithm')
        Algo.clear()
        Algo.send_keys('algorithm and pseudo')
        '''
        self.web.find_element_by_xpath("//select[@id='ace-mode']/option[text()='C']").click()

        code=r'#include<stdio.h> \r\n void main(){int a=5; printf(\"%d\",a);}'
        scr='''
        var editor= ace.edit("editor");
        editor.setValue(" '''+code+''' ");
        '''
        self.web.execute_script(scr)
        run_code=self.web.find_element_by_id('run-code')
        run_code.click()
        start_time=time.time()
        while self.web.find_element_by_id('result').text == '':
            time.sleep(0.001)
        stop_time=time.time() 
        pause=self.web.find_element_by_id('pause-test')
        pause.click()
        print('code test done ')
        return stop_time - start_time


logging.basicConfig(filename='logdata',level=logging.INFO,format='%(message)s')
logging.info('#')
if __name__ == '__main__':
    thread_list=[]
    userlist=get_user_data()
    n=int(input('enter the number of users:'))
    for userdata in userlist[:n]:

        print(userdata)
        t=Thread(target=node,args=[userdata])
        thread_list.append(t)
        t.start()

# print(*thread_list,sep='\n')
# get_links('http://ec2-52-66-12-101.ap-south-1.compute.amazonaws.com/code-test/list-code-test-sch/0/')
# web.get('http://ec2-52-66-12-101.ap-south-1.compute.amazonaws.com/student/change-profile-info-stud/')
