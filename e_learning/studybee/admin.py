from django.contrib import admin

from .models import AboutUs, Article, ChatMessage, ContactMessage, Course, CustomUser, LiveClass, LiveClassResource, OtpVerification


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'username', 'email', 'mobile_no', 'gender', 'dob', 'is_staff')
    search_fields = ('full_name', 'username', 'email', 'mobile_no')
    list_filter = ('is_staff', 'is_active', 'gender')
    fieldsets = (
        ('Account', {'fields': ('username', 'email', 'password')}),
        ('Profile', {'fields': ('full_name', 'mobile_no', 'dob', 'gender', 'profile_image', 'address', 'alternate_mobile_no', 'is_email_verified')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    readonly_fields = ('date_joined', 'last_login')


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
    list_filter = ('is_used', 'created_at')


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'instructor', 'price', 'discount_price', 'language', 'created_at')
    search_fields = ('title', 'category', 'instructor', 'description', 'language')
    list_filter = ('category', 'language', 'created_at')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at', 'slug')


@admin.register(AboutUs)
class AboutUsAdmin(admin.ModelAdmin):
    list_display = ('title', 'subtitle', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)
    search_fields = ('title', 'subtitle', 'overview', 'mission', 'vision', 'values')


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author', 'published_at', 'reading_time')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'category', 'author', 'summary')
    list_filter = ('category', 'published_at', 'created_at')
    ordering = ('-published_at', '-created_at')
    readonly_fields = ('published_at', 'created_at', 'updated_at', 'slug')


@admin.register(LiveClass)
class LiveClassAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'instructor_name', 'class_date', 'class_time', 'status', 'student_count')
    list_filter = ('status', 'subject', 'class_date')
    search_fields = ('title', 'subject', 'instructor_name', 'course_name')
    ordering = ('-class_date', '-class_time')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(LiveClassResource)
class LiveClassResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'live_class', 'resource_type', 'created_at')
    list_filter = ('resource_type', 'created_at')
    search_fields = ('title', 'live_class__title')
    readonly_fields = ('created_at',)


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('get_user_name', 'get_message_preview', 'created_at')
    search_fields = ('user__full_name', 'user__email', 'user_message', 'bot_response')
    list_filter = ('created_at',)
    readonly_fields = ('created_at', 'user_message', 'bot_response')
    ordering = ('-created_at',)

    def get_user_name(self, obj):
        return obj.user.full_name if obj.user else 'Guest'
    get_user_name.short_description = 'User'

    def get_message_preview(self, obj):
        preview = obj.user_message[:50]
        return f"{preview}..." if len(obj.user_message) > 50 else preview
    get_message_preview.short_description = 'Message Preview'
