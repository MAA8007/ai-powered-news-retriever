from django.shortcuts import render
from .models import Article, Bookmark
from django.http import StreamingHttpResponse, JsonResponse
from .tasks import update_url_database_function_with_yield, get_rag_response
import logging
from django.db.models import Q
import json
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login
@login_required
def bookmark_article(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        article_id = data.get('article_id')
        action = data.get('action')
        
        article = get_object_or_404(Article, id=article_id)
        
        if action == 'add':
            bookmark, created = Bookmark.objects.get_or_create(user=request.user, article=article)
            if created:
                return JsonResponse({'status': 'success', 'message': 'Article bookmarked.'})
            else:
                return JsonResponse({'status': 'exists', 'message': 'Article already bookmarked.'})
        elif action == 'remove':
            try:
                bookmark = Bookmark.objects.get(user=request.user, article=article)
                bookmark.delete()
                return JsonResponse({'status': 'success', 'message': 'Bookmark removed.'})
            except Bookmark.DoesNotExist:
                return JsonResponse({'status': 'not_found', 'message': 'Bookmark does not exist.'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid action.'}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)


@login_required
def bookmark_list(request):
    bookmarks = Bookmark.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'bookmark_list.html', {'bookmarks': bookmarks})
def get_categories_with_websites():
    """
    Retrieves a dictionary of grouped categories with their corresponding websites.
    """
    categories_with_websites = {
        'World_News': ['Pakistan', 'Global News'],
        'Sports': ['Liverpool FC', 'Football', 'Formula 1'],
        'Science': ['Science & Technology', 'AI News'],
        'Lifestyle': ['Self Dev', 'Travel'],
        'Finance': ['Business & Finance'],
    }
    
    # Dictionary to hold the actual websites for each category
    grouped_websites = {key: [] for key in categories_with_websites.keys()}
    
    # Fetch all distinct articles with their categories and websites
    articles = Article.objects.values('category', 'website').distinct()

    for article in articles:
        category = article['category']
        website = article['website']

        # Add websites to the appropriate grouped category
        for group, categories in categories_with_websites.items():
            if category in categories:
                if website not in grouped_websites[group]:
                    grouped_websites[group].append(website)
    
    return grouped_websites

@login_required
def bookmark_list(request):
    bookmarks = Bookmark.objects.filter(user=request.user).order_by('-created_at')
    categories_with_websites = get_categories_with_websites()
    return render(request, 'bookmark_list.html', {'bookmarks': bookmarks, 'categories_with_websites': categories_with_websites})

def search_articles(request):
    query = request.GET.get('q')
    articles = Article.objects.filter(title__icontains=query).order_by('-published') if query else Article.objects.all().order_by('-published')
    categories_with_websites = get_categories_with_websites()
    return render(request, 'search_results.html', {'articles': articles, 'query': query, 'categories_with_websites': categories_with_websites})

def home(request):
    liv_articles = Article.objects.filter(website__icontains="This is Anfield").order_by('-published')[:20]
    football_articles = Article.objects.filter(category__icontains="Football").order_by('-published')[:20]
    f1_articles = Article.objects.filter(category__icontains="Formula 1").order_by('-published')[:20]
    selfdev_articles = Article.objects.filter(category__icontains="Self Dev").order_by('-published')[:20]
    news_articles = Article.objects.filter(category__icontains="Global News").order_by('-published')[:20]
    pak_articles = Article.objects.filter(category__icontains="Pakistan").order_by('-published')[:20]

    categories_with_websites = get_categories_with_websites()

    context = {
        'liv': liv_articles,
        'football': football_articles,
        'f1': f1_articles,
        'selfdev': selfdev_articles,
        'news': news_articles,
        'pak': pak_articles,
        'categories_with_websites': categories_with_websites
    }

    return render(request, 'home.html', context)

def category_page(request, category_name):
    articles = Article.objects.filter(category__icontains=category_name).order_by('-published')[:99]
    categories_with_websites = get_categories_with_websites()
    return render(request, 'category_page.html', {'articles': articles, 'categories_with_websites': categories_with_websites})

def manage(request):
    categories_with_websites = get_categories_with_websites()
    return render(request, 'manage.html', {'categories_with_websites': categories_with_websites})

def website_page(request, website_name):
    articles = Article.objects.filter(website=website_name).order_by('-published')[:99]
    categories_with_websites = get_categories_with_websites()
    return render(request, 'website_page.html', {'articles': articles, 'categories_with_websites': categories_with_websites})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def sse_view(request):
    logger = logging.getLogger(__name__)

    def event_stream():
        try:
            for message in update_url_database_function_with_yield():
                logger.info(f"Sending message: {message}")
                yield f"data: {message}\n\n"
        except Exception as e:
            logger.error(f"Error in SSE: {str(e)}")

    return StreamingHttpResponse(event_stream(), content_type='text/event-stream')

def chat_with_bot(request):
    if request.method == 'POST':
        user_input = request.POST.get('query')
        if user_input:
            response = get_rag_response(user_input)
            return JsonResponse({'response': response, 'query': user_input})
    return JsonResponse({'response': "Sorry, I didn't understand that."})