## Create View
# mini_fb/views.py
# Define the views for the mini_fb app:
#from django.shortcuts import render
import profile

from django.forms import BaseModelForm
from django.http import HttpResponse
from .models import *
from django.views.generic import ListView, DetailView, View
from django.views.generic.edit import CreateView
from .forms import *
from django.urls import reverse
from typing import Any

#class-based view
class ShowAllProfilesView(ListView):
    '''Create a subclass of ListView to display all mini_fb articles.'''
    model = Profile # retrieve objects of type Article from the database
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profiles' # how to find the data in the template file (context variable)

#A more detailed version for a single profile
class ShowProfilePageView(DetailView):
    '''Create a class that inheirits DetailView to display a single profile'''
    model = Profile
    template_name = 'mini_fb/show_profile.html'
    context_object_name = 'profile'

#The view to create a new profile
class CreateProfileView(CreateView):
    '''A view to create a new profile and save it to the database.'''
    form_class = CreateProfileForm
    template_name = "mini_fb/create_profile_form.html"

#The view to create a new StatusMessage
class CreateStatusMessageView(CreateView):
    '''A view to create a new StatusMessage and save it to the database.'''
    form_class = CreateStatusMessageForm
    template_name = "mini_fb/create_status_form.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        '''
        Build the dict of context data for this view.
        '''
        # superclass context data
        context = super().get_context_data(**kwargs)
        # find the pk from the URL
        pk = self.kwargs['pk']
        # find the corresponding article
        profile = Profile.objects.get(pk=pk)
        # add article to context data
        context['profile'] = profile
        return context
    
    def form_valid(self, form):
        '''
        Handle the form submission. We need to set the foreign key by 
        attaching the Profile to the StatusMessage object.
        We can find the article PK in the URL (self.kwargs).
        '''
        print(form.cleaned_data)
        #find Article identified by the PK from the URL pattern
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        #Attach Article to the instance of the comment set to its PK
        form.instance.profile = profile


        # save the status message to database
        sm = form.save()
        # read the file from the form:
        files = self.request.FILES.getlist('files')
        for f in files:
            image = Image()
            image.image_file = f
            image.status_message = sm
            image.save()


        #Delegate work to super
        return super().form_valid(form)

    def get_success_url(self) -> str:
        '''Return the URL to redirect to after successfully submitting form.'''
        return reverse('show_profile', kwargs={'pk': self.kwargs['pk']})

from django.views.generic.edit import UpdateView
class UpdateProfileView(UpdateView):
    '''A view to update an Article and save it to the database.'''
    form_class = UpdateProfileForm
    template_name = "mini_fb/update_profile_form.html"
    model = Profile ## add this model and the QuerySet will automatically find instance by PK
    
    def form_valid(self, form):
        '''
        Handle the form submission to create a new Profile object.
        '''
        print(f'UpdateArticleView: form.cleaned_data={form.cleaned_data}')
        return super().form_valid(form)
    
    def get_success_url(self) -> str:
        '''Return the URL to redirect to after successfully submitting form.'''
        return reverse('show_profile', kwargs={'pk': self.kwargs['pk']})

class UpdateStatusMessageView(UpdateView):
    '''A view to update an StatusMessage and save it to the database.'''
    form_class = UpdateStatusMessageForm
    template_name = "mini_fb/update_status_form.html"
    model = StatusMessage ## add this model and the QuerySet will automatically find instance by PK
    
    def form_valid(self, form):
        '''
        Handle the form submission to create a new StatusMessage object.
        '''
        print(f'UpdateArticleView: form.cleaned_data={form.cleaned_data}')
        return super().form_valid(form)
    
    def get_success_url(self):
        '''Return a the URL to which we should be directed after the delete.'''
        # get the pk for this status
        pk = self.kwargs.get('pk')
        message = StatusMessage.objects.filter(pk=pk).first() # get one object from QuerySet
        
        # find the article to which this Comment is related by FK
        message = message.profile
        
        # reverse to show the article page
        return reverse('show_profile', kwargs={'pk':message.pk})

from django.views.generic.edit import DeleteView
class DeleteStatusMessageView(DeleteView):
    '''A view to delete a status message and remove it from the database.'''
    context_object_name = 'status_message'
    template_name = "mini_fb/delete_status_form.html"
    model = StatusMessage

    def get_success_url(self):
        '''Return a the URL to which we should be directed after the delete.'''
        # get the pk for this status
        pk = self.kwargs.get('pk')
        message = StatusMessage.objects.filter(pk=pk).first() # get one object from QuerySet
        
        # find the article to which this Comment is related by FK
        message = message.profile
        
        # reverse to show the article page
        return reverse('show_profile', kwargs={'pk':message.pk})

from django.shortcuts import redirect
class CreateFriendView(View):
    '''A view to create a new friend for a user.'''
    def dispatch(self, request, *args, **kwargs):
        pk = kwargs.get('pk') 
        other_pk = kwargs.get('other_pk')
        
        # Retrieve the Profile instances
        profile = Profile.objects.get(id=pk)
        otherProfile = Profile.objects.get(id=other_pk)

        profile.add_friend(otherProfile)

        # Redirect back to the profile page
        return redirect(reverse('show_profile', kwargs={'pk': pk}))

class ShowFriendSuggestionsView(DetailView):
    '''Show suggestions for a given profile'''
    model = Profile
    template_name = 'mini_fb/friend_suggestions.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get friend suggestions for the current profile
        context['suggestions'] = self.object.get_friend_suggestions()
        return context

class ShowNewsFeedView(DetailView):
    '''Show news feed for a given profile'''
    model = Profile
    template_name = 'mini_fb/news_feed.html'
    context_object_name = 'profile'  # This will be the Profile instance

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get the news feed for the current profile
        context['news_feed'] = self.object.get_news_feed()
        return context