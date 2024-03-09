from django.shortcuts import render, HttpResponse
from serpapi import GoogleSearch

# Create your views here.
def fetchevents(request):
    params = {
    "engine": "google_events",
    "q": "Events in Mumbai",
    "hl": "en",
    "gl": "us",
    "api_key": "26e70021815702b5f137092dd576848621e3f9d5f6ec76fae0ac49148a0fa8f6"
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    events_results = results["events_results"]
    print(events_results)

    if request.method == 'POST':
        # Assuming the form contains a field named 'location'
        location = request.POST.get('location')
        params = {
        "engine": "google_events",
        "q": "Events in " + location,
        "hl": "en",
        "gl": "us",
        "api_key": "26e70021815702b5f137092dd576848621e3f9d5f6ec76fae0ac49148a0fa8f6"
        }
        search = GoogleSearch(params)
        results = search.get_dict()
        events_results = results["events_results"]
        print(events_results)
        return render(request,'event/events.html',{'events':events_results})
    return render(request,'event/events.html',{'events':events_results})


def process_location(request):
    if request.method == 'POST':
        # Assuming the form contains a field named 'location'
        location = request.POST.get('location')
        
        # Do whatever processing you need to do with the location data
        # For now, let's just print it
        print("Location submitted:", location)
        
        # You can return an HttpResponse or render a template as needed
        return HttpResponse("Location submitted successfully!")
    else:
        # Handle cases where the form is not submitted via POST
        # For example, you might want to render a form page again
        return HttpResponse("Invalid request method")
    

def event_details(request):
    return render(request, 'event/event_details.html')


