import requests
from bs4 import BeautifulSoup
import argparse
import re
from urllib.parse import urlparse


def _extract_social_media_links(soup):
    """
    Extracts social media links from a given webpage using a given pattern.

    :param soup: A BeautifulSoup object.
    :return: A dictionary of social media platforms and their corresponding links.
    """

    # Define a dictionary of social media platforms and their corresponding patterns or CSS classes
    social_media_patterns = {
        'Facebook': r'(?:facebook.com/)(\w+)',
        'Twitter': r'(?:twitter.com/)(\w+)',
        'Instagram': r'(?:instagram.com/)(\w+)',
        'LinkedIn': r'(?:linkedin.com/)(\w+)',
        'YouTube': r'(?:youtube.com/)(\w+)',
        'Pinterest': r'(?:pinterest.com/)(\w+)',
        'Snapchat': r'(?:snapchat.com/)(\w+)',
        'TikTok': r'(?:tiktok.com/)(\w+)',
        'Reddit': r'(?:reddit.com/u/)(\w+)',
        'WhatsApp': r'(?:wa.me/)(\w+)',
        'WeChat': r'(?:wechat.com/)(\w+)',
        'Telegram': r'(?:t.me/)(\w+)',
        'Tumblr': r'(?:tumblr.com/)(\w+)',
        'Flickr': r'(?:flickr.com/people/)(\w+)',
        'Quora': r'(?:quora.com/profile/)(\w+)',
        'GitHub': f'(?:github.com/)(\w+)'
        }

    social_media_links = {}

    # get social media links
    for platform, pattern in social_media_patterns.items():
        regex = re.compile(pattern, re.IGNORECASE)
        link = soup.find('a', href=regex)

        if link:
            social_media_links[platform] = link['href']

    return social_media_links

def _extract_details(soup):
    """
    Extracts details from a given webpage.

    :param soup: A BeautifulSoup object.
    :return: A dictionary of extracted details.
    """

    # Extract email addresses, social media links, author names, geolocations, phone numbers, usernames from a given webpage
    email_addresses = set(email['href'].replace('mailto:', '') for email in soup.find_all('a', href=lambda href: href and 'mailto:' in href))
    extracted_social_links = _extract_social_media_links(soup)
    author_names = set(author['content'] for author in soup.find_all('meta', attrs={'name': 'author'}))
    geolocations = set(location['content'] for location in soup.find_all('meta', attrs={'name': 'geo.position'}))

    webpage_text = soup.get_text()

    # extract based on regex
    email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'
    extracted_emails = set(re.findall(email_regex, webpage_text))
    phone_regex3 = r'\(\d{3}\)\s\d{3}\s\d{5}'
    phone_regex = r'\b\+?\d{10,12}\b'
    phone_regex2 = r'\b(?:\+\d{1,3}[- ]?)?\(?\d{3}\)?[- ]?\d{3}\)?[- ]?\d{4}\b'
    extracted_phone_numbers = set(re.findall(phone_regex, webpage_text))
    extracted_phone_numbers2 = set(re.findall(phone_regex2, webpage_text))
    extracted_phone_numbers3 = set(re.findall(phone_regex3, webpage_text))
    username_regex = r'@[A-Za-z0-9_]+'
    extracted_usernames = set(re.findall(username_regex, webpage_text))

    return {
        'email_addresses': list(set(email_addresses).union(extracted_emails)),
        'author_names': list(set(author_names)),
        'geolocations': list(set(geolocations)),
        'phone_numbers': list(set(extracted_phone_numbers).union(extracted_phone_numbers2).union(extracted_phone_numbers3)),
        'usernames': list(set(extracted_usernames)),
        'social_links': extracted_social_links
        }

def _extract_urls_html(to_check, checked=[]):
    """
    Extracts all the URLs from a given webpage.

    :param to_check: The URL to check.
    """

    # check if the URL starts with http or https, if not, add it to the beginning of the URL.
    # This is to make sure that the URL is valid and that the requests module can handle it.
    if not to_check.startswith('http://') and not to_check.startswith('https://'):
        to_check = 'https://' + to_check

    try:
        response = requests.get(to_check)
    except:
        return [], None
    soup = BeautifulSoup(response.text, 'html.parser')

    # find all the links in the webpage
    urls = []
    for link in soup.find_all('a'):
        try:        
            url = link.get('href')
            url = urlparse(to_check).scheme + '://' + urlparse(to_check).netloc + urlparse(url).path
            if url not in checked:
                urls.append(url)
        except:
            pass

    return urls, soup

def get_data(url):
    """
    Extracts all the data from a given webpage.

    :param url: The URL to check.
    """

    # check if the URL starts with http or https, if not, add it to the beginning of the URL.
    # This is to make sure that the URL is valid and that the requests module can handle it.
    if not url.startswith('http://') and not url.startswith('https://'):
        url = 'https://' + url
    urls = [url]

    data = []
    checked = []
    count = 0
    MAX_RUNS = 50
    while urls:
        if count > MAX_RUNS:
                break
        for url in urls:
            # get new urls and relevan html in soup format
            try:
                new_urls, soup = _extract_urls_html(url, checked=checked)
                data.append({'source': url, 'data': _extract_details(soup)})
                checked.append(url)
            except:
                pass
        count += len(urls)
        urls = list(set(urls).union(new_urls))
    
    return data


"""
Test Code
"""

# from_website = 'hawk-eyes.io'
# data = get_data(from_website)

# for d in data:s
#     source = d['source']
#     details = d['data']

#     # emails
#     for email in details['email_addresses']:
#         print(email)
#         print(source)
#         print()
    
#     # author_names
#     for name in details['author_names']:
#         print(name)
#         print(source)
#         print() 

#     # geolocation
#     for location in details['geolocations']:
#         print(location)
#         print(source)
#         print()

#     # phone_numbers
#     for number in details['phone_numbers']:
#         print(number)
#         print(source)
#         print()

#     # usernames
#     for username in details['usernames']:
#         print(username)
#         print(source)
#         print()

#     # social_links
#     for platform, link in details['social_links'].items(): 
#         print(platform, link)
#         print(source)
#         print()