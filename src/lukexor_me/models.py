from django.db import models
from django.utils import timezone
from django.utils.http import urlquote
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from . import settings


class Article(models.Model):
    article_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    permalink_title = models.CharField(max_length=45, unique=True)
    summary = models.CharField(max_length=255)
    body = models.TextField()
    authors = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                     related_name='articles',
                                     related_query_name='article',
                                     db_table='article_author')
    category = models.ForeignKey('Category',
                                 related_name='articles',
                                 related_query_name='article')
    tags = models.ManyToManyField('Tag',
                                  related_name='articles',
                                  related_query_name='article',
                                  db_table='article_tag',
                                  blank=True)
    minutes_to_read = models.PositiveIntegerField()
    comments = models.ManyToManyField('Comment',
                                      related_name='comment',
                                      related_query_name='comment',
                                      db_table='article_comment',
                                      blank=True)
    created = models.DateTimeField('date published', default=timezone.now)
    updated = models.DateTimeField(default=timezone.now, auto_now=True)

    class Meta:
        db_table = 'article'
        verbose_name = 'article'
        verbose_name_plural = 'articles'

    def get_authors(self):
        authors = []
        for author in self.authors.all():
            authors.append(author.get_full_name())

        return ", ".join(authors)

    def get_tags(self):
        tags = []
        for tag in self.tags.all():
            tags.append(tag.name)

        return ", ".join(tags)

    def comment_count(self):
        return self.comments.all().count()

    def time_to_read(self):
        return "%d minute read" % (self.minutes_to_read)

    get_authors.short_description = 'Author(s)'
    comment_count.short_description = 'Comments'

    def __unicode__(self):
        return self.title


class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now, auto_now=True)

    class Meta:
        db_table = 'category'
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __unicode__(self):
        return self.name


class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    body = models.TextField()
    created = models.DateTimeField('date posted', default=timezone.now)
    updated = models.DateTimeField(default=timezone.now, auto_now=True)

    class Meta:
        db_table = 'comment'
        verbose_name = 'comment'
        verbose_name_plural = 'comments'

    def __unicode__(self):
        return "%s - %s" % (self.body, self.user)


class CustomUserManager(BaseUserManager):

    def _create_user(self, email, password,
                     is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser, last_login=now,
                          created=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, False, False,
                                 **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True,
                                 **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):

    """
    A fully featured User model with admin-compliant permissions that uses
    a full-length email field as the username.

    Email and password are required. Other fields are optional.
    """
    user_id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=254, unique=True)
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45, blank=True, null=True)
    website = models.CharField(max_length=2083, blank=True, null=True)
    gravatar = models.CharField(max_length=2083, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    is_staff = models.BooleanField('staff status', default=False,
                                   help_text='Designates whether the user can log into this admin '
                                   'site.')
    is_active = models.BooleanField('active', default=True,
                                    help_text='Designates whether this user should be treated as '
                                    'active. Unselect this instead of deleting accounts.')
    created = models.DateTimeField('date added', default=timezone.now)
    updated = models.DateTimeField(default=timezone.now, auto_now=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'user'
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def get_absolute_url(self):
        return "/users/%s/" % urlquote(self.email)

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    def email_user(self, subject, message, from_email=None):
        send_mail(subject, message, from_email, [self.email])

    get_full_name.short_description = 'Full Name'

    def __unicode__(self):
        return self.get_full_name()


class Project(models.Model):
    project_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    permalink_title = models.CharField(max_length=45, unique=True)
    summary = models.CharField(max_length=255)
    description = models.TextField()
    website = models.CharField(max_length=2083, blank=True, null=True)
    roles = models.ManyToManyField('Role',
                                   related_name='roles',
                                   related_query_name='roles',
                                   db_table='project_role')
    clients = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                     related_name='client',
                                     related_query_name='client',
                                     db_table='project_client',
                                     blank=True)
    date_started = models.DateTimeField(blank=True, null=True)
    date_completed = models.DateTimeField(blank=True, null=True)
    created = models.DateTimeField('date added', default=timezone.now)
    updated = models.DateTimeField(default=timezone.now, auto_now=True)

    class Meta:
        db_table = 'project'
        verbose_name = 'project'
        verbose_name_plural = 'projects'

    def get_roles(self):
        roles = []
        for role in self.roles.all():
            roles.append(role.name)

        return ", ".join(roles)

    def get_clients(self):
        clients = []
        for client in self.clients.all():
            clients.append(client.get_full_name())

        if clients:
            return ", ".join(clients)
        else:
            return "N/A"

    get_roles.short_description = 'Role(s)'
    get_clients.short_description = 'Client(s)'

    def __unicode__(self):
        return self.title


class Role(models.Model):
    role_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now, auto_now=True)

    class Meta:
        db_table = 'role'
        verbose_name = 'role'
        verbose_name_plural = 'roles'

    def __unicode__(self):
        return self.name


class Tag(models.Model):
    tag_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now, auto_now=True)

    class Meta:
        db_table = 'tag'
        verbose_name = 'tag'
        verbose_name_plural = 'tags'

    def __unicode__(self):
        return self.name
