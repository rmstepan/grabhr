import os
import re
import urllib2
import urllib
import time
import json
from bs4 import BeautifulSoup
from selenium import webdriver

global keyword, driver , header , directory
PexelsUrls,FlickrUrls,GoogleUrls  = [],[],[]

rate  = 10
index = 0
driver = webdriver.PhantomJS()
header = {
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"
         }


def showInfo():
    print "#script >> Welcome to image downloader"
    print "#script >> Press CTRL+C anytime if you want to stop the download"
    print "\n\n"

def prepare():
    global keyword,directory,rate
    keyword = raw_input("#script >> Enter a keyword: ")
    rate    = int(raw_input("#script >> Enter a rate of download (eg. rate 10 ~ 500 pictures): "))
    directory = keyword
    if not os.path.exists(directory):
        os.mkdir(directory)
        print "#script >> Successfully created directory with name '"+directory+"'"

def pexelGrab(driver,header,rate):
    global index
    keyword.replace(" ","%20")
    driver.get("https://www.pexels.com/search/" + keyword + "/")
    for i in range(1,rate):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
    html_source = driver.page_source
    soup = BeautifulSoup(html_source,"html.parser")
    global PexelsUrls

    for line in soup.find_all('img', {'height': 350}, Limit=None):
        line = str(line)

        start = re.search(r"[^a-zA-Z](src=)[^a-zA-Z]", line).start(1) + 5
        line = line[start:]

        end = re.search(r"[^a-zA-Z](h=350&amp)[^a-zA-Z]", line).start(1) - 1
        line = line[:end]
        type = line[line.rfind('.'):]
        line = line + "?w=1280&h=1024"

        PexelsUrls.append((line, type))


def flickrGrab(driver,header,rate):
    global index
    keyword.replace(" ", "%20")
    driver.get("https://www.flickr.com/search/?text=" + keyword + "/")
    for i in range(1, rate):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
    html_source = driver.page_source
    soup = BeautifulSoup(html_source, "html.parser")
    global FlickrUrls

    for line in soup.find_all('div', {'class': 'photo-list-photo-view'}, Limit=None):
        try:
            line = str(line)

            start = re.search(r"[^a-zA-Z](url)[^a-zA-Z]", line).start(1) + 4
            line = line[start:]

            end = re.search(r"[^a-zA-Z](jpg)[^a-zA-Z]", line).start(1)+3
            line = line[:end]
            type = line[line.rfind('.'):]
            line = line[:-6]+"_b"+type
            firstC = re.search(r"[^a-zA-Z](c)[^a-zA-Z]", line).start(1)
            line = "https://" + line[firstC:]
            FlickrUrls.append((line,type))
        except Exception as e:
            pass

def googleGrab(header):
    global index,keyword
    #keyword.replace(" ", "%20")
    keyword = urllib.quote(keyword)
    url = "https://www.google.com/search?q=%s&source=lnms&tbm=isch&biw=1280&bih=1024" % keyword
    soup = BeautifulSoup(urllib2.urlopen(urllib2.Request(url,headers=header)),"html.parser")
    global GoogleUrls

    for line in soup.find_all("div",{"class":"rg_meta"}):
        link, type, width , height = json.loads(line.text)["ou"], json.loads(line.text)["ity"],\
        json.loads(line.text)["ow"],json.loads(line.text)["oh"]
        if width>=900 and height>=700:
            GoogleUrls.append((link, type))

def savePics():
    global index
    total = 0
    total += len(PexelsUrls)
    total += len(FlickrUrls)
    total += len(GoogleUrls)

    for i, (line, type) in enumerate(PexelsUrls):
        try:
            os.system("cls")
            showInfo()
            print "#script >> Saved " + str(index) + " photos out of " + str(total) + " ..."
            index += 1
            req = urllib2.Request(line, headers={'User-Agent': header})
            raw_img = urllib2.urlopen(req).read()

            f = open(os.path.join(directory, "img" + "_" + str(index) + type), 'wb')

            f.write(raw_img)
            f.close()
        except Exception as e:
            print "could not load : " + str(i)
            print e


    for i, (line, type) in enumerate(FlickrUrls):
        try:
            os.system("cls")
            showInfo()
            print "#script >> Saved " + str(index) + " photos out of " + str(total) + " ..."
            index += 1
            req = urllib2.Request(line, headers={'User-Agent': header})
            raw_img = urllib2.urlopen(req).read()

            f = open(os.path.join(directory, "img" + "_" + str(index) + type), 'wb')

            f.write(raw_img)
            f.close()
        except Exception as e:
            print "could not load : " + str(i)
            print e


    for i, (line, type) in enumerate(GoogleUrls):
        try:
            os.system("cls")
            showInfo()
            print "#script >> Saved " + str(index) + " photos out of " + str(total) + " ..."
            index += 1
            req = urllib2.Request(line, headers={'User-Agent': header})
            raw_img = urllib2.urlopen(req).read()

            f = open(os.path.join(directory, "img" + "_" + str(index) + "." + type), 'wb')

            f.write(raw_img)
            f.close()
        except Exception as e:
            print "could not load : " + str(i)
            print e



showInfo()
prepare()
print "#script >> Loading webpages..."
pexelGrab(driver,header,rate)
flickrGrab(driver,header,rate)
googleGrab(header)
savePics()
print "#script >> Download complete!"
print "#script >> Exiting..."

driver.close()

