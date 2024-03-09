from django.shortcuts import render,HttpResponse
from django.shortcuts import render
import google.generativeai as genai
import re
import networkx as nx
import matplotlib.pyplot as plt
from pyvis.network import Network
from django.template import loader
import webbrowser


# Create your views here.
def visualise(request):
    inputLink = 'https://www.businesstoday.in/magazine/the-buzz/story/crisis-at-byjus-the-recent-battle-between-investors-and-byju-raveendran-can-have-profound-implications-for-the-troubled-company-420681-2024-03-08'
    response = get_ai_response(inputLink)
    print(response)
    # Extract nodes
    nodes_match = re.search(r'\*\*Nodes:\*\*(.*?)\*\*', response, re.DOTALL)
    nodes_text = nodes_match.group(1).strip()
    nodes = re.findall(r'\* (.+)', nodes_text)

    # Extract edges with a more flexible approach
    edges_match = re.search(r'\*\*Edges:\*\*\s*(.*?)\*\*', response, re.DOTALL)
    edges_text = edges_match.group(1).strip()

    # Extract edges considering variations in whitespace and special characters
    edges = re.findall(r'\* \((.*?), (.+?)\)', edges_text)

    # Convert the edges to the desired form
    edges = [(edge[0].strip('('), edge[1].strip(')')) for edge in edges]
    # Extract relations
    relations_match = re.search(r'\*\*Relations:\*\*(.*?)\*\*', response, re.DOTALL)
    relations_text = relations_match.group(1).strip()
    relations = re.findall(r'\* (.+)', relations_text)


    # Print the results
    print("Nodes:", nodes)
    print("\nEdges:", edges)
    print("\nRelations:", relations)
    # print("\nLinks:", links)

    name = 'Freddie Mercury'
    url = "https://en.wikipedia.org/wiki/"+name

    def display_page(url):
        webbrowser.open_new(url)

    G = nx.Graph()
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)
   
 # Create PyVis network object
    pyvis_network = Network(notebook=True,
                            height='400px',
                            width='100%',
                            bgcolor='#222222',
                            font_color='white')

    pyvis_network.from_nx(G)

    # Save the graph as an HTML file
    html_file_path = 'templates/visualise/graph.html'  # Change the path as needed
    pyvis_network.save_graph(html_file_path)

    # Render the HTML template
    template = loader.get_template('visualise/visualise.html')
    context = {'html_file_path': html_file_path}
    return HttpResponse(template.render(context, request))



# def chat_with_ai(request):

#     if request.method == 'POST':
#         cropType = request.POST.get('cropType')
#         landArea = request.POST.get('landArea')
#         season = request.POST.get('season')
#         soilquality = request.POST.get('soilquality')


#         response = get_ai_response(cropType,landArea,season,soilquality)

#         return render(request, 'resources/ai.html', {'cropType': cropType,'landArea': landArea,'season': season, 'response': response})
#     return render(request, 'resources/ai.html', {})

def get_ai_response(inputLink):
    genai.configure(api_key="AIzaSyA4uR6gq5njTMtQXJwSpIdq_zC1LA1ugS0")  # Set up your API key
    generation_config = {  # Your generation config
        "temperature": 0.1,
        "top_p": 1,
        "top_k": 1,
        "max_output_tokens": 2048,
    }
    safety_settings = [  # Your safety settings
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        # Add other settings as needed
    ]
    model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                                  generation_config=generation_config,
                                  safety_settings=safety_settings)
    convo = model.start_chat(history=[])
    context = "Act as a news or events interconnector which takes a link as input, scrapes the main contents of the link like names of major people, events mentioned, how is that event affecting other events of that category.Basically you need to scrape the relationships between events in nodes and edgegs form. Nodes being the events and the edges being how are they connected. Give it in this form [(EventA,EventB),(EventB,EventC)] meaning event A is related to event B and event B is related to Event C, give edges in form[(A,B), (B,C)] and give a list of Relations between the nodes in a separate python list. Along with this provide only 'Links' of multiple related events."
    message = f"{context} Link to Scrape : {inputLink} "
    response = convo.send_message(message)
    answer = convo.last.text
    # print(f'hi{answer}')
    return convo.last.text # Assuming 'message' contains the response text








