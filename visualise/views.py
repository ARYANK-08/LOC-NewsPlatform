from django.shortcuts import render,HttpResponse
from django.shortcuts import render
import google.generativeai as genai
import re
import networkx as nx
import matplotlib.pyplot as plt
from pyvis.network import Network
from django.template import loader
import webbrowser
from dotenv import load_dotenv
import os

# Create your views here.
def visualise(request, link):
    inputLink = link
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
    relations = re.findall(r"\* (.+)", relations_text)

    # Use regex to extract links
    links = re.findall(r'https://[^\s]+', response)


    # Print the results
    print("Nodes:", nodes)
    print("\nEdges:", edges)
    print("\nRelations:", relations)
    print("\nLinks:", links)


    G = nx.Graph()
    G.add_nodes_from(nodes, title = relations)
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
    return html_file_path
    # Render the HTML template
    # template = loader.get_template('visualise/visualise.html')
    # context = {'html_file_path': html_file_path}
    # return HttpResponse(template.render(context, request))



# def chat_with_ai(request):

#     if request.method == 'POST':
#         cropType = request.POST.get('cropType')
#         landArea = request.POST.get('landArea')
#         season = request.POST.get('season')
#         soilquality = request.POST.get('soilquality')


#         response = get_ai_response(cropType,landArea,season,soilquality)

#         return render(request, 'resources/ai.html', {'cropType': cropType,'landArea': landArea,'season': season, 'response': response})
#     return render(request, 'resources/ai.html', {})
load_dotenv()
def get_ai_response(inputLink):
    try:
        genai.configure(api_key=(os.getenv("S2GOOGLE_API_KEY")))  # Set up your API key
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
        context = "Act as a news or events interconnector which takes a link as input, scrapes the main contents of the link like names of major people, events mentioned, how is that event affecting other events of that category.Basically you need to scrape the relationships between events in nodes and edgegs form. Nodes being the events and the edges being how are they connected. Give ateast 5 nodes. Give it in this form [(EventA,EventB),(EventB,EventC)] meaning event A is related to event B and event B is related to Event C, give edges in form[(A,B), (B,C)] and give a list of Relations between the nodes in a separate python list. Along with this provide only 'Links' of multiple related events."
        message = f"{context} Link to Scrape : {inputLink} "
        response = convo.send_message(message)
        answer = convo.last.text
    except:
        print('bt1')
        genai.configure(api_key=(os.getenv("A1GOOGLE_API_KEY")))  # Set up your API key
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
        context = "Act as a news or events interconnector which takes a link as input, scrapes the main contents of the link like names of major people, events mentioned, how is that event affecting other events of that category.Basically you need to scrape the relationships between events in nodes and edgegs form. Nodes being the events and the edges being how are they connected. Give ateast 5 nodes. Give it in this form [(EventA,EventB),(EventB,EventC)] meaning event A is related to event B and event B is related to Event C, give edges in form[(A,B), (B,C)] and give a list of Relations between the nodes in a separate python list. Along with this provide only 'Links' of multiple related events."
        message = f"{context} Link to Scrape : {inputLink} "
        response = convo.send_message(message)
        answer = convo.last.text
    # print(f'hi{answer}')
    return convo.last.text # Assuming 'message' contains the response text



from django.conf import settings

from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
import urllib.parse
load_dotenv()
genai.configure(api_key=(os.getenv("GOOGLE_API_KEY")))
def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    chunks = text_splitter.split_text(text)
    return chunks

def get_vector_store(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    index_path = os.path.join(settings.BASE_DIR, "faiss_index")
    vector_store.save_local(index_path)
    return index_path

def get_conversational_chain():
    prompt_template = """
    Act as a stock analyzer and analyse all the details of the provided context like financial report, etc. Answer the user on the basis of the provided context in 15-20 words.
{context} (Provide the PDF containing the data for analysis)

Question:
{question}

Answer:
    """

    model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3)

    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)

    return chain

def user_input(user_question):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    new_db = FAISS.load_local(os.path.join(settings.BASE_DIR, "faiss_index"), embeddings)
    docs = new_db.similarity_search(user_question)
    chain = get_conversational_chain()
    response = chain({"input_documents": docs, "question": user_question}, return_only_outputs=True)
    response_text = response["output_text"]
    if response_text == "":
        response_text = "It seems that the answer is out of context. Here is a general response: ..."
    return response_text

def gemini(request):
    

    if request.method == 'POST':
        # Handle PDF upload
        pdf_docs = request.FILES.getlist('pdf_files')
        raw_text = get_pdf_text(pdf_docs)
        text_chunks = get_text_chunks(raw_text)
        pdf_path = get_vector_store(text_chunks)  # Save the PDF path

        # Handle user question
        user_question = request.POST.get('user_question')
        response_text = user_input(user_question)

        # Return response
        return render(request, 'news/financial_report.html', {'response_text': response_text})
    else:
        return render(request, 'news/financial_report.html')
    







