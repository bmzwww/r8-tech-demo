import datetime
import src.optimized

def test_advanced_get_articles_time():
    dt = datetime.datetime.now()
    result_one = src.optimized.get_articles()
    totatl_time_in_seconds = (datetime.datetime.now() - dt).total_seconds()
    assert result_one.__len__() == 41 and totatl_time_in_seconds < 5 # less than 5 seconds