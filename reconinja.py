import sys
import re
from bs4 import BeautifulSoup
import requests

def block_print(content):
        print("-" * 30)
        print(content)
        print("-" * 30 + "\n")

def sublock_print(content):
        print(content)
        print("-"* 30)

class reconinja:
    def __init__(self,url,level):
        self.url = url
        self.level = level

    def extract_links_from_url(self,url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = [a['href'] for a in soup.find_all('a', href=True)]
        return links

    def robotsregex(self,content):
        # Regular expression to capture Allow and Disallow rules
        pattern = r'(Allow|Disallow):\s*(/[^\s]*)'

        # Find all matches
        matches = re.findall(pattern, content)

        # Organize the matches into a dictionary
        rules = {'Allow': [], 'Disallow': []}
        for action, path in matches:
            rules[action].append(path)
        print("Allow:")
        for path in rules['Allow']:
            print(f" {self.url}{path}")
        print("\nDisallow:")
        for path in rules['Disallow']:
            print(f"  {self.url}{path}")

    def robotsanalysis(self):
         block_print("Robots.txt assets")
         sublock_print("URLs")
         print(rn.extract_links_from_url(self.url+"/robots.txt"))
         sublock_print("File Paths")
         rn.robotsregex(requests.get(self.url+"/robots.txt").text)

input_url = sys.argv[1]
rn = reconinja(input_url,1)
rn.robotsanalysis()