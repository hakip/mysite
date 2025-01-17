import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question

def create_question(question_text, days):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

def create_choice(question, choice_text):
	return question.choice_set.create(choice_text=choice_text, votes=0)

class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        """was_published_recently() returns False for questions whose pub_date
        is in the future."""
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)
    def test_was_published_recently_with_old_question(self):
        """was_published_recently() returns False for questions whose pub_date
        is older than 1 day."""
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """was_published_recently() returns True for questions whose pub_date
        is within the last day."""
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)



class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on the
        index page.
        """
        quest = create_question(question_text="Past question.", days=-30)
        create_choice(question=quest, choice_text="Past choice")
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_future_question(self):
        """
        Questions with a pub_date in the future aren't displayed on
        the index page.
        """
        future_quest = create_question(question_text="Future question.", days=30)
        create_choice(question=future_quest, choice_text="Future choice")
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        are displayed.
        """
        past_quest = create_question(question_text="Past question.", days=-30)
        create_choice(question=past_quest, choice_text="Past choice")
        future_quest = create_question(question_text="Future question.", days=30)
        create_choice(question=future_quest, choice_text="Future choice")
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        quest1 = create_question(question_text="Past question 1.", days=-30)
        quest2 = create_question(question_text="Past question 2.", days=-5)
        create_choice(question=quest1, choice_text="Past choice 1")
        create_choice(question=quest2, choice_text="Past choice 2")
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question 2.>', '<Question: Past question 1.>']
        )

    def test_question_without_choices(self):
    	"""
    	Question without choices won't be published.
    	"""
    	question = create_question(question_text="Question without choices", days=-1)
    	response = self.client.get(reverse('polls:index'))
    	self.assertContains(response, "No polls are available.")
    	self.assertQuerysetEqual(response.context['latest_question_list'], [])

class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future
        returns a 404 not found.
        """
        future_question = create_question(question_text='Future question.', days=5)
        create_choice(question=future_question, choice_text="Future choice")
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past
        displays the question's text.
        """
        past_question = create_question(question_text='Past Question.', days=-5)
        create_choice(question=past_question, choice_text="Past choice")
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)

    def test_question_without_choices(self):
    	"""
    	The detail view of a question without any choice
    	returns a 404 not found.
    	"""
    	question = create_question(question_text='Question text', days=-5)
    	url = reverse('polls:detail', args=(question.id,))
    	response = self.client.get(url)
    	self.assertEqual(response.status_code, 404)

    def test_question_with_choices(self):
    	"""
    	The detail view of a question with choices
    	returns the question's text and choices.
    	"""
    	question = create_question(question_text='Question text', days=-5)
    	choice = create_choice(question=question, choice_text="Choice")
    	url = reverse('polls:detail', args=(question.id,))
    	response = self.client.get(url)
    	self.assertContains(response, question.question_text)
    	self.assertContains(response, choice.choice_text)