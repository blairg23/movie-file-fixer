from unittest import mock, TestCase

import faker
import movie_file_fixer

module_under_test = "movie_file_fixer"

fake = faker.Faker()


class MovieFileFixerTestCase(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_thingy(self):
        assert 1 == 1
