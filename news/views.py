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

import google.generativeai as genai


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
