from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.html import strip_tags
from django.utils.http import urlquote
from django.utils import timezone
from lukexor_me import settings
import re, markdown_deux, logging

logger = logging.getLogger(__name__)

# Global helpers
def summary_text(text, length=40):
    html_text = markdown_deux.markdown(text, "trusted")
    stripped_text = strip_tags(html_text).strip()

    word_separator = re.compile('[ ]')
    words = word_separator.split(stripped_text)

    if len(words) > length:
        shortened_text = "%s ..." % (' '.join(words[0:length]))
    else:
        shortened_text = ' '.join(words)

    return shortened_text

class Article(models.Model):
    article_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, unique=True)
    permalink_title = models.CharField(max_length=45, unique=True)
    body = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    category = models.ForeignKey('Category', default=1)
    tags = models.ManyToManyField('Tag', blank=True)
    minutes_to_read = models.PositiveIntegerField(default=0)
    date_published = models.DateTimeField(blank=True, null=True)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now, auto_now=True)

    def comment_count(self):
        return self.comment_set.all().count()
    comment_count.short_description = 'Comments'

    def get_absolute_url(self):
        year = None
        month = None

        if self.date_published:
            year = self.date_published.strftime('%Y')
            month = self.date_published.strftime('%m')

        if year and month:
            return reverse('article_permalink', args=[year, month, self.permalink_title])
        else:
            return ''

    def get_tags(self):
        tags = []
        for tag in self.tags.all():
            tags.append(tag.name)

        return ", ".join(tags)
    get_tags.short_description = 'Tag(s)'

    def summary(self):
        return summary_text(self.body, 40)

    def time_to_read(self):
        return "%d minute read" % (self.minutes_to_read)

    def __unicode__(self):
        return self.title


class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45, unique=True)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now, auto_now=True)

    class Meta:
        verbose_name_plural = 'categories'

    def __unicode__(self):
        return self.name

class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    article = models.ForeignKey('Article', blank=True, null=True)
    project = models.ForeignKey('Project', blank=True, null=True)
    body = models.TextField()
    created = models.DateTimeField('date posted', default=timezone.now)
    updated = models.DateTimeField(default=timezone.now, auto_now=True)

    def __unicode__(self):
        return "%s - %s" % (strip_tags(self.body), self.user.get_full_name())


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
    full_name = models.CharField(max_length=255)
    preferred_name = models.CharField(max_length=90, blank=True, null=True)
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
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def get_absolute_url(self):
        return "/users/%s/" % urlquote(self.email)

    def get_full_name(self):
        full_name = "%s" % (self.full_name)
        return full_name.strip()
    get_full_name.short_description = 'Full Name'

    def get_short_name(self):
        preferred_name = "%s" % (self.preferred_name)
        return preferred_name.strip()
    get_short_name.short_description = 'Preferred Name'

    def email_user(self, subject, message, from_email=None):
        send_mail(subject, message, from_email, [self.email])

    def __unicode__(self):
        return self.get_full_name()


class Project(models.Model):
    project_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, unique=True)
    permalink_title = models.CharField(max_length=45, unique=True)
    body = models.TextField()
    website = models.CharField(max_length=2083, blank=True, null=True)
    roles = models.ManyToManyField('Role')
    client = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)
    tags = models.ManyToManyField('Tag', blank=True)
    date_started = models.DateTimeField(blank=True, null=True)
    date_completed = models.DateTimeField(blank=True, null=True)
    date_published = models.DateTimeField(blank=True, null=True)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now, auto_now=True)

    def get_absolute_url(self):
        year = None
        month = None

        if self.date_published:
            year = self.date_published.strftime('%Y')
            month = self.date_published.strftime('%m')

        if year and month:
            return reverse('project_permalink', args=[year, month, self.permalink_title])
        else:
            return ''

    def comment_count(self):
        return self.comment_set.all().count()
    comment_count.short_description = 'Comments'

    def get_roles(self):
        roles = []
        for role in self.roles.all():
            roles.append(role.name)

        return ", ".join(roles)
    get_roles.short_description = 'Role(s)'

    def get_tags(self):
        tags = []
        for tag in self.tags.all():
            tags.append(tag.name)

        return ", ".join(tags)
    get_tags.short_description = 'Tag(s)'

    def summary(self):
        return summary_text(self.body, 40)

    def __unicode__(self):
        return self.title


class Role(models.Model):
    role_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45, unique=True)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now, auto_now=True)

    def __unicode__(self):
        return self.name


class Tag(models.Model):
    tag_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45, unique=True)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now, auto_now=True)

    def __unicode__(self):
        return self.name
