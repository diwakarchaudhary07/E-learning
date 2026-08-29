from django.contrib import admin

from .models import AboutUs, ContactMessage, Course, CustomUser, LiveClass, LiveClassResource, OtpVerification


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'username', 'email', 'mobile_no', 'gender', 'dob', 'is_staff')
    search_fields = ('full_name', 'username', 'email', 'mobile_no')
    list_filter = ('is_staff', 'is_active', 'gender')
    fieldsets = (
        ('Account', {'fields': ('username', 'email', 'password')}),
        ('Profile', {'fields': ('full_name', 'mobile_no', 'dob', 'gender', 'profile_image', 'address', 'alternate_mobile_no')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    list_filter = ('created_at',)
    readonly_fields = ('created_at',)


@admin.register(OtpVerification)
class OtpVerificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'otp_code', 'created_at', 'expires_at', 'is_used')
    readonly_fields = ('created_at', 'expires_at')
    search_fields = ('user__username', 'user__email', 'otp_code')


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'instructor', 'price', 'discount_price', 'language', 'created_at')
    search_fields = ('title', 'category', 'instructor', 'description', 'language')
    list_filter = ('category', 'language', 'created_at')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('-created_at',)


@admin.register(AboutUs)
class AboutUsAdmin(admin.ModelAdmin):
    list_display = ('title', 'subtitle', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)
    search_fields = ('title', 'subtitle', 'overview', 'mission', 'vision', 'values')


@admin.register(LiveClass)
class LiveClassAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'instructor_name', 'class_date', 'class_time', 'status', 'student_count')
    list_filter = ('status', 'subject', 'class_date')
    search_fields = ('title', 'subject', 'instructor_name', 'course_name')
    ordering = ('-class_date', '-class_time')


@admin.register(LiveClassResource)
class LiveClassResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'live_class', 'resource_type')
    list_filter = ('resource_type',)
    search_fields = ('title', 'live_class__title')
