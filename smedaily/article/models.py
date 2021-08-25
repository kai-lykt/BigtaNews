from django.db import models
from django.conf import settings
from smedaily.common.models import TimeStampMixin


# Create your models here.
class Article(TimeStampMixin):
    """Article
    작성기"""
    title = models.CharField(max_length=200, help_text='제목')
    content = models.TextField(help_text='내용')
    stock = models.CharField(max_length=200, help_text='관련종목', blank=True, default=' ')
    writer = models.ForeignKey(
        settings.AUTH_USER_MODEL
        , on_delete=models.PROTECT
        , related_name='my_article'
        , to_field='username'
        , help_text='작성자'
    )
    proto = models.TextField(blank=True, default=' ', help_text='해당 프로토 아티클')
    relate_dart = models.TextField(blank=True, default=' ', help_text='관련자료 id. , 로 구분')

    class Meta:
        db_table = 'article_post'
        indexes = [
            models.Index(fields=['title'], name='article_post_title_idx')
        ]

    def __str__(self):
        return self.title
