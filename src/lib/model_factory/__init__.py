import django
django.setup()

from lukexor_me import models


def create_article(**kwargs):
    return models.Article.objects.update_or_create(**kwargs)


def add_article_tag(**kwargs):
    return kwargs['article'].tags.add(kwargs['tag'])


def create_author(**kwargs):
    return models.CustomUser.objects.update_or_create(**kwargs)


def create_category(**kwargs):
    return models.Category.objects.update_or_create(**kwargs)


def create_project(**kwargs):
    return models.Project.objects.update_or_create(**kwargs)


def add_project_role(**kwargs):
    return kwargs['project'].roles.add(kwargs['role'])


def add_project_tag(**kwargs):
    return kwargs['project'].tags.add(kwargs['tag'])

def create_role(**kwargs):
    return models.Role.objects.update_or_create(**kwargs)


def create_tag(**kwargs):
    return models.Tag.objects.update_or_create(**kwargs)
