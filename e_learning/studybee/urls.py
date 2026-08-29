from django.urls import path

from .views import (about_view, ai_chat_send, ai_chat_view, contact_view,
                    course_detail_view, course_list_view, dashboard, home,
                    live_classes_view, login_view, logout_view, profile_view,
                    register_view, verify_otp_view)

urlpatterns = [
    path('', home, name='home'),
    path('about/', about_view, name='about'),
    path('contact/', contact_view, name='contact'),
    path('courses/', course_list_view, name='courses'),
    path('courses/<slug:slug>/', course_detail_view, name='course_detail'),
    path('live-classes/', live_classes_view, name='live_classes'),
    path('ai-chat/', ai_chat_view, name='ai_chat'),
    path('ai-chat/send/', ai_chat_send, name='ai_chat_send'),
    path('register/', register_view, name='register'),
    path('verify-otp/<int:user_id>/', verify_otp_view, name='verify_otp'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    path('profile/', profile_view, name='profile'),
]
