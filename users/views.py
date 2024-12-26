from django.shortcuts import render, redirect
from .models import Profile


#login & users registration import 
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout


from django.contrib import messages # Flash message import

# you can remove this aftter cutomize it on form.py 
# from django.contrib.auth.forms import UserCreationForm # To get the register form filed from django buildin

from .forms import CustomUserCreationForm

from django.contrib.auth.decorators import login_required # only authenticated user can access the Add Project form when they login import

from .forms import ProfileForm, SkillForm

from .utils import searchProfile #Search Profile Query









#**LOGIN VIEWS FUNCTION**#
def loginUser(request):

    page = 'login'
    
    # when i type login it will not showing anymore
    if request.user.is_authenticated:
        return redirect('profiles')
    #Noted: procceed to block the Add Project form in projects apps views
    

    


    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Username does not exit')
            # print('Username does not exit') # The messages not imported yet

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user) 
            return redirect('profiles')
        else:
            messages.error(request, 'Username or password is incorect')
            # print('Username or password is incorect') # The messages not imported yet

    return render(request, 'users/login_register.html')
    #****Noted after this procced to navbar login/logout****#


def logoutUser(request):
    logout(request)
    messages.success(request, 'User was succesfuly logout') #Flassmessages for logout    Noted: Proceed to user registration
    return redirect('login')
# After this procced to loginUser to hide the login when you type login path



# User registration
def registerUser(request):
    page = 'register' #register render on login html template Proceed to login html
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, 'User was SUCCESS CREATED') # test it first

            login(request, user) # the user can login
            return redirect('edit-account') # when user login it will redirect to edit-account
        
        else:
            messages.success(request, 'An error has accured during registration')
        # Noted customize the register form, Procced form.py, create form.py

    context = {'page': page, 'form': form}
    return render(request, 'users/login_register.html', context)
    






# Profile views
def profiles(request):
    profiles, search_query = searchProfile(request)
    context = {'profiles': profiles, 'searh_query': search_query}
    return render(request, 'users/profiles.html', context)



# User profile views
def userProfile(request, pk): 
    profile = Profile.objects.get(id=pk)

    topSkills = profile.skill_set.exclude(description__exact="")
    otherSkills = profile.skill_set.filter(description="")

    context = {'profile': profile, 'topSkills': topSkills, 'otherSkills': otherSkills}
    return render(request, 'users/user-profile.html', context)


#*************AFTER RENDER PROFILE & USER-PROFILE  PROCEED TO SIGNALS**************************#







# User Account Views
@login_required(login_url='login')
def userAccount(request):
    profile = request.user.profile  # Accessing the data from user-profile    

    skills = profile.skill_set.all()    # Function to get name, and description in Skill

    projects = profile.project_set.all() # To get projects details 

    context = {'profile': profile, 'skills': skills, 'projects': projects}
    return render(request, 'users/account.html', context) 
# NOTED after this procceed to  acount.html  html template to render the date 




# Edit Account
@login_required(login_url='login')
def editAcount(request):
    profile =  request.user.profile
    form = ProfileForm(instance=profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile) 
        if form.is_valid():
            form.save()
            return redirect('account')
    context = {'form': form}    #Procced to Signal 
    return render(request, 'users/profile_form.html', context)






@login_required(login_url='login')
def createSkill(request):
    profile = request.user.profile
    form = SkillForm()

    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request, 'Skill was added successfully') #
            return redirect('account')
    context = {'form': form}
    return render(request, 'users/skill_form.html', context)



@login_required(login_url='login')
def updateSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance=skill)

    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, 'Skill was updated') 
            return redirect('account')
    context = {'form': form}
    return render(request, 'users/skill_form.html', context)



def deleteSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    if request.method == 'POST':
        skill.delete()
        messages.success(request, 'Skill was deleted successfuly') 
        return redirect('account')
    context = {'object': skill}
    return render(request, 'delete-project.html', context)