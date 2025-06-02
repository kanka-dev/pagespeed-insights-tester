import requests
import time
import csv
from xml.etree import ElementTree
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv('PAGESPEED_API_KEY')
SITEMAP_URL = os.getenv('SITEMAP_URL')
CSV_FILENAME = 'pagespeed_report.csv'
NAMESPACE = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}

def get_urls_from_sitemap(url):
    urls = []
    try:
        res = requests.get(url)
        if res.status_code != 200:
            print(f"Could not load sitemap: {res.status_code}")
            return []

        tree = ElementTree.fromstring(res.content)

        if tree.tag.endswith('sitemapindex'):
            for sitemap in tree.findall('ns:sitemap', NAMESPACE):
                loc = sitemap.find('ns:loc', NAMESPACE)
                if loc is not None:
                    urls += get_urls_from_sitemap(loc.text)
        else:
            for url_tag in tree.findall('ns:url', NAMESPACE):
                loc = url_tag.find('ns:loc', NAMESPACE)
                if loc is not None:
                    urls.append(loc.text)
    except Exception as e:
        print(f"Error parsing sitemap: {e}")
    return urls

def test_pagespeed(url):
    try:
        api = 'https://www.googleapis.com/pagespeedonline/v5/runPagespeed'
        params = {
            'url': url,
            'key': API_KEY,
            'strategy': 'mobile',
        }
        r = requests.get(api, params=params)
        data = r.json()

        if 'lighthouseResult' not in data:
            print(f"⚠️  No lighthouseResult for {url}: {data.get('error', {}).get('message', 'Unknown error')}")
            return {
                'url': url,
                'performance': None,
                'accessibility': None,
                'best_practices': None,
                'seo': None
            }

        categories = data['lighthouseResult']['categories']

        return {
            'url': url,
            'performance': categories['performance']['score'] * 100,
            'accessibility': categories['accessibility']['score'] * 100,
            'best_practices': categories['best-practices']['score'] * 100,
            'seo': categories['seo']['score'] * 100
        }

    except Exception as e:
        print(f"❌ Error for {url}: {e}")
        return {
            'url': url,
            'performance': None,
            'accessibility': None,
            'best_practices': None,
            'seo': None
        }


def save_to_csv(results, filename):
    with open(filename, mode='w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['url', 'performance', 'accessibility', 'best_practices', 'seo']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for row in results:
            writer.writerow(row)

def main():
    urls = get_urls_from_sitemap(SITEMAP_URL)
    print(f"{len(urls)} URLs found\n")

    results = []
    for url in urls:
        print(f"Testing: {url}")
        data = test_pagespeed(url)
        print(f"  → Performance: {data['performance']} | Accessibility: {data['accessibility']} | Best Practices: {data['best_practices']} | SEO: {data['seo']}")
        results.append(data)
        time.sleep(1.2)

    save_to_csv(results, CSV_FILENAME)
    print(f"\n✅ CSV saved as '{CSV_FILENAME}'")

if __name__ == "__main__":
    main()