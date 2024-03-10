from django.shortcuts import render,HttpResponse
from visualise.views import visualise
from pyvis.network import Network
from django.template import loader
import webbrowser
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
from serpapi import GoogleSearch

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
    
    sites = [
        "site:economictimes.indiatimes.com",
        "site:livemint.com",
        "site:hindustantimes.com",
        "site:bloombergquint.com",
        "site:moneycontrol.com",
        "site:ndtv.com",
        "site:businesstoday.in",
        "site:financialexpress.com",
        "site:thehindubusinessline.com",
        "site:firstpost.com",
        "site:moneylife.in",
        "site:dsij.in",
        "site:zeebiz.com",
        "site:businessworld.in",
        "site:goodreturns.in",
        "site:investing.com",
        "site:indiainfoline.com"
    ]
    
    if category:
        params = {
            'api_key': '26e70021815702b5f137092dd576848621e3f9d5f6ec76fae0ac49148a0fa8f6',
            'engine': 'google',
            'tbm': 'nws',
            'q': f'{category} {" OR ".join(sites)}',  # Use OR operator to search across multiple sites
        }   
        search = GoogleSearch(params)
        results = search.get_dict().get('news_results', [])
    else:
        results = None
    
    print(results)
    context = {'news_data': results, 'base_id': base_id, 'category': category}
    return render(request, 'news/dashboard.html', context)

import google.generativeai as genai



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

def summary_news(request):   
    url = request.GET.get('url')
    html_file_path = visualise(request,url)

    # Check if 'url' parameter is missing or empty
    if not url:
        url = 'https://timesofindia.indiatimes.com/india/bjp-is-irrelevant-in-thiruvananthapuram-main-fight-is-between-left-and-congress-ldf-candidate-pannyan-raveendran/articleshow/108355512.cms'

    try:
        genai.configure(api_key="AIzaSyA4uR6gq5njTMtQXJwSpIdq_zC1LA1ugS0")

        # Set up the model
        generation_config = {
        "temperature": 0.9,
        "top_p": 1,
        "top_k": 1,
        "max_output_tokens": 2048,
        }

        safety_settings = [
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        ]

        model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                                    generation_config=generation_config,
                                    safety_settings=safety_settings)

        convo = model.start_chat(history=[
        ])

        convo.send_message(f"summarise this url news in 100 words and give 2-3 important links{url}. Also search for the same context on google and check whether the news in the content of url link is reliable or not. Answer in one word 'Reliable' or 'Unreliable' and suport your answer in 15 -20 words")
        result = convo.last.text
    except:
        genai.configure(api_key="AIzaSyCeIzo3yb2MYwp536XX_BODXUZBwjkP14Y")

        # Set up the model
        generation_config = {
        "temperature": 0.9,
        "top_p": 1,
        "top_k": 1,
        "max_output_tokens": 2048,
        }

        safety_settings = [
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        ]

        model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                                    generation_config=generation_config,
                                    safety_settings=safety_settings)

        convo = model.start_chat(history=[
        ])

        convo.send_message(f"summarise this url news in 100 words and give 2-3 important links{url}. Also search for the same context on google and check whether the news in the content of url link is reliable or not. Answer in one word 'Reliable' or 'Unreliable' and suport your answer in 15 -20 words")
        result = convo.last.text
    context = { 
        'result' : result,
        'html_file_path': html_file_path
    }
    print(context)
    template = loader.get_template('news/summary.html')
    return HttpResponse(template.render(context, request))


from django.shortcuts import render

def ai_news(request):
    if request.method == 'POST':
        user_input = request.POST.get('user_input', '')
        try:
            genai.configure(api_key="AIzaSyA4uR6gq5njTMtQXJwSpIdq_zC1LA1ugS0")
        except:
            genai.configure(api_key="AIzaSyA4uR6gq5njTMtQXJwSpIdq_zC1LA1ugS0")

        # Set up the model
        generation_config = {
            "temperature": 0.9,
            "top_p": 1,
            "top_k": 1,
            "max_output_tokens": 2048,
        }

        safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
        ]

        model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                                    generation_config=generation_config,
                                    safety_settings=safety_settings)

        convo = model.start_chat(history=[])
        context = 'You are an AI news assistant who will give URL links and headlines based on the interests and inputs I receive.'
        convo.send_message(f"{context} {user_input}")
        result = convo.last.text

        return render(request, 'news/ai_news.html', {'result': result})

    return render(request, 'news/ai_news.html')

