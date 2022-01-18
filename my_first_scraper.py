import requests as req
import re
from bs4 import BeautifulSoup


def request_github_trending(url):
    response = req.get(url)
    return response


def extract(html):
    soap = BeautifulSoup(html, "html.parser")
    rows = soap.find_all('article', {"class":["Box-row"]})
    if rows:
              return rows
    else:
              print("Failed in getting rows")
def transform(html_peace):
    my_hash = []
    for row in html_peace:
        h1_tag =  row.find(class_ = 'h3 lh-condensed')
        elem_data = {'deverloper': '', 'repository_name': '', 'nbr_stars': ''}
        tag_a = h1_tag.find('a')

        text = re.findall(r'[\w]+.*[\w]+',tag_a.get_text() )
        elem_data['deverloper'] =  text[0]
        elem_data['repository_name'] =  text[1]

        star_box = row.find(class_ = 'f6')
        star_elem = star_box.find('a')
        star_value =re.findall(r"[-+]?\d*\,?\d+|\d+",star_elem.text)
        elem_data['nbr_stars'] =  star_value[0]

        my_hash.append(elem_data)
        
    return my_hash

def formated(repositories_data):
    csv_string = 'Developer, Repository Name, Number of Stars'
    for i in repositories_data:
        csv_string += '\n' + ','.join(list(i.values()))
    return csv_string

def parse(url):
    response =  request_github_trending(url)
    
    if response.status_code == 200:
        rows =  extract(response.text)
        transformed_data = transform(rows)
        result = formated(transformed_data)
        return result
    else:
        print("FAILED !!!!!")
        
URL = 'https://github.com/trending'
rslt  = parse(URL)
print(rslt)