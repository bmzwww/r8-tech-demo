from dataclasses import dataclass, field
import time
import traceback
from typing import List, Optional
from flask import Flask, json, render_template
import requests

app = Flask(__name__)
api_uri = 'https://jsonmock.hackerrank.com/api/articles?page='

@dataclass
class DataItem:
    title: Optional[str]
    url: Optional[str]
    author: str
    num_comments: Optional[int]
    story_id: Optional[int]
    story_title: Optional[str]
    story_url: Optional[str]
    parent_id: Optional[int]
    created_at: int

@dataclass
class DataItemWithComment(DataItem):
    comment_text: Optional[str]

@dataclass
class Page:
    page: int
    per_page: int
    total: int
    total_pages: int
    data: List[DataItem | DataItemWithComment] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict) -> 'Page':
       
            data_items: List[DataItem | DataItemWithComment] = []
            for item in data['data']:
                try: 
                    if 'comment_text' in item:
                        data_items.append(DataItemWithComment(**item))
                    else:
                        data_items.append(DataItem(**item))          

                except Exception as ex:
                    traceback.print_exc()
               
            return cls(
                page=data['page'],
                per_page=data['per_page'],
                total=data['total'],
                total_pages=data['total_pages'],
                data=data_items
            )
   

@app.route('/')
def index_page():
    top_ten_articles: List[str] = []
    sorted_articles = sort_articles(filter_articles(get_articles())) 
    
    limit = 10
    for article in sorted_articles:               
        top_ten_articles.append(get_article_title(article))
        if top_ten_articles.__len__() >= limit:
            break
    
    # Renders a HTML file. (For web page streaming.)
    return render_template('simple.html', names=top_ten_articles)

def get_article_title(article: DataItem|DataItemWithComment):
    article_title = None

    try:
        if article.title is not None and str.isprintable(article.title):
            article_title = article.title
        elif article.story_title is not None and str.isprintable(article.story_title):
            article_title = article.story_title
    except Exception as ex:
        traceback.print_exc()

    return article_title

def sort_articles(articles: List[DataItem|DataItemWithComment]):
    sorted_articles: List[DataItem|DataItemWithComment] = sorted(articles, key=lambda article: article.num_comments, reverse=True)
    
    # Result
    return sorted_articles

def filter_articles(articles: List[DataItem|DataItemWithComment]):
    filtered_out: List[DataItem|DataItemWithComment] = []

    for article in articles:
        # Get article_title
        article_title = get_article_title(article)

        # Check article_title
        if article_title is None:
            continue
        if not str.isprintable(article_title):
            continue

        # Check num_comments
        if article.num_comments is None:
            continue

        # Add article to collection
        filtered_out.append(article)
    
    # Result
    return filtered_out


def get_articles():
    articles: List[DataItem|DataItemWithComment] = []

    # Get aricles
    page_number = 1   
    page_limit = 1
    total = 1

    while (page_number <= page_limit and articles.__len__() < total):
        page = load_page(page_number)
        page_number += 1

        if page is None:
            continue

        page_limit = page.total_pages  
        total = page.total

        for article in page.data:
            articles.append(article)
    
    # Result
    return articles
    
def load_page(page_number):
    invalid_page = 'Invalid page number'

    try:
        res = requests.get(api_uri + page_number.__str__())

        if res.text.startswith('{"error":'):
            error = res.text.split(':"')[1].split('"')[0]
            raise Exception(error)
        
        response = json.loads(res.text)    
        page = Page.from_dict(response)
        # raise Exception('test')
        return page
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
    app.run("0.0.0.0", port=os.getenv('PORT', 9900))
