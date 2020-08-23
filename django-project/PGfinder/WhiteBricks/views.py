import json
import random
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
#from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.core.mail import EmailMessage
from django.db.models import Q 

from .tokens import account_activation_token
from django.core.mail import EmailMessage
from .models import Property, Notifications, Profile 
from .forms import AccomodationForm, ProfileForm, PasswordChangeForm
from .filters import OrderFilter
from .serializer import PropertySerializer
#from .decerator import ajax_login_required
#for the trial


# Home page
def index(request):
  context = {}
  if request.user.is_authenticated:
    profile = Profile.objects.get(user=request.user.id)
    context = {'profile': profile}
  return render(request, 'myhome/index.html', context)

# About us
def about(request):
  context = {}
  if request.user.is_authenticated:
    profile = Profile.objects.get(user=request.user.id)
    context = {'profile': profile}
  return render(request, "myhome/about.html", context)

# Contact
def contact(request):
  context = {}
  if request.user.is_authenticated:
    profile = Profile.objects.get(user=request.user.id)
    context = {'profile': profile}
    
  if request.method == "POST":
    name = request.POST['name']
    from_email = request.POST['email']
    message = request.POST['message']

    email_message = "From: {} \n Email: {}\n Message: {}".format(name, from_email, message)
    subject = "Message from {}".format(name)

    email = EmailMessage(
      subject, 
      email_message, 
      from_email, 
      to=['hafismuhammed25@gmail.com']
      )
    email.send()

    return JsonResponse({"status": "success"})
  else:
    return render(request, 'myhome/contact.html', context)

# Register
def Register(request):
  if request.method == 'POST':
    firstname = request.POST["first_name"]
    lastname = request.POST["last_name"]
    username = request.POST["username"]
    email = request.POST["email"]
    con_number = request.POST["con_number"]
    password1 = request.POST["password1"]
    password2 = request.POST["password2"]

    if User.objects.filter(username=username).exists():
      return JsonResponse({'status': 'used_username'})
    elif User.objects.filter(email=email).exists():
      return JsonResponse({'status': 'used_email'})
    else:
      user = User.objects.create_user(username=username, email=email, password=password1, first_name=firstname, last_name=lastname)
      user.is_active = False
      user.save()

      profile = Profile(user=user, contact_number=con_number)
      profile.save()
      #Activation email
      current_site = get_current_site(request)
      mail_subject ='Activate your account'
      message = render_to_string('acc_active_email.html', {
        'user': user,
        'domain': current_site.domain,
        'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
        'token' : account_activation_token.make_token(user),
         })
      to_email = email
      email = EmailMessage(
        mail_subject, message, to=[to_email]
        )
      email.send()

      return JsonResponse({'status': 'success'})

  else:
      return render(request, "myhome/register.html")

#account activation
def activate(request, uidb64, token):
  try:
    uid = force_text(urlsafe_base64_decode(uidb64))
    user = User.objects.get(pk=uid)
  except(TypeError, ValueError, OverflowError, User.DoesNotExist):
    user = None
  if user is not None and account_activation_token.check_token(user, token):
    user.is_active = True
    user.save()
    login(request, user)
    
    messages.add_message(request, messages.SUCCESS, 'Thank you for email conformation.Now you can login your account')
    return render(request, 'activation_view.html', {'subject':user})
    #return HttpResponse('Thank you for email conformation.Now you can login your account')
  else:
    messages.add_message(request, messages.ERROR, 'activation link is invalid')
    return HttpResponse('activation link is invalid')



# login
def loginPage(request):
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
         
          if user.is_active:
            login(request, user)
            messages.add_message(request, messages.SUCCESS, 'You are Successfully Logined')
            return HttpResponseRedirect('/whitebricks/home/')
         
          else:
            messages.add_message(request, messages.ERROR, 'Sorry, Incorrect Username or Password. Try Agin')
            return HttpResponseRedirect('/whitebricks/login/')
        else:
          messages.add_message(request, messages.ERROR, 'Sorry, Incorrect username or password. Try Again')
          return HttpResponseRedirect('/whitebricks/login/')
      
    else:
      return render(request, "myhome/login.html")

#logout
def logingout(request):
  logout(request)
  messages.add_message(request, messages.SUCCESS, 'Successfully Logout')
  return HttpResponseRedirect('/whitebricks/home/')

#change password
@login_required(login_url='/whitebricks/login/')
def change_password(request):
  context = {}
  if request.user.is_authenticated:
    profile = Profile.objects.get(user=request.user.id)
    context = {'profile': profile}

  if request.method == 'POST':
    old_password = request.POST['old_password']
    new_password1 = request.POST['new_password1']
    new_password2 = request.POST['new_password2']
    
    user = User.objects.get(id=request.user.id)
    if user.check_password(old_password):
      user.set_password(new_password1)
      user.save()

      mail_subject = 'Password Change Conformation'
      message = "Hi, {} \n You've successfully changed your Whitebricks account password.\n \n Thanks for using WhiteBricks service ! \n The WhiteBricks Team".format(request.user.first_name)
      to_email = request.user.email
      email = EmailMessage(
        mail_subject, message, to=[to_email]
      )
      email.send()

      login(request, user)
      messages.add_message(request, messages.SUCCESS, 'Password Successfully Changed !')
      return HttpResponseRedirect('/whitebricks/home/')
    else:
      messages.add_message(request, messages.ERROR, 'Incorrect Current Password')
      return HttpResponseRedirect('/whitebricks/change_password')
    
  else:
    return render(request, 'myhome/password_change_form.html', context)

#forgot password
def forgot_password(request):
  if request.method == "POST":
    username = request.POST['u_name']
    new_pasword = request.POST['new_pass']

    user = User.objects.get(username=username)
    user.set_password(new_pasword)
    user.save()
    login(request, user)
    messages.add_message(request, messages.SUCCESS, 'Password Successfully Changed !')
    return HttpResponseRedirect('/whitebricks/home/')
  else:
    return render(request, 'myhome/forgot_password.html')

def reset_password(request):
  username = request.GET.get('u_name')
  try:
    user = User.objects.get(username=username)
    otp = random.randint(1000, 9999)
    #profile = Profile.objects.get(user=user)
    #profile.verify_otp = otp
    #profile.save()
    message = "Dear {} \n {} is your One Time Password(OTP). Do not share it with other \n \n Thanks for using WhiteBricks service ! \n The WhiteBricks Team".format(user.first_name, otp)
    subject = "Password Reset Verification"
    
    try:
      email = EmailMessage(subject, message, to=[user.email])
      email.send()
      return JsonResponse({"status":"sent", "email":user.email, "rotp":otp})
    except:
      return JsonResponse({"status":"error", "email":user.email})
  
  except:
    return JsonResponse({"status":"failed"}) 
  
#profile settings
@login_required(login_url='/whitebricks/login/')
def edit_profile(request):
  if request.method == 'POST':
    profile_form = ProfileForm(request.POST, request.FILES)

    if profile_form.is_valid():

      user_objects = User.objects.get(id=request.user.id)
      user_objects.first_name = profile_form.cleaned_data['first_name']
      user_objects.last_name = profile_form.cleaned_data['last_name']
      user_objects.email = profile_form.cleaned_data['email'] 
      
      user_objects.save()

      #if Profile.objects.get(user=request.user.id):
        #profile_objects = Profile.objects.get(user=request.user.id)
      #else:
      profile_objects = Profile.objects.get(user=request.user.id)
      profile_objects.contact_number = profile_form.cleaned_data['contact_number']
      profile_objects.gender = profile_form.cleaned_data['gender']
      profile_objects.occupation = profile_form.cleaned_data['occupation']
      profile_objects.address = profile_form.cleaned_data['address']
      profile_objects.about = profile_form.cleaned_data['about']
      profile_objects.profile_pic = profile_form.cleaned_data['profile_pic']
      profile_objects.user = request.user

      profile_objects.save()

      return HttpResponseRedirect('/whitebricks/edit_profile')
  else:
    user_details = User.objects.get(id=request.user.id)
    profile = Profile.objects.get(user=request.user)
    #property_details = Property.objects.get(id=requested_property_id)
    profile_form = ProfileForm(
      initial={
      "firt_name":user_details.first_name, "last_name":user_details.last_name, 
      "email":user_details.email, "conact_number":profile.contact_number,
      "gender":profile.gender,"occupation":profile.occupation,
      "address":profile.address, "about":profile.about,
      "profile_pic":profile.profile_pic,
      })
    context = {
      'form':profile_form, 
      'user':user_details, 
      'profile':profile
      }
  return render(request, 'myhome/edit_profile.html', context)

  
  # Ad posting
@login_required(login_url='/whitebricks/login/')
def Adverticement(request):
  if request.method == 'POST':
    property_form = AccomodationForm(request.POST, request.FILES)

    if property_form.is_valid():
      
      property_object = Property()
      property_object.headline = property_form.cleaned_data['headline']
      property_object.city = property_form.cleaned_data['city']
      property_object.location = property_form.cleaned_data['location'] 
      property_object.facilites = property_form.cleaned_data['facilites']
      property_object.rent = property_form.cleaned_data['rent']
      property_object.email = property_form.cleaned_data['email'] 
      property_object.mobile = property_form.cleaned_data['mobile']
      property_object.images = request.FILES['images']
      property_object.owner = request.user
      
      property_object.save()
      messages.add_message(request, messages.SUCCESS, 'Successfully added your new property')
      return HttpResponseRedirect('/whitebricks/my_property/')
  else:
    profile = Profile.objects.get(user=request.user.id)
    property_form = AccomodationForm(request.POST, request.FILES)
    context = {
      'profile': profile,
      'form': property_form
    }
  return render(request, 'myhome/myroom.html', context)

#search property  
def search(request):
  qur = request.GET.get('search', None)
  if qur is not None:
    looking = Q(city__icontains=qur)
    properties = Property.objects.filter(looking)
  else:
    accomodations = Property.objects.all()
    if request.user.is_authenticated:
      profile = Profile.objects.get(user=request.user.id)
      context = {'profile': profile}
  context = {'properties': properties}
  return render(request, 'myhome/search.html', context)

def property_previw(request, requested_id):
  property_id = request.GET.get('property')
  property_details = Property.objects.get(id=requested_id)
  context = {'property': property_details,}
  return render(request, "myhome/property_detail_view.html", context)

# View cont info:
def contact_details(request):
    #property_id = request.GET.get('id')
    #print(property_id)
  if request.user.is_authenticated:
    property_details = Property.objects.all()
    seraializer = PropertySerializer(property_details, many=True)
    details = seraializer.data
      #context = {'property': serializer.data}
      #jsnor = json.dumps({'authenticated': True})
    
    return JsonResponse(details, safe=False )
  else:
    return JsonResponse({"authenticated": False})

#property view
def property_list(request):
  profile = Profile.objects.get(user=request.user.id)
  properties = Property.objects.values('types')
  context = {
    'profile':profile,
    'properties': properties
  }
  return render(request, 'myhome/all_property.html', context)

@login_required(login_url='/whitebricks/login/')
def my_property(request):
  profile = Profile.objects.get(user=request.user.id)
  properties = Property.objects.filter(owner=request.user)
  context = { 
    'profile': profile,
    'properties': properties 
    }
  return render(request, 'myhome/property.html', context)

# editing
def edit_property(request, requested_property_id):
  if request.method == 'POST':
    property_form = AccomodationForm(request.POST, request.FILES)

    if property_form.is_valid():
      
      property_details = Property.objects.get(id=requested_property_id)
      property_details.headline = property_form.cleaned_data['headline']
      property_details.city = property_form.cleaned_data['city']
      property_details.location = property_form.cleaned_data['location'] 
      property_details.facilites = property_form.cleaned_data['facilites']
      property_details.rent = property_form.cleaned_data['rent']
      property_details.email = property_form.cleaned_data['email'] 
      property_details.mobile = property_form.cleaned_data['mobile']
      property_details.images = request.FILES['images']

      property_details.save()
      messages.add_message(request, messages.SUCCESS, 'Successfully updated your property details')
      return HttpResponseRedirect('/whitebricks/my_property/')
  else:
    profile = Profile.objects.get(user=request.user.id)
    property_details = Property.objects.get(id=requested_property_id)
    property_form = AccomodationForm(
      initial={
      "headline": property_details.headline, "city": property_details.city,
      "address": property_details.address, "types": property_details.types,
      "location": property_details.location, "facilities": property_details.facilites, 
      "rent": property_details.rent, "email": property_details.email, 
      "mobile":property_details.mobile, "images": property_details.images
      })
    context = {
      'form': property_form,
      'property': property_details,
      'profile': profile
    }
  return render(request, 'property/edit.html', context)

# Delete property
def delete_property(request, requested_id):
  property_details = Property.objects.get(id=requested_id)
  property_details.delete()

  messages.add_message(request, messages.WARNING, 'Your property is deleted permanently')
  return HttpResponseRedirect('/whitebricks/my_property/')


  

  '''
  properties = Property.objects.get(id=request.POST.get('id'))
  is_liked = False
  if properties.liked.filter(id=request.user.id).exists():
    properties.liked.remove(request.user)
    is_liked = False 
  else:
    properties.liked.add(request.user)
    is_liked = True

    context = {
      'properties': properties,
      'is_liked': is_liked,
      'total_likes': properties.total_likes(),
    }
    if request.is_ajax():
      html = render_to_string(request, 'like_section.html', context)
      return JsonResponse({'form':html})'''


  '''
  user = request.user

  if request.method == 'POST':
    post_id = request.POST('post_id')
    post_obj = Property.objects.get(id=post_id)
    
    if user in post_obj.liked.all():
      post_obj.liked.remove(user)
    else:
      post_obj.liked.add(user)

    like, created = Like.objects.get_or_create(user=user, post_id=post_id)

    if not created:
      if like.value == 'Like':
        like.value == 'Unlike'
      else:
        like.value == 'Like'
    Like.save()
  
  return HttpResponseRedirect('posts:post-list')'''

  
  #properties = Property.objects.get(id=requested_id)
  #property = Property.objects.all()

def notification(request):
  if request.user.is_authenticated:
    user = request.user 
    if request.method == 'POST':
  
      property_id = request.POST['property'] 
      owner = request.POST['owner_id']
      print(property_id)
      print(owner)
      property_object = Property.objects.get(id=property_id)
      owner_object = User.objects.all().get(username=owner)
      notification = "Hi {}, {} \n have intrested in your property '{}'".format(property_object.owner, user.first_name, property_object.headline) 
      property_object.notify.add(user)
      notifications = Notifications.objects.create(notification=notification, property=property_object, owner=owner_object)

      notifications.save()
      return JsonResponse({"msg":"success", "authenticated": True})
  else:
    return JsonResponse({"authenticated": False})

#notification view
def view_notification(request):
  profile = Profile.objects.get(user=request.user.id)
  notification = Notifications.objects.filter(owner=request.user.id)
  context = {
    'profile': profile,
    'notifications':notification
  }
  return render(request, 'myhome/notification.html', context)

#delete notifications
def delete_notification(request):
  notifications = Notifications.objects.filter(owner=request.user.id)
  notifications.delete()
  return HttpResponseRedirect('/whitebricks/veiw_notification')
  
#new notification indicator
'''
def notification_upadate(request):
  flag = request.GET.get('flag', None)
  target = request.GET('target', 'box')
  last_notification = int(flag) if flag.isdigit() else None

  if last_notification:
    new_notifications = request.user.notifications.filter(
      id=last_notification).active().prefetch()

    notification_list = []
    for notify in new_notifications:
      notification = notify.as_json()'''
      
