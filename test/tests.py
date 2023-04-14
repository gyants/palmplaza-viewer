import unittest
import requests
from unittest import TestCase

class TestScraping(TestCase):
    def test_get(self):
        url = 'https://www.palm-plaza.com/cgi-bin/CCforum/board.cgi?az=list&forum=DCForumID4&archive='
        response = requests.get(url)
        self.assertEqual(response.status_code, 200, f'Request failed with status code {response.status_code}')
    
    def test_first_div(self):
        url = 'https://www.palm-plaza.com/cgi-bin/CCforum/board.cgi?az=list&forum=DCForumID4&archive='
        response = requests.get(url)
        