#!/usr/bin/python3
"""
Recursive function that queries the Reddit API, parses the title of all hot articles, and prints a sorted count of given keywords
"""

import requests


def count_words(subreddit, word_list, count_dict=None, after=None):
    """
    Recursive function that queries the Reddit API, parses the title of all hot articles, and prints a sorted count of given keywords
    """
    headers = {'User-Agent': 'Mozilla/5.0'}
    params = {'limit': 100}
    if after:
        params['after'] = after
    url = 'https://www.reddit.com/r/{}/hot.json'.format(subreddit)
    response = requests.get(url, headers=headers, params=params, allow_redirects=False)
    if response.status_code == 404:
        return
    if not count_dict:
        count_dict = {}
        for word in word_list:
            count_dict[word.lower()] = 0
    data = response.json().get('data')
    after = data.get('after')
    children = data.get('children')
    for child in children:
        title = child.get('data').get('title').lower()
        for word in word_list:
            count = title.count(word.lower())
            if count > 0:
                count_dict[word.lower()] += count
    if after:
        count_words(subreddit, word_list, count_dict, after=after)
    else:
        sorted_dict = sorted(count_dict.items(), key=lambda x: (-x[1], x[0]))
        for word, count in sorted_dict:
            if count > 0:
                print('{}: {}'.format(word, count))
