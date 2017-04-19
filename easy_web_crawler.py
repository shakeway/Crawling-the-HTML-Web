from urllib.request import urlopen
import re

def crawl(url, maxurls):
	"""Starting from this URL, crawl the web until
    you have collected maxurls URLS, then return them
    as a set"""
	urls = set([url])
	while(len(urls) < maxurls):
		# remove a URL at random
		url = urls.pop()
		print("URL: ", url)
		links = get_links(url)
		urls.update(links)
		# add the url back to the set
		urls.add(url)

	return urls

def get_links(url):
	"""Scan the text for http URLs and return a set
    of URLs found, without duplicates"""
	text = get_page(url)

	# look for any http URL in the page
	links = set()
	urlpattern = r"(https?\://[a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,3}(/[^<'\";]*)?)"

	matches = re.findall(urlpattern, text)

	for match in matches:
		links.add(match[0])

	return links


def get_page(url):
	"""Get the text of the web page at the given URL
    return a string containing the content"""
    
	fd = urlopen(url)
	content = fd.read()
	fd.close()

	return content.decode('utf8')


url = 'http://www.python.org/'
links = crawl(url, 100)
print("collected ", len(links), " links:")
for link in links:
	print(link)