from bs4 import BeautifulSoup
import urllib.request
import random
import ssl

class HackerFetcher:
  def __init__(self, hacker_id):
    self.hacker_id = hacker_id
    self.url = f'https://devpost.com/{hacker_id}'
    ssl_context = ssl.SSLContext()
    source = urllib.request.urlopen(self.url, context=ssl_context).read()
    self.soup = BeautifulSoup(source, 'lxml')
  
  def get_hackathon_count(self):
    return self.soup.find(href=f'/{self.hacker_id}/challenges').find(class_='totals').text
  
  def get_skills(self):
    portifolio_tags = self.soup.find(class_='portfolio-tags')
    skills_tags = portifolio_tags.find_all('li')
    return [
      {
        'title': tag.text, 
        'href': (atag := tag.find('a')) and atag['href']
      } 
      for tag in skills_tags
    ]
  
  def get_projects(self):
    project_tags = self.soup.find(id='software-entries').find_all(class_='gallery-item')
    contributor_tags = lambda curr_tag: member_tags.find_all('span', class_='user-profile-link') if (member_tags := curr_tag.find(class_='members')) else []
    return [
      {
        'thumbnail': (img := tag.find('img', class_='software_thumbnail_image')) and img['src'],
        'href': (a := tag.find('a', class_='link-to-software')) and a['href'],
        'title': (title_div := tag.find('div', class_='software-entry-name')) and title_div.find('h5').text.strip(),
        'description': (description_div := tag.find('div', class_='software-entry-name')) and description_div.find('p').text.strip(),
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

def fetch_hacker_stats(hacker_request):
  if 'id' in hacker_request:
    hacker_id = hacker_request.get('id')
    # TODO: raise ValueError in case hacker_id is not found
    fetcher = HackerFetcher(hacker_id)
    projects = fetcher.get_projects()
    skills = fetcher.get_skills()
    random.shuffle(projects)
    random.shuffle(skills)
    return {
      'hacker_id': hacker_id,
      'hacker_url': fetcher.url,
      'hackathon_count': fetcher.get_hackathon_count(),
      'projects': projects,
      'skills': skills
    }
  raise KeyError('id must be present in request')