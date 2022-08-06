from operator import contains
import os
from bs4 import BeautifulSoup
import requests
import pandas as pd
import random
my_headers = [
    {'User-Agent':"Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"},
    {'User-Agent':"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36"},
    {'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0"},
    {'User-Agent':"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14"},
    {'User-Agent':"Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)"},
    {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11'},
    {'User-Agent':'Opera/9.25 (Windows NT 5.1; U; en)'},
    {'User-Agent':'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)'},
    {'User-Agent':'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)'},
    {'User-Agent':'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12'},
    {'User-Agent':'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9'},
    {'User-Agent':"Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7"},
    {'User-Agent':"Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0 "}
]
uagent=random.choice(my_headers)
proxy="8.219.97.248:80"
#end of the head

##############################
#the first part of the url the part befor the page number
url_part1=''
#the seconed part of the url the part after the page number
url_part2=''
#the first page you wish to star scraping
start=15
#the page after the last page you wish to scrap
end=20
#the list that will hold all the titles of the article
list_article_title=[]
#the list that will hold the year of puplish
list_year=[]
#the list that will hold the authoers
list_author=[]
#the journal where the article was puplished
list_journal=[]
#the links for the aricles
list_links=[]
#the list for the article abstracts
list_abstract=[]
#the doi list
list_doi=[]
#the fin;e data
end_data=[]

#the function to get all the titles it take the page of the titles
def get_articls_name_by_page(num):
    title_list=[]    
    response=requests.get(f"{url_part1}{num}{url_part2}",headers=uagent )
    print(response)
    html=response.text
    soup=BeautifulSoup(html,'html.parser')
    articals_title=soup.find_all("a", {"class": "title"})
    for i in articals_title:
        title_list.append(i.text)
        print(i.text)
        print("//////////////////////")
    return title_list
def get_articls_year_by_page(num):
    year_list=[]
    response=requests.get(f"{url_part1}{num}{url_part2}",headers=uagent )
    print(response)
    html=response.text
    soup=BeautifulSoup(html,'html.parser')
    articals_year=soup.find_all("span", {"class": "year"})
    for i in articals_year:
        year_list.append(i.text)
        print(i.text)
        print("//////////////////////")
    return year_list
def get_articls_author_by_page(num):
    author_list1=[]
    no_author_list=[]
    response=requests.get(f"{url_part1}{num}{url_part2}",headers=uagent )
    print(response)
    html=response.text
    soup=BeautifulSoup(html,'html.parser')
    no_author_list2=soup.find_all("p",{"class":"meta"})
    articals_author=[]
    for i in range(len(no_author_list2)):
        articals_author.append(no_author_list2[i].find("span", {"class": "authors"}))
        try:
            author_list1.append(articals_author[i].text)
        except:
            pass
        print(articals_author[i])
        print("//////////////////////")
    
    
    for i in range(len(no_author_list2)):
        if  not no_author_list2[i].find("span",{"class":"authors"}) and no_author_list2[i].find("span",{"class":"year"}):
            
            no_author_list.append(i)
        else:
            pass
    if no_author_list:
        for i in no_author_list:
            print(i)
            author_list1.insert(i,"no authors")
    
    return author_list1
def get_journal_by_page(num):
    journal_list=[]
    response=requests.get(f"{url_part1}{num}{url_part2}",headers=uagent )
    print(response)
    html=response.text
    soup=BeautifulSoup(html,'html.parser')
    articals_journal=soup.find_all("a", {"class": "publication-title"})
    for i in range(len( articals_journal)):
        
        journal_list.append(articals_journal[i].text)
        print(articals_journal[i].text)
        print("//////////////////////")
    
    
    return journal_list
def get_links_by_page(num):
    link_list=[]
    response=requests.get(f"{url_part1}{num}{url_part2}",headers=uagent )
    print(response)

    html=response.text
    soup=BeautifulSoup(html,'html.parser')
    articals_d=soup.find_all("a", {"class": "title"},href=True)
    for i in articals_d:
        
        link_list.append("https://link.springer.com/"+i['href'])
        print("https://link.springer.com/"+i['href'])
        print("//////////////////////")
    return link_list
def get_abstract_by_page(link):
    abstract_list=[]
    
    
    responce=requests.get(link,headers=uagent)
    html=responce.text
    soup=BeautifulSoup(html,'html.parser')
    articals_d=[]
    articals_d=soup.find_all("div",{"id":"Abs1-section"})
    if(articals_d):
        for i in articals_d:
            abstract_list.append(i.text)
            print(i.text)
            print("//////////////////////")
        return abstract_list
    else:
        abstract_list=[]
        abstract_list.append("no abstract")
        print("no abstract")
        print("//////////////////////")
        return abstract_list
def get_doi_by_page(link):
    doi_list=[]
    
    doi="https://doi.org/"
    list2=link.split("/")
    doi_list.append(f"{doi}{list2[-2]}/{list2[-1]}")
    print(f"{doi}{list2[-2]}/{list2[-1]}")
    print("//////////////////////")
    return doi_list
for i in range(start,end):
    list_article_title.append( get_articls_name_by_page(i))
for i in list_article_title:
    print(i)
    print("//////////////////////")
for i in range(start,end):    
    list_year.append( get_articls_year_by_page(i))
    
for i in list_year:
    print(i)

for i in range(start,end):
    
    
    list_author.append(get_articls_author_by_page(i))
    

for i in list_author:
    print(i)
    print("//////////////////////")
for i in range(start,end):
    
    list_journal.append(get_journal_by_page(i))
    

for i in list_journal:
    print(i)
    print("/////////////////")
for i in range(start,end):

    list_links.append(get_links_by_page(i))


for i in list_links:
    print(i)
    print("/////////////////")

for i in list_links:
    for j in i:
        print(j)
        list_abstract.append(get_abstract_by_page(j))

for i in list_abstract:
    print(i)
    print("/////////////////")
for i in list_links:
    for j in i:
        print(j)
        list_doi.append(get_doi_by_page(j))

for i in list_doi:
    print(i)
    print("////////////////////")

#the dict that will hold all the lists
dict1={'YEAR':"",
       'AUTHOR':"",
       'Journal':"",
       'link':"",
       'DOI':"",
       'Title':"",
       'Abstract':"",
       }
YEAR_list=[]
for a in range(len(list_year)):
    for b in range (len(list_year[a])):
        YEAR_list.append(list_year[a][b])

AUTHOR_list=[]
for a in range(len(list_author)):
    for b in range (len(list_author[a])):
        AUTHOR_list.append(list_author[a][b])
Journal_list=[]
for a in range(len(list_journal)):
    for b in range (len(list_journal[a])):
        Journal_list.append(list_journal[a][b])
link_list=[]
for a in range(len(list_links)):
    for b in range (len(list_links[a])):
        link_list.append(list_links[a][b])
DOI_list=[]
for a in range(len(list_doi)):
    for b in range (len(list_doi[a])):
        DOI_list.append(list_doi[a][b])
Title_list=[]
for a in range(len(list_article_title)):
    for b in range (len(list_article_title[a])):
        Title_list.append(list_article_title[a][b])
Abstract_list=[]
for a in range(len(list_abstract)):
    for b in range (len(list_abstract[a])):
        Abstract_list.append(list_abstract[a][b])
for i in range (len(YEAR_list)):
    dict1={'YEAR':YEAR_list[i],
       'AUTHOR':AUTHOR_list[i],
       'Journal':Journal_list[i],
       'link':link_list[i],
       'DOI':DOI_list[i],
       'Title':Title_list[i],
       'Abstract':Abstract_list[i],
       }
    end_data.append(dict1)
for i in end_data:
    print(i)
df=pd.DataFrame(end_data)
df.to_excel("data.xlsx",index=False)