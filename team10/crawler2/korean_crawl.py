import requests
from bs4 import BeautifulSoup
# 국어국문학과 공지 crawl

URL = "http://korean.knu.ac.kr"

def korean_newnotice_crawl(URL):
    req = requests.get(URL)
    html = req.text
    soup = BeautifulSoup(html,'html.parser')
    checklist = []
    noticesCrop = soup.find("div",{"class": "notice"})
    noticeList = noticesCrop.find_all("li")
    for notice in noticeList: #최신 게시물들을 크롤링
        korean_crawl(notice)
        
def korean_crawl(notice):
    title = notice.find("a").get_text()
    herf = notice.find("a").get("href")
    content = extract_content_txt(herf)
    image_url = extract_content_image(herf)
    download_url = extract_content_attach(herf)
    modify_dt = extract_content_date(herf)
    dict = {'title': title, 'modify_dt': modify_dt, 'content': content, 'type': "학사공지", 'url': herf, 'image_url': image_url,'download_url': download_url}
    return dict

def extract_content_txt(url):
    req = requests.get(url)
    html = req.text
    soup = BeautifulSoup(html,'html.parser')
    contents = soup.find("div",{"id" : "bo_v_con"}).get_text()
    return content

def extract_content_image(url):
    req = requests.get(url)
    html = req.text
    soup = BeautifulSoup(html,'html.parser')
    cont = soup.find("div",{"id" : "bo_v_img"})
    image = cont.find("img").get("src")
    filename = image[-4:]
    return image

def extract_content_attach(url):
    req = requests.get(url)
    html = req.text
    soup = BeautifulSoup(html,'html.parser')
    cont = soup.find("section",{"id": "bo_v_file"})
    downloadlink = cont.find("a")["href"]
    fname = cont.find("a").get_text(strip=True)
    fname = fname.split(".")
    filename = "."+fname[1][:3]
    return downloadlink

def extract_content_date(url):
    req = requests.get(url)
    html = req.text
    soup = BeautifulSoup(html,'html.parser')
    cont = soup.find("section",{"id": "bo_v_file"})
    dte = cont.find_all("span")
    date = date[1].get_text()[7:]
    return date

