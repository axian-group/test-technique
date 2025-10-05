from django.test import TestCase
from django.contrib.auth.models import User
from .models import Article

class ArticleTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="editor", password="pass123")
        self.article = Article.objects.create(title="Test", content="Content", author=self.user)

    def test_article_creation(self):
        self.assertEqual(self.article.title, "Test")

    def test_article_str(self):
        self.assertEqual(str(self.article), "Test")

    def test_article_author(self):
        self.assertEqual(self.article.author.username, "editor")

    def test_article_status_default(self):
        self.assertEqual(self.article.status, "draft")

    def test_article_update(self):
        self.article.title = "Updated"
        self.article.save()
        self.assertEqual(Article.objects.get(id=self.article.id).title, "Updated")
