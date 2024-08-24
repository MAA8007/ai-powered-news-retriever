import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from .models import Article
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
import os
import pandas as pd
from dateutil.parser import parse
import requests
from bs4 import BeautifulSoup
from django.utils.dateparse import parse_datetime
from django.db import IntegrityError
import random
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor
import csv 
from langchain_groq import ChatGroq
from groq import Groq


openai_api_key = os.getenv("OPENAI_API_KEY")
google_api_key = os.getenv("GOOGLE_API_KEY")
groq_api_key = os.getenv("GROQ_API_KEY")



### Function to fetch RSS feed and update the database with progress updates
def update_url_database_function_with_yield():
    rss_feed_details = [
    
    ('https://magazine.sebastianraschka.com/feed', 'item', 'link', 'title', 'media:content', 'url', 'AI News', 'Ahead of AI', 'pubDate'),
    
    ('https://venturebeat.com/category/ai/feed/', 'item', 'link', 'title', 'media:content', 'url', 'AI News', 'VentureBeat', 'pubDate'),
    
    ('https://ai-techpark.com/category/ai/feed/', 'item', 'link', 'title', 'content:encoded', 'img', 'AI News', 'AI-Tech Park', 'pubDate'),
    
    ('https://www.aiacceleratorinstitute.com/rss/', 'item', 'link', 'title', 'media:content', 'url', 'AI News', 'AI Accelerator Institute', 'pubDate'),
    
    ('https://aibusiness.com/feeds/rss.xml', 'item', 'link', 'title', 'media:thumbnail', 'url', 'AI News', 'AI Business', 'pubDate'),
    
    ('https://knowtechie.com/category/ai/feed/', 'item', 'link', 'title', 'content:encoded', 'src', 'AI News', 'KnowTechie', 'pubDate'),
    
    ('https://aimodels.substack.com/feed', 'item', 'link', 'title', 'enclosure', 'url', 'AI News', 'AIModels.fyi', 'pubDate'),
    
    ('https://www.aisnakeoil.com/feed', 'item', 'link', 'title', 'enclosure', 'url', 'AI News', 'AI Snake Oil', 'pubDate'),
    
    ('https://siliconangle.com/category/ai/feed/', 'item', 'link', 'title', 'enclosure', 'url', 'AI News', 'SiliconANGLE', 'pubDate'),
    
    ('https://www.marktechpost.com/feed/', 'item', 'link', 'title', 'media:content', 'url', 'AI News', 'MarkTechPost', 'pubDate'),
    
    ('https://www.theguardian.com/technology/artificialintelligenceai', 'item', 'link', 'title', 'media:content', 'url', 'AI News', 'Artificial intelligence (AI) | The Guardian', 'pubDate'),
    
    ('https://news.mit.edu/topic/mitmachine-learning-rss.xml', 'item', 'link', 'title', 'media:content', 'url', 'AI News', 'MIT News - Machine learning', 'pubDate'),
    
    ('https://www.technologyreview.com/feed/', 'item', 'link', 'title', 'media:content', 'url', 'AI News', 'MIT Technology Review', 'pubDate'),


    ('https://www.ft.com/world?format=rss', 'item', 'link', 'title', 'media:content', 'url', 'Global News', 'Financial Times', 'pubDate'),
    ('https://www.ft.com/global-economy?format=rss', 'item', 'link', 'title', 'media:content', 'url', 'Global News', 'Financial Times', 'pubDate'),
    ('https://www.ft.com/world/uk?format=rss', 'item', 'link', 'title', 'media:content', 'url', 'Global News', 'Financial Times', 'pubDate'),
    ('https://www.ft.com/world/us?format=rss', 'item', 'link', 'title', 'media:content', 'url', 'Global News', 'Financial Times', 'pubDate'),
    ('https://www.ft.com/world/africa?format=rss', 'item', 'link', 'title', 'media:content', 'url', 'Global News', 'Financial Times', 'pubDate'),
    ('https://www.ft.com/world/asia-pacific?format=rss', 'item', 'link', 'title', 'media:content', 'url', 'Global News', 'Financial Times', 'pubDate'),
    ('https://www.ft.com/world/europe?format=rss', 'item', 'link', 'title', 'media:content', 'url', 'Global News', 'Financial Times', 'pubDate'),
    ('https://www.ft.com/companies/financials?format=rss', 'item', 'link', 'title', 'media:content', 'url', 'Business & Finance', 'Financial Times', 'pubDate'),
    ('https://www.ft.com/companies/health?format=rss', 'item', 'link', 'title', 'media:content', 'url', 'Self Dev', 'Financial Times', 'pubDate'),
    ('https://www.ft.com/emerging-markets?format=rss', 'item', 'link', 'title', 'media:content', 'url', 'Business & Finance', 'Financial Times', 'pubDate'),
    ('https://www.ft.com/companies/technology?format=rss', 'item', 'link', 'title', 'media:content', 'url', 'Science & Technology', 'Financial Times', 'pubDate'),
    ('https://www.ft.com/world/americas?format=rss', 'item', 'link', 'title', 'media:content', 'url', 'Global News', 'Financial Times', 'pubDate'),
    ('https://www.ft.com/world/mideast?format=rss', 'item', 'link', 'title', 'media:content', 'url', 'Global News', 'Financial Times', 'pubDate'),
    ('https://www.ft.com/companies?format=rss', 'item', 'link', 'title', 'media:content', 'url', 'Business & Finance', 'Financial Times', 'pubDate'),
    ('https://www.ft.com/companies/energy?format=rss', 'item', 'link', 'title', 'media:content', 'url', 'Business & Finance', 'Financial Times', 'pubDate'),
    ('https://www.ft.com/companies/industrials?format=rss', 'item', 'link', 'title', 'media:content', 'url', 'Business & Finance', 'Financial Times', 'pubDate'),
    ('https://www.ft.com/companies/media?format=rss', 'item', 'link', 'title', 'media:content', 'url', 'Self Dev', 'Financial Times', 'pubDate'),
    ('https://www.ft.com/companies/professional-services?format=rss', 'item', 'link', 'title', 'media:content', 'url', 'Business & Finance', 'Financial Times', 'pubDate'),
    ('https://www.ft.com/companies/retail-consumer?format=rss', 'item', 'link', 'title', 'media:content', 'url', 'Business & Finance', 'Financial Times', 'pubDate'),
    ('https://www.ft.com/companies/telecoms?format=rss', 'item', 'link', 'title', 'media:content', 'url', 'Business & Finance', 'Financial Times', 'pubDate'),
    ('https://www.ft.com/companies/transport?format=rss', 'item', 'link', 'title', 'media:content', 'url', 'Business & Finance', 'Financial Times', 'pubDate'),
    ('https://www.ft.com/markets?format=rss', 'item', 'link', 'title', 'media:content', 'url', 'Business & Finance', 'Financial Times', 'pubDate'),
    ('https://www.ft.com/climate-capital?format=rss', 'item', 'link', 'title', 'media:content', 'url', 'Science & Technology', 'Financial Times', 'pubDate'),
    ('https://www.ft.com/opinion?format=rss', 'item', 'link', 'title', 'media:content', 'url', 'Politics', 'Financial Times', 'pubDate'),
    ('https://www.ft.com/work-careers?format=rss', 'item', 'link', 'title', 'media:content', 'url', 'Self Dev', 'Financial Times', 'pubDate'),
 
    ('https://www.newyorker.com/feed/everything', 'item', 'link', 'title', 'media:content', 'url', 'Global News', 'New Yorker', 'pubDate'),
    ('https://www.newyorker.com/feed/posts', 'item', 'link', 'title', 'media:content', 'url', 'Global News', 'New Yorker', 'pubDate'),
    ('https://www.newyorker.com/feed/magazine/rss', 'item', 'link', 'title', 'media:content', 'url', 'Global News', 'New Yorker', 'pubDate'),
    ('https://www.newyorker.com/feed/news', 'item', 'link', 'title', 'media:content', 'url', 'Global News', 'New Yorker', 'pubDate'),
    ('https://www.newyorker.com/feed/news/news-desk', 'item', 'link', 'title', 'media:content', 'url', 'Global News', 'New Yorker', 'pubDate'),
    ('https://www.newyorker.com/feed/news/daily-comment', 'item', 'link', 'title', 'media:content', 'url', 'Self Dev', 'New Yorker', 'pubDate'),
    ('https://www.newyorker.com/feed/news/amy-davidson', 'item', 'link', 'title', 'media:content', 'url', 'Self Dev', 'New Yorker', 'pubDate'),
    ('https://www.newyorker.com/feed/news/john-cassidy', 'item', 'link', 'title', 'media:content', 'url', 'Self Dev', 'New Yorker', 'pubDate'),
    ('https://www.newyorker.com/feed/culture', 'item', 'link', 'title', 'media:content', 'url', 'Self Dev', 'New Yorker', 'pubDate'),
    ('https://www.newyorker.com/feed/culture/culture-desk', 'item', 'link', 'title', 'media:content', 'url', 'Self Dev', 'New Yorker', 'pubDate'),
    ('https://www.newyorker.com/feed/culture/cultural-comment', 'item', 'link', 'title', 'media:content', 'url', 'Self Dev', 'New Yorker', 'pubDate'),
    ('https://www.newyorker.com/feed/culture/photo-booth', 'item', 'link', 'title', 'media:content', 'url', 'Self Dev', 'New Yorker', 'pubDate'),
    ('https://www.newyorker.com/feed/humor', 'item', 'link', 'title', 'media:content', 'url', 'Self Dev', 'New Yorker', 'pubDate'),
    ('https://www.newyorker.com/feed/humor/borowitz-report', 'item', 'link', 'title', 'media:content', 'url', 'Self Dev', 'New Yorker', 'pubDate'),
    ('https://www.newyorker.com/feed/cartoons/issue-cartoons', 'item', 'link', 'title', 'media:content', 'url', 'Self Dev', 'New Yorker', 'pubDate'),
    ('https://www.newyorker.com/feed/cartoons/daily-cartoon', 'item', 'link', 'title', 'media:content', 'url', 'Self Dev', 'New Yorker', 'pubDate'),
    ('https://www.newyorker.com/feed/tag/books/rss', 'item', 'link', 'title', 'media:content', 'url', 'Self Dev', 'New Yorker', 'pubDate'),
    ('https://www.newyorker.com/feed/books/page-turner', 'item', 'link', 'title', 'media:content', 'url', 'Self Dev', 'New Yorker', 'pubDate'),
    ('https://www.newyorker.com/feed/tech', 'item', 'link', 'title', 'media:content', 'url', 'Science & Technology', 'New Yorker', 'pubDate'),
    ('https://www.newyorker.com/feed/tech/elements', 'item', 'link', 'title', 'media:content', 'url', 'Science & Technology', 'New Yorker', 'pubDate'),
    ('https://www.newyorker.com/services/rss/feeds/campaign_trail.xml', 'item', 'link', 'title', 'media:content', 'url', 'Politics', 'New Yorker', 'pubDate'),
    ('https://www.newyorker.com/feed/podcast/fiction', 'item', 'link', 'title', 'media:content', 'url', 'Self Dev', 'New Yorker', 'pubDate'),
    ('http://feeds.wnyc.org/tnyauthorsvoice', 'item', 'link', 'title', 'media:content', 'url', 'Self Dev', 'New Yorker', 'pubDate'),
    ('https://www.newyorker.com/services/rss/feeds/poetry_podcast.xml', 'item', 'link', 'title', 'media:content', 'url', 'Self Dev', 'New Yorker', 'pubDate'),
    ('https://www.newyorker.com/services/rss/feeds/newyorker_outloud.xml', 'item', 'link', 'title', 'media:content', 'url', 'Self Dev', 'New Yorker', 'pubDate'),

    
    ('http://www.thisisanfield.com/feed/', 'item', 'link', 'title', 'enclosure', 'url', 'Liverpool FC','This is Anfield', 'pubDate'),
    ('http://www.theguardian.com/football/rss', 'item', 'link', 'title', 'media:content', 'url', 'Football', 'The Guardian', 'pubDate'),

    ('https://theathletic.com/team/liverpool/?rss=1', 'item', 'link', 'title', 'media:content', 'href', 'Liverpool FC','The Athletic','pubDate'),
    ('https://theathletic.com/premier-league/?rss', 'item', 'link', 'title', 'media:content', 'href', 'Football','The Athletic', 'published'),
    ('https://theathletic.com/soccer/?rss',  'item', 'link', 'title', 'media:content', 'href', 'Football','The Athletic','published'),
    ('https://theathletic.com/champions-league/?rss',  'item', 'link', 'title', 'media:content', 'href', 'Football','The Athletic', 'published'),

    ('https://www.autosport.com/rss/feed/f1', 'item', 'link', 'title', 'enclosure', 'url', 'Formula 1', 'Autosport', 'pubDate'),
    ('https://the-race.com/category/formula-1/feed/', 'item', 'link', 'title','media:content', 'url', 'Formula 1', 'The Race', 'pubDate'),
    ('https://aeon.co/feed.rss', 'item', 'link', 'title', 'media:content', 'url', 'Self Dev', "Aeon", 'pubDate'),
    ('https://psyche.co/feed', 'item', 'link', 'title', 'media:content', 'url', 'Self Dev', "Psyche", 'pubDate'),

    ('http://www.nytimes.com/services/xml/rss/nyt/Opinion.xml', 'item', 'link', 'title', 'media:content', 'url', 'Politics', "New York Times", 'pubDate'),
    ('http://www.nytimes.com/services/xml/rss/nyt/Magazine.xml', 'item', 'link', 'title', 'media:content', 'url', 'Self Dev', "New York Times", 'pubDate'),
    ('http://www.nytimes.com/services/xml/rss/nyt/Science.xml', 'item', 'link', 'title', 'media:content', 'url', 'Science & Technology', "New York Times", 'pubDate'),
    ('http://www.nytimes.com/services/xml/rss/nyt/Travel.xml', 'item', 'link', 'title', 'media:content', 'url', 'Travel', "New York Times", 'pubDate'),
    ('http://www.nytimes.com/services/xml/rss/nyt/Style.xml', 'item', 'link', 'title', 'media:content', 'url', 'Self Dev', "New York Times", 'pubDate'),
    ('http://www.nytimes.com/services/xml/rss/nyt/Technology.xml', 'item', 'link', 'title', 'media:content', 'url', 'Science & Technology', "New York Times", 'pubDate'),
    ('http://www.nytimes.com/services/xml/rss/nyt/Business.xml', 'item', 'link', 'title', 'media:content', 'url', 'Business & Finance', "New York Times", 'pubDate'),
    ('http://www.nytimes.com/services/xml/rss/nyt/HomePage.xml', 'item', 'link', 'title', 'media:content', 'url', 'Global News', "New York Times", 'pubDate'),
    ('https://www.nytimes.com/wirecutter/rss/', 'item', 'link', 'title', 'description', 'src', 'Science & Technology', "New York Times Wirecutter", 'pubDate'),

    ('http://www.smithsonianmag.com/rss/innovation/', 'item', 'link', 'title', 'enclosure', 'url', 'Science & Technology', "Smithsonian", 'pubDate'),
    ('http://www.smithsonianmag.com/rss/latest_articles/', 'item', 'link', 'title', 'enclosure', 'url', 'Science & Technology', "Smithsonian", 'pubDate'),

    ('http://feeds.feedburner.com/dawn-news', 'item', 'link', 'title',  'media:content', 'url', 'Pakistan', "Dawn", 'pubDate'),
    ('https://feeds.feedburner.com/dawn-news-world', 'item', 'link', 'title',  'media:content', 'url', 'Global News', "Dawn", 'pubDate'),

    ('http://www.theverge.com/android/rss/index.xml', 'entry', 'id', 'title', 'media:content', 'url', 'Science & Technology', 'The Verge', 'published'),
    ('http://www.theverge.com/apple/rss/index.xml', 'entry', 'id', 'title', 'media:content', 'url', 'Science & Technology', 'The Verge', 'published'),
    ('http://www.theverge.com/apps/rss/index.xml', 'entry', 'id', 'title', 'media:content', 'url', 'Science & Technology', 'The Verge', 'published'),
    ('https://www.theverge.com/rss/climate-change/index.xml', 'entry', 'id', 'title', 'media:content', 'url', 'Science & Technology', 'The Verge', 'published'),
    ('https://www.theverge.com/rss/cryptocurrency/index.xml', 'entry', 'id', 'title', 'media:content', 'url', 'Science & Technology', 'The Verge', 'published'),
    ('https://www.theverge.com/rss/creators/index.xml', 'entry', 'id', 'title', 'media:content', 'url', 'Science & Technology', 'The Verge', 'published'),
    ('https://www.theverge.com/rss/cyber-security/index.xml', 'entry', 'id', 'title', 'media:content', 'url', 'Science & Technology', 'The Verge', 'published'),
    ('https://www.theverge.com/rss/good-deals/index.xml', 'entry', 'id', 'title', 'media:content', 'url', 'Science & Technology', 'The Verge', 'published'),
    ('https://www.theverge.com/rss/decoder-podcast-with-nilay-patel/index.xml', 'entry', 'id', 'title', 'media:content', 'url', 'Science & Technology', 'The Verge', 'published'),
    ('https://www.theverge.com/rss/elon-musk/index.xml', 'entry', 'id', 'title', 'media:content', 'url', 'Science & Technology', 'The Verge', 'published'),
    ('https://www.theverge.com/rss/facebook/index.xml', 'entry', 'id', 'title', 'media:content', 'url', 'Science & Technology', 'The Verge', 'published'),
    ('https://www.theverge.com/rss/film/index.xml', 'entry', 'id', 'title', 'media:content', 'url', 'Science & Technology', 'The Verge', 'published'),
    ('https://www.theverge.com/rss/gadgets/index.xml', 'entry', 'id', 'title', 'media:content', 'url', 'Science & Technology', 'The Verge', 'published'),
    ('https://www.theverge.com/rss/games/index.xml', 'entry', 'id', 'title', 'media:content', 'url', 'Science & Technology', 'The Verge', 'published'),
    ('https://www.theverge.com/rss/google/index.xml', 'entry', 'id', 'title', 'media:content', 'url', 'Science & Technology', 'The Verge', 'published'),
    ('https://www.theverge.com/rss/hot-pod-newsletter/index.xml', 'entry', 'id', 'title', 'media:content', 'url', 'Science & Technology', 'The Verge', 'published'),
    ('https://www.theverge.com/rss/how-to/index.xml', 'entry', 'id', 'title', 'media:content', 'url', 'Science & Technology', 'The Verge', 'published'),
    ('https://www.theverge.com/rss/meta/index.xml', 'entry', 'id', 'title', 'media:content', 'url', 'Science & Technology', 'The Verge', 'published'),
    ('http://www.theverge.com/microsoft/rss/index.xml', 'entry', 'id', 'title', 'media:content', 'url', 'Science & Technology', 'The Verge', 'published'),
    ('http://www.theverge.com/policy/rss/index.xml', 'entry', 'id', 'title', 'media:content', 'url', 'Science & Technology', 'The Verge', 'published'),
    ('https://www.theverge.com/rss/reviews/index.xml', 'entry', 'id', 'title', 'media:content', 'url', 'Science & Technology', 'The Verge', 'published'),
    ('https://www.theverge.com/rss/samsung/index.xml', 'entry', 'id', 'title', 'media:content', 'url', 'Science & Technology', 'The Verge', 'published'),
    ('https://www.theverge.com/rss/science/index.xml', 'entry', 'id', 'title', 'media:content', 'url', 'Science & Technology', 'The Verge', 'published'),
    ('https://www.theverge.com/rss/space/index.xml', 'entry', 'id', 'title', 'media:content', 'url', 'Science & Technology', 'The Verge', 'published'),
    ('https://www.theverge.com/rss/streaming-wars/index.xml', 'entry', 'id', 'title', 'media:content', 'url', 'Science & Technology', 'The Verge', 'published'),
    ('https://www.theverge.com/rss/tesla/index.xml', 'entry', 'id', 'title', 'media:content', 'url', 'Science & Technology', 'The Verge', 'published'),
    ('https://www.theverge.com/rss/the-vergecast/index.xml', 'entry', 'id', 'title', 'media:content', 'url', 'Science & Technology', 'The Verge', 'published'),
    ('https://www.theverge.com/rss/tiktok/index.xml', 'entry', 'id', 'title', 'media:content', 'url', 'Science & Technology', 'The Verge', 'published'),
    ('https://www.theverge.com/rss/transportation/index.xml', 'entry', 'id', 'title', 'media:content', 'url', 'Science & Technology', 'The Verge', 'published'),
    ('https://www.theverge.com/rss/tv/index.xml', 'entry', 'id', 'title', 'media:content', 'url', 'Science & Technology', 'The Verge', 'published'),
    ('https://www.theverge.com/rss/twitter/index.xml', 'entry', 'id', 'title', 'media:content', 'url', 'Science & Technology', 'The Verge', 'published'),
    ('https://www.theverge.com/rss/youtube/index.xml', 'entry', 'id', 'title', 'media:content', 'url', 'Science & Technology', 'The Verge', 'published')

]
    yield "Starting the update process..."
    

    items = []  # Assuming you have a list to store the results

    with ThreadPoolExecutor() as executor:
        futures = {executor.submit(fetch_feed, *item): item for item in rss_feed_details}
        for future in futures:
            item = futures[future]
            try:
                items.extend(future.result())
            except Exception as e:
                print(f"Error fetching feed: {e}, the item is {item}")

    
    total_items = len(items)
    processed_items = 0

    yield "Checking and storing items in the database..."
    for message in check_and_store_items_with_yield(items):
        processed_items += 1
        progress = (processed_items / total_items) * 100
        yield f"data: {message} ({processed_items}/{total_items} processed) | Progress: {progress:.2f}%\n\n"

    yield "Update process completed successfully."

    documents = get_documents_from_db()
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=2024, chunk_overlap=204)
    all_splits = text_splitter.split_documents(documents)
    
    vectorstore = FAISS.from_documents(documents=all_splits, embedding=OpenAIEmbeddings(model="text-embedding-3-small", api_key=openai_api_key))
    filepath = os.path.join(os.path.dirname(__file__), 'vectorstore')
    vectorstore.save_local(filepath)

#('https://theathletic.com/team/liverpool/?rss=1', 'item', 'link', 'title', 'media:content', '', 'Liverpool FC','The Athletic','pubDate'),
def fetch_feed(url, main_tag, link_tag, title_tag, image_tag, image_attr, category, website, date_tag):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml-xml')
    entries = [] 

    for entry in soup.find_all(main_tag):
        try:
            title = entry.find(title_tag).text
            link = entry.find(link_tag).text
            date = entry.find(date_tag).text
            published = normalize_datetime_to_django_format(date)
            image = " "

            if image_tag:
                if "NPR" in website:
                    content_encoded = entry.find('content:encoded').text
                    image_soup = BeautifulSoup(content_encoded, 'html.parser')
                    image = image_soup.find('img')['src']
                    if "https" not in image or image == None:
                        images = [
                            'https://images.unsplash.com/photo-1495020689067-958852a7765e?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8bmV3c3xlbnwwfHwwfHx8MA%3D%3D',
                            'https://images.unsplash.com/photo-1523995462485-3d171b5c8fa9?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8M3x8bmV3c3xlbnwwfHwwfHx8MA%3D%3D',
                            'https://images.unsplash.com/photo-1502772066658-3006ff41449b?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTF8fG5ld3N8ZW58MHx8MHx8fDA%3D',
                            'https://plus.unsplash.com/premium_photo-1673474112205-037558e54995?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTN8fHdvcmxkfGVufDB8fDB8fHww',
                            'https://images.unsplash.com/photo-1707276121668-39bcc7c2fc47?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTR8fHdvcmxkfGVufDB8fDB8fHww',
                            'https://images.unsplash.com/photo-1616438096142-602cf94da735?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mjd8fHdvcmxkfGVufDB8fDB8fHww',
                            'https://images.unsplash.com/photo-1615363049459-db5d76db4b8f?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MzJ8fHdvcmxkfGVufDB8fDB8fHww',
                            'https://images.unsplash.com/photo-1526470608268-f674ce90ebd4?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MzZ8fHdvcmxkfGVufDB8fDB8fHww',
                            'https://images.unsplash.com/photo-1444703686981-a3abbc4d4fe3?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NDJ8fHdvcmxkfGVufDB8fDB8fHww',
                            'https://plus.unsplash.com/premium_photo-1672423156257-9a2bc5e1f480?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NXx8ZmluYW5jZXxlbnwwfHwwfHx8MA%3D%3D',
                            'https://images.unsplash.com/photo-1607269910784-aafe40882991?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTZ8fGZpbmFuY2V8ZW58MHx8MHx8fDA%3D',
                            'https://plus.unsplash.com/premium_photo-1679279544754-ad72be8acf94?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MzN8fGZpbmFuY2V8ZW58MHx8MHx8fDA%3D',
                            'https://plus.unsplash.com/premium_photo-1688822016374-5cd4536db272?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NDF8fGZpbmFuY2V8ZW58MHx8MHx8fDA%3D',
                            'https://plus.unsplash.com/premium_photo-1678824564752-0dbccfa53670?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8ODV8fGZpbmFuY2V8ZW58MHx8MHx8fDA%3D'
                        ]

                        image = random.choice(images)

                elif "Ahead of AI" in website:
                        enclosure = entry.find('enclosure')
                        image = enclosure['url'] if enclosure else None
                        
                elif "AI-Tech Park" in website:
                    content_encoded = entry.find('content:encoded')
                    description = entry.find('description')
                    if content_encoded:
                        content_soup = BeautifulSoup(content_encoded.text, 'html.parser')
                        img_tag = content_soup.find('img')
                        if img_tag:
                            image = img_tag['src']
                    elif description:
                        description_soup = BeautifulSoup(description.text, 'html.parser')
                        img_tag = description_soup.find('img')
                        if img_tag:
                            image = img_tag['src']
                
                elif "AI Accelerator Institute" in website:
                    media_content = entry.find('media:content')
                    image = media_content['url'] if media_content else None
                    
                    if not image:  # If no image found in 'media:content', look in 'content:encoded'
                        content_encoded = entry.find('content:encoded')
                        if content_encoded:
                            content_soup = BeautifulSoup(content_encoded.text, 'html.parser')
                            img_tag = content_soup.find('img')
                            if img_tag:
                                image = img_tag['src']
                elif "AI Business" in website:
                    media_thumbnail = entry.find('media:thumbnail')
                    media_content = entry.find('media:content')
                    
                    image = media_thumbnail['url'] if media_thumbnail else None
                    if not image and media_content:
                        image = media_content['url']

                elif "KnowTechie" in website:
                    content_encoded = entry.find('content:encoded')
                    image = None

                    if content_encoded:
                        content_soup = BeautifulSoup(content_encoded.text, 'html.parser')
                        img_tag = content_soup.find('img')
                        if img_tag and 'src' in img_tag.attrs:
                            image = img_tag['src']

                elif 'AIModels.fyi' in website:
                    enclosure = entry.find('enclosure')
                    if enclosure and enclosure.get('type', '').startswith('image/'):
                        image = enclosure['url']
                    else:
                        content_encoded = entry.find('content:encoded')
                        if content_encoded:
                            content_soup = BeautifulSoup(content_encoded.text, 'html.parser')
                            img_tag = content_soup.find('img')
                            if img_tag and 'src' in img_tag.attrs:
                                image = img_tag['src']
                elif "VentureBeat" in website:
                    image = None
                    media_content = entry.find('media:content')
                    if media_content and media_content.get('url'):
                        image = media_content['url']
                    else:
                        content_encoded = entry.find('content:encoded')
                        if content_encoded:
                            content_soup = BeautifulSoup(content_encoded.text, 'html.parser')
                            img_tag = content_soup.find('img')
                            if img_tag and 'src' in img_tag.attrs:
                                image = img_tag['src']
                elif "AI Snake Oil" in website:
                    enclosure = entry.find('enclosure')
                    if enclosure and enclosure.get('url'):
                        image = enclosure['url']
                    else:
                        content_encoded = entry.find('content:encoded')
                        if content_encoded:
                            content_soup = BeautifulSoup(content_encoded.text, 'html.parser')
                            img_tag = content_soup.find('img')
                            if img_tag and 'src' in img_tag.attrs:
                                image = img_tag['src']

                elif "SiliconANGLE" in website:
                    enclosure = entry.find('enclosure')
                    if enclosure and enclosure.get('url'):
                        image = enclosure['url']
                    else:
                        media_content = entry.find('media:content')
                        if media_content and media_content.get('url'):
                            image = media_content['url']
                        else:
                            media_thumbnail = entry.find('media:thumbnail')
                            if media_thumbnail and media_thumbnail.get('url'):
                                image = media_thumbnail['url']

                elif "MarkTechPost" in website:
                    description = entry.find('description')
                    if description:
                        description_soup = BeautifulSoup(description.text, 'html.parser')
                        img_tag = description_soup.find('img')
                        if img_tag and img_tag.get('src'):
                            image = img_tag['src']
                    
                    # Check in media:content
                    if not image:
                        media_content = entry.find('media:content')
                        if media_content and media_content.get('url'):
                            image = media_content['url']

                elif 'Artificial intelligence (AI) | The Guardian' in website:
                    media_content = entry.find('media:content')
                    if media_content and media_content.get('url'):
                        image = media_content['url']

                elif 'MIT News - Machine learning' in website:
                    media_content = entry.find('media:content')
                    if media_content and media_content.get('url'):
                        image = media_content['url']

                elif 'MIT Technology Review' in website:
                    media_content = entry.find('media:content')
                    if media_content and media_content.get('url'):
                        image = media_content['url']
                    else:
                        images = [
                            'https://images.unsplash.com/photo-1495020689067-958852a7765e?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8bmV3c3xlbnwwfHwwfHx8MA%3D%3D',
                            'https://images.unsplash.com/photo-1523995462485-3d171b5c8fa9?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8M3x8bmV3c3xlbnwwfHwwfHx8MA%3D%3D',
                            'https://images.unsplash.com/photo-1502772066658-3006ff41449b?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTF8fG5ld3N8ZW58MHx8MHx8fDA%3D',
                            'https://plus.unsplash.com/premium_photo-1673474112205-037558e54995?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTN8fHdvcmxkfGVufDB8fDB8fHww',
                            'https://images.unsplash.com/photo-1707276121668-39bcc7c2fc47?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTR8fHdvcmxkfGVufDB8fDB8fHww',
                            'https://images.unsplash.com/photo-1616438096142-602cf94da735?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mjd8fHdvcmxkfGVufDB8fDB8fHww',
                            'https://images.unsplash.com/photo-1615363049459-db5d76db4b8f?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MzJ8fHdvcmxkfGVufDB8fDB8fHww',
                            'https://images.unsplash.com/photo-1526470608268-f674ce90ebd4?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MzZ8fHdvcmxkfGVufDB8fDB8fHww',
                            'https://images.unsplash.com/photo-1444703686981-a3abbc4d4fe3?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NDJ8fHdvcmxkfGVufDB8fDB8fHww',
                            'https://plus.unsplash.com/premium_photo-1672423156257-9a2bc5e1f480?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NXx8ZmluYW5jZXxlbnwwfHwwfHx8MA%3D%3D',
                            'https://images.unsplash.com/photo-1607269910784-aafe40882991?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTZ8fGZpbmFuY2V8ZW58MHx8MHx8fDA%3D',
                            'https://plus.unsplash.com/premium_photo-1679279544754-ad72be8acf94?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MzN8fGZpbmFuY2V8ZW58MHx8MHx8fDA%3D',
                            'https://plus.unsplash.com/premium_photo-1688822016374-5cd4536db272?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NDF8fGZpbmFuY2V8ZW58MHx8MHx8fDA%3D',
                            'https://plus.unsplash.com/premium_photo-1678824564752-0dbccfa53670?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8ODV8fGZpbmFuY2V8ZW58MHx8MHx8fDA%3D'
                        ]

                        image = random.choice(images)

                elif "CNBC" in website: 
                    image_u = entry.find("media:content")
                    if image_u is not None:
                        image = image_u.get("url")
                    else:
                        images = [
                            'https://images.unsplash.com/photo-1495020689067-958852a7765e?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8bmV3c3xlbnwwfHwwfHx8MA%3D%3D',
                            'https://images.unsplash.com/photo-1523995462485-3d171b5c8fa9?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8M3x8bmV3c3xlbnwwfHwwfHx8MA%3D%3D',
                            'https://images.unsplash.com/photo-1502772066658-3006ff41449b?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTF8fG5ld3N8ZW58MHx8MHx8fDA%3D',
                            'https://plus.unsplash.com/premium_photo-1673474112205-037558e54995?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTN8fHdvcmxkfGVufDB8fDB8fHww',
                            'https://images.unsplash.com/photo-1707276121668-39bcc7c2fc47?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTR8fHdvcmxkfGVufDB8fDB8fHww',
                            'https://images.unsplash.com/photo-1616438096142-602cf94da735?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mjd8fHdvcmxkfGVufDB8fDB8fHww',
                            'https://images.unsplash.com/photo-1615363049459-db5d76db4b8f?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MzJ8fHdvcmxkfGVufDB8fDB8fHww',
                            'https://images.unsplash.com/photo-1526470608268-f674ce90ebd4?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MzZ8fHdvcmxkfGVufDB8fDB8fHww',
                            'https://images.unsplash.com/photo-1444703686981-a3abbc4d4fe3?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NDJ8fHdvcmxkfGVufDB8fDB8fHww',
                            'https://plus.unsplash.com/premium_photo-1672423156257-9a2bc5e1f480?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NXx8ZmluYW5jZXxlbnwwfHwwfHx8MA%3D%3D',
                            'https://images.unsplash.com/photo-1607269910784-aafe40882991?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTZ8fGZpbmFuY2V8ZW58MHx8MHx8fDA%3D',
                            'https://plus.unsplash.com/premium_photo-1679279544754-ad72be8acf94?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MzN8fGZpbmFuY2V8ZW58MHx8MHx8fDA%3D',
                            'https://plus.unsplash.com/premium_photo-1688822016374-5cd4536db272?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NDF8fGZpbmFuY2V8ZW58MHx8MHx8fDA%3D',
                            'https://plus.unsplash.com/premium_photo-1678824564752-0dbccfa53670?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8ODV8fGZpbmFuY2V8ZW58MHx8MHx8fDA%3D'
                        ]

                        image = random.choice(images)

                elif "Reuters" in website:
                    image_tag = entry.find('media:content') or entry.find('image') or None
                    if image_tag:
                        image = image_tag.get('url')
                    else:
                        images = [
                            'https://images.unsplash.com/photo-1495020689067-958852a7765e?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8bmV3c3xlbnwwfHwwfHx8MA%3D%3D',
                            'https://images.unsplash.com/photo-1523995462485-3d171b5c8fa9?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8M3x8bmV3c3xlbnwwfHwwfHx8MA%3D%3D',
                            'https://images.unsplash.com/photo-1502772066658-3006ff41449b?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTF8fG5ld3N8ZW58MHx8MHx8fDA%3D',
                            'https://plus.unsplash.com/premium_photo-1673474112205-037558e54995?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTN8fHdvcmxkfGVufDB8fDB8fHww',
                            'https://images.unsplash.com/photo-1707276121668-39bcc7c2fc47?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTR8fHdvcmxkfGVufDB8fDB8fHww',
                            'https://images.unsplash.com/photo-1616438096142-602cf94da735?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mjd8fHdvcmxkfGVufDB8fDB8fHww',
                            'https://images.unsplash.com/photo-1615363049459-db5d76db4b8f?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MzJ8fHdvcmxkfGVufDB8fDB8fHww',
                            'https://images.unsplash.com/photo-1526470608268-f674ce90ebd4?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MzZ8fHdvcmxkfGVufDB8fDB8fHww',
                            'https://images.unsplash.com/photo-1444703686981-a3abbc4d4fe3?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NDJ8fHdvcmxkfGVufDB8fDB8fHww',
                            'https://plus.unsplash.com/premium_photo-1672423156257-9a2bc5e1f480?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NXx8ZmluYW5jZXxlbnwwfHwwfHx8MA%3D%3D',
                            'https://images.unsplash.com/photo-1607269910784-aafe40882991?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTZ8fGZpbmFuY2V8ZW58MHx8MHx8fDA%3D',
                            'https://plus.unsplash.com/premium_photo-1679279544754-ad72be8acf94?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MzN8fGZpbmFuY2V8ZW58MHx8MHx8fDA%3D',
                            'https://plus.unsplash.com/premium_photo-1688822016374-5cd4536db272?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NDF8fGZpbmFuY2V8ZW58MHx8MHx8fDA%3D',
                            'https://plus.unsplash.com/premium_photo-1678824564752-0dbccfa53670?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8ODV8fGZpbmFuY2V8ZW58MHx8MHx8fDA%3D'
                        ]

                        image = random.choice(images)

                elif "The New Yorker" in website:
                    image = entry.find('media:thumbnail')['url'] if entry.find('media:thumbnail') else 'No Image'
                    if image == 'No Image':
                        images = [
                            'https://images.unsplash.com/photo-1495020689067-958852a7765e?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8bmV3c3xlbnwwfHwwfHx8MA%3D%3D',
                            'https://images.unsplash.com/photo-1523995462485-3d171b5c8fa9?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8M3x8bmV3c3xlbnwwfHwwfHx8MA%3D%3D',
                            'https://images.unsplash.com/photo-1502772066658-3006ff41449b?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTF8fG5ld3N8ZW58MHx8MHx8fDA%3D',
                            'https://plus.unsplash.com/premium_photo-1673474112205-037558e54995?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTN8fHdvcmxkfGVufDB8fDB8fHww',
                            'https://images.unsplash.com/photo-1707276121668-39bcc7c2fc47?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTR8fHdvcmxkfGVufDB8fDB8fHww',
                            'https://images.unsplash.com/photo-1616438096142-602cf94da735?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mjd8fHdvcmxkfGVufDB8fDB8fHww',
                            'https://images.unsplash.com/photo-1615363049459-db5d76db4b8f?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MzJ8fHdvcmxkfGVufDB8fDB8fHww',
                            'https://images.unsplash.com/photo-1526470608268-f674ce90ebd4?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MzZ8fHdvcmxkfGVufDB8fDB8fHww',
                            'https://images.unsplash.com/photo-1444703686981-a3abbc4d4fe3?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NDJ8fHdvcmxkfGVufDB8fDB8fHww',
                            'https://plus.unsplash.com/premium_photo-1672423156257-9a2bc5e1f480?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NXx8ZmluYW5jZXxlbnwwfHwwfHx8MA%3D%3D',
                            'https://images.unsplash.com/photo-1607269910784-aafe40882991?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTZ8fGZpbmFuY2V8ZW58MHx8MHx8fDA%3D',
                            'https://plus.unsplash.com/premium_photo-1679279544754-ad72be8acf94?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MzN8fGZpbmFuY2V8ZW58MHx8MHx8fDA%3D',
                            'https://plus.unsplash.com/premium_photo-1688822016374-5cd4536db272?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NDF8fGZpbmFuY2V8ZW58MHx8MHx8fDA%3D',
                            'https://plus.unsplash.com/premium_photo-1678824564752-0dbccfa53670?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8ODV8fGZpbmFuY2V8ZW58MHx8MHx8fDA%3D'
                        ]

                        image = random.choice(images)

                elif "Psyche" in website or "Aeon" in website:
                    description_content = entry.find('description').text
                    description_soup = BeautifulSoup(description_content, 'html.parser')
                    image_tag_obj = description_soup.find('img')
                    image = image_tag_obj.get('src')
                
                elif "The Athletic" in website:
                    media_content = entry.find('media:content')
                    if media_content:
                        image = media_content.get('url')
                    else:
                        if "liverpool" in url:
                            image = 'https://images.unsplash.com/photo-1518188049456-7a3a9e263ab2?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1674&q=80'
                        else:
                            image = 'https://images.unsplash.com/photo-1486286701208-1d58e9338013?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1770&q=80'
                        
                elif "The Guardian" in website:
                    media_content_tags = entry.find_all('media:content')

                    # Initialize variables to store the URL with the highest width
                    max_width = 0
                    selected_image = None

                    # Iterate through the media content tags to find the one with the highest width
                    for media_content in media_content_tags:
                        if 'url' in media_content.attrs and 'width' in media_content.attrs:
                            width = int(media_content['width'])
                            url = media_content['url']
                            if width > max_width:
                                max_width = width
                                selected_image = url

                    # Use the selected image URL
                    if selected_image:
                        image = selected_image
                    else:
                        image = 'https://images.unsplash.com/photo-1555862124-94036092ab14?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1771&q=80'

                elif website == "New York Times Wirecutter":
                    description_content = entry.find('description').text
                    description_soup = BeautifulSoup(description_content, 'html.parser')
                    image_tag_obj = description_soup.find('img')
                    if image_tag_obj:
                        image = image_tag_obj['src']
                    else:
                        images = ["https://images.unsplash.com/photo-1451187580459-43490279c0fa?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1772&q=80","https://images.unsplash.com/photo-1531297484001-80022131f5a1?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8dGVjaHxlbnwwfDB8MHx8fDA%3D&auto=format&fit=crop&w=1400&q=60","https://images.unsplash.com/photo-1523961131990-5ea7c61b2107?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NXx8dGVjaHxlbnwwfDB8MHx8fDA%3D&auto=format&fit=crop&w=1400&q=60","https://images.unsplash.com/photo-1550745165-9bc0b252726f?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8OHx8dGVjaHxlbnwwfDB8MHx8fDA%3D&auto=format&fit=crop&w=1400&q=60","https://images.unsplash.com/photo-1550751827-4bd374c3f58b?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTB8fHRlY2h8ZW58MHwwfDB8fHww&auto=format&fit=crop&w=1400&q=60","https://images.unsplash.com/photo-1518770660439-4636190af475?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTF8fHRlY2h8ZW58MHwwfDB8fHww&auto=format&fit=crop&w=1400&q=60","https://images.unsplash.com/photo-1496065187959-7f07b8353c55?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTR8fHRlY2h8ZW58MHwwfDB8fHww&auto=format&fit=crop&w=1400&q=60"]
                        image = random.choice(images)


                elif "New York Times" in website:
                    media_content = entry.find('media:content')

                    if media_content and media_content.get('url'):
                        image = media_content.get('url')
                    else:
                        print("No media:content or url found for this entry")
                        images = ["https://images.unsplash.com/photo-1451187580459-43490279c0fa?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1772&q=80","https://images.unsplash.com/photo-1531297484001-80022131f5a1?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8dGVjaHxlbnwwfDB8MHx8fDA%3D&auto=format&fit=crop&w=1400&q=60","https://images.unsplash.com/photo-1523961131990-5ea7c61b2107?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NXx8dGVjaHxlbnwwfDB8MHx8fDA%3D&auto=format&fit=crop&w=1400&q=60","https://images.unsplash.com/photo-1550745165-9bc0b252726f?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8OHx8dGVjaHxlbnwwfDB8MHx8fDA%3D&auto=format&fit=crop&w=1400&q=60","https://images.unsplash.com/photo-1550751827-4bd374c3f58b?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTB8fHRlY2h8ZW58MHwwfDB8fHww&auto=format&fit=crop&w=1400&q=60","https://images.unsplash.com/photo-1518770660439-4636190af475?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTF8fHRlY2h8ZW58MHwwfDB8fHww&auto=format&fit=crop&w=1400&q=60","https://images.unsplash.com/photo-1496065187959-7f07b8353c55?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTR8fHRlY2h8ZW58MHwwfDB8fHww&auto=format&fit=crop&w=1400&q=60"]
                        image = random.choice(images)

                elif website == "Autosport":
                    enclosure_tag = entry.find('enclosure')
                    if enclosure_tag and 'url' in enclosure_tag.attrs:
                        image = enclosure_tag['url']
                    else:
                        image = 'https://images.unsplash.com/photo-1656337449909-141091f4df4a?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=774&q=80'

                elif website == 'The Race':
                    media_content = entry.find('media:content')
                    if media_content and 'url' in media_content.attrs:
                        image = media_content['url']
                    else:
                        image = 'https://images.unsplash.com/photo-1656337449909-141091f4df4a?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=774&q=80'

                elif website == 'This is Anfield':
                    media_thumbnail = entry.find('media:thumbnail')
                    if media_thumbnail and 'url' in media_thumbnail.attrs:
                        image = media_thumbnail['url']
                    else:
                        image = 'https://images.unsplash.com/photo-1555862124-94036092ab14?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1771&q=80'

                elif website == 'The Verge':
                    content = entry.find('content')
                    if content:
                        content_soup = BeautifulSoup(content.text, 'html.parser')
                        img_tag = content_soup.find('img')
                        image = img_tag.get('src') if img_tag else None
                
                elif 'smithsonian' in url:
                        enclosure = entry.find('enclosure')
                        image = enclosure.get('url') if enclosure else None
                        """ images = ["https://images.unsplash.com/photo-1451187580459-43490279c0fa?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1772&q=80","https://images.unsplash.com/photo-1531297484001-80022131f5a1?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8dGVjaHxlbnwwfDB8MHx8fDA%3D&auto=format&fit=crop&w=1400&q=60","https://images.unsplash.com/photo-1523961131990-5ea7c61b2107?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NXx8dGVjaHxlbnwwfDB8MHx8fDA%3D&auto=format&fit=crop&w=1400&q=60","https://images.unsplash.com/photo-1550745165-9bc0b252726f?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8OHx8dGVjaHxlbnwwfDB8MHx8fDA%3D&auto=format&fit=crop&w=1400&q=60","https://images.unsplash.com/photo-1550751827-4bd374c3f58b?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTB8fHRlY2h8ZW58MHwwfDB8fHww&auto=format&fit=crop&w=1400&q=60","https://images.unsplash.com/photo-1518770660439-4636190af475?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTF8fHRlY2h8ZW58MHwwfDB8fHww&auto=format&fit=crop&w=1400&q=60","https://images.unsplash.com/photo-1496065187959-7f07b8353c55?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTR8fHRlY2h8ZW58MHwwfDB8fHww&auto=format&fit=crop&w=1400&q=60"]
                        image = random.choice(images)
 """
                elif "dawn" in link:
                    media_content = entry.find('media:content')
                    if media_content and 'url' in media_content.attrs:
                        image = media_content['url']
                    else:
                        image = 'https://images.unsplash.com/photo-1588414884049-eb55cd4c72b4?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=776&q=80'
            
                else:
                    image = entry.find(image_tag, {image_attr: True})
                    if not image:
                        images = [
                            'https://images.unsplash.com/photo-1495020689067-958852a7765e?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8bmV3c3xlbnwwfHwwfHx8MA%3D%3D',
                            'https://images.unsplash.com/photo-1523995462485-3d171b5c8fa9?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8M3x8bmV3c3xlbnwwfHwwfHx8MA%3D%3D',
                            'https://images.unsplash.com/photo-1502772066658-3006ff41449b?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTF8fG5ld3N8ZW58MHx8MHx8fDA%3D',
                            'https://plus.unsplash.com/premium_photo-1673474112205-037558e54995?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTN8fHdvcmxkfGVufDB8fDB8fHww',
                            'https://images.unsplash.com/photo-1707276121668-39bcc7c2fc47?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTR8fHdvcmxkfGVufDB8fDB8fHww',
                            'https://images.unsplash.com/photo-1616438096142-602cf94da735?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mjd8fHdvcmxkfGVufDB8fDB8fHww',
                            'https://images.unsplash.com/photo-1615363049459-db5d76db4b8f?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MzJ8fHdvcmxkfGVufDB8fDB8fHww',
                            'https://images.unsplash.com/photo-1526470608268-f674ce90ebd4?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MzZ8fHdvcmxkfGVufDB8fDB8fHww',
                            'https://images.unsplash.com/photo-1444703686981-a3abbc4d4fe3?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NDJ8fHdvcmxkfGVufDB8fDB8fHww',
                            'https://plus.unsplash.com/premium_photo-1672423156257-9a2bc5e1f480?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NXx8ZmluYW5jZXxlbnwwfHwwfHx8MA%3D%3D',
                            'https://images.unsplash.com/photo-1607269910784-aafe40882991?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTZ8fGZpbmFuY2V8ZW58MHx8MHx8fDA%3D',
                            'https://plus.unsplash.com/premium_photo-1679279544754-ad72be8acf94?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MzN8fGZpbmFuY2V8ZW58MHx8MHx8fDA%3D',
                            'https://plus.unsplash.com/premium_photo-1688822016374-5cd4536db272?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NDF8fGZpbmFuY2V8ZW58MHx8MHx8fDA%3D',
                            'https://plus.unsplash.com/premium_photo-1678824564752-0dbccfa53670?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8ODV8fGZpbmFuY2V8ZW58MHx8MHx8fDA%3D'
                        ]

                        image = random.choice(images)
            
            else:
                images = [
                            'https://images.unsplash.com/photo-1495020689067-958852a7765e?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8bmV3c3xlbnwwfHwwfHx8MA%3D%3D',
                            'https://images.unsplash.com/photo-1523995462485-3d171b5c8fa9?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8M3x8bmV3c3xlbnwwfHwwfHx8MA%3D%3D',
                            'https://images.unsplash.com/photo-1502772066658-3006ff41449b?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTF8fG5ld3N8ZW58MHx8MHx8fDA%3D',
                            'https://plus.unsplash.com/premium_photo-1673474112205-037558e54995?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTN8fHdvcmxkfGVufDB8fDB8fHww',
                            'https://images.unsplash.com/photo-1707276121668-39bcc7c2fc47?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTR8fHdvcmxkfGVufDB8fDB8fHww',
                            'https://images.unsplash.com/photo-1616438096142-602cf94da735?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mjd8fHdvcmxkfGVufDB8fDB8fHww',
                            'https://images.unsplash.com/photo-1615363049459-db5d76db4b8f?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MzJ8fHdvcmxkfGVufDB8fDB8fHww',
                            'https://images.unsplash.com/photo-1526470608268-f674ce90ebd4?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MzZ8fHdvcmxkfGVufDB8fDB8fHww',
                            'https://images.unsplash.com/photo-1444703686981-a3abbc4d4fe3?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NDJ8fHdvcmxkfGVufDB8fDB8fHww',
                            'https://plus.unsplash.com/premium_photo-1672423156257-9a2bc5e1f480?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NXx8ZmluYW5jZXxlbnwwfHwwfHx8MA%3D%3D',
                            'https://images.unsplash.com/photo-1607269910784-aafe40882991?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTZ8fGZpbmFuY2V8ZW58MHx8MHx8fDA%3D',
                            'https://plus.unsplash.com/premium_photo-1679279544754-ad72be8acf94?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MzN8fGZpbmFuY2V8ZW58MHx8MHx8fDA%3D',
                            'https://plus.unsplash.com/premium_photo-1688822016374-5cd4536db272?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NDF8fGZpbmFuY2V8ZW58MHx8MHx8fDA%3D',
                            'https://plus.unsplash.com/premium_photo-1678824564752-0dbccfa53670?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8ODV8fGZpbmFuY2V8ZW58MHx8MHx8fDA%3D'
                        ]

                image = random.choice(images)
            
            entries.append([title, link, category, website, published, image])

        except Exception as e:
            print(f"Error processing an entry from {url}: {e}")
            continue

    return entries

def normalize_datetime_to_django_format(dt_str):
    dt = parse(dt_str)
    return dt.strftime('%Y-%m-%d %H:%M:%S%z')

def fetch_nyt(url):
    response = requests.get("https://r.jina.ai/"+url)
    return response.text

### Check and store new items in the database with progress updates

def process_item(item):
    title, link, category, website, published, image = item
    
    if int(published[0:4]) >= 2023:
        if not Article.objects.filter(link=link).exists():
            yield f"Fetching full text for: {title}"
            
            if "nytimes" in link or "www.nytimes.com/athletic" in link:
                full_text = fetch_nyt(link)
            else:
                full_text = fetch_full_article(link)
            
            yield f"Summarizing article: {title}"
            sum = summarize_text(full_text) if full_text else "No summary available"
            summary = "This is an article by "+ website + ". " + sum
            yield f"summary: {summary}"


            Article.objects.create(
                title=title,
                link=link,
                summary=summary,
                category=category,
                website=website,
                published=published,
                image=image,
            )
            yield f"Stored article: {title}"

        else:
            yield f"Article with link {link} already exists. Skipping..."

    else:
        yield f"This Article is too old to be stored: {title}"
        
def check_and_store_items_with_yield(items):
    total_items = len(items)
    processed_count = 0

    with ThreadPoolExecutor(max_workers=1) as executor:
        futures = [executor.submit(process_item, item) for item in items]

        for future in concurrent.futures.as_completed(futures):
            try:
                for result in future.result():
                    processed_count += 1
                    yield f"{result} | Processed {processed_count}/{total_items}"
            except Exception as e:
                yield f"An error occurred: {e}"

### Function to summarize text using OpenAI
def summarize_text(text):
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"), )

    system_prompt = {
    "role": "system",
    "content":
    "You are a text processing model. Your task is to extract and return the main body of text from the provided content. Focus on the core text of the article, preserving its paragraph structure. Ignore any extraneous elements such as advertisements, navigation links, or non-article content. Do not exceed the length of 10 sentences.",
}

# Initialize the chat history
    chat_history = [system_prompt]

    # Get user input from the console
    user_input = text

    # Append the user input to the chat history
    chat_history.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(model="llama-3.1-70b-versatile",
                                                messages=chat_history,
                                                temperature=1.2)
    return response.choices[0].message.content

    """ llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
        api_key=openai_api_key, 
    ) """


    """ llm = ChatGroq(
    model="llama3-groq-70b-8192-tool-use-preview",
    api_key=groq_api_key,
    #model="llama3-8b-8192",
    #model="llama-3.1-8b-instant",
    ) 

    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        )  
    
    messages = [
        (
            "system",
            "You are a text processing model. Your task is to extract and return the main body of text from the provided content. Focus on the core text of the article, preserving its paragraph structure. Ignore any extraneous elements such as advertisements, navigation links, or non-article content. Do not exceed the length of 10 sentences.",
        ),
        ("human", text),
    ]
    summarized_text = llm.invoke(messages)
    return summarized_text.content """

### Function to fetch full article content
def fetch_full_article(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        article_text = ' '.join(p.text for p in soup.find_all('p'))
        return article_text
    return None


### Function to get documents from the database for RAG
def get_documents_from_db():
    articles = Article.objects.all()
    documents = []
    for article in articles:
        metadata = {
            'source': article.link,
            'title': article.title,
            'description': article.summary,
            'category': article.category,
            'website': article.website,
            'published': article.published.strftime('%Y-%m-%d %H:%M:%S%z'),
            'language': 'en-US'  # Assuming the language is English
        }
        doc = Document(page_content=article.summary, metadata=metadata)
        documents.append(doc)
    return documents

### Function to generate a response using RAG
def get_rag_response(query):
    filepath = os.path.join(os.path.dirname(__file__), 'vectorstore')
    vectorstore = FAISS.load_local(filepath, OpenAIEmbeddings(model="text-embedding-3-small", api_key=openai_api_key), allow_dangerous_deserialization=True)

    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 10})
    
    llm = ChatOpenAI(model="gpt-4o-mini", api_key=openai_api_key)

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    

    template = """Use the following pieces of context to answer the question at the end.
    If you don't know the answer, just say that you don't know, don't try to make up an answer.
    Use 10 sentences maximum and keep the answer as concise as possible.

    {context}

    Question: {question}

    Helpful Answer:"""
    custom_rag_prompt = PromptTemplate.from_template(template)

    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | custom_rag_prompt
        | llm
        | StrOutputParser()
    )

    answer = rag_chain.invoke(query)
    return answer
















""" 
rss_feed_details = [
    ('https://www.ft.com/world?format=rss', 'item', 'link', 'title', 'media:content', 'url', 'Global News', 'Financial Times', 'pubDate'),
    ('https://www.ft.com/global-economy?format=rss', 'item', 'link', 'title', 'media:content', 'url', 'Global News', 'Financial Times', 'pubDate'),
    ('https://www.ft.com/world/uk?format=rss', 'item', 'link', 'title', 'media:content', 'url', 'Global News', 'Financial Times', 'pubDate'),
    ('https://www.ft.com/world/us?format=rss', 'item', 'link', 'title', 'media:content', 'url', 'Global News', 'Financial Times', 'pubDate'),
    ('https://www.ft.com/world/africa?format=rss', 'item', 'link', 'title', 'media:content', 'url', 'Global News', 'Financial Times', 'pubDate'),
    ('https://www.ft.com/world/asia-pacific?format=rss', 'item', 'link', 'title', 'media:content', 'url', 'Global News', 'Financial Times', 'pubDate'),
    ('https://www.ft.com/world/europe?format=rss', 'item', 'link', 'title', 'media:content', 'url', 'Global News', 'Financial Times', 'pubDate'),
    ('https://www.ft.com/companies/financials?format=rss', 'item', 'link', 'title', 'media:content', 'url', 'Business & Finance', 'Financial Times', 'pubDate'),
    ('https://www.ft.com/companies/health?format=rss', 'item', 'link', 'title', 'media:content', 'url', 'Self Dev', 'Financial Times', 'pubDate'),
    ('https://www.ft.com/emerging-markets?format=rss', 'item', 'link', 'title', 'media:content', 'url', 'Business & Finance', 'Financial Times', 'pubDate'),
    ('https://www.ft.com/companies/technology?format=rss', 'item', 'link', 'title', 'media:content', 'url', 'Science & Technology', 'Financial Times', 'pubDate'),
    ('https://www.ft.com/world/americas?format=rss', 'item', 'link', 'title', 'media:content', 'url', 'Global News', 'Financial Times', 'pubDate'),
    ('https://www.ft.com/world/mideast?format=rss', 'item', 'link', 'title', 'media:content', 'url', 'Global News', 'Financial Times', 'pubDate'),
    ('https://www.ft.com/companies?format=rss', 'item', 'link', 'title', 'media:content', 'url', 'Business & Finance', 'Financial Times', 'pubDate'),
    ('https://www.ft.com/companies/energy?format=rss', 'item', 'link', 'title', 'media:content', 'url', 'Business & Finance', 'Financial Times', 'pubDate'),
    ('https://www.ft.com/companies/industrials?format=rss', 'item', 'link', 'title', 'media:content', 'url', 'Business & Finance', 'Financial Times', 'pubDate'),
    ('https://www.ft.com/companies/media?format=rss', 'item', 'link', 'title', 'media:content', 'url', 'Self Dev', 'Financial Times', 'pubDate'),
    ('https://www.ft.com/companies/professional-services?format=rss', 'item', 'link', 'title', 'media:content', 'url', 'Business & Finance', 'Financial Times', 'pubDate'),
    ('https://www.ft.com/companies/retail-consumer?format=rss', 'item', 'link', 'title', 'media:content', 'url', 'Business & Finance', 'Financial Times', 'pubDate'),
    ('https://www.ft.com/companies/telecoms?format=rss', 'item', 'link', 'title', 'media:content', 'url', 'Business & Finance', 'Financial Times', 'pubDate'),
    ('https://www.ft.com/companies/transport?format=rss', 'item', 'link', 'title', 'media:content', 'url', 'Business & Finance', 'Financial Times', 'pubDate'),
    ('https://www.ft.com/markets?format=rss', 'item', 'link', 'title', 'media:content', 'url', 'Business & Finance', 'Financial Times', 'pubDate'),
    ('https://www.ft.com/climate-capital?format=rss', 'item', 'link', 'title', 'media:content', 'url', 'Science & Technology', 'Financial Times', 'pubDate'),
    ('https://www.ft.com/opinion?format=rss', 'item', 'link', 'title', 'media:content', 'url', 'Politics', 'Financial Times', 'pubDate'),
    ('https://www.ft.com/work-careers?format=rss', 'item', 'link', 'title', 'media:content', 'url', 'Self Dev', 'Financial Times', 'pubDate'),

    ("https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=100003114", 'item', 'link', 'title', 'media:content', 'url', 'Global News', 'CNBC', 'pubDate'),  # Top News
    ("https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=100727362", 'item', 'link', 'title', 'media:content', 'url', 'Global News', 'CNBC', 'pubDate'),  # World News
    ("https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=15837362", 'item', 'link', 'title', 'media:content', 'url', 'Global News', 'CNBC', 'pubDate'),  # US News
    ("https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=19832390", 'item', 'link', 'title', 'media:content', 'url', 'Global News', 'CNBC', 'pubDate'),  # Asia News
    ("https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=19794221", 'item', 'link', 'title', 'media:content', 'url', 'Global News', 'CNBC', 'pubDate'),  # Europe News
    ("https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=10001147", 'item', 'link', 'title', 'media:content', 'url', 'Business & Finance', 'CNBC', 'pubDate'),  # Business
    ("https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=15839135", 'item', 'link', 'title', 'media:content', 'url', 'Business & Finance', 'CNBC', 'pubDate'),  # Earnings
    ("https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=100370673", 'item', 'link', 'title', 'media:content', 'url', 'Self Dev', 'CNBC', 'pubDate'),  # Commentary
    ("https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=20910258", 'item', 'link', 'title', 'media:content', 'url', 'Business & Finance', 'CNBC', 'pubDate'),  # Economy
    ("https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=10000664", 'item', 'link', 'title', 'media:content', 'url', 'Business & Finance', 'CNBC', 'pubDate'),  # Finance
    ("https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=19854910", 'item', 'link', 'title', 'media:content', 'url', 'Science & Technology', 'CNBC', 'pubDate'),  # Technology
    ("https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=10000113", 'item', 'link', 'title', 'media:content', 'url', 'Politics', 'CNBC', 'pubDate'),  # Politics
    ("https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=10000108", 'item', 'link', 'title', 'media:content', 'url', 'Self Dev', 'CNBC', 'pubDate'),  # Health Care
    ("https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=10000115", 'item', 'link', 'title', 'media:content', 'url', 'Self Dev', 'CNBC', 'pubDate'),  # Real Estate
        ("https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=10000115", 'item', 'link', 'title', 'media:content', 'url', 'Self Dev', 'CNBC', 'pubDate'),  # Real Estate
    ("https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=10001054", 'item', 'link', 'title', 'media:content', 'url', 'Self Dev', 'CNBC', 'pubDate'),  # Wealth
    ("https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=10000101", 'item', 'link', 'title', 'media:content', 'url', 'Self Dev', 'CNBC', 'pubDate'),  # Autos
    ("https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=19836768", 'item', 'link', 'title', 'media:content', 'url', 'Business & Finance', 'CNBC', 'pubDate'),  # Energy
    ("https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=10000110", 'item', 'link', 'title', 'media:content', 'url', 'Self Dev', 'CNBC', 'pubDate'),  # Media
    ("https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=10000116", 'item', 'link', 'title', 'media:content', 'url', 'Self Dev', 'CNBC', 'pubDate'),  # Retail
    ("https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=10000739", 'item', 'link', 'title', 'media:content', 'url', 'Travel', 'CNBC', 'pubDate'),  # Travel
    ("https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=44877279", 'item', 'link', 'title', 'media:content', 'url', 'Self Dev', 'CNBC', 'pubDate'),  # Small Business
    ("https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=15839069", 'item', 'link', 'title', 'media:content', 'url', 'Business & Finance', 'CNBC', 'pubDate'),  # Investing
    ("https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=100646281", 'item', 'link', 'title', 'media:content', 'url', 'Self Dev', 'CNBC', 'pubDate'),  # Financial Advisors
    ("https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=21324812", 'item', 'link', 'title', 'media:content', 'url', 'Self Dev', 'CNBC', 'pubDate'),  # Personal Finance
    ("https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=23103686", 'item', 'link', 'title', 'media:content', 'url', 'Science & Technology', 'CNBC', 'pubDate'),  # Charting Asia
    ("https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=17646093", 'item', 'link', 'title', 'media:content', 'url', 'Self Dev', 'CNBC', 'pubDate'),  # Funny Business
    ("https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=20409666", 'item', 'link', 'title', 'media:content', 'url', 'Business & Finance', 'CNBC', 'pubDate'),  # Market Insider
    ("https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=38818154", 'item', 'link', 'title', 'media:content', 'url', 'Business & Finance', 'CNBC', 'pubDate'),  # NetNet
    ("https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=20398120", 'item', 'link', 'title', 'media:content', 'url', 'Business & Finance', 'CNBC', 'pubDate'),  # Trader Talk
    ("https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=19206666", 'item', 'link', 'title', 'media:content', 'url', 'Business & Finance', 'CNBC', 'pubDate'),  # Buffett Watch
    ("https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=15839263", 'item', 'link', 'title', 'media:content', 'url', 'Business & Finance', 'CNBC', 'pubDate'),  # Buffett Watch

    ('https://feeds.npr.org/1001/rss.xml', 'item', 'link', 'title', 'media:content', 'url', 'Global News', 'NPR', 'pubDate'),
    ('https://feeds.npr.org/1002/rss.xml', 'item', 'link', 'title', 'media:content', 'url', 'Global News', 'NPR', 'pubDate'),
    ('https://feeds.npr.org/1003/rss.xml', 'item', 'link', 'title', 'media:content', 'url', 'Global News', 'NPR', 'pubDate'),
    ('https://feeds.npr.org/1004/rss.xml', 'item', 'link', 'title', 'media:content', 'url', 'Global News', 'NPR', 'pubDate'),
    ('https://feeds.npr.org/1006/rss.xml', 'item', 'link', 'title', 'media:content', 'url', 'Global News', 'NPR', 'pubDate'),
    ('https://feeds.npr.org/1007/rss.xml', 'item', 'link', 'title', 'media:content', 'url', 'Science & Technology', 'NPR', 'pubDate'),
    ('https://feeds.npr.org/1008/rss.xml', 'item', 'link', 'title', 'media:content', 'url', 'Self Dev', 'NPR', 'pubDate'),
    ('https://feeds.npr.org/1009/rss.xml', 'item', 'link', 'title', 'media:content', 'url', 'Global News', 'NPR', 'pubDate'),
    ('https://feeds.npr.org/1012/rss.xml', 'item', 'link', 'title', 'media:content', 'url', 'Global News', 'NPR', 'pubDate'),
    ('https://feeds.npr.org/1013/rss.xml', 'item', 'link', 'title', 'media:content', 'url', 'Self Dev', 'NPR', 'pubDate'),
    ('https://feeds.npr.org/1014/rss.xml', 'item', 'link', 'title', 'media:content', 'url', 'Global News', 'NPR', 'pubDate'),
    ('https://feeds.npr.org/1015/rss.xml', 'item', 'link', 'title', 'media:content', 'url', 'Global News', 'NPR', 'pubDate'),
    ('https://feeds.npr.org/1016/rss.xml', 'item', 'link', 'title', 'media:content', 'url', 'Self Dev', 'NPR', 'pubDate'),
    ('https://feeds.npr.org/1017/rss.xml', 'item', 'link', 'title', 'media:content', 'url', 'Global News', 'NPR', 'pubDate'),
    ('https://feeds.npr.org/1018/rss.xml', 'item', 'link', 'title', 'media:content', 'url', 'Self Dev', 'NPR', 'pubDate'),
    ('https://feeds.npr.org/1019/rss.xml', 'item', 'link', 'title', 'media:content', 'url', 'Science & Technology', 'NPR', 'pubDate'),
    ('https://feeds.npr.org/1020/rss.xml', 'item', 'link', 'title', 'media:content', 'url', 'Self Dev', 'NPR', 'pubDate'),
    ('https://feeds.npr.org/1023/rss.xml', 'item', 'link', 'title', 'media:content', 'url', 'Travel', 'NPR', 'pubDate'),
    ('https://feeds.npr.org/1024/rss.xml', 'item', 'link', 'title', 'media:content', 'url', 'Science & Technology', 'NPR', 'pubDate'),
    ('https://feeds.npr.org/1025/rss.xml', 'item', 'link', 'title', 'media:content', 'url', 'Science & Technology', 'NPR', 'pubDate'),
    ('https://feeds.npr.org/1026/rss.xml', 'item', 'link', 'title', 'media:content', 'url', 'Science & Technology', 'NPR', 'pubDate'),
    ('https://feeds.npr.org/1027/rss.xml', 'item', 'link', 'title', 'media:content', 'url', 'Science & Technology', 'NPR', 'pubDate'),
    ('https://feeds.npr.org/1028/rss.xml', 'item', 'link', 'title', 'media:content', 'url', 'Self Dev', 'NPR', 'pubDate'),
    ('https://feeds.npr.org/1029/rss.xml', 'item', 'link', 'title', 'media:content', 'url', 'Self Dev', 'NPR', 'pubDate'),
    ('https://feeds.npr.org/1030/rss.xml', 'item', 'link', 'title', 'media:content', 'url', 'Self Dev', 'NPR', 'pubDate'),
    ('https://feeds.npr.org/1031/rss.xml', 'item', 'link', 'title', 'media:content', 'url', 'Global News', 'NPR', 'pubDate'),
    ('https://feeds.npr.org/1032/rss.xml', 'item', 'link', 'title', 'media:content', 'url', 'Self Dev', 'NPR', 'pubDate'),
    ('https://feeds.npr.org/1033/rss.xml', 'item', 'link', 'title', 'media:content', 'url', 'Self Dev', 'NPR', 'pubDate'),
    ('https://feeds.npr.org/1034/rss.xml', 'item', 'link', 'title', 'media:content', 'url', 'Self Dev', 'NPR', 'pubDate'),
    ('https://feeds.npr.org/1039/rss.xml', 'item', 'link', 'title', 'media:content', 'url', 'Self Dev', 'NPR', 'pubDate'),
    ('https://feeds.npr.org/1040/rss.xml', 'item', 'link', 'title', 'media:content', 'url', 'Self Dev', 'NPR', 'pubDate'),
    ('https://feeds.npr.org/1045/rss.xml', 'item', 'link', 'title', 'media:content', 'url', 'Self Dev', 'NPR', 'pubDate'),
    ('https://feeds.npr.org/1046/rss.xml', 'item', 'link', 'title', 'media:content', 'url', 'Self Dev', 'NPR', 'pubDate'),
    ('https://feeds.npr.org/1047/rss.xml', 'item', 'link', 'title', 'media:content', 'url', 'Self Dev', 'NPR', 'pubDate'),
    ('https://feeds.npr.org/1048/rss.xml', 'item', 'link', 'title', 'media:content', 'url', 'Self Dev', 'NPR', 'pubDate'),
    ('https://feeds.npr.org/1051/rss.xml', 'item', 'link', 'title', 'media:content', 'url', 'Self Dev', 'NPR', 'pubDate'),
    ('https://feeds.npr.org/1052/rss.xml', 'item', 'link', 'title', 'media:content', 'url', 'Self Dev', 'NPR', 'pubDate'),
    ('https://feeds.npr.org/1053/rss.xml', 'item', 'link', 'title', 'media:content', 'url', 'Travel', 'NPR', 'pubDate'),
    ('https://feeds.npr.org/1054/rss.xml', 'item', 'link', 'title', 'media:content', 'url', 'Travel', 'NPR', 'pubDate'),
    ('https://feeds.npr.org/1055/rss.xml', 'item', 'link', 'title', 'media:content', 'url', 'Football', 'NPR', 'pubDate'),
    ('https://feeds.npr.org/1056/rss.xml', 'item', 'link', 'title', 'media:content', 'url', 'Global News', 'NPR', 'pubDate'),
    ('https://feeds.npr.org/1057/rss.xml', 'item', 'link', 'title', 'media:content', 'url', 'Global News', 'NPR', 'pubDate'),
    ('https://feeds.npr.org/1059/rss.xml', 'item', 'link', 'title', 'media:content', 'url', 'Global News', 'NPR', 'pubDate'),
    ('https://feeds.npr.org/1061/rss.xml', 'item', 'link', 'title', 'media:content', 'url', 'Self Dev', 'NPR', 'pubDate'),
    ('https://feeds.npr.org/1062/rss.xml', 'item', 'link', 'title', 'media:content', 'url', 'Global News', 'NPR', 'pubDate'),
    ('https://feeds.npr.org/1064/rss.xml', 'item', 'link', 'title', 'media:content', 'url', 'Self Dev', 'NPR', 'pubDate'),
    ('https://feeds.npr.org/1065/rss.xml', 'item', 'link', 'title', 'media:content', 'url', 'Travel', 'NPR', 'pubDate'),
    ('https://feeds.npr.org/1066/rss.xml', 'item', 'link', 'title', 'media:content', 'url', 'Self Dev', 'NPR', 'pubDate'),
    ('https://feeds.npr.org/1070/rss.xml', 'item', 'link', 'title', 'media:content', 'url', 'Global News', 'NPR', 'pubDate'),
    ('https://feeds.npr.org/1074/rss.xml', 'item', 'link', 'title', 'media:content', 'url', 'Self Dev', 'NPR', 'pubDate'),
    ('https://feeds.npr.org/1076/rss.xml', 'item', 'link', 'title', 'media:content', 'url', 'Global News', 'NPR', 'pubDate'),
    ('https://feeds.npr.org/1077/rss.xml', 'item', 'link', 'title', 'media:content', 'url', 'Global News', 'NPR', 'pubDate'),
    ('https://feeds.npr.org/1078/rss.xml', 'item', 'link', 'title', 'media:content', 'url', 'Global News', 'NPR', 'pubDate'),
    ('https://feeds.npr.org/1083/rss.xml', 'item', 'link', 'title', 'media:content', 'url', 'Global News', 'NPR', 'pubDate'),
    ('https://feeds.npr.org/1085/rss.xml', 'item', 'link', 'title', 'media:content', 'url', 'Self Dev', 'NPR', 'pubDate'),
    ('https://feeds.npr.org/1086/rss.xml', 'item', 'link', 'title', 'media:content', 'url', 'Self Dev', 'NPR', 'pubDate'),
    ('https://feeds.npr.org/1087/rss.xml', 'item', 'link', 'title', 'media:content', 'url', 'Travel', 'NPR', 'pubDate'),
    ('https://feeds.npr.org/1088/rss.xml', 'item', 'link', 'title', 'media:content', 'url', 'Travel', 'NPR', 'pubDate'),
    ('https://feeds.npr.org/1089/rss.xml', 'item', 'link', 'title', 'media:content', 'url', 'Self Dev', 'NPR', 'pubDate'),
    ('https://feeds.npr.org/1090/rss.xml', 'item', 'link', 'title', 'media:content', 'url', 'Global News', 'NPR', 'pubDate'),
    ('https://feeds.npr.org/1095/rss.xml', 'item', 'link', 'title', 'media:content', 'url', 'Global News', 'NPR', 'pubDate'),
    ('https://feeds.npr.org/1096/rss.xml', 'item', 'link', 'title', 'media:content', 'url', 'Travel', 'NPR', 'pubDate'),
    ('https://feeds.npr.org/1103/rss.xml', 'item', 'link', 'title', 'media:content', 'url', 'Self Dev', 'NPR', 'pubDate'),
    ('https://feeds.npr.org/1104/rss.xml', 'item', 'link', 'title', 'media:content', 'url', 'Self Dev', 'NPR', 'pubDate'),
    ('https://feeds.npr.org/1105/rss.xml', 'item', 'link', 'title', 'media:content', 'url', 'Self Dev', 'NPR', 'pubDate'),
    ('https://feeds.npr.org/1106/rss.xml', 'item', 'link', 'title', 'media:content', 'url', 'Self Dev', 'NPR', 'pubDate'),
    ('https://feeds.npr.org/1107/rss.xml', 'item', 'link', 'title', 'media:content', 'url', 'Self Dev', 'NPR', 'pubDate'),
    ('https://feeds.npr.org/1108/rss.xml', 'item', 'link', 'title', 'media:content', 'url', 'Self Dev', 'NPR', 'pubDate'),
    ('https://feeds.npr.org/1109/rss.xml', 'item', 'link', 'title', 'media:content', 'url', 'Self Dev', 'NPR', 'pubDate'),
    ('https://feeds.npr.org/1110/rss.xml', 'item', 'link', 'title', 'media:content', 'url', 'Self Dev', 'NPR', 'pubDate'),
    ('https://feeds.npr.org/1124/rss.xml', 'item', 'link', 'title', 'media:content', 'url', 'Global News', 'NPR', 'pubDate'),
    ('https://feeds.npr.org/1125/rss.xml', 'item', 'link', 'title', 'media:content', 'url', 'Global News', 'NPR', 'pubDate'),
    ('https://feeds.npr.org/1126/rss.xml', 'item', 'link', 'title', 'media:content', 'url', 'Global News', 'NPR', 'pubDate'),
    ('https://feeds.npr.org/1127/rss.xml', 'item', 'link', 'title', 'media:content', 'url', 'Global News', 'NPR', 'pubDate'),
    ('https://feeds.npr.org/1128/rss.xml', 'item', 'link', 'title', 'media:content', 'url', 'Self Dev', 'NPR', 'pubDate'),
    ('https://feeds.npr.org/1131/rss.xml', 'item', 'link', 'title', 'media:content', 'url', 'Science & Technology', 'NPR', 'pubDate'),
    ('https://feeds.npr.org/1132/rss.xml', 'item', 'link', 'title', 'media:content', 'url', 'Science & Technology', 'NPR', 'pubDate'),
    ('https://feeds.npr.org/1133/rss.xml', 'item', 'link', 'title', 'media:content', 'url', 'Self Dev', 'NPR', 'pubDate'),
    ('https://feeds.npr.org/1134/rss.xml', 'item', 'link', 'title', 'media:content', 'url', 'Self Dev', 'NPR', 'pubDate'),
    ('https://feeds.npr.org/1135/rss.xml', 'item', 'link', 'title', 'media:content', 'url', 'Science & Technology', 'NPR', 'pubDate'),
    ('https://feeds.npr.org/1136/rss.xml', 'item', 'link', 'title', 'media:content', 'url', 'Global News', 'NPR', 'pubDate'),
    ('https://feeds.npr.org/1137/rss.xml', 'item', 'link', 'title', 'media:content', 'url', 'Self Dev', 'NPR', 'pubDate'),
    ('https://feeds.npr.org/1138/rss.xml', 'item', 'link', 'title', 'media:content', 'url', 'Self Dev', 'NPR', 'pubDate'),
    ('https://feeds.npr.org/1139/rss.xml', 'item', 'link', 'title', 'media:content', 'url', 'Travel', 'NPR', 'pubDate'),
    ('https://feeds.npr.org/1141/rss.xml', 'item', 'link', 'title', 'media:content', 'url', 'Self Dev', 'NPR', 'pubDate'),
    ('https://feeds.npr.org/1142/rss.xml', 'item', 'link', 'title', 'media:content', 'url', 'Science & Technology', 'NPR', 'pubDate'),
    ('https://feeds.npr.org/1143/rss.xml', 'item', 'link', 'title', 'media:content', 'url', 'Self Dev', 'NPR', 'pubDate'),
    ('https://feeds.npr.org/1144/rss.xml', 'item', 'link', 'title', 'media:content', 'url', 'Self Dev', 'NPR', 'pubDate'),
    ('https://feeds.npr.org/1145/rss.xml', 'item', 'link', 'title', 'media:content', 'url', 'Self Dev', 'NPR', 'pubDate'),
    ('https://feeds.npr.org/1146/rss.xml', 'item', 'link', 'title', 'media:content', 'url', 'Global News', 'NPR', 'pubDate'),
    ('https://feeds.npr.org/1149/rss.xml', 'item', 'link', 'title', 'media:content', 'url', 'Global News', 'NPR', 'pubDate'),
    ('https://feeds.npr.org/1150/rss.xml', 'item', 'link', 'title', 'media:content', 'url', 'Global News', 'NPR', 'pubDate'),
    ('https://feeds.npr.org/1151/rss.xml', 'item', 'link', 'title', 'media:content', 'url', 'Self Dev', 'NPR', 'pubDate'),
    ('https://feeds.npr.org/1161/rss.xml', 'item', 'link', 'title', 'media:content', 'url', 'Self Dev', 'NPR', 'pubDate'),
    ('https://feeds.npr.org/1162/rss.xml', 'item', 'link', 'title', 'media:content', 'url', 'Global News', 'NPR', 'pubDate'),
    ('https://feeds.npr.org/1163/rss.xml', 'item', 'link', 'title', 'media:content', 'url', 'Self Dev', 'NPR', 'pubDate'),
    ('https://feeds.npr.org/1164/rss.xml', 'item', 'link', 'title', 'media:content', 'url', 'Self Dev', 'NPR', 'pubDate'),
    ('https://feeds.npr.org/1165/rss.xml', 'item', 'link', 'title', 'media:content', 'url', 'Global News', 'NPR', 'pubDate'),
    ('https://feeds.npr.org/1166/rss.xml', 'item', 'link', 'title', 'media:content', 'url', 'Self Dev', 'NPR', 'pubDate'),
    ('https://feeds.npr.org/1167/rss.xml', 'item', 'link', 'title', 'media:content', 'url', 'Science & Technology', 'NPR', 'pubDate'),

    ('https://www.newyorker.com/feed/everything', 'item', 'link', 'title', 'media:content', 'url', 'Global News', 'New Yorker', 'pubDate'),
    ('https://www.newyorker.com/feed/posts', 'item', 'link', 'title', 'media:content', 'url', 'Global News', 'New Yorker', 'pubDate'),
    ('https://www.newyorker.com/feed/magazine/rss', 'item', 'link', 'title', 'media:content', 'url', 'Global News', 'New Yorker', 'pubDate'),
    ('https://www.newyorker.com/feed/news', 'item', 'link', 'title', 'media:content', 'url', 'Global News', 'New Yorker', 'pubDate'),
    ('https://www.newyorker.com/feed/news/news-desk', 'item', 'link', 'title', 'media:content', 'url', 'Global News', 'New Yorker', 'pubDate'),
    ('https://www.newyorker.com/feed/news/daily-comment', 'item', 'link', 'title', 'media:content', 'url', 'Global News', 'New Yorker', 'pubDate'),
    ('https://www.newyorker.com/feed/news/amy-davidson', 'item', 'link', 'title', 'media:content', 'url', 'Global News', 'New Yorker', 'pubDate'),
    ('https://www.newyorker.com/feed/news/john-cassidy', 'item', 'link', 'title', 'media:content', 'url', 'Global News', 'New Yorker', 'pubDate'),
    ('https://www.newyorker.com/feed/culture', 'item', 'link', 'title', 'media:content', 'url', 'Self Dev', 'New Yorker', 'pubDate'),
    ('https://www.newyorker.com/feed/culture/culture-desk', 'item', 'link', 'title', 'media:content', 'url', 'Self Dev', 'New Yorker', 'pubDate'),
    ('https://www.newyorker.com/feed/culture/cultural-comment', 'item', 'link', 'title', 'media:content', 'url', 'Self Dev', 'New Yorker', 'pubDate'),
    ('https://www.newyorker.com/feed/culture/photo-booth', 'item', 'link', 'title', 'media:content', 'url', 'Self Dev', 'New Yorker', 'pubDate'),
    ('https://www.newyorker.com/feed/humor', 'item', 'link', 'title', 'media:content', 'url', 'Self Dev', 'New Yorker', 'pubDate'),
    ('https://www.newyorker.com/feed/humor/borowitz-report', 'item', 'link', 'title', 'media:content', 'url', 'Self Dev', 'New Yorker', 'pubDate'),
    ('https://www.newyorker.com/feed/cartoons/issue-cartoons', 'item', 'link', 'title', 'media:content', 'url', 'Self Dev', 'New Yorker', 'pubDate'),
    ('https://www.newyorker.com/feed/cartoons/daily-cartoon', 'item', 'link', 'title', 'media:content', 'url', 'Self Dev', 'New Yorker', 'pubDate'),
    ('https://www.newyorker.com/feed/tag/books/rss', 'item', 'link', 'title', 'media:content', 'url', 'Self Dev', 'New Yorker', 'pubDate'),
    ('https://www.newyorker.com/feed/books/page-turner', 'item', 'link', 'title', 'media:content', 'url', 'Self Dev', 'New Yorker', 'pubDate'),
    ('https://www.newyorker.com/feed/tech', 'item', 'link', 'title', 'media:content', 'url', 'Science & Technology', 'New Yorker', 'pubDate'),
    ('https://www.newyorker.com/feed/tech/elements', 'item', 'link', 'title', 'media:content', 'url', 'Science & Technology', 'New Yorker', 'pubDate'),
    ('http://feeds.wnyc.org/newyorkerradiohour', 'item', 'link', 'title', 'media:content', 'url', 'Self Dev', 'New Yorker', 'pubDate'),
    ('https://www.newyorker.com/services/rss/feeds/campaign_trail.xml', 'item', 'link', 'title', 'media:content', 'url', 'Politics', 'New Yorker', 'pubDate'),
    ('https://www.newyorker.com/feed/podcast/fiction', 'item', 'link', 'title', 'media:content', 'url', 'Self Dev', 'New Yorker', 'pubDate'),
    ('http://feeds.wnyc.org/tnyauthorsvoice', 'item', 'link', 'title', 'media:content', 'url', 'Self Dev', 'New Yorker', 'pubDate'),
    ('https://www.newyorker.com/services/rss/feeds/poetry_podcast.xml', 'item', 'link', 'title', 'media:content', 'url', 'Self Dev', 'New Yorker', 'pubDate'),
    ('https://www.newyorker.com/services/rss/feeds/newyorker_outloud.xml', 'item', 'link', 'title', 'media:content', 'url', 'Self Dev', 'New Yorker', 'pubDate'),

    ("https://www.reutersagency.com/feed/?taxonomy=best-sectors&post_type=best", 'item', 'link', 'title', 'media:content', 'url', 'Global News', 'Reuters', 'pubDate'),
    ("https://www.reutersagency.com/feed/?best-sectors=equities&post_type=best", 'item', 'link', 'title', 'media:content', 'url', 'Business & Finance', 'Reuters', 'pubDate'),
    ("https://www.reutersagency.com/feed/?best-sectors=foreign-exchange-fixed-income&post_type=best", 'item', 'link', 'title', 'media:content', 'url', 'Business & Finance', 'Reuters', 'pubDate'),
    ("https://www.reutersagency.com/feed/?best-sectors=economy&post_type=best", 'item', 'link', 'title', 'media:content', 'url', 'Business & Finance', 'Reuters', 'pubDate'),
    ("https://www.reutersagency.com/feed/?best-sectors=commodities-energy&post_type=best", 'item', 'link', 'title', 'media:content', 'url', 'Business & Finance', 'Reuters', 'pubDate'),
    ("https://www.reutersagency.com/feed/?taxonomy=best-topics&post_type=best", 'item', 'link', 'title', 'media:content', 'url', 'Global News', 'Reuters', 'pubDate'),
    ("https://www.reutersagency.com/feed/?best-topics=business-finance&post_type=best", 'item', 'link', 'title', 'media:content', 'url', 'Business & Finance', 'Reuters', 'pubDate'),
        ("https://www.reutersagency.com/feed/?best-topics=deals&post_type=best", 'item', 'link', 'title', 'media:content', 'url', 'Business & Finance', 'Reuters', 'pubDate'),
    ("https://www.reutersagency.com/feed/?best-topics=political-general&post_type=best", 'item', 'link', 'title', 'media:content', 'url', 'Politics', 'Reuters', 'pubDate'),
    ("https://www.reutersagency.com/feed/?best-topics=environment&post_type=best", 'item', 'link', 'title', 'media:content', 'url', 'Science & Technology', 'Reuters', 'pubDate'),
    ("https://www.reutersagency.com/feed/?best-topics=tech&post_type=best", 'item', 'link', 'title', 'media:content', 'url', 'Science & Technology', 'Reuters', 'pubDate'),
    ("https://www.reutersagency.com/feed/?best-topics=health&post_type=best", 'item', 'link', 'title', 'media:content', 'url', 'Self Dev', 'Reuters', 'pubDate'),
    ("https://www.reutersagency.com/feed/?best-topics=sports&post_type=best", 'item', 'link', 'title', 'media:content', 'url', 'Football', 'Reuters', 'pubDate'),
    ("https://www.reutersagency.com/feed/?best-topics=lifestyle-entertainment&post_type=best", 'item', 'link', 'title', 'media:content', 'url', 'Self Dev', 'Reuters', 'pubDate'),
    ("https://www.reutersagency.com/feed/?best-topics=human-interest&post_type=best", 'item', 'link', 'title', 'media:content', 'url', 'Self Dev', 'Reuters', 'pubDate'),
    ("https://www.reutersagency.com/feed/?best-topics=journalist-spotlight&post_type=best", 'item', 'link', 'title', 'media:content', 'url', 'Self Dev', 'Reuters', 'pubDate'),
    ("https://www.reutersagency.com/feed/?taxonomy=best-regions&post_type=best", 'item', 'link', 'title', 'media:content', 'url', 'Global News', 'Reuters', 'pubDate'),
    ("https://www.reutersagency.com/feed/?best-regions=middle-east&post_type=best", 'item', 'link', 'title', 'media:content', 'url', 'Global News', 'Reuters', 'pubDate'),
    ("https://www.reutersagency.com/feed/?best-regions=africa&post_type=best", 'item', 'link', 'title', 'media:content', 'url', 'Global News', 'Reuters', 'pubDate'),
    ("https://www.reutersagency.com/feed/?best-regions=europe&post_type=best", 'item', 'link', 'title', 'media:content', 'url', 'Global News', 'Reuters', 'pubDate'),
    ("https://www.reutersagency.com/feed/?best-regions=north-america&post_type=best", 'item', 'link', 'title', 'media:content', 'url', 'Global News', 'Reuters', 'pubDate'),
    ("https://www.reutersagency.com/feed/?best-regions=south-america&post_type=best", 'item', 'link', 'title', 'media:content', 'url', 'Global News', 'Reuters', 'pubDate'),
    ("https://www.reutersagency.com/feed/?best-regions=asia&post_type=best", 'item', 'link', 'title', 'media:content', 'url', 'Global News', 'Reuters', 'pubDate'),
    ("https://www.reutersagency.com/feed/?taxonomy=best-customer-impacts&post_type=best", 'item', 'link', 'title', 'media:content', 'url', 'Global News', 'Reuters', 'pubDate'),
    ("https://www.reutersagency.com/feed/?best-customer-impacts=market-impact&post_type=best", 'item', 'link', 'title', 'media:content', 'url', 'Global News', 'Reuters', 'pubDate'),
    ("https://www.reutersagency.com/feed/?best-customer-impacts=media-customer-impact&post_type=best", 'item', 'link', 'title', 'media:content', 'url', 'Global News', 'Reuters', 'pubDate'),
    ("https://www.reutersagency.com/feed/?post_type=reuters-best", 'item', 'link', 'title', 'media:content', 'url', 'Global News', 'Reuters', 'pubDate'),
    ("https://www.reutersagency.com/feed/?best-types=the-big-picture&post_type=best", 'item', 'link', 'title', 'media:content', 'url', 'Global News', 'Reuters', 'pubDate'),
    ("https://www.reutersagency.com/feed/?best-types=reuters-news-first&post_type=best", 'item', 'link', 'title', 'media:content', 'url', 'Global News', 'Reuters', 'pubDate'),

    ('http://www.thisisanfield.com/feed/', 'item', 'link', 'title', 'enclosure', 'url', 'Liverpool FC','This is Anfield', 'pubDate'),
    ('http://www.theguardian.com/football/rss', 'item', 'link', 'title', 'media:content', 'url', 'Football', 'The Guardian', 'pubDate'),

    ('https://theathletic.com/team/liverpool/?rss=1', 'item', 'link', 'title', 'media:content', 'href', 'Liverpool FC','The Athletic','pubDate'),
    ('https://theathletic.com/premier-league/?rss', 'item', 'link', 'title', 'media:content', 'href', 'Football','The Athletic', 'published'),
    ('https://theathletic.com/soccer/?rss',  'item', 'link', 'title', 'media:content', 'href', 'Football','The Athletic','published'),
    ('https://theathletic.com/champions-league/?rss',  'item', 'link', 'title', 'media:content', 'href', 'Football','The Athletic', 'published'),

    ('https://www.autosport.com/rss/feed/f1', 'item', 'link', 'title', 'enclosure', 'url', 'Formula 1', 'Autosport', 'pubDate'),
    ('https://the-race.com/category/formula-1/feed/', 'item', 'link', 'title','media:content', 'url', 'Formula 1', 'The Race', 'pubDate'),
    ('https://aeon.co/feed.rss', 'item', 'link', 'title', 'media:content', 'url', 'Self Dev', "Aeon", 'pubDate'),
    ('https://psyche.co/feed', 'item', 'link', 'title', 'media:content', 'url', 'Self Dev', "Psyche", 'pubDate'),

    ('http://www.nytimes.com/services/xml/rss/nyt/Opinion.xml', 'item', 'link', 'title', 'media:content', 'url', 'Politics', "New York Times", 'pubDate'),
    ('http://www.nytimes.com/services/xml/rss/nyt/Magazine.xml', 'item', 'link', 'title', 'media:content', 'url', 'Self Dev', "New York Times", 'pubDate'),
    ('http://www.nytimes.com/services/xml/rss/nyt/Science.xml', 'item', 'link', 'title', 'media:content', 'url', 'Science & Technology', "New York Times", 'pubDate'),
    ('http://www.nytimes.com/services/xml/rss/nyt/Travel.xml', 'item', 'link', 'title', 'media:content', 'url', 'Travel', "New York Times", 'pubDate'),
    ('http://www.nytimes.com/services/xml/rss/nyt/Style.xml', 'item', 'link', 'title', 'media:content', 'url', 'Self Dev', "New York Times", 'pubDate'),
    ('http://www.nytimes.com/services/xml/rss/nyt/Technology.xml', 'item', 'link', 'title', 'media:content', 'url', 'Science & Technology', "New York Times", 'pubDate'),
    ('http://www.nytimes.com/services/xml/rss/nyt/Business.xml', 'item', 'link', 'title', 'media:content', 'url', 'Business & Finance', "New York Times", 'pubDate'),
    ('http://www.nytimes.com/services/xml/rss/nyt/HomePage.xml', 'item', 'link', 'title', 'media:content', 'url', 'Global News', "New York Times", 'pubDate'),
    ('https://www.nytimes.com/wirecutter/rss/', 'item', 'link', 'title', 'description', 'src', 'Science & Technology', "New York Times Wirecutter", 'pubDate'),

    ('http://www.smithsonianmag.com/rss/innovation/', 'item', 'link', 'title', 'enclosure', 'url', 'Science & Technology', "Smithsonian", 'pubDate'),
    ('http://www.smithsonianmag.com/rss/latest_articles/', 'item', 'link', 'title', 'enclosure', 'url', 'Science & Technology', "Smithsonian", 'pubDate'),

    ('http://feeds.feedburner.com/dawn-news', 'item', 'link', 'title',  'media:content', 'url', 'Pakistan', "Dawn", 'pubDate'),
    ('https://feeds.feedburner.com/dawn-news-world', 'item', 'link', 'title',  'media:content', 'url', 'Global News', "Dawn", 'pubDate'),

    ('https://www.theverge.com/rss/reviews/index.xml', 'entry', 'id', 'title', 'media:content', 'url', 'Science & Technology', 'The Verge', 'published'),
]



def delete_or_resummarize_summary_if_jina_ai():
    articles = Article.objects.filter(summary__icontains="jina")
    
    for article in articles:
        print(f"Found 'Jina AI' in article: {article.title}")
        full_text = fetch_nyt(article.link)
        article.summary = summarize_text(full_text)
        article.save()
        print(f"Resummarized and saved summary for article: {article.title}")
        time.sleep(3)

def delete_images_for_specific_websites():
    target_websites = ["Psyche", "Aeon", "The Athletic", "New York Times", "Smithsonian"]
    articles = Article.objects.filter(website__in=target_websites)
    
    for article in articles:
        article.image = None
        article.save()
        print(f"Deleted image for article: {article.title} from {article.website}")

def delete_summary_if_jina_ai():
    articles = Article.objects.filter(summary__icontains="Jina AI")
    
    for article in articles:
        article.summary = None
        article.save()
        print(f"Deleted summary for article: {article.title} containing 'Jina AI'")

def reparse_rss_and_update_images():
    for url, main_tag, link_tag, title_tag, image_tag, image_attr, category, website, date_tag in rss_feed_details:
        print("WE REPARSING FR FR")
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'lxml-xml')
            entries = []

            for entry in soup.find_all(main_tag):
                try:
                    title = entry.find(title_tag).text
                    link = entry.find(link_tag).text
                    date = entry.find(date_tag).text
                    published = normalize_datetime_to_django_format(date)
                    
                    if image_tag:
                        if "Psyche" in website or "Aeon" in website:
                            description_content = entry.find('description')
                            if description_content:
                                description_soup = BeautifulSoup(description_content.text, 'html.parser')
                                image_tag_obj = description_soup.find('img')
                                image = image_tag_obj.get('src') if image_tag_obj else None
                            else:
                                image = None 

                        elif "The Athletic" in website:
                            media_content = entry.find('media:content')
                            image = media_content.get('url') if media_content else None
                            if not image:
                                image = (
                                    'https://images.unsplash.com/photo-1518188049456-7a3a9e263ab2?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1674&q=80'
                                    if "liverpool" in url else
                                    'https://images.unsplash.com/photo-1486286701208-1d58e9338013?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1770&q=80'
                                )

                        elif "The Guardian" in website:
                            media_content_tags = entry.find_all('media:content')
                            max_width = 0
                            selected_image = None

                            for media_content in media_content_tags:
                                if 'url' in media_content.attrs and 'width' in media_content.attrs:
                                    width = int(media_content['width'])
                                    url = media_content['url']
                                    if width > max_width:
                                        max_width = width
                                        selected_image = url

                            image = selected_image or 'https://images.unsplash.com/photo-1555862124-94036092ab14?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1771&q=80'

                        elif "New York Times Wirecutter" in website:
                            description_content = entry.find('description').text
                            description_soup = BeautifulSoup(description_content, 'html.parser')
                            image_tag_obj = description_soup.find('img')
                            if image_tag_obj:
                                image = image_tag_obj['src']
                            else:
                                images = [
                                    "https://images.unsplash.com/photo-1451187580459-43490279c0fa?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1772&q=80",
                                    "https://images.unsplash.com/photo-1531297484001-80022131f5a1?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8dGVjaHxlbnwwfDB8MHx8fDA%3D&auto=format&fit=crop&w=1400&q=60",
                                    "https://images.unsplash.com/photo-1523961131990-5ea7c61b2107?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NXx8dGVjaHxlbnwwfDB8MHx8fDA%3D&auto=format&fit=crop&w=1400&q=60",
                                    "https://images.unsplash.com/photo-1550745165-9bc0b252726f?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8OHx8dGVjaHxlbnwwfDB8MHx8fDA%3D&auto=format&fit=crop&w=1400&q=60",
                                    "https://images.unsplash.com/photo-1550751827-4bd374c3f58b?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTB8fHRlY2h8ZW58MHwwfDB8fHww&auto=format&fit=crop&w=1400&q=60",
                                    "https://images.unsplash.com/photo-1518770660439-4636190af475?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTF8fHRlY2h8ZW58MHwwfDB8fHww&auto=format&fit=crop&w=1400&q=60",
                                    "https://images.unsplash.com/photo-1496065187959-7f07b8353c55?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTR8fHRlY2h8ZW58MHwwfDB8fHww&auto=format&fit=crop&w=1400&q=60"
                                ]
                                image = random.choice(images)

                        elif "New York Times" in website:
                            media_content = entry.find('media:content')
                            image = media_content.get('url') if media_content else None
                            if not image:
                                images = {
                                    'Opinion': ["https://images.unsplash.com/photo-1506543277633-99deabfcd722?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=750&q=80"],
                                    'Magazine': ["https://images.unsplash.com/photo-1548706108-582111196a20?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1782&q=80"],
                                    'Business': [
                                        "https://images.unsplash.com/photo-1504711434969-e33886168f5c?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2940&q=80",
                                        "https://images.unsplash.com/photo-1572883454114-1cf0031ede2a?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8M3x8YnVpbGRpbmdzfGVufDB8fDB8fHww&auto=format&fit=crop&w=800&q=60"
                                    ],
                                    'Home': ["https://images.unsplash.com/photo-1521295121783-8a321d551ad2?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1770&q=80"],
                                    'Travel': [
                                        "https://images.unsplash.com/photo-1488085061387-422e29b40080?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2231&q=80",
                                        "https://images.unsplash.com/photo-1501785888041-af3ef285b470?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Nnx8dHJhdmVsfGVufDB8MHwwfHx8MA%3D%3D&auto=format&fit=crop&w=800&q=60"
                                    ]
                                }
                                image = random.choice(images.get(category, [])) if category in images else None

                        elif "Autosport" in website:
                            enclosure_tag = entry.find('enclosure')
                            image = enclosure_tag.get('url') if enclosure_tag else 'https://images.unsplash.com/photo-1656337449909-141091f4df4a?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=774&q=80'

                        elif website == 'The Race':
                            media_content = entry.find('media:content')
                            image = media_content.get('url') if media_content else 'https://images.unsplash.com/photo-1656337449909-141091f4df4a?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=774&q=80'

                        elif website == 'This is Anfield':
                            media_thumbnail = entry.find('media:thumbnail')
                            image = media_thumbnail.get('url') if media_thumbnail else 'https://images.unsplash.com/photo-1555862124-94036092ab14?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1771&q=80'

                        elif website == 'The Verge':
                            content = entry.find('content')
                            content_soup = BeautifulSoup(content.text, 'html.parser')
                            img_tag = content_soup.find('img')
                            image = img_tag.get('src') if img_tag else None

                        elif 'smithsonian' in url:
                            enclosure = entry.find('enclosure')
                            image = enclosure.get('url') if enclosure else random.choice([
                                "https://images.unsplash.com/photo-1451187580459-43490279c0fa?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1772&q=80",
                                "https://images.unsplash.com/photo-1531297484001-80022131f5a1?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8dGVjaHxlbnwwfDB8MHx8fDA%3D&auto=format&fit=crop&w=1400&q=60"
                            ])

                        elif "dawn" in link:
                            media_content = entry.find('media:content')
                            image = media_content.get('url') if media_content else 'https://images.unsplash.com/photo-1588414884049-eb55cd4c72b4?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=776&q=80'

                        else:
                            image = entry.find(image_tag, {image_attr: True})
                            if not image:
                                image = 'https://images.unsplash.com/photo-1588414884049-eb55cd4c72b4?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=776&q=80'

                    else:
                        image = 'https://images.unsplash.com/photo-1588414884049-eb55cd4c72b4?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=776&q=80'

                    # Update or create article with the new image
                    article, created = Article.objects.update_or_create(
                        link=link,
                        defaults={
                            'title': title,
                            'category': category,
                            'website': website,
                            'published': published,
                            'image': image
                        }
                    )

                except Exception as e:
                    print(f"Error processing an entry from {url}: {e}")
                    continue

        except Exception as e:
            print(f"Error fetching feed from {url}: {e}")
             """