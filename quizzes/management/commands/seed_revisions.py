from django.core.management.base import BaseCommand
from quizzes.models import Quiz, Question
from django.utils import timezone

class Command(BaseCommand):
    help = 'Seeds revision quizzes for Spaced Repetition System'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding SRS Revision Quizzes...')

        # Revision Intervals: 1 day, 3 days, 7 days, 20 days
        revisions = [
            (1, 'Limits: Revision 1', 'Limits'),
            (2, 'Limits: Revision 2', 'Limits'),
            (3, 'Limits: Revision 3', 'Limits'),
            (4, 'Limits: Revision 4', 'Limits'),
        ]

        # Common description for all revision quizzes
        rev_description = "Spaced Repetition Review. This quiz is automatically scheduled to strengthen your long-term retention. Please answer honestly."

        for level, title, topic in revisions:
            # Create Quiz
            quiz, created = Quiz.objects.get_or_create(
                title=title,
                defaults={
                    'subject': Quiz.Subject.CALCULUS_1,
                    'topic': topic,
                    'quiz_type': Quiz.QuizType.REVISION,
                    'evaluation_method': Quiz.EvaluationMethod.SELF_EVAL,
                    'description': rev_description,
                    'created_at': timezone.now()
                }
            )
            
            if not created:
                self.stdout.write(f'Revision Quiz "{title}" already exists. Ensuring description/mode.')
                quiz.description = rev_description
                quiz.evaluation_method = Quiz.EvaluationMethod.SELF_EVAL
                quiz.save()
            else:
                self.stdout.write(f'Created Revision Quiz: {title}')

            # Clear old questions to ensure fresh seed
            quiz.question_set.all().delete()

            # Define Questions based on Level Difficulty
            # Structure: 3 Easy, 2 Hard, 1 Practical
            
            questions_data = []

            if level == 1: # 1 Day Later - Mostly Basic Recall
                questions_data = [
                    (1, 'State the definition of continuity at a point x=c.', 'Limit exists, Function is defined, Limit equals Function value.', None), # Easy
                    (2, 'What is the limit of sin(x)/x as x approaches 0?', '1', None), # Easy
                    (3, 'If left limit != right limit, does the limit exist?', 'No', None), # Easy
                    (4, 'Explain the Squeeze Theorem.', 'If f <= g <= h and limits of f and h match, limit of g is the same.', None), # Harder
                    (5, 'Describe an Infinite Discontinuity.', 'The function goes to + or - infinity at the point.', None), # Harder
                    (6, 'Evaluate limit as x->2 of (x^2-4)/(x-2).', '4', 'Factor (x-2)(x+2), cancel x-2, plug in 2.'), # Practical
                ]
            
            elif level == 2: # 3 Days Later - Slightly harder
                questions_data = [
                     (1, 'What is an indeterminate form?', '0/0 or infinity/infinity (and others). Requires more work.', None), # Easy
                     (2, 'Value of limit x->inf of 1/x?', '0', None), # Easy
                     (3, 'Does a limit at x=c depend on f(c)?', 'No.', None), # Easy
                     (4, 'How to prove limit x->0 of (1-cos x)/x = 0?', 'Multiply by conjugate (1+cos x).', None), # Harder
                     (5, 'Explain IVT.', 'Continuous function on [a,b] takes all values between f(a) and f(b).', None), # Harder
                     (6, 'Find horizontal asymptote of (3x^2+1)/(x^2-5).', 'y = 3', 'Ratio of leading coefficients.'), # Practical
                ]

            elif level == 3: # 7 Days Later - Mix
                questions_data = [
                     (1, 'Limit of constant c as x->a?', 'c', None), # Easy
                     (2, 'Can a function cross its horizontal asymptote?', 'Yes, horizontal asymptotes describe end behavior, not local behavior.', None), # Easy
                     (3, 'Limit of e^x as x-> -infinity?', '0', None), # Easy
                     (4, 'Why is |x|/x not continuous at 0?', 'Jump discontinuity (Left limit -1, Right limit 1).', None), # Harder
                     (5, 'Precise definition of limit (epsilon-delta) - conceptual summary?', 'For every error tolerance epsilon, there is a vicinity delta such that points within delta land within epsilon.', None), # Harder
                     (6, 'Evaluate limit x->0 of (sqrt(1+x)-1)/x.', '1/2', 'Conjugate method.'), # Practical
                ]

            elif level == 4: # 20 Days Later - Mastery
                questions_data = [
                     (1, 'What is a removable discontinuity?', 'Hole. Limit exists but function is undefined or different.', None), # Easy 
                     (2, 'Limit x->0+ of ln(x)?', '-Infinity', None), # Easy
                     (3, 'Limit x->inf of sin(x)?', 'DNE (Oscillates).', None), # Easy
                     (4, 'Explain why polynomial functions are continuous everywhere.', 'Because they are built from x and constants using + and *, which preserve continuity.', None), # Harder
                     (5, 'Relationship between differentiable and continuous?', 'Differentiable implies Continuous. Continuous does NOT imply Differentiable.', None), # Harder
                     (6, 'Find c such that f(x) is continuous: 2x+1 (x<1), c*x^2 (x>=1).', 'c = 3', 'Left limit 3, Right limit c(1)^2 -> c=3.'), # Practical
                ]

            # Create Questions
            for order, text, answer, explanation in questions_data:
                Question.objects.create(
                    quiz=quiz,
                    question_order=order,
                    question_text=text,
                    model_answer=answer,
                    explanation=explanation,
                    accepted_answers=[]
                )
            
            self.stdout.write(f'  - Added {len(questions_data)} questions to {title}')

        self.stdout.write('SRS Seeding Complete.')
