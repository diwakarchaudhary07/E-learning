from datetime import date, timedelta

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import LoginForm, ProfileForm, RegisterForm
from .models import AboutUs, Article, ChatMessage, ContactMessage, Course, CustomUser, LiveClass, OtpVerification


def home(request):
    courses = Course.objects.all().order_by('-created_at')[:6]
    return render(request, 'home.html', {'courses': courses})


def about_view(request):
    about = AboutUs.objects.order_by('-created_at').first()
    return render(request, 'about.html', {'about': about})


def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        subject = request.POST.get('subject', '').strip()
        message = request.POST.get('message', '').strip()
        if name and email and subject and message:
            ContactMessage.objects.create(
                name=name,
                email=email,
                subject=subject,
                message=message,
            )
            return render(request, 'contact.html', {'success': True})

    return render(request, 'contact.html')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            otp_code = OtpVerification.generate_code()
            otp = OtpVerification.objects.create(
                user=user,
                otp_code=otp_code,
                expires_at=timezone.now() + timedelta(minutes=10),
            )
            try:
                send_mail(
                    'Verify your email',
                    f'Your OTP is {otp_code}. It expires in 10 minutes.',
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    fail_silently=False,
                )
            except Exception:
                messages.error(request, 'OTP could not be sent. Please check your SMTP credentials and try again.')
                return redirect('register')

            messages.success(request, 'Account created. Please verify your email with the OTP sent to your inbox.')
            return redirect('verify_otp', user_id=user.id)
    else:
        form = RegisterForm()

    return render(request, 'auth/register.html', {'form': form})


def verify_otp_view(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    otp_obj = OtpVerification.objects.filter(user=user).order_by('-created_at').first()

    if request.method == 'POST':
        otp_code = request.POST.get('otp_code', '').strip()
        if otp_obj and otp_obj.is_valid() and otp_code == otp_obj.otp_code:
            otp_obj.is_used = True
            otp_obj.save()
            user.is_active = True
            user.is_email_verified = True
            user.save()
            login(request, user)
            messages.success(request, 'Email verified successfully. You can now log in.')
            return redirect('home')
        messages.error(request, 'Invalid or expired OTP. Please try again.')

    return render(request, 'auth/verify_otp.html', {'user': user})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if not user.is_email_verified:
                messages.error(request, 'Please verify your email before logging in.')
                return redirect('register')
            login(request, user)
            return redirect('home')
    else:
        form = LoginForm()

    return render(request, 'auth/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required(login_url='login')
def dashboard(request):
    return render(request, 'auth/dashboard.html', {'user': request.user})


def calculate_age(date_of_birth):
    if not date_of_birth:
        return None
    today = date.today()
    return today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))


@login_required(login_url='login')
def profile_view(request):
    user = request.user
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('profile')
    else:
        form = ProfileForm(instance=user)

    return render(request, 'auth/profile.html', {'form': form, 'user': user, 'age': calculate_age(user.dob)})


def course_list_view(request):
    courses = Course.objects.all().order_by('-created_at')
    return render(request, 'courses.html', {'courses': courses})


def live_classes_view(request):
    live_class = (
        LiveClass.objects.filter(status=LiveClass.STATUS_LIVE)
        .order_by('-class_date', '-class_time')
        .first()
    )
    if not live_class:
        live_class = (
            LiveClass.objects.filter(status=LiveClass.STATUS_UPCOMING)
            .order_by('class_date', 'class_time')
            .first()
        )

    upcoming_classes = (
        LiveClass.objects.filter(status=LiveClass.STATUS_UPCOMING)
        .order_by('class_date', 'class_time')[:5]
    )
    recorded_classes = (
        LiveClass.objects.filter(status=LiveClass.STATUS_COMPLETED)
        .order_by('-class_date', '-class_time')[:3]
    )
    return render(request, 'live_classes.html', {
        'live_class': live_class,
        'upcoming_classes': upcoming_classes,
        'recorded_classes': recorded_classes,
    })


def article_list_view(request):
    articles = Article.objects.all().order_by('-published_at', '-created_at')[:6]
    return render(request, 'articles.html', {'articles': articles})


def article_detail_view(request, slug):
    article = get_object_or_404(Article, slug=slug)
    return render(request, 'article_detail.html', {'article': article})


def course_detail_view(request, slug):
    course = get_object_or_404(Course, slug=slug)
    return render(request, 'course_detail.html', {'course': course})


def get_ai_response(message: str) -> str:
    text = message.strip().lower()
    if not text:
        return 'Please type a question so I can help.'

    if 'hello' in text or 'hi' in text or 'hey' in text:
        return 'Hi there! I am your AI assistant. Ask me anything about our courses, live classes, or how to navigate the site.'

    if 'course' in text or 'study' in text or 'class' in text:
        course_titles = list(Course.objects.values_list('title', flat=True)[:8])
        if course_titles:
            suggestions = ', '.join(course_titles[:4])
            return (
                'I can help you with our course catalog. Here are some popular courses: ' 
                f'{suggestions}. Ask me for details about any of these or a topic you want to learn.'
            )
        return 'I can help you find available courses and live classes. Tell me which subject or program you want to study.'

    if 'live' in text or 'schedule' in text or 'enroll' in text:
        return 'Our live classes are available in the Live Classes section. Ask me for schedule details or how to enroll.'

    if 'price' in text or 'fee' in text or 'cost' in text or 'discount' in text:
        return 'Course pricing depends on the program. Visit a course detail page for exact pricing and discount information.'

    if 'login' in text or 'register' in text or 'account' in text:
        return 'You can register from the Register page and log in using your email. Once logged in, go to Dashboard for personalized content.'

    if 'contact' in text or 'help' in text or 'support' in text:
        return 'For support, use the Contact page or ask me about specific site features like courses, live classes, or registration.'

    if 'where' in text or 'how' in text:
        return 'Ask me about courses, live classes, pricing, registration, or which page you want to visit.'

    return 'I’m here to help. Please ask me about courses, live classes, schedules, registration, or how to navigate the site.'


def ai_chat_view(request):
    return render(request, 'ai_chat.html')


def ai_chat_send(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method.'}, status=400)

    message = request.POST.get('message', '').strip()
    if not message:
        return JsonResponse({'error': 'Please enter a message.'}, status=400)

    response_text = get_ai_response(message)
    ChatMessage.objects.create(
        user=request.user if request.user.is_authenticated else None,
        user_message=message,
        bot_response=response_text,
    )
    return JsonResponse({'reply': response_text})
