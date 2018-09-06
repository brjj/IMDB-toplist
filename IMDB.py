from urllib.request import urlopen;
from bs4 import BeautifulSoup;
import pickle
import codecs
import time
import sys
from datetime import datetime;
import os


def isEmpty(text):
    alphabet = "abcdefghijklmnopqrstuvwxyzåäö"
    numbers = "1234567890"
    for l in alphabet:
        if(l in text or l.upper() in text):
            return False
    for i in numbers:
        if(i in text):
            return False
    return True
def saveFile(dataList, filename):
    try:
        with open(filename, "wb") as output:
            pickle.dump(dataList, output, pickle.HIGHEST_PROTOCOL);
    except:
        print("Couldn't save file.")

def loadFile(filename):
    if(not os.path.exists(filename)):
        return -1;
    try:
        with open(filename, "rb") as inp:
            file = pickle.load(inp);
        return file;
    except:
        print("Couldn't load file.")
        
def gatherData(url, filename):
    try:
        r = urlopen(url)
        data = r.read()
        soup = BeautifulSoup(data, "html.parser")
    except:
        print("Could not fetch the site.")
        return

    table = soup.find("table")

    x = 0
    arr= []
    for row in table.findAll("tr"):
        if x == 0:
            x +=1
            continue
        tmp = row.find("td", attrs={"class": "titleColumn"})
        name = tmp.find("a").next
        year = tmp.find("a").next.next.next.text.strip()
        link = "https://www.imdb.com" + tmp.find("a")['href']
        rating = row.find("td", attrs={"class": "ratingColumn imdbRating"}).text.strip()
        if(rating ==""):
            rating = "0"
        arr.append((str(name), year, rating, str(link)))
        x+=1

    saveFile(arr, filename)
    
def compareLists(fileOld, fileNew):
    oldlist = loadFile(fileOld)
    newlist = loadFile(fileNew)
    if(oldlist == -1):
        saveFile(newlist, fileOld)
        return
    txtName = fileNew[:-4]
    prefix = datetime.now().strftime("[20%y/%m/%d - %H:%M] ")
    if(txtName == "movies"):
        prefix = "Movie"
    else:
        prefix = "TV show"
    txtName += "_changes.txt"

    with codecs.open(txtName, "a") as f:
        for i,j  in enumerate(newlist):
            if j[0] != oldlist[i][0]:
                f.write(prefix+ " %s at rank %d changed to %s.\n" % (oldlist[i][0], i+1, j[0]))
                print(prefix+ " %s at rank %d changed to %s." % (oldlist[i][0], i+1, j[0]))
                continue
            elif(j[1] != oldlist[i][1]):
                f.write(prefix+" %s changed rating from %s to %s\n" % (oldlist[i][0], oldlist[i][1], j[1]))
                print(prefix+" %s changed rating from %s to %s" % (oldlist[i][0], oldlist[i][1], j[1]))
    saveFile(newlist, fileOld)
def main():
    print("Gathering movies...")
    url = "https://www.imdb.com/chart/moviemeter?ref_=nv_mv_mpm_8"
    gatherData(url, "movies.pkl")
    compareLists("oldmovies.pkl", "movies.pkl")

    print("Done\nGathering TV shows in 3 seconds")
    time.sleep(3)
    print("Gathering TV shows...")
    url = "https://www.imdb.com/chart/tvmeter?ref_=nv_tvv_mptv_4"
    gatherData(url, "tvshows.pkl")
    compareLists("oldtvshows.pkl", "tvshows.pkl")

    print("Done")
    
    s = loadFile("movies.pkl");
    with codecs.open("movies.txt", "w", encoding="utf-8") as f:
        for i in s:
            f.write(str(i[0])+ " | " + str(i[1])+  " | " + str(i[2])+ " | " + str(i[3]) +"\n");
            
    s = loadFile("tvshows.pkl");
    with codecs.open("tvshows.txt", "w", encoding="utf-8") as f:
        for i in s:
            f.write(str(i[0])+ " | " + str(i[1])+  " | " + str(i[2])+ " | " + str(i[3]) +"\n");
main()

