from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from quizzes.models import Quiz, Question, QuizAttempt, TopicState
from django.utils import timezone
from datetime import timedelta

class QuizViewsTest(TestCase):
    def setUp(self):
        # Create User
        User = get_user_model()
        self.user = User.objects.create_user(email='test@test.com', password='password')
        self.client = Client()
        self.client.login(email='test@test.com', password='password')

        # Create Quizzes
        self.quiz_calc = Quiz.objects.create(
            title="Calculus Quiz",
            domain=Quiz.Domain.CALCULUS,
            subject=Quiz.Subject.CALCULUS_1,
            topic="Limits",
            quiz_type=Quiz.QuizType.THEORETICAL,
            evaluation_method=Quiz.EvaluationMethod.AUTOMATED
        )

        self.quiz_standard = Quiz.objects.create(
            title="Standard Quiz",
            domain=Quiz.Domain.LINEAR_ALGEBRA,
            subject=Quiz.Subject.MECHANICS,
            topic="Vectors",
            quiz_type=Quiz.QuizType.THEORETICAL,
            evaluation_method=Quiz.EvaluationMethod.AUTOMATED
        )
        self.q1 = Question.objects.create(
            quiz=self.quiz_standard,
            question_text="What is 1+1?",
            model_answer="2",
            question_order=1
        )

        self.quiz_self_eval = Quiz.objects.create(
            title="Self Eval Quiz",
            domain=Quiz.Domain.LINEAR_ALGEBRA,
            subject=Quiz.Subject.MECHANICS,
            topic="Vectors",
            quiz_type=Quiz.QuizType.THEORETICAL,
            evaluation_method=Quiz.EvaluationMethod.SELF_EVAL
        )
        self.q2 = Question.objects.create(
            quiz=self.quiz_self_eval,
            question_text="Explain vectors.",
            model_answer="Direction and magnitude.",
            question_order=1
        )

        self.quiz_revision = Quiz.objects.create(
            title="Vectors: Revision 1",
            domain=Quiz.Domain.LINEAR_ALGEBRA,
            subject=Quiz.Subject.MECHANICS,
            topic="Vectors",
            quiz_type=Quiz.QuizType.REVISION,
            evaluation_method=Quiz.EvaluationMethod.AUTOMATED
        )
        self.q3 = Question.objects.create(
            quiz=self.quiz_revision,
            question_text="Revision Q",
            model_answer="Rev A",
            question_order=1
        )

    def test_quiz_list_access(self):
        # Default (Calculus)
        try:
            print("Accessing quiz list...")
            response = self.client.get(reverse('quizzes:quiz_list'))
            print(f"Status: {response.status_code}")
            if response.status_code != 200:
                print(f"Content: {response.content}")
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "Calculus Quiz")
            print("Default list passed.")
        except Exception as e:
            print(f"FAIL EXCEPTION: {e}")
            raise
        
        # Linear Algebra
        response_la = self.client.get(reverse('quizzes:quiz_list_subject', args=['linear-algebra']))
        self.assertEqual(response_la.status_code, 200)
        self.assertContains(response_la, "Standard Quiz")
        self.assertNotContains(response_la, "Calculus Quiz")
        
        # Revision quiz should NOT be visible yet (no TopicState)
        self.assertNotContains(response_la, "Vectors: Revision 1")

    def test_take_quiz_render(self):
        url = reverse('quizzes:take_quiz', args=[self.quiz_standard.quiz_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Standard Quiz")

    def test_submit_quiz_automated_correct(self):
        url = reverse('quizzes:submit_quiz', args=[self.quiz_standard.quiz_id])
        data = {
            f'question_{self.q1.question_id}': '2'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        
        # Check Attempt
        attempt = QuizAttempt.objects.get(user=self.user, quiz=self.quiz_standard)
        self.assertEqual(attempt.score, 1)
        self.assertEqual(attempt.percentage, 100.0)
        
        # Check SRS Init
        self.assertTrue(TopicState.objects.filter(user=self.user, topic="Vectors").exists())
        state = TopicState.objects.get(user=self.user, topic="Vectors")
        self.assertEqual(state.current_level, 0) # Initial level

    def test_submit_quiz_self_eval_flow(self):
        url = reverse('quizzes:submit_quiz', args=[self.quiz_self_eval.quiz_id])
        
        # Stage 1: Initial Post (View Self Eval)
        data_stage1 = {
            f'question_{self.q2.question_id}': 'My answer'
        }
        response1 = self.client.post(url, data_stage1)
        self.assertEqual(response1.status_code, 200)
        self.assertTemplateUsed(response1, 'quizzes/quiz_self_eval.html')

        # Stage 2: Final Submit
        data_stage2 = {
            'final_submit': 'true',
            f'correct_{self.q2.question_id}': 'on'
        }
        response2 = self.client.post(url, data_stage2)
        self.assertEqual(response2.status_code, 200)
        
        attempt = QuizAttempt.objects.get(user=self.user, quiz=self.quiz_self_eval)
        self.assertEqual(attempt.score, 1)

    def test_duplicate_attempt_prevention(self):
        # Create attempt
        QuizAttempt.objects.create(user=self.user, quiz=self.quiz_standard, score=0, percentage=0)
        
        # Try to take again
        url = reverse('quizzes:take_quiz', args=[self.quiz_standard.quiz_id])
        response = self.client.get(url)
        self.assertRedirects(response, reverse('quizzes:quiz_list'))
        
        messages = list(response.wsgi_request._messages)
        self.assertEqual(len(messages), 1)
        self.assertIn("already attempted", str(messages[0]))

    def test_srs_revision_unlock(self):
        # 1. Pass Standard Quiz to create TopicState
        state = TopicState.objects.create(
            user=self.user, 
            topic="Vectors", 
            current_level=0, 
            next_review_at=timezone.now() - timedelta(minutes=1) # Already unlocked
        )
        
        # 2. Check List for Revision visibility (Linear Algebra)
        response = self.client.get(reverse('quizzes:quiz_list_subject', args=['linear-algebra']))
        self.assertContains(response, "Vectors: Revision 1")
        
        # 3. Take Revision Quiz -> Submit -> Level Up
        url = reverse('quizzes:submit_quiz', args=[self.quiz_revision.quiz_id])
        data = {
            f'question_{self.q3.question_id}': 'Rev A'
        }
        response_submit = self.client.post(url, data)
        self.assertEqual(response_submit.status_code, 200)
        
        state.refresh_from_db()
        self.assertEqual(state.current_level, 1)
        self.assertTrue(state.next_review_at > timezone.now())
