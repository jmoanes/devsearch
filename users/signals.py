from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile

# Welcome register email
from django.core.mail import send_mail # Register welcome email configuration
from django.conf import settings





# When create a new user it automatic addedd to Profile
def createProfile(sender, instance, created, **kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(
            user=user,
            username=user.username,
            email=user.email,
            name=user.first_name,
         )
        
        #Configure register welcome email
        subject = 'Welcome to devsearch'
        message = 'We are you are here!'
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [profile.email],
            fail_silently=False,
        )




#Update after create edit user-account
def updateUser(sender, instance, created, **kwargs):
    profile = instance
    user = profile.user
    if created == False:
        user.first_name = profile.name
        user.username = profile.username
        user.email = profile.email
        user.save()


# When user delete the account in Profile it also automatic deleted
def deleteUser(sender, instance, **kwargs):
     user = instance.user
     user.delete()



post_save.connect(createProfile, sender=User)
post_save.connect(updateUser, sender=Profile)  #Update user-account after the edite user-account made
post_delete.connect(deleteUser, sender=Profile)   


#*********NOTED: AFTER SIGNAL NEXT CREATE USERSS ACCOUNT**************#