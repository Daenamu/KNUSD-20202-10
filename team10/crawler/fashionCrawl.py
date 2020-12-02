import requests
from bs4 import BeautifulSoup
import re
#의류학과

URL = "http://fashion.knu.ac.kr/HOME/fashion/sub.htm?nav_code=fas1465867647"

def fashion_extract_indeed_pages():  # page href list
    pages = [URL]
    base_url = "http://fashion.knu.ac.kr"

    result = requests.get(URL)
    soup = BeautifulSoup(result.text, "html.parser")

    link = soup.find("div", {"class": "paging"})
    links = link.find_all("a")

    for page in links:
        link = page.attrs["href"]
        link = base_url + link
        pages.append(link)

    return pages


def fashion_extract_content_image(url): # 본문 이미지
    base_url = "http://fashion.knu.ac.kr/HOME"
    images = []
    extension = [] # 본문 이미지 파일 확장자
    result = requests.get(url)
    soup = BeautifulSoup(result.text, "html.parser")
    cont = soup.find("div", {"class":"cont"})
    imgs = cont.find_all("a")

    for img in imgs:
        src = img.find("img")
        src = src.attrs["src"]
        src = src[len(".."):]
        src = base_url + src
        alt = img.attrs["title"]
        alt = alt[-9:-6]
        images.append(src)
        extension.append(alt)
    return images


def fashion_extract_content_attach(url):
    attach = []
    extension = [] # 첨부파일 확장자
    base_url = "http://fashion.knu.ac.kr"
    result = requests.get(url)
    soup = BeautifulSoup(result.text, "html.parser")

    try:
        cont = soup.find("div", {"class":"board_view"})
        attach_html = cont.find("table")
        attach_href = attach_html.find_all("a")
        attach_hrefs = attach_href
    except AttributeError as e:
        return attach

    for attach_href in attach_hrefs:
        attach_url = attach_href.attrs["href"] #../../
        attach_url = base_url + attach_url[len("../.."):]
        attach.append(attach_url)
        ext = attach_href.get_text()
        ext = ext[-3:]
        extension.append(ext)
    
    return attach


def fashion_crawl(notice_url):
    link = requests.get(notice_url)
    soup = BeautifulSoup(link.text, "html.parser")

    title_html = soup.find("div", {"class":"board_view"})
    title = title_html.find("h2")
    title = title.get_text()

    modify_html = title_html.find("table")
    modify_htmls = modify_html.find_all("td")
    modify_dt = modify_htmls[1].get_text()

    cont_html = soup.find("div", {"class":"cont"})
    cont = str(cont_html)
    cont = cont.replace("<br/>", '\n')
    cont = cont.replace("<br>", '\n')
    cont = cont.replace("</br>", '\n')
    cont = re.sub("<.+?>",'', cont, 0).strip()
    cont = cont.replace("&lt;", '<')
    cont = cont.replace("&gt;", '>')
    content = cont

    url = notice_url

    image_url = fashion_extract_content_image(notice_url)

    download_url = fashion_extract_content_attach(notice_url)
    
    dict_data = {'title': title, 'modify_dt': modify_dt, 'content': content, 'type': "의류학과", 'url': url, 'image_url': image_url,'download_url': download_url}
    return dict_data


def check_fixed_notice(notice_html): #공지사항 상단 고정 확인 인수 반환
    check = notice_html.find("td")
    check = check.attrs["class"]
    return check[-1]


def fashion_extract_indeed_notices(list_pages):
    notices = []
    page_num = 0
    count = 0
    base_url = "http://fashion.knu.ac.kr"

    for page in list_pages: 
        page_num = page_num + 1
        link = requests.get(page)
        soup = BeautifulSoup(link.text, "html.parser")
        result = soup.find("div", {"class":"board_list"})
        results = result.find_all("tr")

        for result in results[1:]:
            che = check_fixed_notice(result)
            if (che == "fst"):
                notice_td = result.find("td", {"class":"subject"})
                notice_url = notice_td. find("a").attrs["href"]
                notice_url = base_url + notice_url
                notice = fashion_crawl(notice_url)
                count = count + 1
                print(f"{page_num}page {count}번 게시물 crawling")
                #print(notice)
                notices.append(notice)
    return notices


def fashion_check_latest(): # latest notice title return
    base_url = "http://fashion.knu.ac.kr"
    link = requests.get(URL)
    soup = BeautifulSoup(link.text, "html.parser")
    result = soup.find("div", {"class":"board_list"})
    results = result.find_all("tr")

    for result in results[1:]:
        che = check_fixed_notice(result)
        if (che == "fst"):
            notice_td = result.find("td", {"class":"subject"})
            notice_url = notice_td. find("a").attrs["href"]
            notice_url = base_url + notice_url
            notice = fashion_crawl(notice_url)
            break
    return notice['title']


def fashion_extract_latest_notices(latest): # 게시물 업데이트
    notices = []
    base_url = "http://fashion.knu.ac.kr"
    link = requests.get(URL)
    soup = BeautifulSoup(link.text, "html.parser")
    result = soup.find("div", {"class":"board_list"})
    results = result.find_all("tr")

    for result in results[1:]:
        che = check_fixed_notice(result)
        if (che == "fst"):
            notice_td = result.find("td", {"class":"subject"})
            notice_url = notice_td. find("a").attrs["href"]
            notice_url = base_url + notice_url
            notice = fashion_crawl(notice_url)
            if notice['title'] == latest: 
                break
            notices.append(notice)

    return notices