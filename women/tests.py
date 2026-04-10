from http import HTTPStatus
from women.models import Women

from django.test import TestCase
from django.urls import reverse


class GetPagesTestCase(TestCase):
    fixtures = [
        "women_women.json",
        "women_category.json",
        "women_husband.json",
        "women_tagpost.json",
    ]

    def setUp(self):
        """Set up test data for the test cases."""

    def test_home_page(self):
        path = reverse("home")
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "women/index.html")
        self.assertEqual(response.context_data["title"], "Главная страница")

    def test_redirect_addpage(self):
        path = reverse("add_page")
        redirect_uri = reverse("users:login") + "?next=" + path
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, redirect_uri)

    def test_data_home_page(self):
        path = reverse("home")
        posts = Women.published.all().select_related("category")
        response = self.client.get(path)
        self.assertQuerySetEqual(response.context_data["posts"], posts[:5])

    def test_paginate_home_page(self):
        path = reverse("home")
        posts = Women.published.all().select_related("category")
        page, paginate_by = 1, 5
        response = self.client.get(path + f"?page={page}")
        self.assertQuerySetEqual(
            response.context_data["posts"],
            posts[(page - 1) * paginate_by : page * paginate_by],
        )

    def test_content_post(self):
        post = Women.published.first()
        path = reverse("post", args=[post.slug])
        response = self.client.get(path)
        self.assertEqual(post.content, response.context_data["post"].content)

    def tearDown(self):
        """Clean up after tests."""
