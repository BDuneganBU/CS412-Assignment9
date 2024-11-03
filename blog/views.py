## Create View
# blog/views.py
# Define the views for the blog app:
#from django.shortcuts import render
import random

from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from .models import *
from django.views.generic import ListView, DetailView #ListView is a custom component which displays a list of the model
from django.contrib.auth.mixins import LoginRequiredMixin

#class-based view
class ShowAllView(ListView):
    '''Create a subclass of ListView to display all blog articles.'''
    model = Article # retrieve objects of type Article from the database
    template_name = 'blog/show_all.html'
    context_object_name = 'articles' # how to find the data in the template file (context variable)

    def dispatch(self, *args, **kwargs):
        print(f"ShowAllView.dispatch; self.request.user={self.request.user}")
        return super().dispatch(*args, **kwargs)

# The difference between a ListView and a DetailView:
#   ListView shows all objects
#   DetailView shows one object
class RandomArticleView(DetailView):
    '''Show the details for one article.'''
    model = Article
    template_name = 'blog/article.html'
    context_object_name = 'article'
    
    # Method of RandomArticleView to pick one article at random:
    def get_object(self):
        '''Return one Article object chosen at random.'''
        #get_object is a default method for DetailView so we override it to get a random article
        all_articles = Article.objects.all()
        return random.choice(all_articles)
    
class ArticleView(DetailView):
    '''Show the details for one article by Primary Key (PK).'''
    model = Article
    template_name = 'blog/article.html'
    context_object_name = 'article'


## write the CreateCommentView
# comments/views.py
from django.views.generic.edit import CreateView
from .forms import CreateCommentForm, CreateArticleForm, UpdateArticleForm
from django.urls import reverse
from typing import Any
class CreateCommentView(CreateView):
    '''A view to create a new comment and save it to the database.'''
    form_class = CreateCommentForm
    template_name = "blog/create_comment_form.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        article = Article.objects.get(pk=self.kwargs['pk'])
        context['article'] = article
        return context
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        '''
        Build the dict of context data for this view.
        '''
        # superclass context data
        context = super().get_context_data(**kwargs)
        # find the pk from the URL
        pk = self.kwargs['pk']
        # find the corresponding article
        article = Article.objects.get(pk=pk)
        # add article to context data
        context['article'] = article
        return context
    
    def form_valid(self, form):
        '''
        Handle the form submission. We need to set the foreign key by 
        attaching the Article to the Comment object.
        We can find the article PK in the URL (self.kwargs).
        '''
        print(form.cleaned_data)
        #find Article identified by the PK from the URL pattern
        article = Article.objects.get(pk=self.kwargs['pk'])
        #Attach Article to the instance of the comment set to its PK
        form.instance.article = article #like comment.article = article
        #Delegate work to super
        return super().form_valid(form)
    
    ## show how the reverse function uses the urls.py to find the URL pattern
    def get_success_url(self) -> str:
        '''Return the URL to redirect to after successfully submitting form.'''
        #return reverse('show_all')
        return reverse('article', kwargs={'pk': self.kwargs['pk']})

#Multiple Inheiritance!
#Which of the same method determines whose is kept? It is in order of the parameters passed (LoginRequiredMixin > CreateView)
class CreateArticleView(LoginRequiredMixin, CreateView):
    '''A view to create a new Article and save it to the database.'''
    form_class = CreateArticleForm
    template_name = "blog/create_article_form.html"

    def get_login_url(self) -> str:
        '''Return the URL to the login page.'''
        return reverse('login')
    
    def form_valid(self, form):
        '''
        Handle the form submission to create a new Article object.
        '''
        print(f'CreateArticleView: form.cleaned_data={form.cleaned_data}')

        # find the logged in user
        user = self.request.user
        print(f"CreateArticleView user={user} article.user={user}")
        # attach user to form instance (Article object):
        form.instance.user = user

        # delegate work to the superclass version of this method
        return super().form_valid(form)

from django.views.generic.edit import UpdateView
class UpdateArticleView(LoginRequiredMixin, UpdateView):
    '''A view to update an Article and save it to the database.'''
    form_class = UpdateArticleForm
    template_name = "blog/update_article_form.html"
    model = Article ## add this model and the QuerySet will automatically find instance by PK

    def get_login_url(self) -> str:
        '''Return the URL to the login page.'''
        return reverse('login')
    
    def form_valid(self, form):
        '''
        Handle the form submission to create a new Article object.
        '''
        print(f'UpdateArticleView: form.cleaned_data={form.cleaned_data}')
        return super().form_valid(form)

from django.views.generic.edit import DeleteView
class DeleteCommentView(DeleteView):
    '''A view to delete a comment and remove it from the database.'''
    template_name = "blog/delete_comment_form.html"
    model = Comment
    context_object_name = 'comment'
    
    def get_success_url(self):
        '''Return a the URL to which we should be directed after the delete.'''
        # get the pk for this comment
        pk = self.kwargs.get('pk')
        comment = Comment.objects.filter(pk=pk).first() # get one object from QuerySet
        
        # find the article to which this Comment is related by FK
        article = comment.article
        
        # reverse to show the article page
        return reverse('article', kwargs={'pk':article.pk})

from django.contrib.auth.forms import UserCreationForm ## NEW
from django.contrib.auth.models import User ## NEW
from django.contrib.auth import login # NEW
from django.shortcuts import redirect

class RegistrationView(CreateView):
    '''
    show/process form for account registration
    '''
    template_name = 'blog/register.html'
    form_class = UserCreationForm

    def dispatch(self, request: HttpRequest, *args, **kwargs):
        '''Handle the User creation part of the form submission'''
        # handle the POST:
        if self.request.POST:
            # reconstruct the UserCreationForm from the POST data
            user_form = UserCreationForm(self.request.POST)

            if not user_form.is_valid():
                # if the form is invalid, return the error to the template
                return super().dispatch(request, *args, **kwargs)
            # create the user and login
            # NOTICE for mini_fb: attach the user to the Profile instance object so that it 
            # can be saved to the database in super().form_valid()
            user = user_form.save()    

            print(f"RegistrationView.form_valid(): Created user= {user}")   
            login(self.request, user)
            print(f"RegistrationView.form_valid(): User is logged in")   
            
            return redirect(reverse('show_all_articles'))
        
        # GET: handled by super class
        return super().dispatch(*args, **kwargs)