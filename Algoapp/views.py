# subscriptions/views.py
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from .models import *
from datetime import datetime, timedelta
from django.contrib.auth import login, logout, authenticate
from django.utils import timezone 
from django.utils.timezone import make_aware
from datetime import timedelta
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import User
from django.contrib import messages
from Algoapp.otpAuthentication import send_otp
from Algoapp.subscription_otp import send_sub_otp
import random


def home(request):

    # Business Details
    business_data = BusinessDetails.objects.all()

    # Blogs
    blogs = Blog.objects.all()


    # Membership Plans
    plans = MembershipPlan.objects.exclude(name = "Free_Trial").all()


    context = {
        "business_data" : business_data,
        "blogs" : blogs,
        "plans" : plans,
        "first_plan" : list(plans)[0],
    }

    if(request.user.is_authenticated):
        user = request.user

        existing_membership = UserMembership.objects.filter(user=request.user).first()
        if existing_membership:
            if existing_membership.expiration_date:
                expiration_date_aware = make_aware(datetime.combine(existing_membership.expiration_date, datetime.min.time()))

                if not expiration_date_aware > timezone.now():
                    exist_user = free_triel_users.objects.filter(user = user).first()
                    if(exist_user):
                        exist_user.delete()

                    send_sub_otp(user.email, user.username)
                    context['membership_expired'] = '⏰ Time to Renew Your Subscription! ⏳'
        else:
            context['clime_membership'] = "🎉 Unlock Premium Content for 14 Days for Free! 🎁"


    return render(request, 'index.html', context)


def register(request):

    if request.method == 'POST':
        f_name = request.POST.get('f_name')
        l_name = request.POST.get('l_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        re_password = request.POST.get('re_password')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken. Please choose a different one.')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email is already registered. Please use a different email address.')
        else:
            if password == re_password:

                global generateOTP
                global user

                generateOTP = random.randint(100000, 999999)

                user = User(username=username, email=email, first_name=f_name, last_name=l_name)
                user.set_password(password)
                
                send_otp(email, username, generateOTP)

                return render(request, "otp.html" , {"email" : email})

            else:
                messages.error(request, 'Passwords and Conform Password do not match.')

    return render(request, 'resgistration.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check if the user exists in the database

        user = User.objects.filter(username=username).first()
        if(not user):
            messages.error(request, 'Username not Found. Please choose a different one.')
            return redirect('login')
        
        # Check if the password matches
        if check_password(password, user.password):
            login(request, user)  # Log in the user after registration

            return redirect('home')  # Replace 'home' with the URL where you want to redirect after successful login
        else:
            messages.error(request, 'Wrong password')
            return redirect('login')
        
    return render(request, 'loginform.html')  # Default rendering for other cases


def user_logout(request):
    logout(request)
    return redirect('home')


@login_required(login_url = '/login/')
def active_subscription(request):
    if(request.method == 'GET'):

        existing_membership = UserMembership.objects.filter(user=request.user).first()
        if existing_membership:
            if existing_membership.expiration_date:
                expiration_date_aware = make_aware(datetime.combine(existing_membership.expiration_date, datetime.min.time()))

                print(expiration_date_aware)
                print(timezone.now())
                if expiration_date_aware > timezone.now():

                    return render(request, 'active_subscription.html', {'membership': existing_membership, 'warning': "Subscription Activated"})
                else:
                    
                    messages.error(request, 'User membership with this User is Expired. Choice membership')

            else:

                return render(request, 'subscribe_error.html', {'error_message': 'Expiration date is missing'})

        return render(request, 'active_subscription.html', {'warning': "You Don't Have any Subscription"})




@login_required(login_url = '/login/')
def subscribe(request):

    if request.method == 'POST':
        subscription_period = request.POST.get('subscription_type')
        plan_name = request.POST.get('plan_name')


        print(subscription_period)
        print(plan_name)

        plan = MembershipPlan.objects.filter(name = plan_name).first()

        if(plan):


            if subscription_period == 'monthly':
                expiration_date = timezone.now() + timezone.timedelta(days=30)
            elif subscription_period == 'quarterly':
                expiration_date = timezone.now() + timezone.timedelta(days=90)
            elif subscription_period == 'yearly':
                expiration_date = timezone.now() + timezone.timedelta(days=365)


            existing_membership = UserMembership.objects.filter(user=request.user).first()
            if existing_membership:
                if existing_membership.expiration_date:
                    expiration_date_aware = make_aware(datetime.combine(existing_membership.expiration_date, datetime.min.time()))

                    print(expiration_date_aware)
                    print(timezone.now())

                    if expiration_date_aware > timezone.now():
                        
                        messages.error(request, 'Already You have a membership plan ')

                        return redirect('/active_subscription/')
                    else:
                        
                        # tHIS IS WHEN  subscription is expired

                        existing_membership.membership_plan = plan
                        existing_membership.expiration_date = expiration_date
                        existing_membership.subscription_period = subscription_period

                        print(subscription_period)
                        
                        existing_membership.save()
                        messages.error(request, "Congratulations on successfully claiming your membership!")
                        return redirect('home')
                else:

                    # This is for when the expirations_date is not valid

                    return render(request, 'subscribe_error.html', {'error_message': 'Expiration date is missing'})
            else:
                # This is for is user member ship is does't exitst then create a new one
                data = UserMembership(user = request.user, membership_plan = plan, expiration_date = expiration_date, subscription_period = subscription_period)
                data.save()

                redirect("/active_subscription/")

    return redirect('/')


def checkout_success(request):
    return render(request, 'checkout_success.html')
  

def newsLetter(request):
    if request.method == 'POST':
        email = request.POST.get("email")

        exists_email = Newsletter_users.objects.filter(email = email).first()
        if(not exists_email):
            data = Newsletter_users(email = email)
            data.save()
            messages.error(request, 'Success Saved Your Email')
            return redirect('/')
        else:
            messages.error(request, 'Your Email is Alrady Stored')
            return redirect('/')
        

def contactUs(request):
    if(request.method == 'GET'):
        return render(request, 'contact.html') 

    if(request.method == 'POST'):

        f_name = request.POST.get('f_name')
        l_name = request.POST.get('l_name')
        email = request.POST.get('email')
        question = request.POST.get('question')
        phone = request.POST.get('phone')
        w_phone = request.POST.get('w_phone')
        way = request.POST.get('way')

        email_exists = our_clients.objects.filter(email = email).first()
        if(email_exists):
            if(question != email_exists.question):
                data = our_clients(first_name = f_name, last_name = l_name, email = email, phone_number = phone, whatsapp_number = w_phone, question = question, way_to_contact = way)
                messages.error(request, "Your query successfully saved.")
                data.save()
        else:
            data = our_clients(first_name = f_name, last_name = l_name, email = email, phone_number = phone, whatsapp_number = w_phone, question = question, way_to_contact = way)
            messages.error(request, "Your query successfully saved.")

            data.save()

    return redirect("/")




def aboutus(request):
    return render(request, 'about.html')

def terms(request):
    return render(request, 'terms_conditions.html')

def privacy(request):
    return render(request, 'privacy.html')

def questions(request):
    return render(request, 'questions.html')




def allblogs(request):

    allblogs = Blog.objects.all()

    context = {
        "blogs" : allblogs
    }

    return render(request, 'allpost.html', context)


def allplans(request):

    allplans = MembershipPlan.objects.exclude(name = "Free_Trial").all()
    context = {
        "plans" : allplans
    }

    return render(request, 'allPlans.html', context)


def singleblogs(request, id):

    exists_blog = Blog.objects.filter(id = id).first()
    
    if(exists_blog):

        context = {
            "blog" : exists_blog
        }

        return render(request, 'singlepost.html', context)
    return redirect("/allposts/")


def clime_free_trile(request, id):

    user_exists = User.objects.filter(id = id).first()


    if(user_exists):

        today = timezone.now()

        # Make the user's join date aware
        expiration_date_aware = make_aware(datetime.combine(user_exists.date_joined, datetime.min.time()))

        # Calculate the difference between today and the user's join date
        time_difference = today - expiration_date_aware

        # Check if the difference is less than or equal to 14 days
        if time_difference <= timedelta(days=14):

            check_subscription = UserMembership.objects.filter(user = request.user).first()

            if(not check_subscription):
                
                membership_plan = MembershipPlan.objects.filter(name = "Free_Trial").first()

                data = UserMembership(user = request.user, membership_plan = membership_plan, subscription_period = "monthly")

                expiration_date = timezone.now() + timezone.timedelta(days=14)

                data.expiration_date = expiration_date

                data.save()

                save_user = free_triel_users(user = request.user)
                save_user.save()

                messages.error(request, "Congratulations on successfully claiming your membership!")
            else:
                return HttpResponse("Your Free Triel is On Going")
        else:

            user_exists = free_triel_users.objects.filter(user = request.user).first()
            if(user_exists):
                user_exists.delete()
            
            return HttpResponse("You Already enjoied your free trial")
        
    return redirect('home')



def otpvarification(request):
        if request.method == 'POST':

            first=request.POST.get("first")
            second=request.POST.get("second")
            third=request.POST.get("thired")
            fourth=request.POST.get("forth")
            fifth=request.POST.get("fifth")
            sixth=request.POST.get("sixth")

            print(f"This is the opt {generateOTP}")


            concatenated_string = f"{first}{second}{third}{fourth}{fifth}{sixth}"

            otp = int(concatenated_string)

            if(generateOTP == int(otp)):

                # Here save the user
                user.save()
            
                login(request, user)

                send_sub_otp(user.email, user.username)

                return redirect('home')
            
            else:
                messages.error(request,"OTP not correct")
        return render(request, "otp.html")


