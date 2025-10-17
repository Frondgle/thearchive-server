# this was in the book, but I don't know if it's necessary
# import json
# from rest_framework.test import APITestCase
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from thearchiveapi.models import Art


# created with fan as field in mind
class ArtViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.art = Art.objects.create(
            title="Test Art",
            artist="Test Artist",
            medium="Test Medium",
            year=2021,
            image_url="https://example.com/test.jpg",
        )

    def test_retrieve_art(self):
        response = self.client.get(f"/arts/{self.art.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.art.title)
        self.assertEqual(response.data["artist"], self.art.artist)
        self.assertEqual(response.data["medium"], self.art.medium)
        self.assertEqual(response.data["year"], self.art.year)
        self.assertEqual(response.data["image_url"], self.art.image_url)

    def test_retrieve_nonexistent_art(self):
        response = self.client.get("/arts/999/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["message"], "Art matching query does not exist.")

    def test_list_arts(self):
        response = self.client.get("/arts/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], self.art.title)
        self.assertEqual(response.data[0]["artist"], self.art.artist)
        self.assertEqual(response.data[0]["medium"], self.art.medium)
        self.assertEqual(response.data[0]["year"], self.art.year)
        self.assertEqual(response.data[0]["image_url"], self.art.image_url)
