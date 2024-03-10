from django.shortcuts import render
# from .models import News  # if you have a News model
import pickle
import re
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from serpapi import GoogleSearch
import google.generativeai



port_stem = PorterStemmer()
vectorization = TfidfVectorizer()


def get_data(query):

    params = {
    "engine": "google_news",
    "q": query,
    "api_key": "2145d6d7b13649473c8fc27db3144a1fcd104d599cb85342faefc7e612e243ca"
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    news_results = results["news_results"]

def stemming(content):
    con = re.sub('[^a-zA-Z]', ' ', content)
    con = con.lower()
    con = con.split()
    con = [port_stem.stem(word) for word in con if not word in stopwords.words('english')]
    con = ' '.join(con)
    return con

def fake_news(news):
    news = stemming(news)
    input_data = [news]
    vector_form1 = vector_form.transform(input_data)
    prediction = load_model.predict(vector_form1)
    return prediction

def index(request):

    params = {
    "engine": "google_news",
    "q": "Bomb blast in 1998",
    "api_key": "2145d6d7b13649473c8fc27db3144a1fcd104d599cb85342faefc7e612e243ca"
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    news_results = results["news_results"]
    print(news_results)

    if request.method == 'POST':
        sentence = request.POST.get('news_content', '')
        prediction_class = fake_news(sentence)
        print(prediction_class)
        result = 'Reliable' if prediction_class == [0] else 'Unreliable'
        return render(request, 'fakenews/check.html', {'result': result})
    return render(request, 'fakenews/check.html')
