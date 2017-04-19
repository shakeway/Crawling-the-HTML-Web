from bs4 import BeautifulSoup
from urllib.request import urlopen

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

def get_page(url):
	"""Get the text of the web page at the given URL
	return a string containing the content"""
	
	fd = urlopen(url)
	content = fd.read()
	fd.close()

	return content.decode('utf8')


url = 'http://unitguides.mq.edu.au/unit_offerings/49056/unit_guide'
text = get_page(url)
assignments = find_assignments(text)
for assignment in assignments:
	print(assignment)
