from playwright.sync_api import sync_playwright
import time
from bs4 import BeautifulSoup
import csv

def webScraper(keywords):
  for keyword in keywords:
    p = sync_playwright().start()
    browser = p.chromium.launch()
    page = browser.new_page()
    #open chrome using playwright
    page.goto("https://www.wanted.co.kr/")
    page.click("button.Aside_searchButton__rajGo")
    page.get_by_placeholder("검색어를 입력해 주세요.").fill(keyword)
    page.keyboard.down("Enter")
    page.click("a#search_tab_position")
    for x in range(4):
      page.keyboard.down("End")
    #move to page want

    content = page.content()
    p.stop()
    soup = BeautifulSoup(content, "html.parser")
    jobs = soup.find_all("div", class_= "JobCard_container__REty8")
    jobs_db = []
    #save html using BeautifulSoup

    for job in jobs:
      link = f"https://wanted.co.kr{job.find('a')['href']}"
      title = job.find("strong", class_= "JobCard_title__HBpZf").text
      company = job.find("span", class_= "JobCard_companyName__N1YrF").text
      job = {
        "title" : title,
        "link" : link,
        "company" : company
      }
      jobs_db.append(job)
    #get information need by text from html

    file = open(f"{keyword} jobs.csv", "w")
    writer = csv.writer(file)
    writer.writerow(["title", "company", "link"])
    for job in jobs_db:
      writer.writerow(job.values())
    #save information to csv file

keywords = ["react", "javascript", "c++"]

webScraper(keywords)