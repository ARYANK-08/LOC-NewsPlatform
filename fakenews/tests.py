from django.test import TestCase

# Create your tests here.
from serpapi import GoogleSearch

params = {
  "engine": "google_news",
  "q": "pizza",
  "api_key": "2145d6d7b13649473c8fc27db3144a1fcd104d599cb85342faefc7e612e243ca"
}

search = GoogleSearch(params)
results = search.get_dict()
news_results = results["news_results"]
print(news_results)