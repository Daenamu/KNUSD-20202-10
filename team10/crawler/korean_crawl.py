import requests
from bs4 import BeautifulSoup
# 국어국문학과 공지 crawl

PAGE = 1
URL = f"http://korean.knu.ac.kr/bbs/board.php?bo_table=community01&page={PAGE}"

def extract_last_pages():
  result = requests.get(URL)
  soup = BeautifulSoup(result.text, "html.parser")

  pag = soup.find("span",{"class":"pg"})
  link = pag.find("a",{"class":"pg_page pg_end"}).attrs["href"]
  last_page = int(link[-2:])
  return last_page

def extract_content_text(url):
  result = requests.get(url)
  soup = BeautifulSoup(result.text, "html.parser")
  cont_text = soup.find("div",{"id":"bo_v_con"}).text
  return cont_text

def extract_content_image(url):
  images = []
  result = requests.get(url)
  soup = BeautifulSoup(result.text,"html.parser")
  cont = soup.find("div",{"id":"bo_v_img"})
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
  cont = soup.find("section",{"id":"bo_v_file"})
  if cont != None:
    attach_hrefs = cont.find_all("li")
    for attach_href in attach_hrefs:
     href = attach_href.find("a").attrs["href"]
     attach.append(href)
  return attach
    

def korean_crawl(html,url):
  title = html.find("h1",{"id":"bo_v_title"}).string.strip()
  dt = html.find_all("strong")[1].string
  modify_dt = dt.split(" ")
  modify_dt = modify_dt[0].replace("/","-")
  modify_dt = "20"+modify_dt
 
  content = extract_content_text(url)
  image_url = extract_content_image(url)
  download_url = extract_content_attach(url)

  dict_data = {'title':title, 'modify_dt':modify_dt, 'content':content, 'type':"국어국문학과", 'url':url, 'image_url':image_url, 'download_url':download_url}
  return dict_data

def extract_korean_notices(last_pages):
  notices = []
  count = 0

  for page in range(1,last_pages+1):
    link = requests.get(f"http://korean.knu.ac.kr/bbs/board.php?bo_table=community01&page={page}")
    soup = BeautifulSoup(link.text, "html.parser")
    results = soup.find_all("td",{"class":"td_subject"})

    for result in results:
      url = result.find("a").attrs["href"]
      re = requests.get(url)
      sop = BeautifulSoup(re.text,"html.parser")
      notice = korean_crawl(sop,url)
      notices.append(notice)
      count = count + 1
      print(f"{page}page {count}번 게시물 crawling")
  
  return notices 


def check_latest():
  notes = []
  page = 1
  link = requests.get(f"http://korean.knu.ac.kr/bbs/board.php?bo_table=community01&page={page}")
  soup = BeautifulSoup(link.text, "html.parser")
  results = soup.find_all("td",{"class":"td_subject"})
  tops = soup.find_all("tr",{"class":"bo_notice"})

  for top in tops:
    notes.append(top.find("td",{"class":"td_subject"}).text.strip())
  
  title = results[len(notes)].text.strip()
  
  return title
  

def extract_latest_notices(latest):
  notices = []
  page = 1
  link = requests.get(f"http://korean.knu.ac.kr/bbs/board.php?bo_table=community01&page={page}")
  soup = BeautifulSoup(link.text, "html.parser")
  results = soup.find_all("td",{"class":"td_subject"})

  if results != None:
    for result in results:
      url = result.find("a").attrs["href"]
      re = requests.get(url)
      sop = BeautifulSoup(re.text,"html.parser")
      notice = korean_crawl(sop,url)
      if notice['title'] == latest:
        break
      notices.append(notice)
  
  return notices
