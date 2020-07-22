from django import forms
from django.db.models import Count
from .models import Tag, Comment, Reply
from .widgets import CustomCheckboxSelectMultiple
from .fields import SimpleCaptchaField


class PostSearchForm(forms.Form):
    """記事検索フォーム"""
    key_word = forms.CharField(label='検索キーワード', required=False,)

    tags = forms.ModelMultipleChoiceField(
        label='タグでの絞り込み',
        required=False,
        queryset=Tag.objects.annotate(
            post_count=Count('post')).order_by('name'),
        widget=CustomCheckboxSelectMultiple,
    )


class CommentCreateForm(forms.ModelForm):
    """コメント投稿フォーム"""
    captcha = SimpleCaptchaField()

    class Meta:
        model = Comment
        exclude = ('target', 'created_at')
        widgets = {
            'text': forms.Textarea(
                attrs={
                    'placeholder': 'マークダウンに対応しています。\n\n```python\nprint("コードはこのような感じで書く")\n```\n\n[リンクテキスト]\n\n![画像alt](画像URL)'}
            )
        }


class ReplyCreateForm(forms.ModelForm):
    """返信コメント投稿フォーム"""
    captcha = SimpleCaptchaField()

    class Meta:
        model = Reply
        exclude = ('target', 'created_at')
        widgets = {
            'text': forms.Textarea(
                attrs={
                    'placeholder':  'マークダウンに対応しています。\n\n```python\nprint("コードはこのような感じで書く")\n```\n\n[リンクテキスト]\n\n![画像alt](画像URL)'}
            )
        }
