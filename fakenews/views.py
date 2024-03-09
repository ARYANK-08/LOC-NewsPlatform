from django.shortcuts import render
from .models import News  # if you have a News model
import pickle
import re
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer

port_stem = PorterStemmer()
vectorization = TfidfVectorizer()

vector_form = pickle.load(open('vector.pkl', 'rb'))
load_model = pickle.load(open('model.pkl', 'rb'))

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
    if request.method == 'POST':
        sentence = request.POST.get('news_content', '')
        prediction_class = fake_news(sentence)
        result = 'Reliable' if prediction_class == [0] else 'Unreliable'
        return render(request, 'index.html', {'result': result})
    return render(request, 'index.html')
