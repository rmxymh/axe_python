import urllib2
import cookielib
import time
import json
from bs4 import BeautifulSoup

# Global for keep session
jar = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(jar))

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

def has_next(html):
	ret = html.find("?page=next")
	return (ret >= 0)

def get_html(url):
	global opener

	try:
		obj = opener.open(url)
	except:
		print "Retry..."
		obj = opener.open(url)
	html = obj.read()
	obj.close()
	return html

def main():
	html = get_html("http://axe-level-1.herokuapp.com/lv3/")

	page = 1	
	# parse the first page
	print "Parse page %d..." % (page)
	output = parse_table(html)
	page += 1

	while has_next(html):
		print "Parse page %d..." % (page)
		html = get_html("http://axe-level-1.herokuapp.com/lv3/?page=next")
		output += parse_table(html)
		page += 1
		time.sleep(1)
	
	print json.dumps(output, ensure_ascii=False)

if __name__ == "__main__":
	main()
