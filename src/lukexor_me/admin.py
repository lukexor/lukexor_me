from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from lukexor_me.models import Article, Category, Comment, CustomUser, Project, Tag
from lukexor_me.forms import CustomUserChangeForm, CustomUserCreationForm


class CommentsInline(admin.TabularInline):
    model = Article.comments.through


@admin.register(Category)
class Category(admin.ModelAdmin):
    fields = ('name',)
    list_display = ('name', 'created')
    search_fields = ('name',)


@admin.register(Comment)
class Comment(admin.ModelAdmin):
    fields = ('user', 'body')
    list_display = ('user', 'body', 'created')
    list_filter = ('user__last_name', 'created')
    search_fields = ('user', 'body')
    ordering = ('user',)
    date_hierarchy = 'created'

@admin.register(CustomUser)
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
            'fields': ('first_name', 'last_name'),
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser',
                       'groups', 'user_permissions'),
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined'),
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_superuser')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    date_hierarchy = 'date_joined'

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': (('title', 'permalink_title'), ('author', 'time_to_read'), 'body',),
        }),
        ('Labels', {
            'fields': ('category', 'tags', 'comments')
        }),
    )
    inlines = [
        # CommentsInline,
    ]
    formfield_overrides = {
    #    models.TextField: {'widget': RichTextEditorWidget},
    }
    list_display = ('title', 'author', 'time_to_read', 'created')
    list_filter = ('author__last_name', 'category', 'time_to_read', 'created',)
    search_fields = ('title', 'author__first_name', 'author__last_name', 'category__name', 'articletag__tag__name')
    ordering = ('title',)
    date_hierarchy = 'created'


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': (('title', 'permalink_title'),
                       ('role', 'client'), 'description',
                       ('date_started', 'date_completed')
             ),
        }),
    )
    list_display = ('title', 'role', 'client', 'date_completed')
    list_filter = ('role', 'client', 'date_completed')
    search_fields = ('title', 'role', 'client')
    ordering = ('title',)
    date_hierarchy = 'date_started'


@admin.register(Tag)
class Tag(admin.ModelAdmin):
    fields = ('name',)
    list_display = ('name', 'created')
    search_fields = ('name',)
