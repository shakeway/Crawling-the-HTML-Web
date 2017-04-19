from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.parse import urljoin
import re

# Use Beautifulsoup to updat the get_links function

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
	"""scan the text for http URLs and return a set 
	of URLs found, withoout duplicates"""

	# lokk for any http URL in the page
	links = set()

	text = get_page(url)

	soup = BeautifulSoup(text)

	for link in soup.find_all('a'):
		if 'href' in link.attrs:
			newurl = link.attrs['href']
			# resolve relative URLS
			if newurl.startswith('/'):
				newurl = urljoin(url, newurl)
			# ignore any URL that doesn't now start with http
			if newurl.startswith('http'):
				links.add(newurl)

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