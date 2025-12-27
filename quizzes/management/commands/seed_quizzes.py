from django.core.management.base import BaseCommand
from quizzes.models import Quiz, Question
from django.utils import timezone

class Command(BaseCommand):
    help = 'Seeds the database with initial quiz data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding data...')

        # Create Quiz
        quiz, created = Quiz.objects.get_or_create(
            title='Limits: Theoretical Concepts (Self-Eval)',
            defaults={
                'subject': Quiz.Subject.CALCULUS_1,
                'topic': 'Limits',
                'quiz_type': Quiz.QuizType.THEORETICAL,
                'evaluation_method': Quiz.EvaluationMethod.SELF_EVAL,
                'created_at': timezone.now()
            }
        )

        if not created:
            self.stdout.write('Quiz 1 (Self-Eval) already exists.')
        else:
            self.stdout.write(f'Created Quiz: {quiz.title}')

        # Questions
        questions_data = [
            (1, 'State the three conditions that must be met for a function to be **continuous** at x=c.', 
             '1. f(c) is defined. 2. The limit of f(x) as x approaches c exists. 3. The limit equals the function value.'),
            (2, 'Explain the difference between a **Removable Discontinuity** (hole) and a **Non-Removable Discontinuity** (jump/asymptote) in terms of limits.', 
             'Removable: The limit exists, but f(c) is undefined or different. Non-Removable: The limit does not exist (left and right limits differ or go to infinity).'),
            (3, 'If lim_{x->c} f(x) exists, does f(c) have to exist? Give a counter-example if no.', 
             'No. A counter-example is a graph with a hole at x=c. The limit approaches the hole, but the point itself is undefined.'),
            (4, 'Explain the **Squeeze Theorem** (Sandwich Theorem) to a friend who doesn\'t know calculus. Use an analogy.', 
             'If two functions squeeze a third function between them, and both the top and bottom functions approach the same limit L, the middle function is forced to go to L as well. (Analogy: Two policemen walking an arrested person between them).'),
            (5, 'Why is 0/0 called \'indeterminate\' but 5/0 is just \'undefined\'?', 
             '5/0 is undefined because you cannot divide by zero. 0/0 is indeterminate because the answer depends on the specific functions involved; it could be 5, 0, infinity, or anything else depending on which zero is \'stronger\'.'),
            (6, 'How do you define a **Vertical Asymptote** at x=c using limits?', 
             'A vertical asymptote exists at x=c if the limit as x approaches c (from left or right) is positive or negative infinity.'),
            (7, 'How do you define a **Horizontal Asymptote** using limits?', 
             'A horizontal asymptote y=L exists if the limit of f(x) as x approaches infinity (or negative infinity) equals L.'),
            (8, 'If the Left-Hand Limit does not equal the Right-Hand Limit, what can you say about the general Limit?', 
             'The general limit does not exist (DNE).'),
            (9, 'If f(x) is continuous on [0, 5], f(0) = -2, and f(5) = 10, what does the Intermediate Value Theorem (IVT) guarantee happens at least once between x=0 and x=5?', 
             'The IVT guarantees that f(x) must equal 0 (cross the x-axis) at least once between x=0 and x=5, because it must pass through every value between -2 and 10.'),
            (10, 'Describe the behavior of the graph f(x) = sin(1/x) as x approaches 0. Does the limit exist?', 
             'The graph oscillates infinitely fast between -1 and 1 as it gets closer to 0. The limit does not exist because it never settles on a single value.')
        ]

        for order, text, answer in questions_data:
            Question.objects.create(
                quiz=quiz,
                question_order=order,
                question_text=text,
                model_answer=answer,
                accepted_answers=[]
            )
        
        # Create Second Quiz (Automated)
        quiz2, created2 = Quiz.objects.get_or_create(
            title='Limits: Theoretical Concepts',
            defaults={
                'subject': Quiz.Subject.CALCULUS_1,
                'topic': 'Limits',
                'quiz_type': Quiz.QuizType.THEORETICAL,
                'evaluation_method': Quiz.EvaluationMethod.AUTOMATED,
                'created_at': timezone.now()
            }
        )

        if created2:
             self.stdout.write(f'Created Quiz: {quiz2.title}')
             
             questions_data_2 = [
                (1, 'To prove a function is continuous at x=c, we must show that the Limit as x approaches c equals ______.', 'f(c)', ["f(c)", "function value", "value of f", "f of c"]),
                (2, 'If the limit as x approaches c exists, but f(c) is undefined, this specific type of discontinuity is called a ______ discontinuity.', 'removable', ["removable", "point", "hole"]),
                (3, 'If the Limit from the Left is 3 and the Limit from the Right is 5, then the Limit as x approaches c ______.', 'does not exist', ["does not exist", "dne", "undefined", "no limit"]), 
                (4, 'The theorem stating that if f(x) <= g(x) <= h(x) and the outer functions approach the same limit, then g(x) must also approach that limit, is called the ______ Theorem.', 'squeeze', ["squeeze", "sandwich", "pinching"]),
                (5, 'When direct substitution results in 0/0, this result is known as an ______ form.', 'indeterminate', ["indeterminate"]),
                (6, 'A Vertical Asymptote exists at x=c if the limit as x approaches c equals ______.', 'infinity', ["infinity", "infinite", "inf", "positive infinity"]),
                (7, 'To find Horizontal Asymptotes, we must evaluate the limit as x approaches ______.', 'infinity', ["infinity", "infinite", "inf", "+-infinity"]),
                (8, 'The Intermediate Value Theorem guarantees that if f(x) is continuous and changes signs between x=a and x=b, there must be at least one ______ between a and b.', 'root', ["root", "zero", "x-intercept", "solution"]),
                (9, 'For the function f(x) = sin(1/x), the limit as x approaches 0 does not exist because the function ______ infinitely fast.', 'oscillates', ["oscillates", "fluctuates", "wiggles"]),
                (10, 'True or False: If a function has a limit at x=c, it MUST be defined at x=c.', 'false', ["false", "no", "f"])
             ]

             for order, text, answer, accepted in questions_data_2:
                Question.objects.create(
                    quiz=quiz2,
                    question_order=order,
                    question_text=text,
                    model_answer=answer,
                    accepted_answers=accepted
                )
             self.stdout.write(f'Successfully created {len(questions_data_2)} questions for Quiz 2.')
        else:
             self.stdout.write('Quiz 2 already exists.')

        self.stdout.write(f'Seeding complete.')
