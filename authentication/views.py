from django.shortcuts import render, redirect
from django.views import View
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from .utils import token_generator 
import json


class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']
        if not validate_email(email):
            return JsonResponse({'email_error': 'Please provide a valid email address.'}, status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error': 'Sorry this email is already in use.'}, status=409)
        return JsonResponse({'username_valid': True})

    
class UserNameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']
        if not str(username).isalnum():
            return JsonResponse({'username_error': 'username should only contain alphanumeric characters'}, status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error': 'sorry username in use,choose another one '}, status=409)
        return JsonResponse({'email_valid': True})

class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/registration.html')
    
    def post(self, request):
        # GET USER DATA
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        
        context = {
            'field_values': request.POST
        }
        
        # VALIDATE USER DATA
        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password) < 8:
                    messages.error(request, 'Your password must be atleast 8 characters long.')
                    return render(request, 'authentication/registration.html', context)
                user = User.objects.create_user(username=username, email=email)
                user.set_password(password)
                user.is_active = False
                user.save()
                email_subject = 'Account Activation'
                #### Create a link for email verification ####
                domain = get_current_site(request).domain
                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                token = token_generator.make_token(user)
                link = reverse('activate', kwargs={'uidb64': uidb64, 'token': token})
                # 1. create path_to_view class/function
                email_body = f'Hi {user.username}, Please use the included link to verify your account. \n http://{domain}{link}'
                email_sender = 'noreply@semicolo.com'
                email = EmailMessage(
                    email_subject,
                    email_body,
                    "from@example.com",
                    [email],
                )
                email.send(fail_silently=False)
                messages.success(request, 'Account Created Successfully!')
                return render(request, 'authentication/registration.html')      
        # messages.warning(request, 'Warning: !')
        # messages.info(request, 'Info: !')
        # messages.error(request, 'Error: !')
        
        return render(request, 'authentication/registration.html')

class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)
            
            if not token_generator.check_token(user, token):
                return redirect('login'+'?message='+'User already activated')
            if user.is_active:
                return redirect('login')
            
            user.is_active = True
            user.save()
            messages.success(request, f'Congratulations, {user.username} account has been actived successfully')
            return redirect('login')
        except Exception as e:
            pass
        return redirect('login')
    
    
class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')