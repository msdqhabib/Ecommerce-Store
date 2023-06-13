from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from .forms import RegistrationForm,UserForm,UserProfileForm
from .models import Account,UserProfile
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate,login as auth_login,logout as auth_logout
from django.contrib.auth.decorators import login_required
from carts.models import Cart,CartItems
from carts.views import _cart_id
from orders.models import Order
import requests


#Verification email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

def register(request):
    if request.method == 'POST':
       form = RegistrationForm(request.POST)
       if form.is_valid():
           #first we are going to fetch all data after submission
           #when we use django form cleaned_data used to fetch values from form
           first_name = form.cleaned_data['first_name']
           last_name = form.cleaned_data['last_name']
           phone_number = form.cleaned_data['phone_number']
           email = form.cleaned_data['email']
           password = form.cleaned_data['password']
           username = email.split("@")[0]

           user = Account.objects.create_user(first_name=first_name,last_name=last_name,
                                              email=email,username=username,password=password)
           user.phone_number = phone_number
           user.save()

           #User Activation
           current_site = get_current_site(request)
           mail_subject = "Please Activate your account"
           #In message the email body which we going to send
           message = render_to_string('accounts/account_verification_email.html', {
               'user':user,
               'domain': current_site,
               #we are encoding primary keyt so no one can see it
               'uid': urlsafe_base64_encode(force_bytes(user.pk)),
               'token': default_token_generator.make_token(user),
           })
           to_email = email
           send_email = EmailMessage(mail_subject, message, to=[to_email])
           send_email.send()
            # autooscape is safest way of rendering html when you are sending email -->
            # Autoscape gives protection against CSRF -->

            #messages.success(request,'Account succesfuly Created')
           return redirect('/accounts/login/?command=verification&email='+email)


    else:
       form = RegistrationForm()
    
    context = {
        'form':form,
    }
    
    return render(request, 'accounts/register.html',context)


def login(request):
    if request.method == 'POST':
    #    form = AuthenticationForm(request, data=request.POST)
    #    if form.is_valid:
        email = request.POST['email']
        password = request.POST['password']
        # email = request.POST.get('email')
        # password = request.POST.get('password')
        user = authenticate(email=email,password=password)

        if user is not None:
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                is_cart_item_exists = CartItems.objects.filter(cart=cart).exists()
                if is_cart_item_exists:
                    cart_item = CartItems.objects.filter(cart=cart)

                    #Getting product variation by cart id
                    product_variation = []
                    for item in cart_item:
                        variation = item.variations.all()
                        product_variation.append(list(variation))

                    #Get cart items from the user to access his procduct variation
                    cart_item = CartItems.objects.filter(user=user)
                    ex_var_list = []
                    id = []
                    for item in cart_item:
                        existing_variation = item.variations.all()
                        ex_var_list.append(list(existing_variation))
                        id.append(item.id)
            
                    #to get common product variation
                    for pr in product_variation:
                        if pr in ex_var_list:
                            index = ex_var_list.index(pr)
                            item_id = id[index]
                            item = CartItems.objects.get(id=item_id)
                            item.quantity += 1
                            item.user = user
                            item.save()
                        else:
                            cart_item  = CartItems.objects.filter(cart=cart)
                            for item in cart_item:
                                #assigning user to cart items
                                item.user = user
                                item.save()
            except:
                pass
            auth_login(request, user)
            messages.success(request,'You are now logged in!')
            #Http_referrer will grab previous url from where we came
            url = request.META.get('HTTP_REFERER')
            try:
                query = requests.utils.urlparse(url).query
                #next=/cart/checkout/
                #this code split equal sign made next as key and checkout as value
                params = dict(x.split('=') for x in query.split('&'))
                #now we are getting key and value: {'next': '/cart/checkout/'}
                # print('parms --- ', params)
                if 'next' in params:
                    nextPage = params['next']
                    #so when user loggedIn with products in cart it will redirect to checkout page
                    return redirect(nextPage)
            except:
                return redirect('dashboard')
        
        else:
            messages.error(request, 'Invalid email or password.' )
            return redirect('login')
    
    return render(request, 'accounts/login.html')

@login_required(login_url='login')
def logout(request):
    auth_logout(request)
    messages.info(request, "YOu have Sucessfully logged out")
    return redirect('login')
    return 

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user,token):
        user.is_active = True
        user.save()
        messages.success(request, "Congratulations! Your account is activated")
        return redirect('login')
    else:
        messages.error(request, 'Invalid Activation Link')
        return redirect('register')
    
@login_required(login_url='login')
def dashboard(request):
    orders = Order.objects.order_by('-created_at').filter(user_id=request.user.id,is_created=True)
    orders_count = orders.count()
    context = {
        'orders_count': orders_count,
    }
    return render(request, 'accounts/dashboard.html',context)

def my_order(request):
    orders = Order.objects.filter(user=request.user, is_created=True).order_by('-created_at')
    context = {
        'orders':orders
    }
    return render(request, 'accounts/my_order.html',context)

def forgetPassword(request):
     if request.method == 'POST':
        #the 'email' actually coming from template where we name this to email field
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
           #emaill__exact make sure the email enter exactly the same the email stored in db
           user = Account.objects.get(email__exact=email)

           #Forget Password email
           current_site = get_current_site(request)
           mail_subject = "Reset your Password"
           #In message the email body which we going to send
           message = render_to_string('accounts/reset_password_email.html', {
               'user':user,
               'domain': current_site,
               #we are encoding primary keyt so no one can see it
               'uid': urlsafe_base64_encode(force_bytes(user.pk)),
               'token': default_token_generator.make_token(user),
           })
           to_email = email
           send_email = EmailMessage(mail_subject, message, to=[to_email])
           send_email.send()

           messages.success(request, 'Password email has been sent to your email Address')
           return redirect('login')

        else:
            messages.error(request,'Account Does not exist')
            return redirect('forgetPassword')
     return render(request,'accounts/forgetPassword.html')

def resetpassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    #purpose of checking token and user is to know the request is secure or not
    if user is not None and default_token_generator.check_token(user,token):
        #we need uid when we resetting password. so we are saving this in session storage
        request.session['uid']= uid 
        messages.success(request, "Please reset your password")
        return redirect('resetPassword')
    else:
        messages.error(request, 'This link has been expired!')
        return redirect('login')
    
def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            #set_password will saved pass in hash format
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset sucessfully')
            return redirect('login')

        else:
            messages.error(request, 'Password does not matched')
            return redirect('resetPassword')
    return render(request, 'accounts/resetPassword.html')

@login_required(login_url='login')
def edit_profile(request):
    userprofile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        #When you want to upload any files, you must include this request.FILES
        profile_form = UserProfileForm(request.POST,request.FILES ,instance=userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request,'Your Profile has been Updated')
            return redirect('edit_profile')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=userprofile)

    context = {
        'user_form':user_form,
        'profile_form':profile_form,
        'userprofile':userprofile,
    }

    return render(request, 'accounts/edit_profile.html',context)


@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
       current_password = request.POST['current_password']
       new_password = request.POST['new_password']
       confirm_password = request.POST['confirm_password']

       user = Account.objects.get(username__exact=request.user.username)

       if new_password == confirm_password:
           success = user.check_password(current_password)
           if success:
               user.set_password(new_password)
               user.save()
               messages.success(request, 'Password Updated Successfully')
               return redirect('change_password')
           else:
               messages.error(request, 'Please enter Valid current password')
               return redirect('change_password')
       else:
               messages.error(request, 'Password does not match')
               return redirect('change_password')    
               
    return render(request, 'accounts/change_password.html')