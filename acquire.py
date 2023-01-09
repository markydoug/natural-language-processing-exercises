from bs4 import BeautifulSoup
import pandas as pd

import requests


def get_blog_articles():
    '''
    Collects article info of the last five blog articles
    on the Codeup blog and returns a dictionary
    '''
    url = 'https://codeup.com/blog/'
    headers = {'User-Agent': 'Codeup Data Science'}
    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.content, 'html.parser')
    # get all titles
    h2 = soup.find_all('h2')
    # create a dictionary to hold the title and content of the article
    blog_articles = {
        'title':[],
        'content':[],
        'published_date':[]
    }
    for n in range(len(h2)-2):
        #title
        blog_articles['title'].append(h2[n].a.text)
        soup2 = BeautifulSoup(requests.get(h2[n].a['href'], headers=headers).content, 'html.parser')
        
        #content
        paragraphs = soup2.find('div', class_='entry-content').find_all('p')
        content =''
        for t in paragraphs:
            if not t.text.startswith('*Codeup'):
                content += f' {t.text}'
            else:
                break
        blog_articles['content'].append(content)
        
        # date
        dates = soup2.find('span', class_='published')
        date = ''
        for d in dates:
            date += d.text
        blog_articles['published_date'].append(d)
        
    return blog_articles