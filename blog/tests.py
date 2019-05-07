from django.test import TestCase, Client
from django.contrib.auth.models import User
from bs4 import BeautifulSoup
from .models import Post, Category, Tag
from django.utils import timezone


def create_tag(name=''):

    tag, is_created = Tag.objects.get_or_create(
        name = name
    )
    tag.slug = tag.name
    tag.save()
    return tag


class TestModel(TestCase):
    def setUp(self):
        self.client = Client()
        self.author1 = User.objects.create(
            username='user1',
            email='user1@naver.com',
            password='1234',
        )

    def test_tag(self):
        tag1 = create_tag(name='warm')
        tag2 = create_tag(name='cold')
        post1 = Post.objects.create(
            title='tit1',
            content = 'cont1',
            date_posted = timezone.now(),
            author = self.author1
        )
        print('tag1 :', tag1)
        print('tag2 :', tag2)
        post1.tags.add(tag1)
        post1.tags.add(tag2)
        post1.save()

        post2 = Post.objects.create(
            title='tit2',
            content='cont2',
            date_posted=timezone.now(),
            author=self.author1
        )

        post2.tags.add(tag2)
        post2.save()

        self.assertEqual(post1.tags.count(), 2)
        # tt = self.assertEqual(tag2.post_set.count())
        # tt = post1.tags.first().name
        # print('tt', tt)
        # self.assertEqual(tag2.post_set.first(), post1)

        # post_card = main_div

class TestView(TestCase):
    def setUp(self):
        self.client = Client()
        self.author1 = User.objects.create(
            username = 'user1',
            email = 'user1@naver.com',
            password = '1234',
        )
    def test_post_list(self):
        tg1 = create_tag(name='summer')
        tg2 = create_tag(name='spring')
        post1 = Post.objects.create(
            title='tit1',
            content='cont1',
            date_posted=timezone.now(),
            author=self.author1
        )
        print('tag1 :', tg1)
        print('tag2 :', tg2)
        post1.tags.add(tg1)
        post1.tags.add(tg2)
        post1.save()

        post2 = Post.objects.create(
            title='tit2',
            content='cont2',
            date_posted=timezone.now(),
            author=self.author1
        )

        post2.tags.add(tg2)
        post2.save()

        response = self.client.get(tg1.get_absolute_url)
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')
        cont = soup.find('div', id='container')
        self.assertIn('#{}'.format(tg1), cont.text)


        # response = self.client.get('')
        # soup = BeautifulSoup(response.content, 'html.parser')
        # cont = soup.find('div', id='container')

        # pc1 = cont.find('div', id='post-card-{}'.format(post1.pk))
        # self.assertIn('#spring', pc1)


        # response = self.client.get('')
        # self.assertEqual(response.status_code, 200)
        #
        # soup = BeautifulSoup(response.content, 'html.parser')
        # title = soup.title
        #
        # print(title)
        #
        # self.assertEqual(Post.objects.count(), 0)
        #
        # post1 = Post.objects.create(
        #     title='tit1',
        #     content = 'cont1',
        #     date_posted = timezone.now(),
        #     author = self.author1
        # )
        # self.assertEqual(Post.objects.count(), 1)

        # category1 = Category.objects.create(
        #     name='food', slug='food'
        # )






