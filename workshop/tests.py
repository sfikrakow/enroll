from django.test import TestCase

from .models import User


class TestUserGetName(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser11', password='12345', first_name='Jan Paweł',
                                             last_name='von Kowalskiąęźć')

    def test_get_name(self):
        self.assertEquals('Jan Paweł von Kowalskiąęźć', self.user.__str__())
