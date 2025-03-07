import requests

from bs4 import BeautifulSoup 

jobList = []

def scrapePage(url):
  print(f"scrapping {url}...")
  response = requests.get(url)

  soup = BeautifulSoup(response.content, "html.parser")

  jobs = soup.find("section", class_ = "jobs").find_all("li", class_ = "new-listing-container")
  jobs = [job for job in jobs if "metana-ad" not in job.get("class", [])]

  for job in jobs:
    title = job.find("h4", class_ = "new-listing__header__title").text
    region = job.find_all("p", class_ = "new-listing__categories__category")[-1].text
    company = job.find("p", class_ = "new-listing__company-name").text
    url = job.find_all("a")[1]["href"]
    jobData = {
      "title" : title,
      "company" : company,
      "region" : region,
      "url": f"https://weworkremotely.com{url}"
    }
    jobList.append(jobData)

def getPages(url):
  response = requests.get("https://weworkremotely.com/remote-full-time-jobs")
  soup = BeautifulSoup(response.content, "html.parser")
  return len(soup.find("div", class_= "pagination").find_all("span",class_= "page"))

url = "https://weworkremotely.com/remote-full-time-jobs"

pages = getPages(url)

for x in range(pages):
    scrapePage(f"{url}?page={x+1}")

print(len(jobList))