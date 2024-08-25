# AI powered News Aggregator

![Project Screenshot](screen.png)

## Project Overview

This project is a comprehensive system designed to fetch, process, and store articles from various RSS feeds, focusing on news related to AI, business, technology, and other categories. The system leverages cutting-edge technologies and APIs to automate the retrieval, summarization, and storage of article data in a Django-based backend for efficient querying and retrieval.

## Key Features

1. **RSS Feed Integration**:
    - Automatically fetches articles from various RSS feeds.
    - Extracts essential information such as title, link, publication date, and associated images.
    - Categorizes articles into predefined categories like AI News, Business & Finance, Science & Technology, etc.

2. **Content Processing**:
    - Extracts content from articles using Jina AI to create concise summaries while preserving the core message.
    - Summarizes article content using advanced yet cost-effective language models like OpenAI's GPT and Groq's Llama models.
    
![Project Screenshot](article.png)

3. **Retrieval-Augmented Generation (RAG)**:
    - Utilizes a FAISS-based vector store for efficient similarity search through document embeddings.
    - Offers a chatbot interface where users can query the database and receive relevant answers based on stored articles.
    - Employs custom prompts and language models to generate concise and accurate responses to user queries.

![GPT-4o-mini Chatbot](chatbot.png)

4. **Concurrency and Performance**:
    - Utilizes Python's `concurrent.futures` and `ThreadPoolExecutor` to parallelize feed fetching and content processing, improving performance and scalability.
    - Includes yield-based progress updates during database updates to provide real-time feedback.

5. **Extensibility**:
    - Easily expandable with additional RSS feeds, categories, or language models.
    - Designed with modularity in mind, allowing for easy integration of new features and updates.

6. **Bookmarking Functionality**:
    - Allows user to bookmark their favourite articles for convenient access at a later time. 

## Technologies Used

- **Django**: Backend framework for database management and serving the application.
- **LangChain**: Framework for building language model applications, used for prompt management and interaction with language models.
- **FAISS**: Library for efficient similarity search, used for storing and retrieving document embeddings.
- **BeautifulSoup**: Web scraping library for parsing HTML content and extracting necessary information from articles.
- **Concurrent Futures**: Python library for concurrent programming, handling multiple RSS feeds and content processing tasks simultaneously.

## Installation

### Prerequisites

- Python 3.8+
- pip (Python package manager)
- Virtual environment tool (optional but recommended)

### Setup Instructions

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/MAA8007/ai-powered-news-retriever
    cd your-repo
    ```

2. **Create and Activate a Virtual Environment** (optional but recommended):
    ```bash
    python3 -m venv env
    source env/bin/activate  # On Windows: env\Scripts\activate
    ```

3. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Set Up Environment Variables**:
    Create a `.env` file in the root directory of your project and add the necessary environment variables (e.g., API keys, database settings).

    ```bash
    touch .env
    ```

    Example `.env` file:
    ```env
    DJANGO_SECRET_KEY=your_secret_key
    OPENAI_API_KEY=your_openai_api_key
    DATABASE_URL=your_database_url
    ```

5. **Run Migrations**:
    ```bash
    python manage.py migrate
    ```

7. **Run the Development Server**:
    ```bash
    python manage.py runserver
    ```

## Usage

1. **Fetching and Processing Articles**:
    - The system automatically fetches articles from predefined RSS feeds and processes them in the background.
    - You can trigger a manual update using:
      ```bash
      python manage.py update_articles
      ```

2. **Querying Articles**:
    - Access the Django admin interface or a custom search interface to query and retrieve articles based on categories, keywords, or summaries.

3. **Extending the System**:
    - To add new RSS feeds, update the `feeds.json` configuration file and include the new feed URLs.
    - To add new categories, update the database model and corresponding view templates.

## Contributing

Contributions are welcome! Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes and commit them (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a new Pull Request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Special thanks to the developers of Django, LangChain, FAISS, and BeautifulSoup for their excellent tools.
- Shoutout to the OpenAI and Groq teams for their advancements in language models.
