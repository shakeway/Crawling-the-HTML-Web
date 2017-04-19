from urllib.parse import urljoin, urlparse
from urllib.robotparser import RobotFileParse

# Dictionary to save parsed robots.txt file
ROBOTS = dict()

def robot_check(url):
	# check whether we're allowed to fetch this URL from this site
	netloc = urlparse(url).netloc

	if netloc not in ROBOTS:
		robotsurl = urljoin(url, '/robots.txt')
		ROBOTS[netloc] = RobotFileParse(robotsurl)
		ROBOTS[netloc].read()

	return ROBOTS[netloc].can_fetch('*', url)

def get_page(url):
	# get the text of the web page at the given URL
	# return a string containing the content
	if robot_check(url):
		
		# open the URL with a custom User-agent header
		opener = urllib.request.build_opener()
		opener.addheaders = [('User-agent', 'Lin')]
		fd = opener.open(url)
		content = fd.read()
		fd.close()

		return content.decode('utf8')
	else:
		print("Disallow: ", url)
		return ''