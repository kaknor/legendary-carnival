import requests
from bs4 import BeautifulSoup

# TODO : Clean the code....
def crawl_response_page(anchor):
	print(anchor["href"])
	question = anchor["href"].split(r"/")[-1]
	print(question)
	print("title")
	print(anchor["title"])
	target_url = rf"https://intra.sigl.epita.fr{anchor['href']}"
	print(f"url = {target_url}")
	res = requests.get(target_url)
	soup = BeautifulSoup(res.content, features="html.parser")
	print(f"Response {res.status_code}")
	divs = soup.findAll("div", {"class": "kmsgtext"})
	for msg in divs:
		# TODO : Create dir if it does not exists.
		with open(f"crawled_intra/responses", "a") as f:
			print(f"Writting {question} to responses")
			f.write("==========================")
			f.write(msg.text)
			f.write("==========================")

def crawl_page(page_number=-1):
	print("###############################################")
	if page_number == -1:
		url = r"https://intra.sigl.epita.fr/index.php/forum/cote-client"
	else:
		url = rf"https://intra.sigl.epita.fr/index.php/forum/cote-client?start={page_number}"
	r = requests.get(url)
	print(f"Status code for page {page_number} : {r.status_code}")

	soup = BeautifulSoup(r.content, features="html.parser")
	count_pages = 0
	for anchor in soup.findAll("a", {"class": "ktopic-title km"}, href=True):
		crawl_response_page(anchor)
		count_pages += 1
		print(f"TOTAL NUMBER OF PAGES {count_pages}")

if __name__ == "__main__":
	crawl_page()
	for number in [20, 40, 60]:
		crawl_page(number)