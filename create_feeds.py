from multiprocessing.pool import ThreadPool

import requests


def submit_feed(i: int):
    print(f'***Request {i}')

    args = {'title': f'Feed {i}', 'url': 'https://www.robinwieruch.de/index.xml'}

    url = f'http://localhost:5000/new-task?title={args["title"]}&url={args["url"]}'
    req = requests.get(url)

    print(f'R {i} Status code: {req.status_code}')
    print(f'R {i} Response text: {req.text}')
    req.raise_for_status()


def create_feeds():
    pool = ThreadPool(5)
    results = pool.map(submit_feed, range(1, 11))
    pool.close()
    pool.join()
    return results


if __name__ == '__main__':
    create_feeds()
    # submit_feed(1)
