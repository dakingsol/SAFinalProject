from urllib.request import urlopen
from bs4 import BeautifulSoup
import csv
import sys
import time
import re


def overall(csv_file):
	with open(csv_file, "a", newline="") as myfile:
		wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
		#scrapey(wr, "test")
		wr.writerow(['date','awayteam','awayteamrank','hometeam','hometeamrank','percentbetaway','percentbethome','awayOpeningSpread','awayOpeningLine','homeOpeningSpread','homeOpeningLine','awayClosingSpread','awayClosingLine','homeClosingSpread','homeClosingLine','awayOpeningMoney','homeOpeningMoney','awayClosingMoney','homeClosingMoney','winningTeam','losingTeam','winningScore','losingScore'])
		year = 7
		month = 1
		day = 1
		while year < 18:
			if len(str(year)) == 1:
				realyear = "200" + str(year)
				print(realyear)
			else:
				realyear = "20" + str(year)
				print(realyear)
			while month < 13:
				if len(str(month)) == 1:
					realmonth = "0" + str(month)
				else:
					realmonth = str(month)
				if month == 2:
					while day < 29:
						if len(str(day)) == 1:
							realday = "0" + str(day)
						else:
							realday = str(day)
						day += 1
						yearly = realyear + realmonth + realday
						print(yearly)
						scrapey(wr, yearly)
					day = 1
				elif any(month == i for i in (1,3,5,7,8,10,12)):
					while day < 32:
						if len(str(day)) == 1:
							realday = "0" + str(day)
						else:
							realday = str(day)
						day += 1
						yearly = realyear + realmonth + realday
						print(yearly)
						scrapey(wr, yearly)
					day = 1
				else:
					while day < 31:
						if len(str(day)) == 1:
							realday = "0" + str(day)
						else:
							realday = str(day)
						day += 1
						yearly = realyear + realmonth + realday
						print(yearly)
						scrapey(wr, yearly)
					day = 1
				month += 1
			year += 1
			month = 1
	
def scrapey(wr, yearly):
	website = 'https://www.sportsbookreview.com/betting-odds/college-football/?date=' + yearly
	#website = 'https://www.sportsbookreview.com/betting-odds/college-football/?date=20070915'
	html = urlopen(website)
	soup = BeautifulSoup(html, "html.parser")
	sub = soup.find(class_="content-final content-complete ")
	if not sub == None:
		games = sub.find_all(class_="event-holder holder-complete")
		for g in games:
			awayteam = findAwayTeam(g)[0]
			awayteamrank = findAwayTeam(g)[1]
			hometeam = findHomeTeam(g)[0]
			hometeamrank = findHomeTeam(g)[1]
			percentbetaway = findPercentBet(g)[0]
			percentbethome = findPercentBet(g)[1]
			awayOpeningSpread = findOpeningLS(g)[0]
			awayOpeningLine = findOpeningLS(g)[1]
			homeOpeningSpread = findOpeningLS(g)[2]
			homeOpeningLine = findOpeningLS(g)[3]
			awayClosingSpread = findClosingLS(g)[0]
			awayClosingLine = findClosingLS(g)[1]
			homeClosingSpread = findClosingLS(g)[2]
			homeClosingLine = findClosingLS(g)[3]
			winningTeam = whoWon(g, awayteam, hometeam)[0]
			losingTeam = whoWon(g, awayteam, hometeam)[1]
			winningScore = scoreCheck(g)[0]
			losingScore = scoreCheck(g)[1]
			if not awayClosingSpread == None:
				if not winningTeam == None:
					if not winningScore == None:
						awayOpeningMoney = getMoneyLine(g)[0]
						homeOpeningMoney = getMoneyLine(g)[1]
						awayClosingMoney = getMoneyLine(g)[2]
						homeClosingMoney = getMoneyLine(g)[3]
						wr.writerow([yearly,awayteam,awayteamrank,hometeam,hometeamrank,percentbetaway,percentbethome,awayOpeningSpread,awayOpeningLine,homeOpeningSpread,homeOpeningLine,awayClosingSpread,awayClosingLine,homeClosingSpread,homeClosingLine, awayOpeningMoney,homeOpeningMoney,awayClosingMoney,homeClosingMoney,winningTeam,losingTeam,winningScore,losingScore])
						print('row written')	

def getMoneyLine(g):
	update = g.find(class_="eventLink")
	website2 = update.get("href")
	#website2 = "https://www.sportsbookreview.com/betting-odds/college-football/akron-zips-vs-indiana-hoosiers-49407/"
	html2 = urlopen(website2)
	soup2 = BeautifulSoup(html2, "html.parser")
	first = soup2.find(class_="eventLine status-complete")
	if first == None:
		update = g.find(class_="eventLink")
		website2 = update.get("href")
		html2 = urlopen(website2)
		soup2 = BeautifulSoup(html2, "html.parser")
		first = soup2.find(class_="eventLine status-complete")
	second = first.next_sibling
	money = second.find(class_="el-div eventLine-opener")
	money2 = money.next_sibling
	awayOpeningMoney = money.find(class_="eventLine-book-value").string
	homeOpeningMoney = money.find(class_="eventLine-book-value").next_sibling.string
	awayClosingMoney = money2.find(class_="eventLine-book-value").string
	homeClosingMoney = money2.find(class_="eventLine-book-value").next_sibling.string
	if awayOpeningMoney == None:
		awayOpeningMoney = "NA"
		homeOpeningMoney = "NA"
	if awayClosingMoney == None:
		awayClosingMoney = "NA"
		homeClosingMoney = "NA"
	output = [awayOpeningMoney, homeOpeningMoney, awayClosingMoney, homeClosingMoney]
	return output
		
def scoreCheck(g):
	k = g.find(class_='score-periods')
	if k.find(class_='first total ') == None:
		return [None, None]
	firstscore = k.find(class_='first total ').string
	if k.next_sibling.find(class_='total ') == None:
		return [None, None]
	secondscore = k.next_sibling.find(class_='total ').string
	first = int(firstscore)
	second = int(secondscore)
	if first > second:
		winningScore = first
		losingScore = second
	else:
		winningScore = second
		losingScore = first
	output = [winningScore, losingScore]
	return output

def whoWon(g, awayteam, hometeam):
	alpha = g.find(class_="icons-winner-arrow")
	if alpha == None:
		return [None, None]
	winner = alpha.parent.a.string
	if winner == awayteam:
		loser = hometeam
	if winner == hometeam:
		loser = awayteam
	output = [winner, loser]
	return output

def findOpeningLS(g):
	rawaway = g.find(class_="el-div eventLine-opener").find(class_="eventLine-book-value").string
	if rawaway == None:
		return ['NA', 'NA', 'NA', 'NA']
	rawhome = rawaway.next_element.next_element.string
	if rawhome == None:
		return [None, None, None, None]
	if "PK" in rawaway:
		aos = 0
		aol = rawaway.split("PK", 1)[1]
	if "PK" in rawhome:
		hos = 0
		hol = rawhome.split("PK", 1)[1]
	if "PK" not in rawaway: 
		aos = rawaway.split()[0]
		aos = aos.replace('½', '.5')
		aol = rawaway.split()[1]
	if "PK" not in rawhome:
		hos = rawhome.split()[0]
		hos = hos.replace('½', '.5')
		hol = rawhome.split()[1]
	output = [aos, aol, hos, hol]
	return output

def findClosingLS(g): 
	rawaway = g.find(class_="el-div eventLine-book").find(class_="eventLine-book-value").string
	if rawaway == None:
		return [None, None, None, None]
	rawhome = rawaway.next_element.next_element.string
	if rawhome == None:
		return [None, None, None, None]
	if "PK" in rawaway:
		acs = 0
		acl = rawaway.split("PK", 1)[1]
	if "PK" in rawhome:
		hcs = 0
		hcl = rawhome.split("PK", 1)[1]
	if "PK" not in rawaway: 
		acs = rawaway.split()[0]
		acs = acs.replace('½', '.5')
		acl = rawaway.split()[1]
	if "PK" not in rawhome:
		hcs = rawhome.split()[0]
		hcs = hcs.replace('½', '.5')
		hcl = rawhome.split()[1]
	output = [acs, acl, hcs, hcl]
	return output

def findPercentBet(g):
	away = g.find(class_="el-div eventLine-consensus").next_element
	home = away.next_element.next_element
	awayout = away.replace('%','')
	homeout = home.replace('%','')
	output = [awayout, homeout]
	return output

def findAwayTeam(g):
	awayteam = g.find_all(class_="team-name")[0].string
	rank = 0
	if(awayteam == None):
		e = g.find_all(class_="team-name")[0].next_element
		rank = re.findall('\d+', e)[0]
		awayteam = e.next_element.string
	output = [awayteam, rank]
	return output

def findHomeTeam(g):
	hometeam = g.find_all(class_="team-name")[1].string
	rank = 0
	if(hometeam == None):
		e = g.find_all(class_="team-name")[1].next_element
		rank = re.findall('\d+', e)[0]
		hometeam = e.next_element.string
	output = [hometeam, rank]
	return output

overall('FindMoneyLine.csv')
