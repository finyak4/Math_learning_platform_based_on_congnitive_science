from django.core.management.base import BaseCommand
from quizzes.models import Quiz, Question
from django.utils import timezone
from quizzes.data.calculus import get_calculus_quizzes
from quizzes.data.linear_algebra import get_linear_algebra_quizzes
from quizzes.data.statistics import get_statistics_quizzes

class Command(BaseCommand):
    help = 'Seeds the database with initial quiz data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding data...')

        # 1. Aggregate all quiz data
        calculus_quizzes = get_calculus_quizzes()
        linear_algebra_quizzes = get_linear_algebra_quizzes()
        statistics_quizzes = get_statistics_quizzes()
        
        all_quizzes_data = calculus_quizzes + linear_algebra_quizzes + statistics_quizzes

        # 2. Define expected quizzes for deletion logic
        # Uniqueness is determined by (Title, Quiz Type)
        expected_keys = set()
        for q_data in all_quizzes_data:
            expected_keys.add((q_data['title'], q_data['type']))

        # 3. Delete quizzes not in the seed data
        for quiz in Quiz.objects.all():
            quiz_key = (quiz.title, quiz.quiz_type)
            if quiz_key not in expected_keys:
                self.stdout.write(f'Deleted quiz not in seed file: {quiz.title} ({quiz.quiz_type})')
                quiz.delete()

        # 4. Create/Update quizzes
        for q_data in all_quizzes_data:
            self.create_or_update_quiz(q_data)

        self.stdout.write(self.style.SUCCESS('Successfully seeded quizzes.'))

    def create_or_update_quiz(self, data):
        # Cleanup duplicates (keep the first one found)
        existing_quizzes = Quiz.objects.filter(
            title=data['title'],
            quiz_type=data['type']
        )
        if existing_quizzes.count() > 1:
            # Keep the first one, delete others
            to_keep = existing_quizzes.first()
            existing_quizzes.exclude(pk=to_keep.pk).delete()
            self.stdout.write(f"Removed duplicate entries for {data['title']}")

        # Get or Create
        quiz, created = Quiz.objects.get_or_create(
            title=data['title'],
            quiz_type=data['type'],
            defaults={
                'domain': data['domain'],
                'subject': data['subject'],
                'topic': data['topic'],
                'description': data['description'],
                'evaluation_method': data['eval_method'],
                'created_at': timezone.now()
            }
        )

        # Update if exists and something changed
        updated = False
        if not created:
            if (quiz.description != data['description'] or 
                quiz.evaluation_method != data['eval_method'] or
                quiz.domain != data['domain'] or
                quiz.subject != data['subject'] or
                quiz.topic != data['topic']):
                
                quiz.description = data['description']
                quiz.evaluation_method = data['eval_method']
                quiz.domain = data['domain']
                quiz.subject = data['subject']
                quiz.topic = data['topic']
                quiz.save()
                updated = True
                self.stdout.write(f"Updated quiz metadata: {quiz.title}")
        else:
            self.stdout.write(f"Created quiz: {quiz.title}")
        
        # Sync questions
        # We delete all existing questions and create new ones to ensure exact match with seed data
        quiz.question_set.all().delete()
        
        questions = data['questions']
        question_objects = []
        
        for q_item in questions:
            q_order = q_text = q_answer = q_accepted = q_explanation = None
            
            # Handle Dictionary format (used in linear_algebra.py)
            if isinstance(q_item, dict):
                q_order = q_item.get('question_order')
                q_text = q_item.get('question_text')
                q_answer = q_item.get('model_answer')
                q_accepted = q_item.get('accepted_answers', [])
                q_explanation = q_item.get('explanation', '')
                
            # Handle Tuple format (used in calculus.py)
            elif isinstance(q_item, tuple):
                # Format 1: (order, text, answer, accepted_answers_list)
                # Format 2: (order, text, answer, explanation_string)
                # Format 3: (order, text, answer)
                
                q_order = q_item[0]
                q_text = q_item[1]
                q_answer = q_item[2]
                
                fourth = q_item[3] if len(q_item) > 3 else None
                
                if isinstance(fourth, list):
                    q_accepted = fourth
                    q_explanation = ''
                elif isinstance(fourth, str):
                    q_explanation = fourth
                    q_accepted = []
                else:
                    q_accepted = []
                    q_explanation = ''

            Question.objects.create(
                quiz=quiz,
                question_order=q_order,
                question_text=q_text,
                model_answer=q_answer,
                accepted_answers=q_accepted,
                explanation=q_explanation or ''
            )
