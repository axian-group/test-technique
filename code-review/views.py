# articles/views.py
from django.http import JsonResponse
from django.views import View
from .models import Article
from django.contrib.auth.models import User
import json

class ArticleView(View):
    
    def get(self, request, article_id=None):
        if article_id:
            # Get single article
            article = Article.objects.get(id=article_id)
            data = {
                'id': article.id,
                'title': article.title,
                'content': article.content,
                'author': article.author.username,
            }
            return JsonResponse(data)
        else:
            # Get all articles
            articles = Article.objects.all()
            data = []
            for article in articles:
                data.append({
                    'id': article.id,
                    'title': article.title,
                    'content': article.content,
                    'author': article.author.username,
                })
            return JsonResponse({'articles': data})
    
    def post(self, request):
        data = json.loads(request.body)
        
        # Create new article
        article = Article()
        article.title = data['title']
        article.content = data['content']
        article.author_id = data['author_id']
        article.save()
        
        return JsonResponse({'message': 'Article created', 'id': article.id})
    
    def put(self, request, article_id):
        data = json.loads(request.body)
        
        # Update article
        article = Article.objects.get(id=article_id)
        article.title = data['title']
        article.content = data['content']
        article.save()
        
        return JsonResponse({'message': 'Article updated'})
    
    def delete(self, request, article_id):
        article = Article.objects.get(id=article_id)
        article.delete()
        return JsonResponse({'message': 'Article deleted'})


class UserLoginView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']
        password = data['password']
        
        # Check user credentials
        user = User.objects.get(username=username)
        if user.password == password:
            # Create session or token here
            return JsonResponse({
                'success': True,
                'user_id': user.id,
                'username': user.username
            })
        else:
            return JsonResponse({'success': False, 'error': 'Invalid credentials'})


class ArticlePublishView(View):
    def post(self, request, article_id):
        # Publish article
        article = Article.objects.get(id=article_id)
        article.status = 'published'
        article.save()
        
        # Send notification to all users
        users = User.objects.all()
        for user in users:
            # Send email notification
            print(f"Sending email to {user.email}")
        
        return JsonResponse({'message': 'Article published'})