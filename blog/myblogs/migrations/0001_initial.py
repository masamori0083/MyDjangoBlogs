# Generated by Django 3.0.3 on 2020-06-26 06:35

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='名無し', max_length=255, verbose_name='名前')),
                ('text', models.TextField(verbose_name='本文')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='作成日')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='タグ名')),
            ],
        ),
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='名無し', max_length=255, verbose_name='名前')),
                ('text', models.TextField(verbose_name='本文')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='作成日')),
                ('target', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myblogs.Comment', verbose_name='対象コメント')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32, verbose_name='タイトル')),
                ('text', models.TextField(verbose_name='本文')),
                ('is_public', models.BooleanField(default=True, verbose_name='公開可能か？')),
                ('description', models.TextField(max_length=130, verbose_name='記事の説明')),
                ('keywords', models.CharField(default='記事のキーワード', max_length=255, verbose_name='記事のキーワード')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='作成日')),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='更新日')),
                ('relation_post', models.ManyToManyField(blank=True, related_name='_post_relation_post_+', to='myblogs.Post', verbose_name='関連記事')),
                ('tags', models.ManyToManyField(blank=True, to='myblogs.Tag', verbose_name='タグ')),
            ],
        ),
        migrations.AddField(
            model_name='comment',
            name='target',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myblogs.Post', verbose_name='対象記事'),
        ),
    ]
