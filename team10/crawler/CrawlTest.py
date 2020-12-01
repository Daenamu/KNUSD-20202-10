from haksaCrawl import extract_indeed_pages, extract_indeed_notices
from dentistryCrawl import dent_extract_indeed_pages, dent_extract_indeed_notices
from childCrawl import child_extract_indeed_pages, child_extract_indeed_notices

'''crawl 테스트용'''

#학사공지 crawl test
#last_indeed_page = extract_indeed_pages()
#indeed_jobs = extract_indeed_notices(last_indeed_page)

#치과대학 crawl test
#last = dent_extract_indeed_pages()
#dent_extract_indeed_notices(last)

#아동학부 crawl test
pages = child_extract_indeed_pages()
child_extract_indeed_notices(pages)