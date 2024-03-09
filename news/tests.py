from django.test import TestCase

# Create your tests here.
from serpapi import GoogleSearch
import os, json
def serp_api():


    params = {
        'api_key': '2145d6d7b13649473c8fc27db3144a1fcd104d599cb85342faefc7e612e243ca',         # your serpapi api
        'engine': 'google',               # SerpApi search engine	
        'tbm': 'nws',                     # Google News engine 
        'q': 'startups',
        'topic_token': 'Startups',  # Replace with the desired topic token
        'publication_token': 'CNN',  # Replace with the desired publication token
     
    }
    results = GoogleSearch(params).get_dict()['news_results']
    print(results)
serp_api()
