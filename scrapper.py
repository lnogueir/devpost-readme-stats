#%%
import bs4 as bs
import urllib.request
# %%

source = urllib.request.urlopen('http://quotes.toscrape.com/').read()

soup = bs.BeautifulSoup(source, 'lxml')

soup.find_all(class_='quote')


