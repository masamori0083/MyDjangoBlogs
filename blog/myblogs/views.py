from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.views import generic
from django.shortcuts import redirect, get_object_or_404
from .forms import PostSearchForm, CommentCreateForm, ReplyCreateForm
from .models import Post, Comment, Reply
from django.http import Http404

# Create your views here.


class PublicPostIndexView(generic.ListView):
    """公開記事の一覧を表示する"""
    model = Post
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.form = form = PostSearchForm(self.request.GET or None)
        if form.is_valid():
            tags = form.cleaned_data.get('tags')
            if tags:
                for tag in tags:
                    queryset = queryset.filter(tags=tag)

            # タイトルか本文にキーワードが含まれたもの
            # キーワードか¥半角スペースで区切られていれば、その回数だけfilterする。つまり、AND。
            key_word = form.cleaned_data.get("key_word")
            if key_word:
                for word in key_word.split():
                    queryset = queryset.filter(
                        Q(title__icontains=word) | Q(text__icontains=word))

        queryset = queryset.order_by('-updated_at').prefetch_related('tags')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = PostSearchForm(self.request.GET or None)
        return context


class PrivatePostIndexView(LoginRequiredMixin, PublicPostIndexView):
    """非公開記事の一覧を表示する"""
    raise_exception = True
    queryset = Post.objects.filter(is_public=False)


class PostDetailView(generic.DetailView):
    """記事詳細ページを表示する"""
    model = Post

    def get_queryset(self):
        return super().get_queryset().prefetch_related('tags', 'comment_set__reply_set')

    def get_object(self, queryset=None):
        """その記事を公開か、ユーザーがログインしていれば表示する。"""
        post = super().get_object()
        if post.is_public or self.request.user.is_authenticated:
            return post
        else:
            raise Http404


class CommentCreate(generic.CreateView):
    """記事へのコメントインタビュー"""
    model = Comment
    form_class = CommentCreateForm

    def form_valid(self, form):
        post_pk = self.kwargs['pk']
        post = get_object_or_404(Post, pk=post_pk)
        comment = form.save(commit=False)
        comment.target = post
        comment.request = self.request
        comment.save()
        return redirect('myblogs:post_detail', pk=post_pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["post"] = get_object_or_404(Post, pk=self.kwargs['pk'])
        return context


class ReplyCreate(generic.CreateView):
    """コメントへの返信作成ビュー"""
    model = Reply
    form_class = ReplyCreateForm
    template_name = 'myblogs/comment_form.html'

    def form_valid(self, form):
        comment_pk = self.kwargs['pk']
        comment = get_object_or_404(Comment, pk=comment_pk)
        reply = form.save(commit=False)
        reply.target = comment
        reply.request = self.request
        reply.save()
        return redirect('myblogs:post_detail', pk=comment.target.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comment_pk = self.kwargs['pk']
        comment = get_object_or_404(Comment, pk=comment_pk)
        context["post"] = comment.target
        return context
