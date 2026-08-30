import random
import string

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.text import slugify


class CustomUser(AbstractUser):
    full_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    mobile_no = models.CharField(max_length=15, blank=True)
    dob = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=255, blank=True)
    alternate_mobile_no = models.CharField(max_length=15, blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True)
    is_email_verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'full_name']

    def __str__(self):
        return self.full_name or self.username


class OtpVerification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='otps')
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def is_valid(self):
        return not self.is_used and timezone.now() < self.expires_at

    @staticmethod
    def generate_code():
        return ''.join(random.choices(string.digits, k=6))

    def __str__(self):
        return f'{self.user} - {self.otp_code}'


class ContactMessage(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    subject = models.CharField(max_length=180)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Contact Message'
        verbose_name_plural = 'Contact Messages'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.subject}"


class AboutUs(models.Model):
    title = models.CharField(max_length=100, default='About Us')
    subtitle = models.CharField(max_length=180, blank=True, default='Learn who we are and why we exist')
    overview = models.TextField(blank=True, default='We are a learning platform committed to helping students and professionals grow through high-quality courses, mentorship, and community support.')
    mission = models.TextField(blank=True, default='To empower every learner with access to practical skills and guidance so they can achieve their goals confidently.')
    vision = models.TextField(blank=True, default='To become the trusted destination for career-ready education and lifelong growth.')
    values = models.TextField(blank=True, default='Integrity, excellence, student-first service, and continuous innovation.')
    banner_image = models.ImageField(upload_to='about_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'About Us Content'
        verbose_name_plural = 'About Us Content'

    def __str__(self):
        return self.title


class Course(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True)
    category = models.CharField(max_length=120)
    instructor = models.CharField(max_length=150)
    description = models.TextField()
    price = models.PositiveIntegerField(default=0)
    discount_price = models.PositiveIntegerField(default=0)
    language = models.CharField(max_length=80, default='English')
    duration = models.CharField(max_length=80)
    total_lessons = models.PositiveIntegerField(default=0)
    total_quizzes = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class LiveClass(models.Model):
    STATUS_UPCOMING = 'upcoming'
    STATUS_LIVE = 'live'
    STATUS_COMPLETED = 'completed'
    STATUS_CHOICES = [
        (STATUS_UPCOMING, 'Upcoming'),
        (STATUS_LIVE, 'Live'),
        (STATUS_COMPLETED, 'Completed'),
    ]

    title = models.CharField(max_length=180, default='Python Programming - Functions')
    subject = models.CharField(max_length=150, default='Python')
    course_name = models.CharField(max_length=200, default='Python Programming')
    instructor_name = models.CharField(max_length=150, default='Rahul Sharma')
    instructor_profile = models.CharField(max_length=180, blank=True, default='Senior Python Trainer')
    class_date = models.DateField(default=timezone.now)
    class_time = models.TimeField(default='10:00:00')
    duration_minutes = models.PositiveIntegerField(default=60)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_UPCOMING)
    student_count = models.PositiveIntegerField(default=125)
    live_indicator = models.BooleanField(default=False)
    description = models.TextField(blank=True, default='Interactive live class with hands-on coding exercises and Q&A.')
    join_link = models.URLField(blank=True, default='https://example.com/live-class')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-class_date', '-class_time']
        verbose_name = 'Live Class'
        verbose_name_plural = 'Live Classes'

    def __str__(self):
        return f'{self.subject} - {self.title}'

    @property
    def formatted_time(self):
        return self.class_time.strftime('%I:%M %p')


class LiveClassResource(models.Model):
    live_class = models.ForeignKey(LiveClass, on_delete=models.CASCADE, related_name='resources')
    title = models.CharField(max_length=180)
    resource_type = models.CharField(max_length=80, default='PDF')
    file_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'{self.live_class.title} - {self.title}'


class Article(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True)
    category = models.CharField(max_length=80, default='Learning')
    summary = models.TextField(max_length=300)
    content = models.TextField(blank=True)
    author = models.CharField(max_length=120, default='StudyBee Team')
    reading_time = models.CharField(max_length=30, default='5 min read')
    published_at = models.DateField(auto_now_add=True)
    image = models.ImageField(upload_to='articles/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-published_at', '-created_at']
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class ChatMessage(models.Model):
    user = models.ForeignKey(
        CustomUser,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='chat_messages',
    )
    user_message = models.TextField()
    bot_response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Chat Message'
        verbose_name_plural = 'Chat Messages'
        ordering = ['created_at']

    def __str__(self):
        author = self.user.full_name if self.user else 'Guest'
        return f'{author}: {self.user_message[:40]}'
