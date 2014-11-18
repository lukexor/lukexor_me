from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.db import models as db_models
from tinymce.widgets import TinyMCE
from . import models, forms


class CommentsInline(admin.TabularInline):
    model = models.Article.comments.through


@admin.register(models.Category)
class Category(admin.ModelAdmin):
    fields = ('name',)
    list_display = ('name', 'created')
    search_fields = ('name',)


@admin.register(models.Comment)
class Comment(admin.ModelAdmin):
    fields = ('user', 'body')
    formfield_overrides = {
        db_models.TextField: {'widget': TinyMCE(attrs={'cols': 100, 'rows': 30})},
    }
    list_display = ('user', 'body', 'created')
    list_filter = ('user__first_name', 'user__last_name', 'created')
    search_fields = ('user', 'body')
    ordering = ('user',)
    date_hierarchy = 'created'

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
            'fields': ('first_name', 'last_name', 'website', 'phone', 'note'),
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
    search_fields = ('email', 'first_name', 'last_name', 'website')
    ordering = ('email',)
    date_hierarchy = 'created'

@admin.register(models.Article)
class ArticleAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': (('title', 'permalink_title'), ('authors', 'minutes_to_read'), 'summary', 'body',),
        }),
        ('Labels', {
            'fields': ('category', 'tags', 'comments')
        }),
    )
    inlines = [
        #CommentsInline,
    ]
    formfield_overrides = {
        db_models.TextField: {'widget': TinyMCE(attrs={'cols': 100, 'rows': 30})},
    }
    list_display = ('title', 'get_authors', 'minutes_to_read', 'category', 'comment_count', 'created')
    list_filter = ('authors', 'category', 'tags', 'minutes_to_read', 'created')
    search_fields = ('title', 'authors__first_name', 'authors__last_name', 'category__name', 'tags__name')
    ordering = ('title',)
    date_hierarchy = 'created'


@admin.register(models.Project)
class ProjectAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': (('title', 'permalink_title'),
                       ('roles', 'clients'), 'website', 'summary', 'description',
                       ('date_started', 'date_completed')
             ),
        }),
    )
    formfield_overrides = {
        db_models.TextField: {'widget': TinyMCE(attrs={'cols': 100, 'rows': 30})},
    }
    list_display = ('title', 'website', 'get_roles', 'get_clients', 'date_started', 'date_completed')
    list_filter = ('roles', 'clients', 'date_completed')
    search_fields = ('title', 'website', 'description', 'clients__first_name', 'clients__last_name')
    ordering = ('title',)
    date_hierarchy = 'date_started'


@admin.register(models.Role)
class Role(admin.ModelAdmin):
    fields = ('name',)
    list_display = ('name', 'created')
    search_fields = ('name',)
    ordering = ('name',)
    date_hierarchy = 'created'

@admin.register(models.Tag)
class Tag(admin.ModelAdmin):
    fields = ('name',)
    list_display = ('name', 'created')
    search_fields = ('name',)
    ordering = ('name',)
    date_hierarchy = 'created'
