from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np

pageLinks = [
    "https://thebimhub.com/companies/?&selected_facets=type_exact%3AService%20Providers&selected_facets=country_exact%3AUnited%20Kingdom&page=",
    "https://thebimhub.com/companies/?&selected_facets=type_exact%3AConsultants&selected_facets=country_exact%3AUnited%20Kingdom&page=",
]

noPages = [4,8]
companyTypes = ["Service Provider", "Consultant"]

allProviders = []
filename = "Providers.txt"
companyPageLink = "https://thebimhub.com"
companies = []

for j in range(0, len(pageLinks)):
    noSpecificPages=noPages[j]
    for i in range(1, noSpecificPages+1):
        pageLink = pageLinks[j] + str(i)
        pageResponse = requests.get(pageLink)
        pageContent = BeautifulSoup(pageResponse.content, "html.parser")

        for div in pageContent.find_all('div', {'class': 'media-body'}):
            # Reset all parameters
            individualCompany = []
            companyName = ""
            companyDescription = ""
            companyWebsite = ""

            # Get company details
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
                individualCompany.append(companyTypes[j])
                individualCompany.append(companyDescription.text.replace('\n', ''))
                individualCompany.append(companyWebsite)
                companies.append(individualCompany)

columns = ['Name','Type','Description','Website']
dataframe = pd.DataFrame(companies, columns=columns)
dataframe.to_csv('./Firms.csv', encoding='utf-8', index=False)
