import urllib2
import cookielib
import time
import json
from bs4 import BeautifulSoup

# Global for keep session
jar = cookielib.CookieJar()
preURL = ""

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

def get_html(url):
	global jar
	global preURL

	print "= ACCESS: " + url
	subheader = {}
	subheader['User-agent'] = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.102 Safari/537.36'
	if len(preURL) > 1:
		subheader['Referer'] = preURL

	try:
		r = urllib2.Request(url, headers=subheader)
		jar.add_cookie_header(r)
		obj = urllib2.urlopen(r)
		jar.extract_cookies(obj, r)
	except:
		print "Retry..."
		r = urllib2.Request(url, headers=subheader)
		jar.add_cookie_header(r)
		obj = urllib2.urlopen(r)
		jar.extract_cookies(obj, r)
	html = obj.read()
	obj.close()
	preURL = url
	return html

def main():
	baseurl = "http://axe-level-4.herokuapp.com/lv4/"
	html = get_html(baseurl)

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
		html = get_html(baseurl + page)
		output += parse_table(html)
		index += 1

	print json.dumps(output, ensure_ascii=False)

if __name__ == "__main__":
	main()
