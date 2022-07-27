from django.test import TestCase

from users.models import User, Subscribe


AUTHOR = 'Author'
NONAME = 'NotAuthor'
EMAIL = 'test@test.ru'


class UserModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username=NONAME, email=EMAIL)
        cls.author = User.objects.create_user(username=AUTHOR)
        cls.subscribe = Subscribe.objects.create(author=cls.author,
                                                 user=cls.user)

    def test_models_have_correct_object_names(self):
        """Проверка корректной работы метода __str__ у моделей."""
        models_expected = {
            self.user: f'{NONAME} <{EMAIL}>',
            self.subscribe: f'{NONAME} <{EMAIL}> подписан на {AUTHOR}'
        }
        for model, expected in models_expected.items():
            with self.subTest(field=model):
                self.assertEqual(str(model), expected)

    def test_model_user_has_correct_verbose_name(self):
        """Проверка корректного отображения verbose_name у модели User."""
        fields_verbose = {
            'username': 'Никнейм',
            'email': 'Электронная почта',
            'first_name': 'Имя',
            'last_name': 'Фамилия'
        }
        for field, expected in fields_verbose.items():
            with self.subTest(field=field):
                self.assertEqual(
                    User._meta.get_field(field).verbose_name, expected
                )

    def test_model_subscribe_has_correct_verbose_name(self):
        """Проверка корректного отображения verbose_name у модели Subscribe."""
        fields_verbose = {
            'user': 'Подписчик',
            'author': 'Автор'
        }
        for field, expected in fields_verbose.items():
            with self.subTest(field=field):
                self.assertEqual(
                    Subscribe._meta.get_field(field).verbose_name, expected
                )
