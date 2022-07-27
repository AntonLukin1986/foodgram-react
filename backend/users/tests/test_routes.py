from django.test import TestCase
from django.urls import reverse


class RoutesURLTest(TestCase):
    def test_named_paths_match_with_explicit_urls(self):
        """Именованные пути совпадают с фактическими URL адресами."""
        cases = [
            ['list', [], '/api/users/'],
            ['detail', {'id': 1}, '/api/users/1/'],
        ]
        for name, param, url in cases:
            with self.subTest(name=name):
                self.assertEqual(reverse(f'users-{name}', kwargs=param), url)
