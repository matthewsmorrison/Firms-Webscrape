from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np

corePageLink = "https://thebimhub.com/companies/?&selected_facets=type_exact%3AService%20Providers&page="
allProviders = []
filename = "Providers.txt"
noPages = 27
companyPageLink = "https://thebimhub.com"
companies = []


for i in range(0, noPages):
    pageLink = corePageLink + str(i)
    pageResponse = requests.get(pageLink)
    pageContent = BeautifulSoup(pageResponse.content, "html.parser")

    for div in pageContent.find_all('div', {'class': 'media-body'}):
        individualCompany = []
        companyBlock = div.find('a', {'class': 'black-link'})
        companyName = companyBlock.text
        companyLinkEnd = companyBlock['href']
        companyDescription = div.find('p')
        companyLink = companyPageLink + companyLinkEnd

        if(companyDescription != None):
            companyPageResponse = requests.get(companyLink)
            companyPageContent = BeautifulSoup(companyPageResponse.content, "html.parser")

            for subDiv in companyPageContent.find_all('div', {'class': 'col-md-8 col-xs-8'}):
                for allA in subDiv.find_all('a'):
                        if(allA.text.startswith("www") or allA.text.startswith("http")):
                            companyWebsite = allA.text

            for subDiv in companyPageContent.find_all('div', {'class': 'col-md-9 col-xs-9'}):
                for allA in subDiv.find_all('a'):
                    if(allA.text.startswith("www") or allA.text.startswith("http")):
                        companyWebsite = allA.text

            individualCompany.append(companyName.replace('\n', ''))
            individualCompany.append(companyDescription.text.replace('\n', ''))
            individualCompany.append(companyWebsite)
            companies.append(individualCompany)

columns = ['Name','Description','Website']
dataframe = pd.DataFrame(companies, columns=columns)
dataframe.to_csv('./Firms.csv', encoding='utf-8', index=False)
