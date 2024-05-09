import requests
import os
import sys
from bs4 import BeautifulSoup

assert len(sys.argv) == 2
subreddit = sys.argv[1]


def make_request(link):
    return requests.get(
        link,
        headers={
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        },
        cookies={'over18': '1'},
    ).content


content = make_request(f'https://old.reddit.com/r/{subreddit}/new/')
soup = BeautifulSoup(content, 'html.parser')

seen_before = set()
if os.path.exists(subreddit):
    with open(subreddit, 'r') as fp:
        seen_before = set(l.strip() for l in fp.readlines())
else:
    with open(subreddit, 'w') as _:
        pass

results = []
for div in soup.find_all('div', class_='entry unvoted'):
    # Advertisements throw exception
    try:
        title = div.select('a.title.may-blank')[0].get_text()
        link = div.select('a.bylink.comments.may-blank')[0]['href']
    except:
        continue

    # This link we've already scraped, so then just exit.
    if link in seen_before:
        break

    print(link)
    results.append(link)

# Append if file is new, prepend if file already has links in it.
if not os.path.exists(subreddit):
    with open(subreddit, 'w') as fp:
        print('\n'.join(results), file=fp)
else:
    # Must be better way to do this? TODO
    with open(subreddit, 'r') as fp:
        content = '\n'.join(results) + '\n' + fp.read()
    with open(subreddit, 'w') as fp:
        fp.write(content)
