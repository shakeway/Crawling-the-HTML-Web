from urllib.request import urlopen
import re

def crawl(url, maxurls):
	urls = set([url])
	while(len(urls) < maxurls):
		url = urls.pop()
		print("URL: ", url)
		links = get_links(url)
		urls.update(links)
		urls.add(url)

	return urls

def get_links(url):
	text = get_page(url)
	links = set()
	urlpattern = r"(https?\://[a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,3}(/[^<'\";]*)?)"

	matches = re.findall(urlpattern, text)

	for match in matches:
		links.add(match[0])

	return links


def get_page(url):
	fd = urlopen(url)
	content = fd.read()
	fd.close()

	return content.decode('utf8')


url = 'http://www.python.org/'
links = crawl(url, 100)
print("collected ", len(links), " links:")
for link in links:
	print(link)