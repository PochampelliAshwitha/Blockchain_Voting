import os
import csv
from django.core.files import File
from django.conf import settings
from Accounts.models import Voter,Candidate
from django.contrib import auth,messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from random import randint
from django.core.mail import send_mail
from django.db import IntegrityError

def voter(request):
    if request.method == "POST":
        form_type = request.POST.get("form_type")  # Check which form was submitted
        request.session['type_user'] = "voter"
        if form_type == "login":
            username = request.POST.get("username")
            password = request.POST.get("password")
            
            if username and password:
                user = authenticate(username=username, password=password)
                if user is not None:
                    try:
                        voter_profile = user.voter_profile
                    except Voter.DoesNotExist:
                        try:
                            candidate_profile = user.candidate_profile
                            messages.warning(request, "Please use the candidate login.")
                            return redirect("candidate")
                        except Candidate.DoesNotExist:
                            messages.error(request, "Please register first as a voter.")
                            return redirect("voter") 
                    
                    otp = str(randint(100000, 999999))
                    request.session['otp'] = otp

                    # Get user's email
                    try:
                        email = user.email
                        request.session['email_user'] = email  # Store username in session
                        if not email:
                            messages.error(request, "No email found for this user.")
                            return render(request, "Voter.html", {"username": username})

                        # Send the OTP to user's email
                        send_mail(
                            subject="Your OTP for Blockchain Voting System",
                            message=f"Hi {user.username},\n\nYour OTP for login is: {otp}",
                            from_email=settings.EMAIL_HOST_USER,  # Must match your settings.EMAIL_HOST_USER
                            recipient_list=[email],
                            fail_silently=False,
                        )

                        request.session['otp'] = otp
                        request.session['temp_user'] = username  
                        messages.success(request, "OTP sent to your email.")
                        return redirect("validate") 

                    except Exception as e:
                        print("Email error:", e)
                        messages.error(request, "Failed to send OTP.")
                        return render(request, "Voter.html", {"username": username})
                else:
                    messages.error(request, "User doesn't exist. Please register first as a voter.")
            return render(request, "Voter.html", {"username": username})

        elif form_type == "signup":
            username = request.POST.get("username")
            password = request.POST.get("password")
            confirm_password = request.POST.get("confirm_password")
            email = request.POST.get("email")
            first_name = request.POST.get("fname")
            last_name = request.POST.get("lname")
            phone_number = request.POST.get("phone")
            photo = request.FILES.get("photo")  

            if password != confirm_password:
                messages.error(request, "Passwords do not match.")
                return redirect("voter")

            try:
                user = User.objects.create_user(
                    username=username,
                    password=password,
                    email=email,
                    first_name=first_name,
                    last_name=last_name
                )

                Voter.objects.create(
                    user=user,
                    phone_number=phone_number,
                    photo=photo
                )

                # auth.login(request, user)
                messages.success(request, "Signup successful. Welcome, voter!")
                return redirect('voter')

            except IntegrityError:
                messages.error(request, "Username already exists.")
                return render(request, "Voter.html", {
                    "username": username,
                    "email": email
                })

            except Exception as e:
                # Optional: for debugging
                print(f"Signup error: {e}")
                messages.error(request, "An unexpected error occurred. Please try again.")
                return redirect("voter")
    return render(request, "Voter.html")

def mask_email(email):
    name, domain = email.split('@')
    visible = name[:4]
    masked = '*' * (len(name) - len(visible))
    return f"{visible}{masked}@{domain}"

def validate(request):
    if request.session.get("type_user") == "voter":
        session_email = request.session.get("email_user")
        if request.method == "POST":
            otp_entered = request.POST.get("otp")
            username = request.session.get("temp_user")
            session_otp = request.session.get("otp")

            if not username or not otp_entered:
                messages.error(request, "Missing OTP or session expired.")
                return redirect("voter")

            if otp_entered == session_otp:
                try:
                    user = User.objects.get(username=username)
                    auth_login(request, user)

                    # Clean up session
                    request.session.pop("otp", None)
                    request.session.pop("temp_user", None)

                    messages.success(request, "Login successful!")
                    return redirect("dash_voter")  # Your dashboard rout                     e

                except User.DoesNotExist:
                    messages.error(request, "User not found.")
                    return redirect("voter")
            else:
                messages.error(request, "Invalid OTP.")
                return render(request, "validate.html", {"username": username, "Type": "Voter"})
            
        masked_email = mask_email(session_email)
        messages.success(request, f"OTP sent to your email: {masked_email}")
        return render(request, "validate.html", {"Type": "Voter", "email": masked_email})
    else:
        session_email = request.session.get("email_user")
        if request.method == "POST":
            otp_entered = request.POST.get("otp")
            username = request.session.get("temp_user")
            session_otp = request.session.get("otp")

            if not username or not otp_entered:
                messages.error(request, "Missing OTP or session expired.")
                return redirect("voter")

            if otp_entered == session_otp:
                try:
                    user = User.objects.get(username=username)
                    auth_login(request, user)

                    # Clean up session
                    request.session.pop("otp", None)
                    request.session.pop("temp_user", None)

                    messages.success(request, "Login successful!")
                    return redirect("dash_candidate")  # Your dashboard rout                     e

                except User.DoesNotExist:
                    messages.error(request, "User not found.")
                    return redirect("candidate")
            else:
                messages.error(request, "Invalid OTP.")
                return render(request, "validate.html", {"username": username, "Type": "Candidate"})
            
        masked_email = mask_email(session_email)
        messages.success(request, f"OTP sent to your email: {masked_email}")
        return render(request, "validate.html", {"Type": "Voter", "email": masked_email})
    
def candidate(request):
    if request.method == "POST":
        form_type = request.POST.get("form_type")  # Check which form was submitted
        request.session['type_user'] = "candidate"
        
        if form_type == "login":
            username = request.POST.get("username")
            password = request.POST.get("password")
            
            if username and password:
                user = authenticate(username=username, password=password)
                if user is not None:
                    try:
                        candidate_profile = user.candidate_profile
                    except Candidate.DoesNotExist:
                        try:
                            voter_profile= user.voter_profile
                            messages.warning(request, "Please use the Voter login.")
                            return redirect("voter")
                        except Voter.DoesNotExist:
                            messages.error(request, "Please register first as a Candidate.")
                            return redirect("candidate") 
                        
                    otp = str(randint(100000, 999999))
                    request.session['otp'] = otp

                    try:
                        email = user.email
                        request.session['email_user'] = email  # Store username in session
                        if not email:
                            messages.error(request, "No email found for this user.")
                            return render(request, "Voter.html", {"username": username})

                        # Send the OTP to user's email
                        send_mail(
                            subject="Your OTP for Blockchain Voting System",
                            message=f"Hi {user.username},\n\nYour OTP for login is: {otp}",
                            from_email=settings.EMAIL_HOST_USER,  # Must match your settings.EMAIL_HOST_USER
                            recipient_list=["228r1a0571@cmrec.ac.in"],
                            fail_silently=False,
                        )

                        request.session['otp'] = otp
                        request.session['temp_user'] = username  
                        messages.success(request, "OTP sent to your email.")
                        return redirect("validate") 

                    except Exception as e:
                        print("Email error:", e)
                        messages.error(request, "Failed to send OTP.")
                        return render(request, "Voter.html", {"username": username})
                else:
                    messages.error(request, "User doesn't exist.")
            return render(request, "Voter.html", {"username": username})

        elif form_type == "signup":
            username = request.POST.get("username")
            password = request.POST.get("password")
            party = request.POST.get("party")
            confirm_password = request.POST.get("confirm_password")
            email = request.POST.get("email")
            first_name = request.POST.get("fname")
            last_name = request.POST.get("lname")
            manifesto = request.POST.get("manifesto")
            photo = request.FILES.get("photo")  

            if password != confirm_password:
                messages.error(request, "Passwords do not match.")
                return redirect("candidate")
            try:
                user = User.objects.create_user(
                    username=username,
                    password=password,
                    email=email,
                    first_name=first_name,
                    last_name=last_name
                )

                Candidate.objects.create(
                    user=user,
                    party=party,
                    manifesto=manifesto,
                    photo=photo
                )

                auth.login(request, user)
                messages.success(request, "Signup successful. Welcome, Candidate!")
                return redirect('candidate')

            except IntegrityError:
                messages.error(request, "Username already exists.")
                return render(request, "Voter.html", {
                    "username": username,
                    "email": email
                })

            except Exception as e:
                # Optional: for debugging
                print(f"Signup error: {e}")
                messages.error(request, "An unexpected error occurred. Please try again.")
                return redirect("candidate")
    return render(request, "candidate.html")

def election_commission(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        if username and password:
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_superuser:
                    auth_login(request, user)
                    messages.success(request, "Superuser login successful")
                    return redirect('/dashboard/dash_election_commission')  # Redirect to superuser dashboard or another page
                else:
                    messages.warning(request, "Please Login Using Voter Or Candidate Login!!")
                    return redirect('/auth/voter')
            else:
                messages.error(request, "Invalid credentials")
                return render(request, "election_commission.html", {"username": username})
    return render(request, "election_commission.html")

def logout(request):
    auth.logout(request)
    messages.success(request, "Logout successful")
    return redirect("voter")

def candidate_profile(request):   
    return render(request, "candidate_profile.html")  

def voter_profile(request):   
    return render(request, "voter_profile.html") 