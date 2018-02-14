import requests
import re
from bs4 import BeautifulSoup
import json

def crawl_snapdeal(search):
	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
	page = requests.get("https://www.snapdeal.com/search?keyword=" + search + "&sort=rlvncy", headers = headers)
	page = page.content
	soup = BeautifulSoup(page, "html.parser")
	tags = soup.find_all(class_ = "product-tuple-image")
	urls = []
	for tag in tags:
		try:
			href = tag.a['href']
			title = tag.find(class_ = "product-image")['title']
			urls.append([href, title])
		except e:
			print(e)

	return urls


def scrap_snapdeal(snapdeal, product):
	output = []
	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

	while True:
		page = requests.get(snapdeal + "/reviews", headers = headers).content

		soup = BeautifulSoup(page, "html.parser")
		tags = soup.find_all("div", class_ = "text");

		for tag in tags:
			review = tag.find("div", class_ = "user-review")

			if review is None:
				continue
			
			ratings = review.find_all(class_ = "active")
			ratings = len(ratings)

			title = review.find(class_ = "head").string
			content = review.find("p").string

			hfreview = tag.find("div", class_ = "hf-review")
			helpful = hfreview.find(class_ = "hf-num").string

			# print(ratings, title, content, helpful)

			output.append([title ,content ,ratings, helpful])

		try:
			nexthref = soup.find("li", class_ = "last").a['href']
			if re.search("http", nexthref):
				snapdeal = nexthref
				# print(snapdeal)
			else:
				break
		except:
			break
		# print(nexthref)

	out = {product : output}

	with open(re.sub("[^a-zA-Z0-9]", " " ,product) + ".json", 'w') as f:
	    json.dump(out, f, indent=4)



# proxy = urllib.request.ProxyHandler({
# 	'http': 'http://edcguest:edcguest@172.31.100.27:3128',
# 	'https': 'https://edcguest:edcguest@172.31.100.27:3128'	
# })
# opener = urllib.request.build_opener(proxy)
# urllib.request.install_opener(opener)

ret = crawl_snapdeal("fidget%20spinner")
cnt = 0
for item in ret:
	print(item[0], item[1])
	scrap_snapdeal(item[0], item[1])