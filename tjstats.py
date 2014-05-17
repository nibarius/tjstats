import json
import subprocess
import urllib2

def getTitels():
    # first posts at: http://www.reddit.com/r/Team_Japanese/new/?count=1375&after=t3_1u58o4
    startTime = 1388448000 # 2013-12-31 00:00:00 (first start post is from 31st)

    ret = []

    needMore = True
    after = ""
    while needMore:
        print "Reading more data from reddit..."
        data = readFromReddit(after)
        print "Got data from reddit"
        children = data["data"]["children"]
        for child in children:
            created = child["data"]["created_utc"]
            if created < startTime:
                needMore = False
                break
            ret.append(child["data"]["title"])

        after = children[-1]["data"]["name"]

    return ret

def readFromReddit(after):
    limit = "100"
    url = "http://www.reddit.com/r/Team_Japanese/new.json?limit=" + limit + "&after=" + after
    req = urllib2.Request(url, headers={ 'User-Agent': 'Team_Japanese stats generator by u/nibarius' })
    response = urllib2.urlopen(req)
    headers = response.info().headers
    if "X-Ratelimit-Used" in headers or "X-Ratelimit-Remaining" in headers or "X-Ratelimit-Reset" in headers:
        print "important headers found: ", headers
        print "implement support for rate limits!"

    j = json.loads(response.read())
    return j

def processTitles(titles):
    filtered = [title for title in titles if title.startswith("2014")]
    print str(len(filtered)) + " logs to process"
    weeks = [0] * 54
    incorrect = 0
    for title in filtered:
        weekStr = title.split(' ', 3)[2]
        if "start" in title.split(' ', 2)[1].lower() or "start" in weekStr.lower():
            weeks[0] += 1
        elif not weekStr.isdigit():
            incorrect += 1
            #print "it's incorrect:", title.split(' ', 3)[:3]
            continue
        else:
            week = int(weekStr)
            weeks[week] += 1
    print "Number of reports:", weeks
    print "Number of incorrectly formatted reports:", incorrect
    return weeks

def writeDataFile(weeks):
    with open("tjstats.dat", "w") as f:
        for i, week in enumerate(weeks):
            if week is 0:
                break
            elif i is 0:
                f.write(str(i) + ",Start," + str(week) + "\n")
            else:
                f.write(str(i) + ",Week " + str(i) + "," + str(week) + "\n")
        print "Raw output printed to tjstats.dat"

def plotGraph():
    command = "gnuplot tjstats.p"
    subprocess.call(command.split())
    print "Graph of WaniKani progress written to: tj_logs.png"

def tjstats():
    posts = getTitels() # get all titles from reddit from this year.
    weeks = processTitles(posts)
    writeDataFile(weeks)
    plotGraph()

if __name__ == "__main__":
    tjstats();
