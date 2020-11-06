'''치과대학 공지 crawl'''
'''
    본문 표 구현하기
    본문 크롤링하기
    치과대학 공지에는 이미지 존재 X
'''

import pandas as pd
import requests
from bs4 import BeautifulSoup
import re

URL = "https://dent.knu.ac.kr/community/notice/list.jsp?page=1&gubun=&svalue=&group="

def dent_extract_indeed_pages():  # last page return
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, "html.parser")

    links = soup.find_all("a", {"onfocus": "this.blur()"})
    link = links[-2]
    link = link.attrs["href"]
    link = re.findall("\d+", link)
    max_page = int(link[0])

    return max_page

def dentistry_crawl(notice_url):
    link = requests.get(notice_url)
    soup = BeautifulSoup(link.text, "html.parser")
    title_html = soup.find("td", {"height":"30"})
    title = title_html.string

    dt_html = soup.find_all("td", {"width":"90"})
    modify_dt = dt_html[2].string

    #dent_content_text(notice_url)

    image_url = []

    url = notice_url
    download_url = dent_extract_content_attach(notice_url)

    dict_data = {'title': title, 'modify_dt': modify_dt, 'content': 'content', 'type': "치과대학", 'url': url, 'image_url': image_url,'download_url': download_url}
    return dict_data

''' 본문 크롤링(표 수정필요)
def dent_content_text(notice_url):
    content_text = ""
    alldfcontents = []
    link = requests.get(notice_url)
    soup = BeautifulSoup(link.text, "html.parser")
    cont_html = soup.find("td", {"style":"padding:15 15 15 15;"})
    conts = cont_html.find_all("p") 
    for cont in conts:
        try:
            table_html = cont.find("table")
            data_table = dent_content_table(table_html, alldfcontents)
            content_text = content_text + "<<<<<<TABLE>>>>>>>" + "\n"
            #alldfcontents = []
        except AttributeError as e:
            text = cont.get_text()
            text = text.replace('\n', '')
            if (dent_content_table_remove_doubling(alldfcontents, text) == 0):
                content_text = content_text + text + "\n"
            #print("NONE")
        #else:
            #print(table_html)
    print(content_text)
    print(alldfcontents)

def dent_content_table(table_html, alldfcontents): #본문 표 정리
    dfcontent=[] #column 뽑아내기
    #alldfcontents = []
    #alldfcontents=[] #column단위 data저장
    tables = table_html.find_all("tr")

    for table in tables:
        tds=table.find_all("td")
        for td in tds:
            data = td.get_text()
            data = data.replace('\n', '')
            dfcontent.append(data)
        alldfcontents.append(dfcontent)
        dfcontent=[]
    df=pd.DataFrame(alldfcontents)
    return df

def dent_content_table_remove_doubling(data_list, data_text):
    for row in data_list:
        for data in row:
            if (data == data_text):
                return 1
    return 0
'''
def dent_extract_content_attach(notice_url): #본문 첨부파일
    attach = []
    extension = [] # 첨부파일 확장자
    basic_url = "https://dent.knu.ac.kr"
    result = requests.get(notice_url)
    soup = BeautifulSoup(result.text, "html.parser")

    attach_html = soup.find("td", {"width":"650"})
    attach_hrefs = attach_html.find_all("a", {"onfocus": "this.blur()"})

    try:
        attach_hrefs = attach_html.find_all("a", {"onfocus": "this.blur()"})
        attach_urls = attach_hrefs
    except AttributeError as e:
        return attach

    for attach_url in attach_urls:
        attach_extension = attach_url.get_text()
        attach_extension = attach_extension[-3:]
        extension.append(attach_extension)

        sub_url = attach_url.attrs["href"]
        final_url = basic_url + sub_url
        attach.append(final_url)

    return attach

    
def dent_extract_indeed_notices(last_pages):
    notices = []
    count = 0

    for page in range(1,last_pages+1): #last_pages+1로 변경
        link = requests.get(f"https://dent.knu.ac.kr/community/notice/list.jsp?page={page}&gubun=&svalue=&group=")
        soup = BeautifulSoup(link.text, "html.parser")
        results = soup.find_all("td", {"width":"345"})

        for result in results[1:]:
            notice_url = result.find("a").attrs["href"]
            notice_url = "https://dent.knu.ac.kr/community/notice/" + notice_url
            count = count + 1
            notice = dentistry_crawl(notice_url)
            print(f"{page - 1}page {count}번 게시물 crawling")
            print(notice)
            notices.append(notice)
    return notices


def dent_check_latest(): # latest notice title return
    link = requests.get(URL)
    soup = BeautifulSoup(link.text, "html.parser")
    results = soup.find_all("td", {"width":"345"})

    for result in results[1:2]:
        notice_url = result.find("a").attrs["href"]
        notice_url = "https://dent.knu.ac.kr/community/notice/" + notice_url
        notice = dentistry_crawl(notice_url)

    return notice['title']

def dent_extract_latest_notices(latest): # 게시물 업데이트
    notices = []
    page = 1
    link = requests.get(f"https://dent.knu.ac.kr/community/notice/list.jsp?page={page}&gubun=&svalue=&group=")
    soup = BeautifulSoup(link.text, "html.parser")
    results = soup.find_all("td", {"width":"345"})

    for result in results[1:]:
        notice_url = result.find("a").attrs["href"]
        notice_url = "https://dent.knu.ac.kr/community/notice/" + notice_url
        notice = dentistry_crawl(notice_url)
        if notice['title'] == latest: 
            break
        notices.append(notice)

    return notices