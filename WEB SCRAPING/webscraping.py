
import requests
from bs4 import BeautifulSoup
import pandas as pd
page = requests.get('https://www.nature.com/articles/s41598-023-28880-x')


html_file = BeautifulSoup(page.text, 'lxml')


title = html_file.findAll('title')
TITLE = str(title[0].text)
print("TITLE : \n",TITLE)


paras = html_file.findAll('p')
abstract = paras[5].text
print("ABSTRACT : \n",abstract)
print(len(abstract.split()))

body = html_file.find('div',class_="main-content")
body_content = body.text.split()
body_word_count = len(body_content)
print("Count of the article body text in words :",body_word_count)


imgs = html_file.findAll('img')
imgs_count = len(imgs)
print("Count of the number of images :",imgs_count)


references = html_file.findAll('li',class_='c-article-references__item js-c-reading-companion-references-item')

ref_lst = []

for reference in references:
    ref = reference.text
    ref = ref.replace('Google Scholar','')
    ref = ref.replace('Article','')
    ref = ref.replace('CAS','')
    ref = ref.replace('Â','')
    url=''
    print(ref)
    if "http" in ref:
        l= ref.find("http")
        url = ref[l:]
        ref=ref[:l]
    ref_dic = {
        'Reference' : ref,
        'Link' :url[:-1]
        }
    ref_lst.append(ref_dic)


paper_stats_dic = {"Tile":title[0].text,
       "Abstract":abstract,
       "Count of the article body text in words" : body_word_count,
       "Count of the number of images" : imgs_count}

paper_stats_DF = pd.DataFrame(paper_stats_dic,index=[1])

paper_stats_DF.to_csv('paper_stats.csv')


references_DF= pd.DataFrame(ref_lst)

references_DF.to_csv('references.csv')

print(paper_stats_DF)
print(references_DF)