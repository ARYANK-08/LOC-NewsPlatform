# import google.generativeai as genai
# from serpapi import GoogleSearch
# from django.shortcuts import render

# # def visualise(request):
# #     inputLink = 'https://www.businesstoday.in/magazine/the-buzz/story/crisis-at-byjus-the-recent-battle-between-investors-and-byju-raveendran-can-have-profound-implications-for-the-troubled-company-420681-2024-03-08'
# #     response = get_ai_response(inputLink)
# #     print(response)

# def get_ai_response(inputLink):
#     genai.configure(api_key="AIzaSyD-8JHmHGyRM-u3tWwQaNUakmzlq5kF5nU")  # Set up your API key
#     generation_config = {  # Your generation config
#         "temperature": 0.1,
#         "top_p": 1,
#         "top_k": 1,
#         "max_output_tokens": 2048,
#     }
#     safety_settings = [  # Your safety settings
#         {
#             "category": "HARM_CATEGORY_HARASSMENT",
#             "threshold": "BLOCK_MEDIUM_AND_ABOVE"
#         },
#         # Add other settings as needed
#     ]
#     model = genai.GenerativeModel(model_name="gemini-1.0-pro",
#                                   generation_config=generation_config,
#                                   safety_settings=safety_settings)
#     convo = model.start_chat(history=[])
#     context = "Act as a news fact checker which takes a source as input, and check weather the news is reliable or not reliable . Answer only in one word 'Reliable' or 'Unreliable' "
#     message = f"{context} Link to Scrape : {inputLink} "
#     response = convo.send_message(message)
#     answer = convo.last.text
#     # print(f'hi{answer}')
#     return convo.last.text # Assuming 'message' contains the response text

# def visualise(link):
#     inputLink = link
#     response = get_ai_response(inputLink)
#     return response



# def index(request):

#     response_objects = []
#     params = {
#         'api_key': '26e70021815702b5f137092dd576848621e3f9d5f6ec76fae0ac49148a0fa8f6',
#         'engine': 'google',
#         'tbm': 'nws',
#         'q': 'Technology',
        
#     }
#     search = GoogleSearch(params)
#     results = search.get_dict().get('news_results', [])
    
#     if results:
#         first_result_source = results[8]['link']
#         print(first_result_source)
#         response = visualise(first_result_source)
#     else:
#         # Handle the case where there are no results
#         print("No results found.")

#     # print(results)
#     print("/////////////////////////////")
#     print(response)

#     context = {'news_data': results}
#     return render(request, 'fakenews/check.html', context)
