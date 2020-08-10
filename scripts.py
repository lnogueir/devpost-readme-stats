#%%
import bs4 as bs
import urllib.request
import ssl

# %%
ssl_context = ssl.SSLContext()
url = 'https://devpost.com/lnogueir'
source = urllib.request.urlopen(url, context=ssl_context).read()

soup = bs.BeautifulSoup(source, 'lxml')

#%%
portifolio_tags = soup.find(class_='portfolio-tags')
tech_tags = portifolio_tags.find_all('li')
project_tags = soup.find(id='software-entries').find_all(class_='gallery-item')
#%%
skills = [
  {
    'title': tag.text, 
    'href': tag.find('a') and tag.find('a')['href']
  } 
  for tag in tech_tags
]


# %%
f = open('templates/default.svg', 'r')
template = f.read()


# %%
import random
a = [1,2,3]
random.shuffle(a)



# %%
