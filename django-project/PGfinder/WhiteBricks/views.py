import random
import uuid
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
from django.views.decorators.csrf import csrf_exempt

from .tokens import account_activation_token
from .models import Property, PropertyImages, Notifications, Profile, PayingGuestCheckout, BookedProperty
from .forms import PropertyForm, ProfileForm, BookingForm
from .decerator import unauthenticated_user
import razorpay


# Home page
def home(request):
  properties = Property.objects.filter(is_booked=False).order_by('-date')[:3]
  context = { 'properties':  properties }
  return render(request, 'myhome/index.html', context)

# About us
def about(request):
    return render(request, "myhome/about.html")

# Contact us
def contact_to_company(request):
  
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
    return render(request, 'myhome/contact.html')

# User registeration
@unauthenticated_user
def user_register(request):
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

#Account activation
def activate_account(request, uidb64, token):
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


@unauthenticated_user
def user_login(request):
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


def user_logout(request):
  logout(request)
  messages.add_message(request, messages.SUCCESS, 'Successfully Logout')
  return HttpResponseRedirect('/whitebricks/home/')

#change password
@login_required(login_url='/whitebricks/login/')
def change_password(request):

  if request.method == 'POST':
    old_password = request.POST['old_password']
    new_password1 = request.POST['new_password1']
    new_password2 = request.POST['new_password2']
    
    user = User.objects.get(id=request.user.id)
    if user.check_password(old_password):
      user.set_password(new_password1)
      user.save()

      mail_subject = 'Password Change Conformation'
      message = "Hi {}, \n You've successfully changed your Whitebricks account password.\n \n Thanks for using WhiteBricks service ! \n The WhiteBricks Team".format(request.user.first_name)
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
    return render(request, 'myhome/password_change_form.html')

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
    profile_form = ProfileForm(request.POST)

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
      profile_objects.user = request.user

      profile_objects.save()

      return HttpResponseRedirect('/whitebricks/edit_profile')
  else:
    user = request.user
    profile = Profile.objects.get(user=request.user)
    profile_form = ProfileForm(
      initial={
      "firt_name":user.first_name, "last_name":user.last_name, 
      "email":user.email, "conact_number":profile.contact_number,
      "gender":profile.gender,"occupation":profile.occupation,
      "address":profile.address, 
      })
    context = {
      'form':profile_form, 
      'user':user, 
      'profile':profile
      }
  return render(request, 'myhome/edit_profile.html', context)

  
# Advertising properties
@login_required(login_url='/whitebricks/login/')
def add_property(request):
  if request.method == 'POST':
    property_form = PropertyForm(request.POST, request.FILES)

    if property_form.is_valid():
      
      property_object = Property()
      property_images = PropertyImages()
      property_object.headline = property_form.cleaned_data['headline']
      property_object.city = property_form.cleaned_data['city']
      property_object.location = property_form.cleaned_data['location'] 
      property_object.address = property_form.cleaned_data['address'] 
      property_object.types = property_form.cleaned_data['types'] 
      property_object.facilites = property_form.cleaned_data['facilites']
      property_object.rent = property_form.cleaned_data['rent']
      property_object.deposit = property_form.cleaned_data['deposit'] 
      property_object.email = property_form.cleaned_data['email'] 
      property_object.mobile = property_form.cleaned_data['mobile']
      property_object.owner = request.user
      property_object.save()
     
      property_images.image = request.FILES['image']
      property_images.property = property_object
      property_images.owner = request.user
      property_images.save()
      messages.add_message(request, messages.SUCCESS, 'Successfully added your new property')
      return HttpResponseRedirect('/whitebricks/my_property/')
  else:
    property_form = PropertyForm(request.POST, request.FILES)
    context = {'form': property_form}
  return render(request, 'myhome/myroom.html', context)

#search property
def search_properties(request):
  qur = request.GET.get('search')
  if qur is not None:
    looking = Q(city__icontains=qur) | Q(address__icontains=qur)
    property_list = Property.objects.filter(looking, is_booked=False)
    paginator = Paginator(property_list, 9)
    page = request.GET.get('page')
    properties = paginator.get_page(page)
    property_count = property_list.count()    

  context = {
      'properties': properties,
      'total_pro': property_count,
      'location': qur
      }
  return render(request, 'myhome/search.html', context)

# property detailed view
@login_required(login_url='/whitebricks/login/')
def property_detailview(request, requested_id):
  user = request.user
  property_details = Property.objects.get(id=requested_id, is_booked=False)
  profile = Profile.objects.get(user=user)  
  booking_form = BookingForm(
    initial = {
        "firt_name":user.first_name, "last_name":user.last_name, 
        "email":user.email, "conact_number":profile.contact_number,
        "address":profile.address, 
      }
  )
  context = {
    'property': property_details,
    'form': booking_form,
    }
  return render(request, "myhome/property_detail_view.html", context)
 
# View property cont info: 
def contact_details(request, requested_id):
  if request.method == 'GET' and request.is_ajax():
    if request.user.is_authenticated:
      contact = Property.objects.get(id=requested_id)
      data = {
        'email': contact.email,
        'mobile': contact.mobile,
        'authenticated': True
      }
      return JsonResponse(data)
    else:
      return JsonResponse({'authenticated': False})

#property view 
def list_properties(request):
  qur = request.GET.get('types')
  property_list = Property.objects.filter(types=qur, is_booked=False)
  paginator = Paginator(property_list, 9)
  page = request.GET.get('page')
  properties = paginator.get_page(page)

  count_pro = property_list.count()

  context = {
    'properties': properties,
    'total_pro': count_pro
  }
  return render(request, 'myhome/all_property.html', context)

# view own property
@login_required(login_url='/whitebricks/login/')
def my_properties(request):
  property_list = Property.objects.filter(owner=request.user)
  paginator = Paginator(property_list, 10)
  page = request.GET.get('page')
  properties = paginator.get_page(page)
  count_pro = property_list.count()

  context = { 
    'properties': properties,
    'total_pro': count_pro 
    }
  return render(request, 'myhome/user_properties.html', context)

# editing property details
def edit_property(request, requested_property_id):
  if request.method == 'POST':
    property_form = PropertyForm(request.POST, request.FILES)

    if property_form.is_valid():
      
      property_details = Property.objects.get(id=requested_property_id, owner=request.user)
      property_images = PropertyImages()
      property_details.headline = property_form.cleaned_data['headline']
      property_details.city = property_form.cleaned_data['city']
      property_details.location = property_form.cleaned_data['location'] 
      property_details.address = property_form.cleaned_data['address'] 
      property_details.types = property_form.cleaned_data['types'] 
      property_details.facilites = property_form.cleaned_data['facilites']
      property_details.rent = property_form.cleaned_data['rent']
      property_details.deposit = property_form.cleaned_data['deposit'] 
      property_details.email = property_form.cleaned_data['email'] 
      property_details.mobile = property_form.cleaned_data['mobile']
      property_details.save()
      
      property_images.image = request.FILES['image']
      property_images.property = property_details
      property_images.owner = request.user
      property_images.save()
      messages.add_message(request, messages.SUCCESS, 'Successfully updated your property details')
      return HttpResponseRedirect('/whitebricks/my_property/')
  else:
    property_details = Property.objects.get(id=requested_property_id, owner=request.user)
    property_images = PropertyImages.objects.filter(property=property_details, owner=request.user)
    property_form = PropertyForm(
      initial={
      "headline": property_details.headline, "city": property_details.city,
      "address": property_details.address, "types": property_details.types,
      "location": property_details.location, "facilities": property_details.facilites, 
      "rent": property_details.rent, "email": property_details.email, 
      "mobile": property_details.mobile, 
      })
    context = {
      'form': property_form,
      'property': property_details,
    }
  return render(request, 'myhome/edit_property.html', context)


def delete_property(request, requested_id):
  property_details = Property.objects.get(id=requested_id)
  property_details.delete()
  messages.add_message(request, messages.WARNING, 'Your property is deleted permanently')
  return HttpResponseRedirect('/whitebricks/my_property/')


# notification settings
def notification(request, requested_id):
  if request.user.is_authenticated:
    user = request.user
    if request.method == 'POST':
      property_object = Property.objects.get(id=requested_id)
      notification = "Hi {}, {} \n  visited  your property '{}' in {}".format(property_object.owner, user.username, property_object.headline, property_object.location) 
      notification = Notifications.objects.create(notification=notification, property=property_object, owner=property_object.owner)
      notification.save()

      return JsonResponse({"msg":"success", "authenticated": True})
    else:
      return JsonResponse({"authenticated": False})

#notification view
def view_notifications(request):
  user = request.user.id
  profile = Profile.objects.get(user=user)
  notification = Notifications.objects.filter(owner=user).order_by('-date')
  Notifications.objects.filter(owner=user, is_seen=False).update(is_seen=True)

  context = {'notifications': notification,}
  return render(request, 'myhome/notification.html', context)

def notification_count(request):
  user = request.user.id
  notification_count = Notifications.objects.filter(owner=user, is_seen=False).count()
  return {'notification_count': notification_count}


def delete_notifications(request):
  notifications = Notifications.objects.filter(owner=request.user.id)
  notifications.delete()
  return HttpResponseRedirect('/whitebricks/veiw_notification')

# booking properties using payment gateways
@login_required(login_url='/whitebricks/login/')
def room_booking(request, requested_id):
  user = request.user
  property_instance = Property.objects.get(id=requested_id)
  
  if request.method == 'POST':
      first_name = request.POST['first_name']
      last_name = request.POST['last_name']
      address = request.POST['address']
      phone = request.POST['contact_number']
      email = request.POST['email']
      
      booking_price = property_instance.deposite
      reciept = str(uuid.uuid1())
      client = razorpay.Client(auth=("rzp_test_8ByHObWr7wXRoA", "vbj5N0Om11HrxPOCqiHGwBbz"))
      DATA = {
        'amount': booking_price * 100,
        'currency': 'USD',
        'receipt': 'WhiteBricks room booking',
        'payment_capture': 1,
        'notes': {}
      }
      order_details = client.order.create(data=DATA)
      paying_guestcheckout_instance = PayingGuestCheckout(
        paying_guest = user,
        order_id = order_details.get('id'),
        total_amount = booking_price,
        reciept_num = reciept,
      )
      paying_guestcheckout_instance.save()

      profile_instance = Profile.objects.get(user=user)
      profile_instance.address = address
      profile_instance.contact_number = phone
      profile_instance.save()
      user.first_name = first_name
      user.last_name = last_name
      user.email = email
      user.save()
      property_instance.is_booked = True
      property_instance.save()

      email_subject = "Message from WhiteBricks- PG booking"
      to_email = property_instance.email
      message_to_owner = """Hi {}, \n Your property in {} have new paying guest. 
      Contact your paying guest for confirmation.
      \n contact details of paying guest:\n Name: {} {}\n Email: {}\n Mobile: {}.
      \n for more details use our helpline.\n \n Thanks for using WhiteBricks service ! 
      \n The WhiteBricks Team""".format(property_instance.owner, property_instance.location, user.first_name, user.last_name, email, phone)
      email = EmailMessage(
        email_subject, message_to_owner, to=[to_email]
      )
      email.send()

      context = {
        'order_id': order_details.get('id'),
        'booking_price': booking_price,
        'amountscript': booking_price * 100,
        'currency': 'USD',
        'companyname': 'WhiteBricks',
        'username': request.user.first_name + ' ' + request.user.last_name,
        'useremail': request.user.email,
        'phone': phone,
        'rzpkey': 'rzp_test_8ByHObWr7wXRoA',
      }
      return render(request, 'myhome/payment.html', context)
  else:
    return HttpResponseRedirect(reverse('property_details', kwargs={
      'requested_id': requested_id
      }))


@csrf_exempt
@login_required(login_url='/whitebricks/login/')
def mark_pymentsuccess(request):
  if request.is_ajax():
    order_id = request.POST['order_id']
    payment_id = request.POST['payment_id']
    payment_signature = request.POST['payment_signature']
    user = request.user
    paying_guestcheckout_instance = PayingGuestCheckout.objects.get(
      order_id = order_id,
      paying_guest = user
    )
    paying_guestcheckout_instance.payment_signature = payment_signature
    paying_guestcheckout_instance.payment_id = payment_id
    paying_guestcheckout_instance.payment_completed = True
    paying_guestcheckout_instance.save()

    email_subject = "Booking confirmation from WhiteBricks"
    to_email = request.user.email
    message_to_pg = """Hi {}, \n You've successfully completed your booking. 
    The house owner will be contact as soon as posible.\n for more details use our helpline.
    \n \n Thanks for using WhiteBricks service ! \n The WhiteBricks Team""".format(request.user.first_name)
    email = EmailMessage(
      email_subject, message_to_pg, to=[to_email]
    )
    email.send()

    return JsonResponse({'result': 'payment completed'})








