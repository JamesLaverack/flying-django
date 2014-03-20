from django.views.generic import TemplateView, ListView, DetailView, FormView, UpdateView, DeleteView
from django.http import HttpResponse, HttpResponseRedirect
from google.appengine.api import users
from .models import BlogPost
from .forms import BlogPostForm

class BlogPostListView(ListView):
    model = BlogPost
    template_name = "blogpost_list.html"

    def get_queryset(self):
        return self.model.all()

class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = "blogpost_detail.html"
    context_object_name = "object"

    def get_object(self, queryset = None):
        return self.model.get(self.kwargs.get(self.slug_url_kwarg, None))

class BlogPostDeleteView(DeleteView):
    model = BlogPost
    template_name = "blogpost_confirm_delete.html"
    success_url = "/"

    def get_object(self, queryset = None):
        return self.model.get(self.kwargs.get(self.slug_url_kwarg, None))


class BlogPostCreateView(FormView):
    form_class = BlogPostForm
    template_name = "blogpost_form.html"
    success_url = "/"

    def form_valid(self, form):
        bp = BlogPost(author = users.get_current_user().user_id(),
                      title = form.cleaned_data['title'],
                      content = form.cleaned_data['content'])
        bp.put()
        return HttpResponseRedirect('/')
        

class BlogPostUpdateView(UpdateView):
    form_class = BlogPostForm
    template_name = "blogpost_update_form.html"
    success_url = "/"
    model = BlogPost

    def get_object(self, queryset = None):
        return self.model.get(self.kwargs.get(self.slug_url_kwarg, None))

    def form_valid(self, form):
        self.object.title = form.cleaned_data['title']
        self.object.content = form.cleaned_data['content']
        self.object.put()

        return HttpResponseRedirect('/')

class HelloWorld(TemplateView):
    template_name = "hello-world.html"

    def get_context_data(self, **kwargs):
        context = super(HelloWorld, self).get_context_data(**kwargs)
        self.request.session['test'] = 'val'
        context['session_test'] = self.request.session['test']
        context['user_name'] = users.get_current_user().nickname()
        return context

hello_world = HelloWorld.as_view()

def googlelogin(request):
 
    google_user = users.get_current_user()
    if google_user:
 
        #user = authenticate(request=request, google_user=google_user)
        #login(request, user)
 
        html = ("Welcome, %s! (<a href=\"%s\">sign out</a>)" %
                    (google_user.nickname(), users.create_logout_url("/")))
    else:
         html = ("Please (<a href=\"%s\">sign in</a>)" %
                 (users.create_login_url("/")))
 
    html = "<html><body>\n%s\n</body></html>"%(html)
 
    return HttpResponse(html)
