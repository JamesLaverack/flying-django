from django.views.generic import TemplateView, ListView, DetailView, FormView, UpdateView, DeleteView
from django.core.urlresolvers import reverse, reverse_lazy
from django.utils.functional import lazy
from django.http import HttpResponse, HttpResponseRedirect
from google.appengine.api import users
from .models import BlogPost, Comment
from .forms import BlogPostForm, CommentForm

class BlogPostListView(ListView):
    model = BlogPost
    template_name = "blogpost_list.html"

    def get_queryset(self):
        return self.model.all()

class BlogPostDetailView(DetailView, FormView):
    form_class = CommentForm
    model = BlogPost
    template_name = "blogpost_detail.html"
    context_object_name = "object"
    success_url = "/"

    def get_context_data(self, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        context = super(DetailView, self).get_context_data(**kwargs)
        context.update(super(FormView, self).get_context_data(form=form, **kwargs))
        return context

    def get_object(self, queryset = None):
        return self.model.get(self.kwargs.get(self.slug_url_kwarg, None))

    def form_valid(self, form):
        c = Comment(author = users.get_current_user().user_id(),
                    content = form.cleaned_data['content'],
                    blogpost = self.get_object())
        c.put()
        return HttpResponseRedirect(reverse('view-post', args=(self.get_object().key(),)))

class BlogPostDeleteView(DeleteView):
    model = BlogPost
    template_name = "blogpost_confirm_delete.html"

    def get_success_url(self):
        return reverse('list-posts')

    def get_object(self, queryset = None):
        return self.model.get(self.kwargs.get(self.slug_url_kwarg, None))

class CommentDeleteView(DeleteView):
    model = Comment
    template_name = "comment_confirm_delete.html"

    def get_success_url(self):
        return reverse('view-post', args=(self.object.blogpost.key(),))

    def get_object(self, queryset = None):
        return self.model.get(self.kwargs.get(self.slug_url_kwarg, None))

class CommentUpdateView(UpdateView):
    form_class = CommentForm
    template_name = "blogpost_update_form.html"
    model = Comment

    def get_object(self, queryset = None):
        return self.model.get(self.kwargs.get(self.slug_url_kwarg, None))

    def form_valid(self, form):
        self.object.content = form.cleaned_data['content']
        self.object.put()

        return HttpResponseRedirect(reverse('view-post', args = (self.object.blogpost.key(),)))

class BlogPostCreateView(FormView):
    form_class = BlogPostForm
    template_name = "blogpost_form.html"

    def form_valid(self, form):
        bp = BlogPost(author = users.get_current_user().user_id(),
                      title = form.cleaned_data['title'],
                      content = form.cleaned_data['content'])
        bp.put()
        return HttpResponseRedirect(reverse('view-post', args = (bp.key(),)))
        

class BlogPostUpdateView(UpdateView):
    form_class = BlogPostForm
    template_name = "blogpost_update_form.html"
    model = BlogPost

    def get_object(self, queryset = None):
        return self.model.get(self.kwargs.get(self.slug_url_kwarg, None))

    def form_valid(self, form):
        self.object.title = form.cleaned_data['title']
        self.object.content = form.cleaned_data['content']
        self.object.put()

        return HttpResponseRedirect(reverse('view-post', args = (self.object.key(),)))
