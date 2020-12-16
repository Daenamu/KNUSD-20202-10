import requests
from bs4 import BeautifulSoup
# 한문학과 공지 crawl

URL = f"http://hanmun.knu.ac.kr/HOME/hanmun/sub.htm?mv_data=c3RhcnRQYWdlPTAmY29kZT1ub3RpY2UmbmF2X2NvZGU9aGFuMTU0NjgyNzc4OCZ0YWJsZT1leF9iYnNfZGF0YV9oYW5tdW4mc2VhcmNoX2l0ZW09JnNlYXJjaF9vcmRlcj0mb3JkZXJfbGlzdD0mbGlzdF9zY2FsZT0mdmlld19sZXZlbD0mdmlld19jYXRlPSZ2aWV3X2NhdGUyPQ==||"

def extract_last_pages():
  result = requests.get(URL)
  soup = BeautifulSoup(result.text, "html.parser")

  pag = soup.find("div",{"class":"left totalpage"})
  link = pag.text.split('/')
  last_pages = link[1][:3]
  
  return last_pages


def extract_content_text(url):
  result = requests.get(url)
  soup = BeautifulSoup(result.text, "html.parser")
  cont_text = soup.find("div",{"class":"cont"}).text.strip()
  
  return cont_text

def extract_content_image(url):
  images = []
  result = requests.get(url)
  soup = BeautifulSoup(result.text,"html.parser")
  cont = soup.find("div",{"class":"cont"})
  imgs = cont.find_all("img")

  for img in imgs:
    if img != None:
      img = img.attrs["src"]
      images.append(img)
  return images


def extract_content_attach(url):
  attach = []
  result = requests.get(url)
  soup = BeautifulSoup(result.text,"html.parser")
  cont = soup.find("div",{"class":"board_view"})
  if cont != None:
    attach_hrefs = cont.find_all("li")
    for attach_href in attach_hrefs:
     href = attach_href.find("a").attrs["href"]
     href = "http://hanmun.knu.ac.kr/"+href[6:]
     attach.append(href)
  return attach

def hanmun_crawl(html,url):
  view = html.select('div.board_view > table > tr ')[1]
  modify_dt = view.find_all("td")[1].string
  title = html.select('div.board_view > h2')[0].string
  print(title)
  content = extract_content_text(url)
  image_url = extract_content_image(url)
  download_url = extract_content_attach(url)

  dict_data = {'title':title, 'modify_dt':modify_dt, 'content':content, 'type':"한문학과", 'url':url, 'image_url':image_url, 'download_url':download_url}
  print(dict_data)
  return dict_data


def extract_pages_url(p_num):
    pages = []
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, "html.parser")

    paging = soup.find("div",{"class":"paging"})

    for page in paging:
      if page != None:
        pages.append(paging.find("a").attrs["href"])

    return "http://hanmun.knu.ac.kr/"+pages[p_num-1]

print(extract_pages_url(3))

def extract_hanmun_notices(last_pages):
  notices = []
  count = 0

  for page in range(1,last_pages+1):
    link = requests.get(extract_pages_url(page))
    soup = BeautifulSoup(link.text, "html.parser")
    results = soup.select('td.subject > a')

    for result in results:
      url = result.find("a").attrs["href"]
      re = requests.get(url)
      sop = BeautifulSoup(re.text,"html.parser")
      notice = hanmun_crawl(sop,url)
      notices.append(notice)
      count = count + 1
      print(f"{page}page {count}번 게시물 crawling")
  
  return notices 


def check_latest():
  link = requests.get("http://hanmun.knu.ac.kr/HOME/hanmun/sub.htm?mv_data=c3RhcnRQYWdlPTAmY29kZT1ub3RpY2UmbmF2X2NvZGU9aGFuMTU0NjgyNzc4OCZ0YWJsZT1leF9iYnNfZGF0YV9oYW5tdW4mc2VhcmNoX2l0ZW09JnNlYXJjaF9vcmRlcj0mb3JkZXJfbGlzdD0mbGlzdF9zY2FsZT0mdmlld19sZXZlbD0mdmlld19jYXRlPSZ2aWV3X2NhdGUyPQ==||")
  soup = BeautifulSoup(link.text, "html.parser")
  result = soup.find("div",{"class":"board_list"})
  table = result.find("tbody")
  links = table.find_all("tr")

  for link in links:
    if link.find("td",{"class":"fst notice"}) == None:
      late = link.find("td",{"class":"subject"})

  url = late.find("a").attrs["href"]
  url = "http://hanmun.knu.ac.kr/"+url
  re = requests.get(url)
  sop = BeautifulSoup(re.text,"html.parser")
  notice = hanmun_crawl(sop,url)

  return notice['title']

def extract_latest_notices(latest):
  notices = []
  link = requests.get("http://hanmun.knu.ac.kr/HOME/hanmun/sub.htm?mv_data=c3RhcnRQYWdlPTAmY29kZT1ub3RpY2UmbmF2X2NvZGU9aGFuMTU0NjgyNzc4OCZ0YWJsZT1leF9iYnNfZGF0YV9oYW5tdW4mc2VhcmNoX2l0ZW09JnNlYXJjaF9vcmRlcj0mb3JkZXJfbGlzdD0mbGlzdF9zY2FsZT0mdmlld19sZXZlbD0mdmlld19jYXRlPSZ2aWV3X2NhdGUyPQ==||")
  soup = BeautifulSoup(link.text, "html.parser")
  results = soup.find_all("td",{"class":"subject"})

  if results != None:
    for result in results:
      url = result.find("a").attrs["href"]
      url = "http://hanmun.knu.ac.kr/"+url
      re = requests.get(url)
      sop = BeautifulSoup(re.text,"html.parser")
      notice = hanmun_crawl(sop,url)
      if notice['title'] == latest:
        break
      notices.append(notice)
  
  return notices
  
