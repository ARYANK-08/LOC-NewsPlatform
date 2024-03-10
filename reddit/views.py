from django.http import HttpResponse
from django.shortcuts import render
from IPython import display
from pprint import pprint
import pandas as pd
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
import praw
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import seaborn as sns


def sentiment_analysis(request):
    reddit = praw.Reddit(client_id='ZhJTQMStZByulQY4pTncow',
                         client_secret='nVvddTZ8k0rT39SePpTwoDf5k97xGQ',
                         user_agent='wingwing_00')

    headlines = set()
    for submission in reddit.subreddit('indianews').new(limit=None):
        headlines.add(submission.title)
        display.clear_output()
        print(len(headlines))

    nltk.download('vader_lexicon')
    sia = SIA()
    results = []

    for line in headlines:
        pol_score = sia.polarity_scores(line)
        pol_score['headline'] = line
        results.append(pol_score)

    df = pd.DataFrame.from_records(results)
    df['label'] = 0
    df.loc[df['compound'] > 0.2, 'label'] = 1
    df.loc[df['compound'] < -0.2, 'label'] = -1

    positive_headlines = list(df[df['label'] == 1].headline)[:5]
    negative_headlines = list(df[df['label'] == -1].headline)[:5]

    # Calculate the percentages of negative, neutral, and positive sentiments
    counts = df['label'].value_counts(normalize=True) * 100
    negative_percentage = counts[-1]
    neutral_percentage = counts[0]
    positive_percentage = counts[1]

    # Plotting the graph
    plt.figure(figsize=(8, 8))
    sns.barplot(x=counts.index, y=counts, palette=["red", "grey", "green"])
    plt.xticks([0, 1, 2], ['Negative', 'Neutral', 'Positive'])
    plt.ylabel("Percentage")

    # Save the plot to a BytesIO object
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode()
    plt.close()

    return render(request, 'sentiment.html', {
        'positive_headlines': positive_headlines,
        'negative_headlines': negative_headlines,
        'graph_image': image_base64,
        'negative_percentage': negative_percentage,
        'neutral_percentage': neutral_percentage,
        'positive_percentage': positive_percentage
    })


def index(request):
    return HttpResponse("Hello, world. This is myapp index.")
