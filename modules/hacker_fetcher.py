from bs4 import BeautifulSoup
import base64
import requests
import urllib.request
import ssl
import os

class HackerFetcher:
  def __init__(self, hacker_id):
    self.hacker_id = hacker_id
    self.url = f'https://devpost.com/{hacker_id}'
    ssl_context = ssl.SSLContext()
    source = urllib.request.urlopen(self.url, context=ssl_context).read()
    self.soup = BeautifulSoup(source, 'lxml')
  
  def get_hackathon_count(self):
    return self.soup.find(href=f'/{self.hacker_id}/challenges').find(class_='totals').text

  def get_hacker_name(self):
    portfolio_tag = self.soup.find(id='portfolio-user-name')
    portfolio_tag.find('small').extract()
    return portfolio_tag.text.strip()
  
  def get_skills(self):
    portifolio_tags = self.soup.find(class_='portfolio-tags')
    skills_tags = portifolio_tags.find_all('li')
    return [
      {
        'title': tag.text, 
        'href': atag['href'] if (atag := tag.find('a')) else '#'
      } 
      for tag in skills_tags
    ]
  
  def get_projects(self):
    project_tags = self.soup.find(id='software-entries').find_all(class_='gallery-item')
    contributor_tags = lambda curr_tag: member_tags.find_all('span', class_='user-profile-link') if (member_tags := curr_tag.find(class_='members')) else []
    return [
      {
        'thumbnail': (img := tag.find('img', class_='software_thumbnail_image')) and get_base64_img_from(img['src']),
        'href': (a := tag.find('a', class_='link-to-software')) and a['href'],
        'title': (title_div := tag.find('div', class_='software-entry-name')) and title_div.find('h5').text.strip(),
        'description': (description_div := tag.find('div', class_='software-entry-name')) and description_div.find('p').text.strip(),
        'is_winner': tag.find(class_='winner') != None,
        'contributors': [
          {
            'img': (member_img_tag := member_tag.find('img')) and member_img_tag['src'], 
            'href': (member_href_tag := member_tag.find(attrs={'data-url': True})) and member_href_tag['data-url']
          }
          for member_tag in contributor_tags(tag)
        ]
      }
      for tag in project_tags
    ]


def get_base64_img_from(url):
  base64_str = 'data:image/'
  file_ext = os.path.splitext(url)[1]
  if file_ext == '.jpg' or file_ext == '.jpeg':
    base64_str += 'jpeg'
  elif file_ext == '.png':
    base64_str += 'png'
  elif file_ext == '.svg':
    base64_str += 'svg+xml'
  elif file_ext == '.gif':
    base64_str += 'gif'
  elif file_ext == '.tiff' or file_ext == '.tif':
    base64_str += 'tiff'
  elif file_ext == '.ico' or file_ext == '.cur':
    base64_str += 'x-icon'
  elif file_ext == '.bmp':
    base64_str += 'bmp'
  elif file_ext == '.webp':
    base64_str += 'webp'

  bin_img_content = base64.b64encode(requests.get(url).content)
  str_img_content = bin_img_content.decode('utf-8')
  base64_str += f';base64,{str_img_content}'
  return base64_str
