## Create a Model 
#
# mini_fb/models.py
# Define the data objects for our application
#
from django.db import models
from django.urls import reverse

#Each model is a class
class Profile(models.Model): #class MUST inheirit 
    '''Encapsulate the idea of an Profile by some author.
    {firstName, lastName, city, email, profileImageURL}'''
    # data attributes of an Profile:
    firstName = models.TextField(blank=False)
    lastName = models.TextField(blank=False)
    city = models.TextField(blank=False)
    email = models.TextField(blank=False)
    profileImageURL = models.URLField(blank=True)
    
    #Default method so name MUST match (Admin can display this rather than the unique ID)
    def __str__(self):
        '''Return a string representation of this Profile object.'''
        return f'{self.firstName} {self.lastName}'
    
    #returns a list of all attached StatusMessages for a given profile
    def get_statusMessages(self):
        '''Return all of the statusMessages about this profile.'''
        messages = StatusMessage.objects.filter(profile=self)
        return messages
    
    #returns the URL which should be returned to when a profile is made
    def get_absolute_url(self) -> str:
        '''Return the URL to redirect to after successfully submitting form.'''
        return reverse('show_all')
    

    def get_friends(self):
        '''Return a list of this profile's friends as Profile instances, excluding self.'''
        #friends where self is profile1
        friendsCaseOne = Friend.objects.filter(profile1=self).values_list('profile2', flat=True)
        #friends where self is profile2
        friendsCaseTwo = Friend.objects.filter(profile2=self).values_list('profile1', flat=True)
            #QuereySet returns id as a list of tuples which does not work for comparrison (we should use a better pk for profiles)
        
        friend_ids = set(friendsCaseOne) | set(friendsCaseTwo)
        friend_ids.discard(self.id)
        # Retrieve the corresponding Profile objects and convert to a list of Profiles rather than a Querey Set
        return list(Profile.objects.filter(id__in=friend_ids))
    
    def add_friend(self, other):
        '''Add a friend relationship with another Profile instance.'''
        # Check that we're not trying to friend ourselves
        invalidFriendship = Friend.objects.filter(profile1=self, profile2=other).exists() | Friend.objects.filter(profile1=other, profile2=self).exists()
        if(self == other):
            invalidFriendship = True

        if not invalidFriendship:
            newFriend = Friend.objects.create(profile1=self, profile2=other)
            newFriend.save()
    
    def get_friend_suggestions(self):
        '''Return a list of profiles that are suggested friends with this profile'''
        existingFriends = set(Friend.objects.filter(profile1=self).values_list('profile1_id', flat=True)) | set(Friend.objects.filter(profile2=self).values_list('profile2_id', flat=True))
        suggestions = Profile.objects.exclude(id__in=existingFriends).exclude(id=self.id)
        return list(suggestions)
    
    def get_news_feed(self):
        '''Return a list of StatusMessages for this Profile and its friends.'''
        friendProfiles = self.get_friends()

        # Include self in the list of IDs to get messages from self and friends
        friendProfiles.append(self.id)  # Add self to the list

        #ordered by desending timestamp
        feed = StatusMessage.objects.filter(profile_id__in=friendProfiles).order_by('-timestamp')

        return list(feed)

class StatusMessage(models.Model):
    '''Encapsulate the idea of a status message for some profile.'''
    #each StatusMessage has a ForeignKey of type Profile creating a many-to-one relationship
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE)
    #timestamp defaults to the current system time
    timestamp = models.DateTimeField(auto_now=True)
    message = models.TextField(blank=False)

    def __str__(self):
        '''Return a string representation of this StatusMessage object.'''
        return f'{self.message}'
    
    def get_images(self):
        '''Return all of the Images about this StatusMessage.'''
        return Image.objects.filter(status_message=self)

    
class Image(models.Model):
    '''Encapsulate the idea of an image file'''
    #each Image has a ForeignKey of type Profile creating a many-to-one relationship
    status_message = models.ForeignKey("StatusMessage", on_delete=models.CASCADE)
    image_file = models.ImageField(blank=True)
    timestamp = models.DateTimeField(auto_now=True)

class Friend(models.Model):
    '''Encapsulate the idea of a friendship between two profiles'''
    profile1 = models.ForeignKey("Profile", on_delete=models.CASCADE, related_name="profile1")
    profile2 = models.ForeignKey("Profile", on_delete=models.CASCADE, related_name="profile2")
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        '''Return a string representation of this Friend object.'''
        return f'{self.profile1} & {self.profile2}'
