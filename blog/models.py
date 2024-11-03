## Create a Model 
#
# blog/models.py
# Define the data objects for our application
#
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

#Each model is a class
class Article(models.Model): #class MUST inheirit 
    '''Encapsulate the idea of an Article by some author.'''
    # data attributes of an Article:
    title = models.TextField(blank=False) #There is a bunch of optional parameters
    author = models.TextField(blank=False) #blank=False means the field is required to be filled for each Article Model
    text = models.TextField(blank=False)
    published = models.DateTimeField(auto_now=True) #auto_now=True sets the time to now upon Model instantiation
    #image_url = models.URLField(blank=True) ## new
    image_file = models.ImageField(blank=True) # an actual image
    # data attributes of a Article:
    user = models.ForeignKey(User, on_delete=models.CASCADE) ## NEW
    
    #Default method so name MUST match (Admin can display this rather than the unique ID)
    def __str__(self):
        '''Return a string representation of this Article object.'''
        return f'{self.title} by {self.author}'

    def get_comments(self):
        '''Return all of the comments about this article.'''
        comments = Comment.objects.filter(article=self)
        return comments
    
    def get_absolute_url(self):
        '''Return the URL to display this Article.'''
        return reverse('article', kwargs={'pk':self.pk})

class Comment(models.Model):
    '''Encapsulate the idea of a Comment on an Article.'''
    
    # data attributes of a Comment:
    article = models.ForeignKey("Article", on_delete=models.CASCADE)
#       *models.ForeignKey attaches many comments to one Article
#       *on_delete=models.CASCADE makes it so when the article is deleted all comments with it as their foreign key's are also deleted
    author = models.TextField(blank=False)
    text = models.TextField(blank=False)
    published = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        '''Return a string representation of this Comment object.'''
        return f'{self.text}'