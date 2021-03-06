from django.views.generic import TemplateView, ListView, DetailView, FormView, UpdateView, DeleteView
from django.core.urlresolvers import reverse, reverse_lazy
from django.utils.functional import lazy
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from google.appengine.api import users
from .models import BlogPost, Comment
from .forms import BlogPostForm, CommentForm

class BlogPostListView(ListView):
    model = BlogPost
    template_name = "blogpost_list.html"

    def get_queryset(self):
        return self.model.all().order("-date")

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
        context['comments'] = self.object.comments.order("date")
        return context

    def get_object(self, queryset = None):
        return self.model.get(self.kwargs.get(self.slug_url_kwarg, None))

    def form_valid(self, form):
        if users.get_current_user() is not None:
            c = Comment(author = users.get_current_user().user_id(),
                        author_name = users.get_current_user().nickname(),
                        content = form.cleaned_data['content'],
                        blogpost = self.get_object())
            c.put()
            return HttpResponseRedirect(reverse('view-post', args=(self.get_object().key(),)))
        else:
            return HttpResponseForbidden()

class BlogPostDeleteView(DeleteView):
    model = BlogPost
    template_name = "blogpost_confirm_delete.html"

    def get_success_url(self):
        return reverse('list-posts')

    def get_object(self, queryset = None):
        return self.model.get(self.kwargs.get(self.slug_url_kwarg, None))

    def delete(self, request, *args, **kwargs):
        if (
            users.get_current_user() is not None and
            self.get_object().author == users.get_current_user().user_id()
            ):
            # Delete all the associated comments when we delete a post
            for comment in self.get_object().comments:
                comment.delete()
            # Call the standard delete function now
            return super(DeleteView, self).delete(request, *args, **kwargs)
        else:
            return HttpResponseForbidden()

class CommentDeleteView(DeleteView):
    model = Comment
    template_name = "comment_confirm_delete.html"

    def get_success_url(self):
        return reverse('view-post', args=(self.object.blogpost.key(),))

    def get_object(self, queryset = None):
        return self.model.get(self.kwargs.get(self.slug_url_kwarg, None))

    def delete(self, request, *args, **kwargs):
        if (
            users.get_current_user() is not None and
            (self.get_object().author == users.get_current_user().user_id() or
             self.get_object().blogpost.author == users.get_current_user().user_id())
            ):
            return super(DeleteView, self).delete(request, *args, **kwargs)
        else:
            return HttpResponseForbidden()

class CommentUpdateView(UpdateView):
    form_class = CommentForm
    template_name = "comment_update_form.html"
    model = Comment

    def get_object(self, queryset = None):
        return self.model.get(self.kwargs.get(self.slug_url_kwarg, None))

    def form_valid(self, form):
        if (
            users.get_current_user() is not None and
            (self.get_object().author == users.get_current_user().user_id() or
             self.get_object().blogpost.author == users.get_current_user().user_id())
            ):
            self.object.content = form.cleaned_data['content']
            self.object.put()
            
            return HttpResponseRedirect(reverse('view-post', args = (self.object.blogpost.key(),)))
        else:
            return HttpResponceForbidden()

class BlogPostCreateView(FormView):
    form_class = BlogPostForm
    template_name = "blogpost_form.html"

    def form_valid(self, form):
        if users.get_current_user() is not None:
            bp = BlogPost(author = users.get_current_user().user_id(),
                          author_name = users.get_current_user().nickname(),
                          title = form.cleaned_data['title'],
                          content = form.cleaned_data['content'])
            bp.put()
            return HttpResponseRedirect(reverse('view-post', args = (bp.key(),)))
        else:
            return HttpResponceForbidden()
        

class BlogPostUpdateView(UpdateView):
    form_class = BlogPostForm
    template_name = "blogpost_update_form.html"
    model = BlogPost

    def get_object(self, queryset = None):
        return self.model.get(self.kwargs.get(self.slug_url_kwarg, None))

    def form_valid(self, form):
        if (
            users.get_current_user() is not None and
            self.get_object().author == users.get_current_user().user_id()
            ):
            self.object.title = form.cleaned_data['title']
            self.object.content = form.cleaned_data['content']
            self.object.put()

            return HttpResponseRedirect(reverse('view-post', args = (self.object.key(),)))
        else:
            return HttpResponceForbidden()
