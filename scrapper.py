#%%
import bs4 as bs
import urllib.request
import ssl

# %%
ssl_context = ssl.SSLContext()
url = 'https://devpost.com/lnogueir'
source = urllib.request.urlopen(url, context=ssl_context).read()

soup = bs.BeautifulSoup(source, 'lxml')

portifolio_tags = soup.find(class_='portfolio-tags')
tech_tags = portifolio_tags.find_all('li')



# %%
f = open('templates/default.svg', 'r')
template = f.read()


# %%
