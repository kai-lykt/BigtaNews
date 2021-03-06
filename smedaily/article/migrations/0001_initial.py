# Generated by Django 3.1 on 2020-09-04 13:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='생성일시')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='수정일시')),
                ('title', models.CharField(help_text='제목', max_length=200)),
                ('content', models.TextField(help_text='내용')),
                ('writer', models.ForeignKey(help_text='작성자', on_delete=django.db.models.deletion.PROTECT, related_name='my_article', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'article_post',
            },
        ),
        migrations.AddIndex(
            model_name='article',
            index=models.Index(fields=['title'], name='article_post_title_idx'),
        ),
    ]
