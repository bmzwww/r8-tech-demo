import time
import traceback
from flask import Flask, json, render_template
import requests

app = Flask(__name__)  

@app.route('/')
def index_page():
    top_ten_articles = []
    articles = get_articles()
    filtered_articles = filter_articles(articles)
    sorted_articles = sort_articles(filtered_articles) 
    
    limit = 10
    for article in sorted_articles:               
        top_ten_articles.append(get_article_title(article))
        if top_ten_articles.__len__() >= limit:
            break
    
    return render_template('simple.html', names=top_ten_articles)

def get_article_title(article):
    article_title = None
    try:
        if article['title'] is not None and str.isprintable(article['title']):
            article_title = article['title']
        elif article['story_title'] is not None and str.isprintable(article['story_title']):
            article_title = article['story_title']
    except Exception as ex:
        traceback.print_exc()

    return article_title

def sort_articles(articles):
    sorted_articles = sorted(articles, key=lambda article: int(article['num_comments']), reverse=True)
    
    # Result
    return sorted_articles

def filter_articles(articles):
    filtered_out = []

    for article in articles:
        # Get article_title
        article_title = get_article_title(article)

        # Check article_title
        if article_title is None:
            continue
        if not str.isprintable(article_title):
            continue

        # Check num_comments
        if article['num_comments'] is None:
            continue

        # Add article to collection
        filtered_out.append(article)
    
    # Result
    return filtered_out


def get_articles():
    articles = []

    # Init variables
    page_number = 1   
    page_limit = 1
    total = 1

    while (page_number <= page_limit and articles.__len__() < total):
        # Get aricles from api
        page = load_page(page_number)
        page_number += 1

        if page is None:
            continue

        page_limit = int(page['total_pages'])
        total = int(page['total'])

        for article in page['data']:
            articles.append(article)
    
    # Result
    return articles
    
def load_page(page_number):
    invalid_page = 'Invalid page number'

    try:
        res = requests.get('https://jsonmock.hackerrank.com/api/articles?page=' + page_number.__str__())

        if res.text.startswith('{"error":'):
            error = res.text.split(':"')[1].split('"')[0]
            raise Exception(error)
        
        return json.loads(res.text)    
        # raise Exception('test')
    except Exception as ex:
        traceback.print_exc()

        if ex.__str__().find(invalid_page) < 0:
            time.sleep(5)
            return load_page(page_number)
        
    # Empty result
    return None

import os

# If file is called directly called, then run the app on the PORT provided defined in ENV or use '6969'.
if __name__ == "__main__":
    app.run("0.0.0.0", port=os.getenv('PORT', 8800))
