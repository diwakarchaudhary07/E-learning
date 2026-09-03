from unittest.mock import patch

from django.conf import settings
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.urls import reverse

from .models import Course, CustomUser, LiveClass, OtpVerification


class CustomUserModelTests(TestCase):
    def test_create_user_with_custom_fields(self):
        User = get_user_model()

        user = User.objects.create_user(
            username='johndoe',
            email='johndoe@example.com',
            password='testpass123',
            full_name='John Doe',
            mobile_no='9876543210',
            dob='1990-01-01',
            address='123 Main Street',
            alternate_mobile_no='9876543211',
            gender='M',
        )

        self.assertEqual(user.full_name, 'John Doe')
        self.assertEqual(user.email, 'johndoe@example.com')
        self.assertEqual(user.mobile_no, '9876543210')
        self.assertEqual(user.address, '123 Main Street')
        self.assertEqual(user.gender, 'M')
        self.assertTrue(user.check_password('testpass123'))


class CourseModelTests(TestCase):
    def test_create_course_with_required_fields(self):
        course = Course.objects.create(
            title='Django Masterclass',
            slug='django-masterclass',
            category='Web Development',
            instructor='John Doe',
            description='Learn Django from scratch.',
            price=199,
            discount_price=149,
            language='English',
            duration='8 weeks',
            total_lessons=24,
            total_quizzes=8,
        )

        self.assertEqual(course.title, 'Django Masterclass')
        self.assertEqual(course.slug, 'django-masterclass')
        self.assertEqual(course.category, 'Web Development')
        self.assertEqual(course.discount_price, 149)
        self.assertEqual(course.total_lessons, 24)
        self.assertEqual(str(course), 'Django Masterclass')


class EmailOtpRegistrationTests(TestCase):
    def test_register_creates_unverified_user_and_otp(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'full_name': 'New User',
            'email': 'newuser@example.com',
            'mobile_no': '9876543210',
            'password1': 'StrongPass123',
            'password2': 'StrongPass123',
        })

        self.assertEqual(response.status_code, 302)
        self.assertIn('verify-otp', response.url)
        user = CustomUser.objects.get(username='newuser')
        self.assertFalse(user.is_active)
        self.assertFalse(user.is_email_verified)
        self.assertTrue(OtpVerification.objects.filter(user=user).exists())

    @patch('studybee.views.send_mail')
    def test_register_uses_real_smtp_settings_without_silencing_failures(self, mock_send_mail):
        with self.settings(EMAIL_HOST_USER='actual-user@gmail.com', EMAIL_HOST_PASSWORD='actual-app-password'):
            response = self.client.post(reverse('register'), {
                'username': 'smtpuser',
                'full_name': 'SMTP User',
                'email': 'smtpuser@example.com',
                'mobile_no': '9876543210',
                'password1': 'StrongPass123',
                'password2': 'StrongPass123',
            })

            self.assertEqual(response.status_code, 302)
            mock_send_mail.assert_called_once()
            self.assertFalse(mock_send_mail.call_args.kwargs.get('fail_silently', False))
            self.assertEqual(mock_send_mail.call_args.args[2], settings.DEFAULT_FROM_EMAIL)

    @patch('studybee.views.send_mail')
    def test_login_sends_otp_before_authenticating(self, mock_send_mail):
        user = CustomUser.objects.create_user(
            username='loginuser',
            email='loginuser@example.com',
            password='StrongPass123',
            full_name='Login User',
            is_active=True,
            is_email_verified=True,
        )

        response = self.client.post(reverse('login'), {
            'username': user.email,
            'password': 'StrongPass123',
        })

        self.assertRedirects(response, reverse('verify_otp', args=[user.id]))
        mock_send_mail.assert_called_once()
        self.assertTrue(any(
            'A login OTP has been sent' in str(message)
            for message in get_messages(response.wsgi_request)
        ))
        self.assertTrue(OtpVerification.objects.filter(user=user, is_used=False).exists())
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    @patch('studybee.views.send_mail')
    def test_login_otp_authenticates_user_after_verification(self, mock_send_mail):
        user = CustomUser.objects.create_user(
            username='verifylogin',
            email='verifylogin@example.com',
            password='StrongPass123',
            full_name='Verify Login',
            is_active=True,
            is_email_verified=True,
        )

        self.client.post(reverse('login'), {
            'username': user.email,
            'password': 'StrongPass123',
        })
        otp = OtpVerification.objects.get(user=user)

        response = self.client.post(reverse('verify_otp', args=[user.id]), {'otp_code': otp.otp_code})

        self.assertRedirects(response, reverse('home'))
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        otp.refresh_from_db()
        self.assertTrue(otp.is_used)


class ProfilePageTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='profileuser',
            email='profile@example.com',
            password='StrongPass123',
            full_name='Jane Doe',
            mobile_no='9876543210',
            dob='1998-03-15',
            gender='Female',
        )
        self.client.force_login(self.user)

    def test_profile_page_shows_user_details(self):
        response = self.client.get(reverse('profile'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Jane Doe')
        self.assertContains(response, 'profile@example.com')
        self.assertContains(response, 'Female')
        self.assertContains(response, 'Edit Profile')

    def test_profile_page_updates_user_details(self):
        response = self.client.post(reverse('profile'), {
            'full_name': 'Jane Smith',
            'email': 'jane@example.com',
            'mobile_no': '1111111111',
            'dob': '1999-06-20',
            'gender': 'Female',
        })

        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertEqual(self.user.full_name, 'Jane Smith')
        self.assertEqual(self.user.email, 'jane@example.com')
        self.assertEqual(self.user.mobile_no, '1111111111')


class LiveClassPageTests(TestCase):
    def test_live_classes_page_loads(self):
        response = self.client.get(reverse('live_classes'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Live Class')
        self.assertContains(response, 'Upcoming Live Classes')

    def test_live_classes_page_uses_database_records(self):
        live_class = LiveClass.objects.create(
            title='Django API Fundamentals',
            subject='Django',
            course_name='Backend Development',
            instructor_name='Amit Kumar',
            instructor_profile='Senior Backend Mentor',
            class_date='2026-08-30',
            class_time='10:00:00',
            duration_minutes=90,
            status=LiveClass.STATUS_LIVE,
            student_count=86,
            live_indicator=True,
            description='Learn APIs and clean backend patterns.',
            join_link='https://example.com/django-live'
        )

        response = self.client.get(reverse('live_classes'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Django API Fundamentals')
        self.assertContains(response, 'Amit Kumar')
        self.assertContains(response, 'Backend Development')
        self.assertContains(response, 'LIVE')


class ArticlePageTests(TestCase):
    def test_articles_page_loads(self):
        response = self.client.get(reverse('articles'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Articles')
        self.assertContains(response, 'Latest Insights')
