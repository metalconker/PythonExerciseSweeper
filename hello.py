import urllib
import urllib.request
import requests
import re
from bs4 import BeautifulSoup

# URL Setup
url = "https://exrx.net/WeightExercises/ErectorSpinae/TBStraightLegDeadlift"
req = urllib.request.Request(url, headers={
                             'User-Agent': "Mozilla/5.0 (X11; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/86.0"})
try:
    page = urllib.request.urlopen(req)
except urllib.error.URLError as e:
    print(e.reason)
soup = BeautifulSoup(page, "lxml")

##############################
# headers = {
#     'Host': 'exrx.glorb.com',
#     'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:79.0) Gecko/20100101 Firefox/79.0',
#     'Accept': 'video/webm,video/ogg,video/*;q=0.9,application/ogg;q=0.7,audio/*;q=0.6,*/*;q=0.5',
#     'Accept-Language': 'en-US,en;q=0.5',
#     'Range': 'bytes=0-',
#     'DNT': '1',
#     'Connection': 'keep-alive',
#     'Referer': 'https://exrx.net/'}

# videoURL = 'https://exrx.glorb.com/api/video/10601'
# r = requests.get(videoURL, headers)
# print(r.headers)
# open("video.mp4", 'wb').write(r.content)


#videoreq = urllib.request.Request(videoURL, headers)
# open("video.mp4", 'wb').write(videoreq..data)

# trying to get the mp4
# x = urllib.request.Request('GET /api/video/b10412543b7667a107e178795cd5bc0c/10226 HTTP/1.1', headers={
#    'Host': "exrx.glorb.com",
#    'User-Agent': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:79.0) Gecko/20100101 Firefox/79.0",
#    'Accept': "video/webm,video/ogg,video/*;q=0.9,application/ogg;q=0.7,audio/*;q=0.6,*/*;q=0.5",
#    'Accept-Language': "en-US,en;q=0.5",
#    'Range': "bytes=0-",
#    'DNT': "1",
#    'Connection': "keep-alive",
#    'Referer': "https://exrx.net/WeightExercises/ErectorSpinae/LVStraightLegDeadlift"})


################################

# File
file = open('scraped_text.txt', 'w')

# Finds the name of the exercise
content = soup.find(
    'div', {"class": "fruitful-page-title fruitfull-title-padding"})
article = 'Exercise: '
for i in content.findAll('h1'):
    article = article + i.text
file.write(article + '\n')

leftDiv = soup.findAll('div', {"class": "col-sm-6"})[0]
rightDiv = soup.findAll('div', {"class": "col-sm-6"})[1]

# Finds the classification of the exercise
classification = ['Utility: ', 'Mechanics: ', 'Force: ']
table = leftDiv.find('table')
links = (table.findAll('tr'))
for index, link in enumerate(links):
    classification[index] += (link.findAll('td')[1].text)
    file.write(classification[index] + '\n')

# Finds the preparation and execution of the exercise
preparation = 'Preparation: '
execution = 'Execution: '
paragraphs = (leftDiv.findAll('p'))
if (len(paragraphs) < 4):
    file.write("PARSE ERROR FOR EXERCISE PREPARATION" + '\n')
else:
    preparation += paragraphs[1].text
    execution += paragraphs[3].text
    file.write(preparation + '\n')
    file.write(execution + '\n')

# Finds the comments
headers = leftDiv.findAll('h2')
leftSideStart = False
rightSideStart = False
for header in headers:
    # Case 1 + 2, comments started on left side,
    if ("Comments" in header):
        leftSideStart = True
        rightSideStart = False
    else:
        leftSideStart = False
        # Case 3: started on the right side
        rightSideStart = True
# Case 1: finished on left side
leftSideFinished = True
# Case 2: finished on right side
if (rightDiv.findChildren()[0].name == "p"):
    leftSideFinished = False

# Case 1: finished on left side
if (leftSideStart and leftSideFinished):
    comments = 'Comments: ' + paragraphs[len(paragraphs)-1].text
    file.write(comments + '\n')

# Case 2: finished on right side
if (leftSideStart and not leftSideFinished):
    comments = 'Comments: ' + paragraphs[len(paragraphs)-1].text + ' '
    rightComments = rightDiv.find('p').text
    comments += rightComments
    file.write(comments + '\n')

# Case 3: comments right side
if (rightSideStart):
    rightComments = rightDiv.find('p').text
    comments = 'Comments: ' + rightComments
    file.write(comments + '\n')

# Finds the muscles
muscleGroupNames = rightDiv.findAll('p')
muscleNames = rightDiv.findAll('ul')
for i in range(1, len(muscleGroupNames)):
    file.write(muscleGroupNames[i].text + ': ')
    currentMuscles = muscleNames[i-1].findAll('li')
    muscles = ""
    for muscle in currentMuscles:
        muscles += muscle.text + ", "
    muscles = muscles[:-2]
    file.write(muscles + '\n')
    # Close file
file.close()
