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

from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.status import (
  HTTP_400_BAD_REQUEST,
  HTTP_404_NOT_FOUND,
  HTTP_200_OK
)
from rest_framework.response import Response
from django.db.models import Q 

from .tokens import account_activation_token
from django.core.mail import EmailMessage
from .models import Property, Notifications 
from .forms import AccomodationForm
from .filters import OrderFilter
from .serializer import PropertySerializer

#for the trial


# Home page
def index(request):
  return render(request, 'myhome/index.html')

# About us
def about(request):
  return render(request, "myhome/about.html")

# Contact
def contact(request):
  if request.method == "POST":
    subject = request.POST['name']
    from_email = request.POST['email']
    email_message = request.POST['message']

    email = EmailMessage(
      subject, 
      email_message, 
      from_email, 
      to=['hafismuhammed25@gmail.com']
      )
    email.send()

    messages.add_message(request, messages.SUCCESS, 'we will get back to you as soon as possible,')
    return HttpResponseRedirect('/whitebricks/contact/')
  
  else:
    return render(request, 'myhome/contact.html')

# Portfolio
def portfolio(request):
  return render(request, 'myhome/portfolio.html')

# Register
def Register(request):
  if request.method == 'POST':
    firstname = request.POST["first_name"]
    lastname = request.POST["last_name"]
    username = request.POST["username"]
    email = request.POST["email"]
    password1 = request.POST["password1"]
    password2 = request.POST["password2"]

    if User.objects.filter(username=username).exists():
      messages.add_message(request, messages.ERROR, 'This username is already taken, Please enter another one')
      return HttpResponse("username is already exist")
    elif User.objects.filter(email=email).exists():
      messages.add_message(request, messages.ERROR, 'This username is already taken, Please enter another one')
      return HttpResponse("email already exist")
    else:
      user = User.objects.create_user(username=username, email=email, password=password1, first_name=firstname, last_name=lastname)
      user.is_active = False
      user.save()
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

      messages.add_message(request, messages.SUCCESS, 'Succesfully created your account,Please Check your email and activate the account')
      return HttpResponse('account created')

  else:
      return render(request, "myhome/register.html")

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
            messages.add_message(request, messages.SUCCESS, 'You are successfully logined')
            return HttpResponseRedirect('/whitebricks/home/')
         
          else:
            messages.add_message(request, messages.ERROR, 'Sorry, Incorrect username or password. Please enter valid username and password.')
            return HttpResponse("Your account is not active")
        else:
          messages.add_message(request, messages.ERROR, 'Sorry, Incorrect username or password. Please enter valid username and password.')
          return HttpResponse('The account does not exist')
      
    else:
      return render(request, "myhome/login.html")

#logout
def logingout(request):
  logout(request)
  messages.add_message(request, messages.SUCCESS, 'Successfully logout')
  return HttpResponseRedirect('/whitebricks/home/')

def reset_email(request):
  return render(request, 'myhome/email_sent_done.html')
  
  # Ad posting
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
    property_form = AccomodationForm(request.POST, request.FILES)
  return render(request, 'myhome/myroom.html', {'form': property_form})
 
 # view ads
def Poster(request,requested_id):
  poster_details = Property.objects.get(id=requested_id)

  myFilter = OrderFilter()

  context = {"accomodation":poster_details}

  return render(request, "myhome/Poster.html", context)
  
def search(request):
  qur = request.GET.get('search', None)
  if qur is not None:
    accomodations = Property.objects.filter(Q(city__icontains=qur))
  else:
    accomodations = Property.objects.all()
  #accomodations = [
  #item for item in Property.objects.all() 
  #if qur in item.city or qur in item.location
  #]
  return render(request, 'myhome/search.html', {'accomodations':accomodations})
 
#property view
@login_required(login_url='/whitebricks/login/')
def my_property(request):
  properties = Property.objects.filter(owner=request.user)
  context = { "properties":properties }
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
    property_details = Property.objects.get(id=requested_property_id)
    property_form = AccomodationForm(
      initial={
      "headline":property_details.headline, "city":property_details.city, 
      "location":property_details.location, "facilities":property_details.facilites, 
      "rent":property_details.rent, "email":property_details.email, 
      "mobile":property_details.mobile, "images":property_details.images
      })
  return render(request, 'property/edit.html', {'form':property_form, 'property':property_details})

# Delete property
def delete_property(request, requested_id):
  property_details = Property.objects.get(id=requested_id)
  property_details.delete()

  messages.add_message(request, messages.WARNING, 'Your property is deleted permanently')
  return HttpResponse('data deleted')

# View cont info:
#@login_required(login_url='/whitebricks/login/') 
def contact_details(request):

    property_details = Property.objects.all()
    seraializer = PropertySerializer(property_details, many=True)
    data = seraializer.data
    #context = {'property': serializer.data}
    return JsonResponse(data, safe=False )

# for api 
@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny))
def login_api(request):
  username = request.data.get("username")
  password = request.data.get("password")
  
  if username is None or password is None:
    return Response({'error': 'Please provide both username and password'},
    status=HTTP_400_BAD_REQUEST)
  user = authenticate(username=username, password=password)

  if not user:
    return Response({'error': 'Invalid Credentials'},
    status=HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)

    return Response({'token': token.key},
    status=HTTP_200_OK)

# testing ajax
def sample_ajax_view(request):
  data = {"foo": "bar"}
  return JsonResponse(data)
  

def sample_view(request):
	return render(request,"ajax_template.html")

# trail for notifications
def post_view(request):
  qs = Property.objects.all()
  user = request.user

  context = {
    "qs": qs,
    "user": user
  }
  return render(request, 'posts/main.html', context)


  #properties = Property.objects.get(id=request.POST.get('property_id'))
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
def like_post(request):
  user = request.user 
  if request.method == 'POST':
    property_id = request.POST['property_id'] 
    owner = request.POST['owner_id']
    property_object = Property.objects.get(id=property_id)
    owner_object = User.objects.all().get(username=owner)
    notification =  user, "have intrested in your property" 
    property_object.notify.add(user)
    notifications = Notifications.objects.create(notification=notification, property=property_object, owner=owner_object)

    notifications.save()
    
    return JsonResponse()
    
   
    
  
   #return HttpResponseRedirect('/whitebricks/search/')  
'''
    notification_object = Notifications()
    notification_object.notification = user, 'have intrested in your',property
    notification_object.person = user
    properties.notify.add(property_object.owner)

    notification_object.save()'''
   
