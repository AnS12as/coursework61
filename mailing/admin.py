from django.contrib import admin
from django.db import models
from .models import Client, Message, Mailing, MailingAttempt, BlogPost


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('email', 'full_name', 'comment')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('subject',)


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('start_datetime', 'periodicity', 'status', 'message')
    filter_horizontal = ('clients',)


@admin.register(MailingAttempt)
class MailingAttemptAdmin(admin.ModelAdmin):
    list_display = ('mailing', 'attempt_datetime', 'status', 'server_response')


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_date', 'views')
    formfield_overrides = {
        models.ImageField: {'widget': admin.widgets.AdminFileWidget},
    }
