from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from library.models import Article, Author, Tag
from common.test_utils import (
    create_article, create_author, create_superuser, create_tag
)


class SetUpData(TestCase):

    def setUp(self):
        self.author = create_author('author', '48s5tb4w3')
        self.avatar_filename = 'avatar.png'
        self.expect_avatar_path = 'static/library/author/author/avatar.png'
        self.another_author = create_author('another_author', 'a49o7wg3qvf')
        self.superuser = create_superuser('superuser', 'aiuh3h347q')

        self.tag = create_tag('tag')
        self.another_tag = create_tag('another_tag')
        self.yet_another_tag = create_tag('yet_another_tag')
        
        self.article = create_article(
            title='article title', 
            author=self.author,
            pub_date=timezone.now() - timedelta(hours=5),
            tags=[self.tag, self.another_tag],
            content='article content'
        )
        self.another_article = create_article(
            title='another article title',
            author=self.author,
            pub_date=timezone.now() - timedelta(hours=2),
            tags=[self.another_tag],
            content='another article content'
        )
        self.yet_another_article = create_article(
            title='yet another article title',
            author=self.author,
            pub_date=timezone.now(),
            tags=[self.yet_another_tag],
            content='yet another article content'
        )


class AuthorTests(SetUpData):

    def test_str(self):
        """
        Checks whether __str__ displays author correctly.
        """
        self.assertEqual(self.author.user_name, str(self.author))

    def test_ordering(self):
        """
        CHecks whether authors are ordered by user_name.
        """
        self.assertQuerySetEqual(
            Author.objects.all(),
            [self.another_author, self.author, self.superuser]
        )

    def test_default_joined(self):
        """
        Checks whether joined is provided by default.
        """
        self.assertTrue(self.author.joined)

    def test_default_slug(self):
        """
        Checks whether slug is provided by default.
        """
        self.assertTrue(self.author.slug)

    def test_create_avatar_path(self):
        self.assertEqual(
            self.author.create_avatar_path(self.avatar_filename), self.expect_avatar_path
        )

    def test_default_avatar(self):
        """
        Checks whether default avatar is provided by default.
        """
        self.assertTrue(self.author.avatar)

    def test_super_user(self):
        """
        Checks superuser attributes.
        """
        self.assertTrue(self.superuser.is_staff)
        self.assertTrue(self.superuser.is_superuser)

    def test_superuser_not_is_superuser(self):
        """
        Checks whether raises ValueError when create superuser with
        inappropriate argument.
        """
        with self.assertRaises(ValueError):
            Author.objects.create_superuser(
            user_name='superuser',
            email='super@ex.com',
            password='o947gh934',
            is_superuser=False,
            )

    def test_superuser_not_is_staff(self):
        """
        Checks whether raises ValueError when create superuser with
        inappropriate argument.
        """
        with self.assertRaises(ValueError):
            Author.objects.create_superuser(
            user_name='superuser',
            email='super@ex.com',
            password='o947gh934',
            is_staff=False,
            )


class TagTests(SetUpData):

    def test_str(self):
        """
        Checks whether __str__ displays tag correctly.
        """
        self.assertEqual(self.tag.name, str(self.tag))

    def test_ordering(self):
        """
        CHecks whether tags are ordered by name.
        """
        self.assertQuerySetEqual(
            Tag.objects.all(),
            [self.another_tag, self.tag, self.yet_another_tag]
        )

    def test_default_slug(self):
        """
        Checks whether slug is provided by default.
        """
        self.assertTrue(self.tag.slug)


class ArticleTests(SetUpData):

    def test_str(self):
        """
        Checks whether __str__ displays article correctly.
        """
        self.assertEqual(self.article.title, str(self.article))

    def test_ordering(self):
        """
        CHecks whether tags are ordered by pub_date, latest first.
        """
        self.assertQuerySetEqual(
            Article.objects.all(),
            [self.yet_another_article, self.another_article, self.article]
        )

    def test_default_pub_date(self):
        """
        Checks whether pub_date is provided by default.
        """
        test_article = Article(
            title='title',author=self.author, content='content'
        )
        test_article.save()
        test_article.tags.set([self.tag])
        self.assertTrue(self.article.pub_date)

    def test_default_slug(self):
        """
        Checks whether slug is provided by default.
        """
        self.assertTrue(self.article.slug)

    def test_tags_as_str(self):
        """
        Checks whether tag_as_str() correctly returns tags as string.
        """
        self.assertEqual(self.article.tags_as_str(), 'another_tag, tag')
