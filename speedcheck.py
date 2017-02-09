from multiprocessing import Queue
from threading import Thread
from splinter import Browser
from datetime import datetime

import re
import sys
import time

filename = 'results_'+datetime.now().strftime("%Y-%m-%d")
 
f = open(filename,'w')
f.write("Street, City, State, Zip, Speed\n")
f.close()
 
e = open('bad_addresses','w')
e.close()

state = 'TX'

def test(street, city, zip):
        try_again = True
        while (try_again):
                try:
                    f = open(filename,'a')
                    browser = Browser('chrome')
                    url = "https://www.att.com/shop/unified/availability.html"
                    browser.visit(url)
                    browser.find_by_id('streetaddress').fill(street)
                    browser.find_by_id('zipcode').fill(zip)
                    browser.find_by_xpath('//*[@id="content"]/div/div[2]/div[1]/div/div/div/form/div[2]/input').first.click()
                    if browser.is_text_present('your home qualifies for AT&T Fiber', wait_time=10):
                        speed = '1000'
                    elif browser.is_text_present('You can get AT&T Fiber at your home', wait_time=10):
                        speed = '1000'
                    elif browser.is_text_present('Mbps', wait_time=10):
                        element = browser.find_by_xpath('//*[@id="content"]/div/div[1]/div[5]/div[1]/div/div[2]/div[2]/div/span/div/div[2]/p[1]/span')
                        speed = re.search("(\d+)",element.text).group(0)
                    else:
                        speed = '0'
                    print (street+', '+city+', '+state+', '+zip+', '+speed)
                    f.write(street+', '+city+', '+state+', '+zip+', '+speed+'\n')
                    browser.quit()
                    try_again=False
                    f.close()
                except:
                    try_again=False
                    e = open('bad_addresses','a')
                    e.write(street+', '+city+', '+state+' '+zip+'\n')
                    e.close()
                    browser.quit()
               
def run_test(i):
    i = i.strip()
    street = i.split(',')[0]
    city = i.split(',')[1]
    zip = i.split(',')[2]
    test(street, city, zip)

def do_stuff(q):
    while True:
        run_test(q.get())
 
q = Queue(maxsize=0)
num_threads = 5
 
for i in range(num_threads):
    worker = Thread(target=do_stuff, args=(q,))
    worker.setDaemon(True)
    worker.start()
 
houses = open('addresses','r')
 
for x in houses.readlines():
    q.put(x)
 