import django
django.setup()
from lukexor_me import models

def create_article(**kwargs):
    defaults = {
        "minutes_to_read": 0,
    }

    defaults.update(kwargs)

    if defaults["category"]:
        defaults["category"] = models.Category.objects.get(name = defaults["category"])

    article = models.Article.objects.filter(title = defaults["title"])

    if article:
        return article
    else:
        article = models.Article.objects.create(**defaults)

        article.authors.add(models.CustomUser.objects.filter(last_name = "Petherbridge").first().user_id)

        return article

def create_author(**kwargs):
    return models.CustomUser.objects.create(**kwargs)

def create_category(**kwargs):
    category = models.Category.objects.get(**kwargs)

    if category:
        return category
    else:
        return models.Category.objects.create(**kwargs)

def create_project(**kwargs):
    project = models.Project.objects.filter(title = kwargs["title"])

    if project:
        return project
    else:
        return models.Project.objects.create(**kwargs)

def create_role(**kwargs):
    role = models.Role.objects.get(**kwargs)

    if role:
        return role
    else:
        return models.Role.objects.create(**kwargs)

def create_tag(**kwargs):
    tag = models.Tag.objects.get(**kwargs)

    if tag:
        return tag
    else:
        return models.Tag.objects.create(**kwargs)
