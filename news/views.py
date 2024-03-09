from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'test.html')

from serpapi import GoogleSearch

from serpapi import GoogleSearch
import os, json

# def dashboard(request):
#     #get category parameter and pass it to serpi_api
    

# def serp_api(category):


#     params = {
#         'api_key': '2145d6d7b13649473c8fc27db3144a1fcd104d599cb85342faefc7e612e243ca',  
#         'engine': 'google',               # SerpApi search engine	
#         'tbm': 'nws',                     # Google News engine 
#         'q': f'{category}',
#         'topic_token': f'{category}'  # Replace with the desired topic token
#         'publication_token': 'CNN',  # Replace with the desired publication token
     
#     }
#     results = GoogleSearch(params).get_dict()['news_results']

def dashboard(request):
    return render(request, 'dashboard.html')

def serp_api(request):
    category = request.GET.get('category')
        # Define a mapping from category to a unique base ID
    category_to_id = {
        'Technology': 100,
            'Entertainment': 1000,
        'Business': 200,
        'Finance': 300,
        # Add more categories as needed
    }

    base_id = category_to_id.get(category, 0)  # Fallback to 0 if category not found

    if category:
        params = {
            'api_key': '2145d6d7b13649473c8fc27db3144a1fcd104d599cb85342faefc7e612e243ca',
            'engine': 'google',
            'tbm': 'nws',
            'q': category,
            
        }
        search = GoogleSearch(params)
        results = search.get_dict().get('news_results', [])
    else:
        results = None
    print(results)
    context = {'news_data': results, 'base_id': base_id }
    return render(request, 'news/dashboard.html', context)


def summary_news(request):
    return render (request,'news/summary.html')
