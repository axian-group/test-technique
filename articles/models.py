from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class Article(models.Model):
    """Article model for content management."""
    
    class Status(models.TextChoices):
        DRAFT = 'draft', _('Draft')
        PUBLISHED = 'published', _('Published')
        ARCHIVED = 'archived', _('Archived')
    
    title = models.CharField(
        _('title'),
        max_length=200,
        help_text=_('Article title (max 200 characters)')
    )
    content = models.TextField(
        _('content'),
        help_text=_('Article content')
    )
    status = models.CharField(
        _('status'),
        max_length=10,
        choices=Status.choices,
        default=Status.DRAFT,
        help_text=_('Article publication status')
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='articles',
        verbose_name=_('author')
    )
    created_at = models.DateTimeField(
        _('created at'),
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        _('updated at'),
        auto_now=True
    )
    published_at = models.DateTimeField(
        _('published at'),
        null=True,
        blank=True,
        help_text=_('Date and time when the article was published')
    )
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = _('article')
        verbose_name_plural = _('articles')
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['status']),
            models.Index(fields=['author']),
        ]
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        """Override save to set published_at when status changes to published."""
        if self.status == self.Status.PUBLISHED and not self.published_at:
            from django.utils import timezone
            self.published_at = timezone.now()
        super().save(*args, **kwargs)
