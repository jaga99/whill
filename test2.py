import urllib
import urllib.request
from bs4 import BeautifulSoup
import re
import time

#beautiful soup
def make_soup(url):
	thepage = urllib.request.urlopen(url)
	soupdata = BeautifulSoup(thepage, "html.parser")
	return soupdata

#error handling
def getcontents (item, index):
	if item is None:
		return None
	return item.contents[index]


#############################################################################################
### Part 1 - Find all the fixtures and URLS
#############################################################################################

#set variables for dynamic date in URL1
Y = "20" + time.strftime("%y")
M = time.strftime("%m")
D = time.strftime("%d")
T = time.strftime("%H")

#URL1 taking in todays date
URL1 = "http://sports.williamhill.com/bet/en-gb/results///T/8398/thisDate/"+str(Y)+ "/" +str(M)+ "/" +str(D)+ "/" +str(T) + ":00:00//Victoria+Stadium.html"
soup = make_soup(URL1)

#Gaining a list of URLS for each fixture this hour, and writing to .txt file
file = open("new.txt","r+")
for record in soup.findAll('tr'):
	for data in record.findAll('td'):
		for data1 in data.findAll('a'):

			file.write("%s\n" % data1.get('href'))




#############################################################################################
### Part 2 - Gain scores for each fixture
#############################################################################################


#Read the file into a variable

#with open('new.txt') as file:
last_line = file.readlines()
file.close()

	#print (last_line)

#Grab the last URL
URL2 = last_line [-1]
soup = make_soup(URL2)




#Gives the E number for each match - primary key
PrimaryK = re.findall("///E/(.*)/thisDate/", URL2)[0] 
print (PrimaryK)



#Find the caption "Correct Sore", if exists carries on, otherwise quits
if soup.find(text = "Correct Score"):
	# Gets the fixture title
	for title in soup.findAll('caption'):
		getcontents(print (title.text.strip()),0)
	# Finds the "Correct Score" text, then hops two TDs to get Match result and odds
	data = soup.find(text = "Correct Score").findNext('td').findNext('td')
	# Could change from a for loop to something else, but this just prints out match result in a tidy format (text only)
	for item in data:
		getcontents(print (data.text.strip()),0)
# If webpage is not fully populated it will only print Primary key and error with BS
else:
	print("gotta wait BS")
