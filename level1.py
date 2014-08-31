# -*- coding: utf-8 -*-
import urllib2
import json
from bs4 import BeautifulSoup

def get_input(mock=False):
	html = None
	if mock:
		print "Using mock data..."
		f = open("../mock_level1.txt", "r")
		html = f.read().decode("utf-8")
		f.close()
	else:
		obj = urllib2.urlopen("http://axe-level-1.herokuapp.com/")
		html = obj.read().decode("utf-8")
		obj.close()

	return html

def main():
	html = get_input(False)

	soup = BeautifulSoup(html)
	rows = soup.find_all('tr')

	# parse title
	title = rows[0]
	title_parser = BeautifulSoup(unicode(title))
	field_title = []
	for t in title_parser.find_all('td')[1:]:
		field_title.append(unicode(t.get_text()))
	
	# parse data
	output = []
	for row in rows[1:]:
		row_parser = BeautifulSoup(unicode(row))
		fields = row_parser.find_all('td')
		rowobj = {}
		rowobj["name"] = unicode(fields[0].get_text())
		rowobj["grades"] = {}
		index = 0
		for f in fields[1:]:
			rowobj["grades"][field_title[index]] = int(f.get_text())
			index += 1
		output.append(rowobj)
	

	print json.dumps(output, ensure_ascii=False)

if __name__ == "__main__":
	main()
