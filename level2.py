# -*- coding: utf-8 -*-
import urllib2
import json
from bs4 import BeautifulSoup

def get_input(url):
	html = None
	obj = urllib2.urlopen(url)
	html = obj.read().decode("utf-8")
	obj.close()

	return html

def parse_table(html):
	soup = BeautifulSoup(html)
	rows = soup.find_all('tr')

	# parse data
	field_title = ["town", "village", "name"]
	output = []
	for row in rows[1:]:
		row_parser = BeautifulSoup(unicode(row))
		fields = row_parser.find_all('td')
		rowobj = {}
		index = 0
		for f in fields:
			rowobj[field_title[index]] = unicode(f.get_text())
			index += 1
		output.append(rowobj)

	return output

def main():
	baseurl = "http://axe-level-1.herokuapp.com/lv2/"
	html = get_input(baseurl)

	soup = BeautifulSoup(html)

	# try to obtain page information first
	pages = []
	links = soup.find_all('a')
	for link in links:
		pages.append(link["href"])

	# parse data - page 1
	print "Parsing page 1... "
	output = parse_table(html)

	# parse the remaining data
	index = 2
	for page in pages[1:]:
		print "Parsing page %d... " % (index)
		html = get_input(baseurl + page)
		output += parse_table(html)
		index += 1

	print json.dumps(output, ensure_ascii=False)

if __name__ == "__main__":
	main()
