from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.db import models as db_models
from django.conf import settings
from django.forms import Textarea
from . import models, forms
from lib import cache
import re, math


class CommentsInline(admin.TabularInline):
    model = models.Comment
    extra = 1
    verbose_name = 'Comment'
    verbose_name_plural = 'Comments'

    fieldsets = (
        (None, {
            'fields': ('user', 'body')
        }),
    )


@admin.register(models.Category)
class Category(admin.ModelAdmin):
    fields = ('name',)
    list_display = ('name', 'created')
    search_fields = ('name',)


@admin.register(models.Comment)
class Comment(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('user', ('article', 'project'), 'body'),
        }),
        ('Date Information', {
            'classes': ('collapse',),
            'fields': ('created', 'updated'),
        })
    )
    readonly_fields = ('created', 'updated')
    formfield_overrides = {
        db_models.TextField: {'widget': Textarea(attrs={'cols': 180, 'rows': 60})},
    }
    list_display = ('user', 'article', 'project', 'body', 'created')
    list_filter = ('project', 'created',)
    search_fields = ('user', 'article', 'project', 'body')
    ordering = ('user','created')
    # date_hierarchy = 'created'

@admin.register(models.CustomUser)
class CustomUserAdmin(UserAdmin):
    # The forms to add and change user instances

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference the removed 'username' field
    fieldsets = (
        (None, {
            'fields': ('email', 'password'),
        }),
        ('Personal info', {
            'fields': ('full_name', 'preferred_name', 'website', 'gravatar', 'phone', 'note'),
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser',
                       'groups', 'user_permissions'),
        }),
        ('Important dates', {
            'fields': ('last_login', 'created'),
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    form = forms.CustomUserChangeForm
    add_form = forms.CustomUserCreationForm
    list_display = ('email', 'get_full_name', 'website', 'phone', 'is_staff', 'is_superuser', 'is_active')
    search_fields = ('email', 'full_name', 'preferred_name', 'website')
    ordering = ('email',)
    # date_hierarchy = 'created'

@admin.register(models.Article)
class ArticleAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': (('title', 'permalink_title'), 'minutes_to_read', 'category', 'tags', 'body',),
        }),
        ('Publish', {
            'fields': ('date_published',)
        }),
        ('Date Information', {
            'classes': ('collapse',),
            'fields': ('created', 'updated')
        })
    )
    inlines = [
        CommentsInline,
    ]
    readonly_fields = ('updated', 'minutes_to_read')
    formfield_overrides = {
        db_models.TextField: {'widget': Textarea(attrs={'cols': 180, 'rows': 60})},
    }
    list_display = ('title', 'author', 'minutes_to_read', 'category', 'comment_count', 'created')
    list_filter = ('author', 'date_published', 'category', 'tags', 'minutes_to_read')
    search_fields = ('title', 'author__full_name', 'category__name', 'tags__name')
    ordering = ('-created',)
    # date_hierarchy = 'created'

    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user

        word_separator = re.compile('[ ]')
        words = word_separator.split(obj.body)

        obj.minutes_to_read = math.ceil(len(words) / settings.AVG_WPM_READING_SPEED)

        cache.expire_view_cache("articles")
        cache.expire_view_cache("permalink", obj.permalink_title)

        obj.save()


@admin.register(models.Project)
class ProjectAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': (('title', 'permalink_title'),
                       'website', 'tags', 'body',
                       ('date_started', 'date_completed')
             ),
        }),
        ('Publish', {
            'fields': ('date_published',)
        }),
        ('Date Information', {
            'classes': ('collapse',),
            'fields': ('created', 'updated'),
        })
    )
    readonly_fields = ('updated',)
    formfield_overrides = {
        db_models.TextField: {'widget': Textarea(attrs={'cols': 180, 'rows': 60})},
    }
    list_display = ('title', 'website', 'get_roles', 'client', 'date_started', 'date_completed')
    list_filter = ('roles', 'client', 'date_published', 'date_completed')
    search_fields = ('title', 'website', 'description', 'client__full_name')
    ordering = ('title',)
    # date_hierarchy = 'date_started'

    def save_model(self, request, obj, form, change):
        cache.expire_view_cache("projects")
        cache.expire_view_cache("permalink", obj.permalink_title)

        obj.save()


@admin.register(models.Role)
class Role(admin.ModelAdmin):
    fields = ('name',)
    list_display = ('name', 'created')
    search_fields = ('name',)
    ordering = ('name',)
    # date_hierarchy = 'created'

@admin.register(models.Tag)
class Tag(admin.ModelAdmin):
    fields = ('name',)
    list_display = ('name', 'created')
    search_fields = ('name',)
    ordering = ('name',)
    # date_hierarchy = 'created'
