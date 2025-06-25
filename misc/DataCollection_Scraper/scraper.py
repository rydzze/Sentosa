import re
import json
import time
import requests
from bs4 import BeautifulSoup

def scrape_wikipedia(url):
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        title = soup.find('h1', {'id': 'firstHeading'}).text.strip()
        content_div = soup.find('div', {'class': 'mw-parser-output'})
        extracted_text = []

        for sup in content_div.find_all('sup', class_='reference'):
            sup.decompose()
        for ref_list in content_div.select('ol.references, li[id^="cite_note"]'):
            ref_list.decompose()

        if content_div:
            for tag in content_div.find_all(['h2', 'p', 'li']):
                if tag.name == 'h2':
                    heading = tag.get_text(strip=True).replace('[sunting | sunting sumber]', '')
                    if 'Bibliografi' in heading or 'Rujukan' in heading:
                        break
                    extracted_text.append(f'\n{heading}\n')
                else:
                    text = tag.get_text(separator=" ", strip=True)
                    if text:
                        extracted_text.append(text)

        content = '\n'.join(extracted_text)
        content = re.sub(r"\s*\[\s*\d+\s*\]", '', content)

        return title, content
    
    except Exception as e:
        return f"Error scraping {url}: {str(e)}", "Error"

def scrape_hellodoktor(url):
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        title = soup.title.string
        content_div = soup.select_one('div.body-content.article-content-wrapper')
        extracted_text = [content_div.get_text(separator=' ', strip=True)]
        content = '\n'.join(extracted_text)
        
        return title, content
    
    except Exception as e:
        return f"Error scraping {url}: {str(e)}", "Error"


print("\n[*] Starting Data Collection ... \n")

with open('urls.txt', 'r') as f:
    urls = [line.strip() for line in f if line.strip()]

data = []
total = len(urls)
for i, url in enumerate(urls, start=1):
    print(f"[{i}/{total}] Scraping: {url}")
    if 'wikipedia' in url:
        title, content = scrape_wikipedia(url)
    elif 'hellodoktor' in url:
        title, content = scrape_hellodoktor(url)
    else:
        title, content = 'Unsupported URL', 'No content scraped.'

    data.append({'title': title, 'content': content})
    time.sleep(3)

with open('raw_text_data.json', 'w', encoding='utf-8') as jsonfile:
    json.dump(data, jsonfile, ensure_ascii=False, indent=4)

print("\n[+] Output saved to 'raw_text_data.json'\n")