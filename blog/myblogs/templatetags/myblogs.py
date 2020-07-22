from django import template
from django.conf import settings
from django.utils.safestring import mark_safe
import markdown
from markdown.extensions import Extension

register = template.Library()


@register.simple_tag
def url_replace(request, field, value):
    """GETパラメーターの一部を置き換える"""
    url_dict = request.GET.copy()
    url_dict[field] = str(value)
    return url_dict.urlencode()


@register.filter
def markdown_to_html(text):
    """マークダウンをhtmlに変換する"""
    html = markdown.markdown(text, extensions=settings.MARKDOWN_EXTENSIONS)
    return mark_safe(html)


class EscapeHtml(Extension):

    def extendMarkdown(self, md):
        md.preprocessors.deregister('html_block')
        md.inlinePatterns.deregister('html')


@register.filter
def markdown_to_html_with_escape(text):
    """マークダウンをhtmlに変換する。
    生のHTMLやCSS、Javascript等のコードをエスケープした上で、マークダウンをHTMLに変換します。"""
    extensions = settings.MARKDOWN_EXTENSIONS + [EscapeHtml()]
    html = markdown.markdown(text, extensions=extensions)
    return mark_safe(html)
