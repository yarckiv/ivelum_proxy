import requests
import re
from bs4 import BeautifulSoup


class HabrPars:
    root_url = 'https://habr.com'

    def get_text(self, new_url, endpoint):
        url = f'{self.root_url}/{endpoint}/'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36',
            'Content-Type': 'text/html', }
        try:
            r = requests.get(url, headers=headers)
        except requests.exceptions.HTTPError as e:
            print(f'Request error: {e}')
        else:
            mod_text = self.wrap_text(new_url, r.text)
            return mod_text

    def wrap_text(self, new_url, text):
        soup = BeautifulSoup(text, 'lxml')
        for a in soup.find_all('a'):
            try:
                if a.get('href').__contains__(self.root_url):
                    a['href'] = a['href'].replace(self.root_url, new_url)
            except AttributeError:
                pass
        match = r'\b(\w{6})\b'
        for script in soup(["script", "style"]):
            script.decompose()
        for txt in soup.findAll(text=True):
            if re.search(match, txt, re.I):
                newtext = re.sub(match, r'\1' + '<sup>TM</sup>', txt.lower())
                txt.replaceWith(newtext)
        return soup.prettify(formatter=None, encoding="ascii")
