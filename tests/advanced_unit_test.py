import src.advanced
import json

example_page_text = '{"page":1,"per_page":10,"total":41,"total_pages":5,"data":[{"title":"A Message to Our Customers","url":"http://www.apple.com/customer-letter/","author":"epaga","num_comments":967,"story_id":null,"story_title":null,"story_url":null,"parent_id":null,"created_at":1455698317},{"title":"“Was isolated from 1999 to 2006 with a 486. Built my own late 80s OS”","url":"http://imgur.com/gallery/hRf2trV","author":"epaga","num_comments":265,"story_id":null,"story_title":null,"story_url":null,"parent_id":null,"created_at":1418517626},{"title":"Apple’s declining software quality","url":"http://sudophilosophical.com/2016/02/04/apples-declining-software-quality/","author":"epaga","num_comments":705,"story_id":null,"story_title":null,"story_url":null,"parent_id":null,"created_at":1454596037},{"title":null,"url":null,"author":"patricktomas","num_comments":376,"story_id":null,"story_title":"Steve Jobs has passed away.","story_url":"http://www.apple.com/stevejobs/","parent_id":null,"created_at":1317858143},{"title":"Google Is Eating Our Mail","url":"https://www.tablix.org/~avian/blog/archives/2019/04/google_is_eating_our_mail/","author":"saintamh","num_comments":685,"story_id":null,"story_title":null,"story_url":null,"parent_id":null,"created_at":1556274921},{"title":"Why I’m Suing the US Government","url":"https://www.bunniestudios.com/blog/?p=4782","author":"saintamh","num_comments":305,"story_id":null,"story_title":null,"story_url":null,"parent_id":null,"created_at":1469106658},{"title":"F.C.C. Repeals Net Neutrality Rules","url":"https://www.nytimes.com/2017/12/14/technology/net-neutrality-repeal-vote.html","author":"panny","num_comments":1397,"story_id":null,"story_title":null,"story_url":null,"parent_id":null,"created_at":1513275215},{"title":"Show HN: This up votes itself","url":"http://news.ycombinator.com/vote?for=3742902&dir=up&whence=%6e%65%77%65%73%74","author":"olalonde","num_comments":83,"story_id":null,"story_title":null,"story_url":null,"parent_id":null,"created_at":1332463239},{"title":null,"url":null,"author":"olalonde","num_comments":null,"story_id":null,"story_title":"Guacamole – A clientless remote desktop gateway","story_url":"https://guacamole.incubator.apache.org/","parent_id":6547669,"created_at":1381763543},{"title":null,"url":null,"author":"WisNorCan","num_comments":981,"story_id":null,"story_title":"Switch from Chrome to Firefox","story_url":"https://www.mozilla.org/en-US/firefox/switch/","parent_id":null,"created_at":1559232559}]}'

def test_advanced_load_page_negative():
    result_one = src.advanced.load_page(-1)
    assert result_one is None

def test_advanced_load_page_overflow():
    result_one = src.advanced.load_page(50)
    assert result_one.total_pages == 5 and result_one.data.__len__() == 0

def test_advanced_load_page():
    result_one = src.advanced.load_page(1)
    assert result_one.total_pages == 5 and result_one.data.__len__() == 10

def test_serialization():
    response = json.loads(example_page_text)    
    page = src.advanced.Page.from_dict(response)
    assert page.data.__len__() == 10

def test_filter_articles():
    response = json.loads(example_page_text)    
    page = src.advanced.Page.from_dict(response)
    result_one = src.advanced.filter_articles(page.data)
    assert result_one.__len__() == 9

def test_sort_articles():
    response = json.loads(example_page_text)    
    page = src.advanced.Page.from_dict(response)
    filtered_article = src.advanced.filter_articles(page.data)
    result_one = src.advanced.sort_articles(filtered_article)
    assert result_one.__len__() == 9 and result_one[0].title == 'F.C.C. Repeals Net Neutrality Rules'

def test_get_article_title():
    response = json.loads(example_page_text)    
    page = src.advanced.Page.from_dict(response)
    title = src.advanced.get_article_title(page.data[0])
    title_2 = src.advanced.get_article_title(page.data[8])

    assert title == 'A Message to Our Customers' and title_2 == 'Guacamole – A clientless remote desktop gateway'
