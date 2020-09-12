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
from django.contrib.auth import update_session_auth_hash
from django.core.mail import EmailMessage
from django.core.paginator import Paginator
from django.db.models import Q 

from .tokens import account_activation_token
from django.core.mail import EmailMessage
from .models import Property, Notifications, Profile 
from .forms import AccomodationForm, ProfileForm, PasswordChangeForm
from .filters import OrderFilter
from .serializer import PropertySerializer
from .decerator import unauthenticated_user, admin_only


# Home page
def home(request):
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
      to=['hafismuhammed25@gmail.com']
      )
    email.send()

    return JsonResponse({"status": "success"})
  else:
    return render(request, 'myhome/contact.html', context)

# Register
@unauthenticated_user
def Register(request):
  if request.method == 'POST':
    firstname = request.POST["first_name"]
    lastname = request.POST["last_name"]
    username = request.POST["username"]
    mail = request.POST["email"]
    con_number = request.POST["con_number"]
    password1 = request.POST["password1"]
    password2 = request.POST["password2"]

    if User.objects.filter(username=username).exists():
      return JsonResponse({'status': 'used_username'})
    elif User.objects.filter(email=mail).exists():
      return JsonResponse({'status': 'used_email'})
    else:
      user = User.objects.create_user(username=username, email=mail, password=password1, first_name=firstname, last_name=lastname)
      user.is_active = False
      user.save()

      profile = Profile(user=user, contact_number=con_number)
      profile.save()
  
      current_site = get_current_site(request)
      mail_subject ='Activate your account'
      message = render_to_string('acc_active_email.html', {
        'user': user,
        'domain': current_site.domain,
        'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
        'token' : account_activation_token.make_token(user),
         })
      to_email = mail
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
    
    return render(request, 'activation_view.html', {'subject':user})
  else:
    return HttpResponse('activation link is invalid')

# login
@unauthenticated_user
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
def add_property(request):
  if request.method == 'POST':
    property_form = AccomodationForm(request.POST, request.FILES)

    if property_form.is_valid():
      
      property_object = Property()
      property_object.headline = property_form.cleaned_data['headline']
      property_object.city = property_form.cleaned_data['city']
      property_object.location = property_form.cleaned_data['location'] 
      property_object.address = property_form.cleaned_data['address'] 
      property_object.types = property_form.cleaned_data['types'] 
      property_object.facilites = property_form.cleaned_data['facilites']
      property_object.rent = property_form.cleaned_data['rent']
      property_object.deposite = property_form.cleaned_data['deposite'] 
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
  qur = request.GET.get('search')
  if qur is not None:
    looking = Q(city__icontains=qur) | Q(address__icontains=qur)
    property_list = Property.objects.filter(looking)
    paginator = Paginator(property_list, 5)
    page = request.GET.get('page')
    properties = paginator.get_page(page)
    property_count = property_list.count()    

  context = {
      'properties': properties,
      'total_pro': property_count,
      'location': qur
      }

  if request.user.is_authenticated:
    profile = Profile.objects.get(user=request.user.id)
    context = {
      'profile': profile,
      'properties': properties,
      'total_pro': property_count,
      'location': qur
      }
  return render(request, 'myhome/search.html', context)

# property detailed view
def property_previw(request, requested_id):
  property_id = request.GET.get('property')
  property_details = Property.objects.get(id=requested_id)
  context = {'property': property_details}
  if request.user.is_authenticated:
    profile = Profile.objects.get(user=request.user.id)
    context = {
      'profile': profile,
      'property': property_details
      }
  return render(request, "myhome/property_detail_view.html", context)

# View property cont info: 
def contact_details(request):
  if request.method == 'GET' and request.is_ajax():
    property_id = request.GET.get('property')
    print(property_id)
    if request.user.is_authenticated:
      contact = Property.objects.get(id=property_id)
      data = {
        'email': contact.email,
        'mobile': contact.mobile,
        'authenticated': True
      }
      return JsonResponse(data)
    else:
      return JsonResponse({'authenticated': False})

#property view 
def property_list(request):
  profile = Profile.objects.get(user=request.user.id)
  qur = request.GET.get('types')
  print(qur)
  property_list = Property.objects.filter(types=qur)
  paginator = Paginator(property_list, 5)
  page = request.GET.get('page')
  properties = paginator.get_page(page)

  count_pro = property_list.count()
  context = {
    'profile':profile,
    'properties': properties,
    'total_pro': count_pro
  }
  return render(request, 'myhome/all_property.html', context)

# view own property
@login_required(login_url='/whitebricks/login/')
def my_property(request):
  profile = Profile.objects.get(user=request.user.id)
  property_list = Property.objects.filter(owner=request.user)
  paginator = Paginator(property_list, 5)
  page = request.GET.get('page')
  properties = paginator.get_page(page)
  count_pro = property_list.count()

  context = { 
    'profile': profile,
    'properties': properties,
    'total_pro': count_pro 
    }
  return render(request, 'myhome/property.html', context)

# editing property details
def edit_property(request, requested_property_id):
  if request.method == 'POST':
    property_form = AccomodationForm(request.POST, request.FILES)

    if property_form.is_valid():
      
      property_details = Property.objects.get(id=requested_property_id)
      property_details.headline = property_form.cleaned_data['headline']
      property_details.city = property_form.cleaned_data['city']
      property_details.location = property_form.cleaned_data['location'] 
      property_details.address = property_form.cleaned_data['address'] 
      property_details.types = property_form.cleaned_data['types'] 
      property_details.facilites = property_form.cleaned_data['facilites']
      property_details.rent = property_form.cleaned_data['rent']
      property_details.deposite = property_form.cleaned_data['deposite'] 
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
      "mobile": property_details.mobile, "images": property_details.images,
      "deposite": property_details.deposite
      })
    context = {
      'form': property_form,
      'property': property_details,
      'profile': profile
    }
  return render(request, 'myhome/edit_property.html', context)

# Delete property
def delete_property(request, requested_id):
  property_details = Property.objects.get(id=requested_id)
  property_details.delete()

  messages.add_message(request, messages.WARNING, 'Your property is deleted permanently')
  return HttpResponseRedirect('/whitebricks/my_property/')

# notification settings
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
  user = request.user.id
  profile = Profile.objects.get(user=user)
  notification = Notifications.objects.filter(owner=user).order_by('-date')
  Notifications.objects.filter(owner=user, is_seen=False).update(is_seen=True)

  context = {
    'profile': profile,
    'notifications': notification,
  }
  return render(request, 'myhome/notification.html', context)

def notification_count(request):
  user = request.user.id
  notification_count = Notifications.objects.filter(owner=user, is_seen=False).count()
  return {'notification_count': notification_count}

#delete notifications
def delete_notification(request):
  notifications = Notifications.objects.filter(owner=request.user.id)
  notifications.delete()
  return HttpResponseRedirect('/whitebricks/veiw_notification')
      
# admin panel
@login_required(login_url='/whitebricks/admin_login/')
@admin_only
def admin_panel(request):
  context = {}
  if request.user.is_authenticated:
    profile = Profile.objects.get(user=request.user.id)

  user_count = User.objects.all().count()
  property_count = Property.objects.all().count()
  property_list = Property.objects.all()
  paginator = Paginator(property_list, 3)
  page = request.GET.get('page')
  properties = paginator.get_page(page)

  coustemer_list = User.objects.all()
  list_no = Paginator(coustemer_list, 10)
  page = request.GET.get('page')
  coustemers = list_no.get_page(page)

  context = {
    'profile': profile,
    'total_user': user_count,
    'total_property': property_count,
    'properties': properties,
    'coustemers': coustemers
  }

  return render(request, 'admin/adminpanel.html', context)

# message to users(for admin)
@login_required(login_url='/whitebricks/login/')
@admin_only
def admin_contact(request):
  context = {}
  if request.user.is_authenticated:
    profile = Profile.objects.get(user=request.user.id)
    context = {'profile': profile}
    
  if request.method == "POST":
    to_email = request.POST['email']
    subject = request.POST['subject']
    message = request.POST['message']

    email = EmailMessage(
      subject, 
      message,  
      to=[to_email]
      )
    email.send()

    return JsonResponse({"status": "success", "email": to_email})
  else:
    return render(request, 'admin/admin_message.html', context)

#coustemer information (for admin)
@login_required(login_url='/whitebricks/login/')
@admin_only
def coustemer_info(request, requested_id):
  profile = Profile.objects.get(user=request.user.id)
  coustemer_info = Profile.objects.prefetch_related('user').get(user=requested_id)
  property_list = Property.objects.filter(owner=requested_id)
  paginator = Paginator(property_list, 3)
  page = request.GET.get('page')
  properties = paginator.get_page(page)
  total_property = property_list.count()
  
  context = {
    'profile': profile,
    'coustemer_info': coustemer_info,
    'properties': properties,
    'total_property': total_property
  }
  return render(request, 'admin/coustemer_info.html', context)

#deleting coustemer property
def delete_coust_pro(request, requested_id):
  property_details = Property.objects.get(id=requested_id)
  property_details.delete()

  messages.add_message(request, messages.WARNING, 'Your property is deleted permanently')
  return HttpResponseRedirect('/whitebricks/admin_panel')
