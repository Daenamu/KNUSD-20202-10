from haksaCrawl import extract_indeed_pages, extract_indeed_notices
import requests
from bs4 import BeautifulSoup
#학사공지 crawl test

last_indeed_page = extract_indeed_pages()
indeed_jobs = extract_indeed_notices(last_indeed_page)