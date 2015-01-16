from django.test import TestCase
from django.utils.http import urlquote
from django.core.urlresolvers import reverse
from lib import model_factory
from lukexor_me import models

class ArticleMethodTests(TestCase):

    def setUp(self):
        author = model_factory.create_user_with_email("article_author@domain.com")

        prog_category = model_factory.create_category(name = "Programming")
        model_factory.create_tag(name = "Tech")
        model_factory.create_tag(name = "Career")

        model_factory.create_article(
            title = "Test article",
            permalink_title = "test-article",
            defaults = {
                'author': author[0],
                'body': "Test content",
                'category': prog_category[0],
                'minutes_to_read': 5,
            }
        )

    def test_comment_count_zero(self):
        article = models.Article.objects.get(title = "Test article")

        self.assertEqual(article.comment_count(), 0)

    def test_comment_count_greater_than_zero(self):
        user = models.CustomUser.objects.get(email = "article_author@domain.com")
        article = models.Article.objects.get(title = "Test article")

        model_factory.create_comment(
            user = user,
            article = article,
            body = "Test comment 1",
        )
        model_factory.create_comment(
            user = user,
            article = article,
            body = "Test comment 2",
        )

        self.assertEqual(article.comment_count(), 2)

    def test_get_absolute_url(self):
        article = models.Article.objects.get(title = "Test article")

        self.assertEqual(article.get_absolute_url(), reverse('article_permalink', args=[article.permalink_title]))

    def test_get_tags_with_none(self):
        article = models.Article.objects.get(title = "Test article")

        self.assertEqual(article.get_tags(), "")

    def test_get_tags_with_one(self):
        article = models.Article.objects.get(title = "Test article")
        tech_tag = models.Tag.objects.get(name = "Tech")

        model_factory.add_article_tag(
            article = article,
            tag = tech_tag,
        )

        self.assertEqual(article.get_tags(), "Tech")

    def test_get_tags_with_greater_than_one(self):
        article = models.Article.objects.get(title = "Test article")
        tech_tag = models.Tag.objects.get(name = "Tech")
        career_tag = models.Tag.objects.get(name = "Career")

        model_factory.add_article_tag(
            article = article,
            tag = tech_tag,
        )
        model_factory.add_article_tag(
            article = article,
            tag = career_tag,
        )

        self.assertEqual(article.get_tags(), "Tech, Career")

    def test_summary_with_less_than_word_limit(self):
        article = models.Article.objects.get(title = "Test article")

        article.body = "Not many characters in this body"
        expected_summary = article.body

        self.assertEqual(article.summary(), expected_summary)

    def test_summary_equal_to_word_limit(self):
        article = models.Article.objects.get(title = "Test article")

        article.body = '1'
        for i in range(2, 41):
            article.body = "%s %d" % (article.body, i)

        expected_summary = "%s" % (article.body)

        self.assertEqual(article.summary(), expected_summary)

    def test_summary_greater_than_word_limit(self):
        article = models.Article.objects.get(title = "Test article")

        article.body = '1'
        for i in range(2, 50):
            article.body = "%s %d" % (article.body, i)

        expected_summary = '1'
        for i in range(2, 41):
            expected_summary = "%s %d" % (expected_summary, i)

        expected_summary = "%s ..." % (expected_summary)

        self.assertEqual(article.summary(), expected_summary)

    def test_summary_with_html_in_body(self):
        article = models.Article.objects.get(title = "Test article")

        article.body = "<b>A body with some <i>HTML</i> in it.</b>"
        expected_summary = "A body with some HTML in it."

        self.assertEqual(article.summary(), expected_summary)

    def test_time_to_read(self):
        article = models.Article.objects.get(title = "Test article")

        article.minutes_to_read = 5

        self.assertEqual(article.time_to_read(), "5 minute read")

    def test_unicode(self):
        article = models.Article.objects.get(title = "Test article")

        self.assertEqual(article.__unicode__(), "Test article")


class ArticleViewTests(TestCase):

    def test_article_index_view_with_no_articles(self):
        """
        If no articles exist, an appropriate message should be displayed.
        """

        response = self.client.get(reverse('articles'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No articles found.")
        self.assertQuerysetEqual(response.context['articles'], [])

    def test_article_index_view_with_past_article(self):
        pass

    def test_article_index_view_with_future_article(self):
        pass

    def test_article_index_view_with_past_and_future_articles(self):
        pass

    def test_article_index_view_with_two_past_articles(self):
        pass

    def test_article_permalink_view_with_no_article(self):
        pass

    def test_article_permalink_view_with_past_article(self):
        pass

    def test_article_permalink_view_with_future_article(self):
        pass

    def test_article_permalink_view_without_comments(self):
        pass

    def test_article_permalink_view_with_comments(self):
        pass


class CategoryMethodTests(TestCase):
    def setUp(self):
        model_factory.create_category(name = "Programming")

    def test_unicode(self):
        category = models.Category.objects.get(name = "Programming")

        self.assertEqual(category.__unicode__(), "Programming")


class CommentMethodTests(TestCase):
    def setUp(self):
        author = model_factory.create_user(
            email = "article_author@domain.com",
            defaults = {
                "full_name": "John Doe",
            }
        )
        prog_category = model_factory.create_category(name = "Programming")

        article = model_factory.create_article(
            title = "Test article",
            permalink_title = "test-article",
            defaults = {
                'author': author[0],
                'body': "Test content",
                'category': prog_category[0],
                'minutes_to_read': 5,
            }
        )

        model_factory.create_comment(
            user = author[0],
            article = article[0],
            body = "Test comment 1",
        )

    def test_unicode(self):
        article = models.Article.objects.get(title = "Test article")
        comment = models.Comment.objects.filter(article_id = article.article_id)[0]

        self.assertEqual(comment.__unicode__(), "%s - %s" % ("Test comment 1", "John Doe"))


class CustomUserManagerMethodTests(TestCase):

    def test_create_user(self):
        user = models.CustomUser.objects.create_user(
            "test_user@domain.com",
            "test_password8",
        )

        self.assertEqual(user.email, "test_user@domain.com")
        self.assertFalse(user.is_staff)
        self.assertTrue(user.is_active)

    def test_create_user_without_email(self):
        with self.assertRaisesRegexp(ValueError, 'The given email must be set'):
            models.CustomUser.objects.create_user(None)

    def test_create_superuser(self):
        superuser = models.CustomUser.objects.create_superuser(
            "test_superuser@domain.com",
            "test_password8",
        )

        self.assertEqual(superuser.email, "test_superuser@domain.com")
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_active)


class CustomUserMethodTests(TestCase):

    def setUp(self):
        model_factory.create_user(
            email = "test_user@domain.com",
            defaults = {
                'full_name': "John Doe",
                'preferred_name': "Johnny",
            }
        )

    def test_get_absolute_url(self):
        user = models.CustomUser.objects.get(email = "test_user@domain.com")

        self.assertEqual(user.get_absolute_url(), "/users/%s/" % urlquote("test_user@domain.com"))

    def test_get_full_name(self):
        user = models.CustomUser.objects.get(email = "test_user@domain.com")

        self.assertEqual(user.get_full_name(), "John Doe")

    def test_get_short_name(self):
        user = models.CustomUser.objects.get(email = "test_user@domain.com")

        self.assertEqual(user.get_short_name(), "Johnny")

    def test_email_user(self):
        user = models.CustomUser.objects.get(email = "test_user@domain.com")

        pass

    def test_unicode(self):
        user = models.CustomUser.objects.get(email = "test_user@domain.com")

        self.assertEqual(user.__unicode__(), "John Doe")


class ProjectMethodTests(TestCase):

    def setUp(self):
        client = model_factory.create_user_with_email("project_client@domain.com")

        model_factory.create_tag(name = "Tech")
        model_factory.create_tag(name = "iOS")
        model_factory.create_role(name = "Developer")
        model_factory.create_role(name = "Designer")

        model_factory.create_project(
            title = "Test project",
            permalink_title = "test-project",
            defaults = {
                'client': client[0],
                'body': "Test content",
                'website': 'http://website.com/',
            }
        )

    def test_comment_count_zero(self):
        project = models.Project.objects.get(title = "Test project")

        self.assertEqual(project.comment_count(), 0)

    def test_comment_count_greater_than_zero(self):
        user = models.CustomUser.objects.get(email = "project_client@domain.com")
        project = models.Project.objects.get(title = "Test project")

        model_factory.create_comment(
            user = user,
            project = project,
            body = "Test comment 1",
        )
        model_factory.create_comment(
            user = user,
            project = project,
            body = "Test comment 2",
        )

        self.assertEqual(project.comment_count(), 2)

    def test_get_absolute_url(self):
        project = models.Project.objects.get(title = "Test project")

        self.assertEqual(project.get_absolute_url(), reverse('project_permalink', args=[project.permalink_title]))

    def test_get_tags_with_none(self):
        project = models.Project.objects.get(title = "Test project")

        self.assertEqual(project.get_tags(), "")

    def test_get_tags_with_one(self):
        project = models.Project.objects.get(title = "Test project")
        tech_tag = models.Tag.objects.get(name = "Tech")

        model_factory.add_project_tag(
            project = project,
            tag = tech_tag,
        )

        self.assertEqual(project.get_tags(), "Tech")

    def test_get_tags_with_greater_than_one(self):
        project = models.Project.objects.get(title = "Test project")
        tech_tag = models.Tag.objects.get(name = "Tech")
        ios_tag = models.Tag.objects.get(name = 'iOS')

        model_factory.add_project_tag(
            project = project,
            tag = tech_tag,
        )
        model_factory.add_project_tag(
            project = project,
            tag = ios_tag,
        )

        self.assertEqual(project.get_tags(), "Tech, iOS")

    def test_get_roles_with_none(self):
        project = models.Project.objects.get(title = "Test project")

        self.assertEqual(project.get_roles(), "")

    def test_get_roles_with_one(self):
        project = models.Project.objects.get(title = "Test project")
        dev_role = models.Role.objects.get(name = "Developer")

        model_factory.add_project_role(
            project = project,
            role = dev_role,
        )

        self.assertEqual(project.get_roles(), "Developer")

    def test_get_roles_with_greather_than_one(self):
        project = models.Project.objects.get(title = "Test project")
        dev_role = models.Role.objects.get(name = "Developer")
        designer_role = models.Role.objects.get(name = "Designer")

        model_factory.add_project_role(
            project = project,
            role = dev_role,
        )
        model_factory.add_project_role(
            project = project,
            role = designer_role,
        )

        self.assertEqual(project.get_roles(), "Developer, Designer")

    def test_summary_with_less_than_word_limit(self):
        project = models.Project.objects.get(title = "Test project")

        project.body = "Not many characters in this body"
        expected_summary = project.body

        self.assertEqual(project.summary(), expected_summary)

    def test_summary_equal_to_word_limit(self):
        project = models.Project.objects.get(title = "Test project")

        project.body = '1'
        for i in range(2, 41):
            project.body = "%s %d" % (project.body, i)

        expected_summary = "%s" % (project.body)

        self.assertEqual(project.summary(), expected_summary)

    def test_summary_greater_than_word_limit(self):
        project = models.Project.objects.get(title = "Test project")

        project.body = '1'
        for i in range(2, 50):
            project.body = "%s %d" % (project.body, i)

        expected_summary = '1'
        for i in range(2, 41):
            expected_summary = "%s %d" % (expected_summary, i)

        expected_summary = "%s ..." % (expected_summary)

        self.assertEqual(project.summary(), expected_summary)

    def test_summary_with_html_in_body(self):
        project = models.Project.objects.get(title = "Test project")

        project.body = "<b>A body with some <i>HTML</i> in it.</b>"
        expected_summary = "A body with some HTML in it."

        self.assertEqual(project.summary(), expected_summary)

    def test_unicode(self):
        project = models.Project.objects.get(title = "Test project")

        self.assertEqual(project.__unicode__(), "Test project")


class RoleMethodTests(TestCase):
    def setUp(self):
        model_factory.create_role(name = "Developer")

    def test_unicode(self):
        dev_role = models.Role.objects.get(name = "Developer")

        self.assertEqual(dev_role.__unicode__(), "Developer")


class TagMethodTests(TestCase):
    def setUp(self):
        model_factory.create_tag(name = "Tech")

    def test_unicode(self):
        tech_tag = models.Tag.objects.get(name = "Tech")

        self.assertEqual(tech_tag.__unicode__(), "Tech")
