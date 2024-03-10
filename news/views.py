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
            'api_key': '26e70021815702b5f137092dd576848621e3f9d5f6ec76fae0ac49148a0fa8f6',
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


def news(request):
    # category = request.GET.get('category')
    params = {
    "engine": "google_news",
    "q": "hindustan times economictimes NDTV ",
    "api_key": "26e70021815702b5f137092dd576848621e3f9d5f6ec76fae0ac49148a0fa8f6"
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    response = results["news_results"]
    print(response)
    print("////////////////////////")
    filtered_news = {}

    for item in response:
        try:
            source_name = item['source']['name']
            if source_name in filtered_news:
                filtered_news[source_name].append(item)
            else:
                filtered_news[source_name] = [item]
        except KeyError:
            # Handle the case where 'source' key is missing in the item
            pass

    # Print the filtered news
    for name, news_list in filtered_news.items():
        print(f"News from {name}:")
        for news_item in news_list:
            print(news_item)

    return render(request,'test.html',{'filtered_news':filtered_news})

def news_list(request, name):
    # Retrieve news list associated with the given name
    # Assuming you have the filtered_news dictionary available here

    params = {
        "engine": "google_news",
        "q": "Hindustan Times economictimes NDTV  ",
        "api_key": "26e70021815702b5f137092dd576848621e3f9d5f6ec76fae0ac49148a0fa8f6"
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    response = results.get("news_results", [])  # Get the news results, default to an empty list if not found

    filtered_news = {}

    for item in response:
        try:
            source_name = item['source']['name']
            if source_name in filtered_news:
                filtered_news[source_name].append(item)
            else:
                filtered_news[source_name] = [item]
        except KeyError:
            # Handle the case where 'source' key is missing in the item
            pass

    name_list = filtered_news.get(name, [])
    context = {'name': name, 'name_list': name_list}
    print(name_list)

    return render(request, 'list.html', context)
