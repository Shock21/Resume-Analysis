from bs4 import BeautifulSoup
import pdfkit
import requests
from Extractor import listElements

def extractPdf( resumeAddress ):
    page = requests.get(resumeAddress, allow_redirects = False)
    soup = BeautifulSoup(page.text, 'html.parser')
    resume = soup.find(id = "divResumeHTML")
    if resume is None:
        return None
    resume.find("div", {'id': 'document'})['style'] = 'margin: 0 auto'
    return resume

def getPageNumbers( link ):
    page = requests.get(livecareer)
    soup = BeautifulSoup(page.text, 'html.parser')

    resume = soup.find("ul", {"class": "pagination"})
    listElements = resume.findChildren('li')
    return int(listElements[-2].a.string)
    

livecareer = 'https://www.livecareer.com/resume-search/search?jt=manager&bg=85&eg=100&comp=&mod=&pg='

counter = 0
pages = getPageNumbers(livecareer + '1')

for i in range (1, pages):
    page = requests.get(livecareer + str(i))
    soup = BeautifulSoup(page.text, 'html.parser')

    list = soup.find("ul", {"class": "resume-list list-unstyled"})

    listElements = list.findChildren('li')
    del listElements[0]
    
    for li in listElements:
        finalResume = extractPdf('https://www.livecareer.com' + li.a['href'])
        if finalResume is None:
            continue
        pdfkit.from_string(str(finalResume), '/home/shock21/Desktop/ResumeDataset/resume-' + str(counter) + '.pdf')
        counter += 1
