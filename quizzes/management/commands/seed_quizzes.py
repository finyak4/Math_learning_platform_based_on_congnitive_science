from django.core.management.base import BaseCommand
from quizzes.models import Quiz, Question
from django.utils import timezone

class Command(BaseCommand):
    help = 'Seeds the database with initial quiz data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding data...')

        # Create Quiz 1 (Self-Eval)
        description_1 = "Write your answer in your own words, then compare it to the model answer. Remember, this exercise is built on trust and personal responsibility. Marking incorrect answers as right mimics progress but hinders true understanding. Embrace the learning process—honesty here is the foundation of your growth."
        
        # Cleanup duplicates for Quiz 1
        qs1 = Quiz.objects.filter(
            title='Limits: Theoretical Concepts',
            quiz_type=Quiz.QuizType.THEORETICAL,
            evaluation_method=Quiz.EvaluationMethod.SELF_EVAL
        )
        if qs1.count() > 1:
            qs1.exclude(pk=qs1.first().pk).delete()
            self.stdout.write('Removed duplicate Quiz 1 entries.')

        quiz, created = Quiz.objects.get_or_create(
            title='Limits: Theoretical Concepts',
            quiz_type=Quiz.QuizType.THEORETICAL,
            evaluation_method=Quiz.EvaluationMethod.SELF_EVAL,
            defaults={
                'subject': Quiz.Subject.CALCULUS_1,
                'topic': 'Limits',
                'description': description_1,
                'created_at': timezone.now()
            }
        )

        # Update description for existing quizzes
        if not created and quiz.description != description_1:
            quiz.description = description_1
            quiz.save()
            self.stdout.write('Updated description for Quiz 1.')

        if not created:
            self.stdout.write('Quiz 1 (Self-Eval) already exists.')
        else:
            self.stdout.write(f'Created Quiz: {quiz.title}')

        # Questions for Quiz 1
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

        if created:
            for order, text, answer in questions_data:
                Question.objects.create(
                    quiz=quiz,
                    question_order=order,
                    question_text=text,
                    model_answer=answer,
                    accepted_answers=[]
                )
        
        # Create Second Quiz (Automated)
        description_2 = "Type in the answer directly. These questions are automatically graded to test your precision and recall."
        
        # Cleanup duplicates for Quiz 2
        qs2 = Quiz.objects.filter(
            title='Limits: Theoretical Concepts',
            quiz_type=Quiz.QuizType.THEORETICAL,
            evaluation_method=Quiz.EvaluationMethod.AUTOMATED
        )
        if qs2.count() > 1:
            qs2.exclude(pk=qs2.first().pk).delete()
            self.stdout.write('Removed duplicate Quiz 2 entries.')

        quiz2, created2 = Quiz.objects.get_or_create(
            title='Limits: Theoretical Concepts',
            quiz_type=Quiz.QuizType.THEORETICAL,
            evaluation_method=Quiz.EvaluationMethod.AUTOMATED,
            defaults={
                'subject': Quiz.Subject.CALCULUS_1,
                'topic': 'Limits',
                'description': description_2,
                'created_at': timezone.now()
            }
        )
        
        # Update description for existing quizzes
        if not created2 and quiz2.description != description_2:
            quiz2.description = description_2
            quiz2.save()
            self.stdout.write('Updated description for Quiz 2.')

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

        # Create Quiz 3 (Practical Skills)
        description_3 = "Solve the problems below. For each question, type your final answer. After submitting, you will see the detailed step-by-step solution. Compare your work honestly and mark yourself correct only if your process and answer align."

        # Cleanup duplicates for Quiz 3
        qs3 = Quiz.objects.filter(
            title='Limits: Practical Skills',
            quiz_type=Quiz.QuizType.PRACTICAL,
            evaluation_method=Quiz.EvaluationMethod.SELF_EVAL
        )
        if qs3.count() > 1:
            qs3.exclude(pk=qs3.first().pk).delete()
            self.stdout.write('Removed duplicate Quiz 3 entries.')

        quiz3, created3 = Quiz.objects.get_or_create(
            title='Limits: Practical Skills',
            quiz_type=Quiz.QuizType.PRACTICAL,
            evaluation_method=Quiz.EvaluationMethod.SELF_EVAL,
            defaults={
                'subject': Quiz.Subject.CALCULUS_1,
                'topic': 'Limits',
                'description': description_3,
                'created_at': timezone.now()
            }
        )

        if not created3 and quiz3.description != description_3:
            quiz3.description = description_3
            quiz3.save()
            self.stdout.write('Updated description for Quiz 3.')

        if created3:
            self.stdout.write(f'Created Quiz: {quiz3.title}')
        else:
            self.stdout.write('Quiz 3 already exists.')
            
        # (Order, Text, Model Answer, Explanation)
        questions_data_3 = [
            (1, 
                'Evaluate the limit using direct substitution: $\lim_{x \\to 5} (x^2 - 4x + 3)$', 
                '8', 
                'Direct Substitution is possible because the function is a polynomial, which is continuous everywhere.\n\nCalculation:\n1. Limit = $5^2 - 4(5) + 3$\n2. Limit = $25 - 20 + 3$\n3. Limit = $5 + 3 = 8$.'),
            
            (2, 
                'Evaluate the limit: $\lim_{x \\to 3} \\frac{x^2 - 9}{x - 3}$', 
                '6', 
                'We have an indeterminate form $0/0$ if we plug in 3.\n\nSteps:\n1. Factor the numerator: $x^2 - 9 = (x - 3)(x + 3)$.\n2. Rewrite the limit: $\lim_{x \\to 3} \\frac{(x - 3)(x + 3)}{x - 3}$.\n3. Cancel the common factor $(x - 3)$.\n4. Evaluate the remaining part: $\lim_{x \\to 3} (x + 3) = 3 + 3 = 6$.'),
            
            (3, 
                'Evaluate the limit: $\lim_{x \\to 0} \\frac{\\sqrt{x+4} - 2}{x}$', 
                '1/4', 
                'Plugging in 0 gives $0/0$. We use the conjugate method.\n\nSteps:\n1. Multiply numerator and denominator by the conjugate: $(\\sqrt{x+4} + 2)$.\n2. Numerator becomes: $(\\sqrt{x+4})^2 - 2^2 = (x + 4) - 4 = x$.\n3. Denominator becomes: $x(\\sqrt{x+4} + 2)$.\n4. The limit is now: $\lim_{x \\to 0} \\frac{x}{x(\\sqrt{x+4} + 2)}$.\n5. Cancel x: $\lim_{x \\to 0} \\frac{1}{\\sqrt{x+4} + 2}$.\n6. Substitute x=0: $\\frac{1}{\\sqrt{4} + 2} = \\frac{1}{2 + 2} = 1/4$.'),
            
            (4, 
                'Evaluate the limit at infinity: $\lim_{x \\to \\infty} \\frac{3x^2 + 5x}{2x^2 - 1}$', 
                '3/2 (or 1.5)', 
                'For limits at infinity of rational functions, compare the highest powers of x.\n\nAnalysis:\n1. Numerator highest degree: 2 (from $3x^2$).\n2. Denominator highest degree: 2 (from $2x^2$).\n3. Since degrees are equal, the limit is the ratio of the leading coefficients.\n4. Ratio = $3/2$.'),
            
            (5, 
                'Evaluate the trigonometric limit: $\lim_{x \\to 0} \\frac{\\sin(5x)}{x}$', 
                '5', 
                'We use the standard limit property: $\lim_{u \\to 0} \\frac{\\sin(u)}{u} = 1$.\n\nSteps:\n1. We need the denominator to match the argument of sine (5x).\n2. Multiply the expression by 5/5: $5 \\cdot \\frac{\\sin(5x)}{5x}$.\n3. Factor out the 5: $5 \\cdot \lim_{x \\to 0} \\frac{\\sin(5x)}{5x}$.\n4. Since $5x \\to 0$ as $x \\to 0$, the limit in brackets is 1.\n5. Result = $5 \\cdot 1 = 5$.'),
            
            (6, 
                'Find the Left-Hand Limit: $\lim_{x \\to 2^-} \\frac{|x - 2|}{x - 2}$', 
                '-1', 
                'We are approaching 2 from the left ($x < 2$).\n\nAnalysis:\n1. If $x < 2$, then $(x - 2)$ is negative.\n2. By definition, $|u| = -u$ when u is negative. So, $|x - 2| = -(x - 2)$.\n3. The expression becomes: $\\frac{-(x - 2)}{x - 2}$.\n4. Canceling terms gives: -1.\n5. The limit of a constant is the constant itself: -1.'),
            
            (7, 
                'Evaluate the complex fraction limit: $\lim_{x \\to 4} \\frac{\\frac{1}{x} - \\frac{1}{4}}{x - 4}$', 
                '-1/16', 
                'Plugging in 4 gives $0/0$.\n\nSteps:\n1. Simplify the numerator fraction: $\\frac{4 - x}{4x}$.\n2. Rewrite the expression: $\\frac{4 - x}{4x} \\cdot \\frac{1}{x - 4}$.\n3. Notice that $(4 - x) = -(x - 4)$.\n4. Rewrite top: $\\frac{-(x - 4)}{4x(x - 4)}$.\n5. Cancel $(x - 4)$: $\\frac{-1}{4x}$.\n6. Evaluate limit as $x \\to 4$: $\\frac{-1}{4(4)} = -1/16$.'),
            
            (8, 
                'Evaluate the limit at infinity: $\lim_{x \\to \\infty} \\frac{x^3 + 1}{e^x}$', 
                '0', 
                'This is a competition between a polynomial ($x^3$) and an exponential function ($e^x$).\n\nConcept:\n1. Exponential functions grow significantly faster than polynomial functions as $x \\to \\infty$.\n2. Therefore, the denominator ($e^x$) will overwhelm the numerator ($x^3$).\n3. The fraction approaches 0.'),
            
            (9, 
                'Evaluate the limit: $\lim_{h \\to 0} \\frac{(3+h)^2 - 9}{h}$', 
                '6', 
                'This limit represents the derivative of $x^2$ at $x=3$. Direct substitution gives $0/0$.\n\nSteps:\n1. Expand the numerator: $(3 + h)^2 = 9 + 6h + h^2$.\n2. Subtract 9: $(9 + 6h + h^2) - 9 = 6h + h^2$.\n3. Divide by h: $\\frac{6h + h^2}{h} = 6 + h$.\n4. Take limit as $h \\to 0$: $6 + 0 = 6$.'),
            
            (10, 
                'Given $f(x) = \\begin{cases} 2x & x < 1 \\\\ 3x^2 & x \\ge 1 \\end{cases}$. Does the limit exist at $x=1$?', 
                'No', 
                'For the limit to exist, the Left-Hand Limit (LHL) must equal the Right-Hand Limit (RHL).\n\n1. LHL ($x \\to 1^-$): Use $f(x) = 2x$. Limit = $2(1) = 2$.\n2. RHL ($x \\to 1^+$): Use $f(x) = 3x^2$. Limit = $3(1)^2 = 3$.\n3. Since $2 \\neq 3$, the limit does NOT exist.')
        ]

        for order, text, answer, explanation in questions_data_3:
            Question.objects.update_or_create(
                quiz=quiz3,
                question_order=order,
                defaults={
                    'question_text': text,
                    'model_answer': answer,
                    'explanation': explanation,
                    'accepted_answers': []
                }
            )
        self.stdout.write(f'Successfully updated/created {len(questions_data_3)} questions for Quiz 3.')

        self.stdout.write(f'Seeding complete.')
