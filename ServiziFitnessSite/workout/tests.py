from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Exercise, TrainingCard


class ExerciseViewTests(TestCase):
    def test_exercise_view_with_no_exercises(self):
        """
        No exercises --> "No execises are available." message should be displayed.
        """
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('workout:exercise_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No execises are available.")
        self.assertQuerysetEqual(response.context['exercise_list'], [])

    def test_exercise_view_with_an_exercise(self):
        """
        One exercise should be displayed.
        """
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        Exercise.objects.create(user=self.user, name='Test exercise')
        response = self.client.get(reverse('workout:exercise_list'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['exercise_list'],
            ['<Exercise: Test exercise (by testuser)>']
        )


class TrainingCardViewTests(TestCase):
    def test_trainingcard_view_with_no_trainingcards(self):
        """
        No trainingcards --> "No trainingcards are available." message should be displayed.
        """
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('workout:trainingcard_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No training cards are available.")
        self.assertQuerysetEqual(response.context['trainingcard_list'], [])

    def test_trainingcard_view_with_a_trainingcard(self):
        """
        One exercise should be displayed.
        """
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        TrainingCard.objects.create(user=self.user, name='Test trainingcard')
        response = self.client.get(reverse('workout:trainingcard_list'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['trainingcard_list'],
            ['<TrainingCard: Test trainingcard (by testuser)>']
        )


class ExerciseSearchViewTests(TestCase):
    def test_exercise_search_view_with_no_exercises(self):
        """
        No public exercises --> "No execises are available." message should be displayed.
        """
        response = self.client.get(reverse('workout:exercise_search'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No execises are available.")
        self.assertQuerysetEqual(response.context['exercise_list'], [])

    def test_exercise_search_view_with_a_public_exercise_without_login(self):
        """
        One public exercise should be displayed.
        """
        self.user = User.objects.create_user(username='testuser', password='12345')
        Exercise.objects.create(user=self.user, name='Test exercise', public=True)
        response = self.client.get(reverse('workout:exercise_search'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['exercise_list'],
            ['<Exercise: Test exercise (by testuser)>']
        )

    def test_exercise_search_view_with_a_private_exercise_without_login(self):
        """
        No exercise should be displayed.
        """
        self.user = User.objects.create_user(username='testuser', password='12345')
        Exercise.objects.create(user=self.user, name='Test exercise', public=False)
        response = self.client.get(reverse('workout:exercise_search'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['exercise_list'], [])

    def test_exercise_search_view_with_a_private_exercise_and_a_private_exercise_without_login(self):
        """
        One exercise should be displayed, only the public one.
        """
        self.user = User.objects.create_user(username='testuser', password='12345')
        Exercise.objects.create(user=self.user, name='Test exercise1', public=False)
        Exercise.objects.create(user=self.user, name='Test exercise2', public=True)
        response = self.client.get(reverse('workout:exercise_search'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['exercise_list'],
            ['<Exercise: Test exercise2 (by testuser)>']
        )


class TrainingCardSearchViewTests(TestCase):
    def test_trainingcard_search_view_with_no_trainingcards(self):
        """
        No public trainingcards --> "No training cards are available." message should be displayed.
        """
        response = self.client.get(reverse('workout:trainingcard_search'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No training cards are available.")
        self.assertQuerysetEqual(response.context['trainingcard_list'], [])

    def test_trainingcard_search_view_with_a_public_trainingcard_without_login(self):
        """
        One public trainingcard should be displayed.
        """
        self.user = User.objects.create_user(username='testuser', password='12345')
        TrainingCard.objects.create(user=self.user, name='Test trainingcard', public=True)
        response = self.client.get(reverse('workout:trainingcard_search'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['trainingcard_list'],
            ['<TrainingCard: Test trainingcard (by testuser)>']
        )

    def test_trainingcard_search_view_with_a_private_trainingcard_without_login(self):
        """
        No trainingcard should be displayed.
        """
        self.user = User.objects.create_user(username='testuser', password='12345')
        TrainingCard.objects.create(user=self.user, name='Test trainingcard', public=False)
        response = self.client.get(reverse('workout:trainingcard_search'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['trainingcard_list'], [])

    def test_trainingcard_search_view_with_a_private_trainingcard_and_a_private_trainingcard_without_login(self):
        """
        One trainingcard should be displayed, only the public one.
        """
        self.user = User.objects.create_user(username='testuser', password='12345')
        TrainingCard.objects.create(user=self.user, name='Test trainingcard1', public=False)
        TrainingCard.objects.create(user=self.user, name='Test trainingcard2', public=True)
        response = self.client.get(reverse('workout:trainingcard_search'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['trainingcard_list'],
            ['<TrainingCard: Test trainingcard2 (by testuser)>']
        )
