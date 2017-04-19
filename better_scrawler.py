from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.parse import urljoin
import re

# Use Beautifulsoup to updat the get_links function

def find_assignments(text):
	"""Given the text of an HTML unit guide from 
    Macquarie University, return a list of the assignments for
    that unit as (name, weighting, due)"""
    soup = BeautifulSoup(text)

    # find the section that has the assignment tabel
    section = soup.find(id = 'assessment-tasks-section')

    # we want the first table in this section, then the tbody inside that 
    # and we want all rows in the body
    tablerows = section.table.tbody.find_all('tr', 'assessment-task-row')

    result = []
    for row in tablerows:
    	name = row.find('td', 'title').a.string.strip()
    	weight = row.find('td', 'weighting').string.strip()
    	due = row.find('td', 'due').string.strip()
    	result.append((name, weight, due))

    return result



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