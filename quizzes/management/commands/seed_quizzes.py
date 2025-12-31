from django.core.management.base import BaseCommand
from quizzes.models import Quiz, Question
from django.utils import timezone

class Command(BaseCommand):
    help = 'Seeds the database with initial quiz data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding data...')

        # Define the quizzes that should exist (title + quiz_type uniquely identifies them)
        expected_quizzes = [
            ('Limits: Theoretical Concepts', 'Theoretical'),
            ('Limits: Practical Skills', 'Practical'),
            ('Limits: Concept Understanding', 'Theoretical'),
            ('Limits: Basic Rules & Properties', 'Theoretical'),
            ('Limits: Advanced Practice', 'Practical'),
            ('Derivatives: Theoretical Concepts', 'Theoretical'),
            ('Derivatives: Basic Rules & Properties', 'Theoretical'),
            ('Derivatives: Practical Skills', 'Practical'),
            ('Derivatives: Chain Rule Concepts', 'Theoretical'),
            ('Derivatives: Chain Rule Practice', 'Theoretical'),
            ('Applications of Derivatives: Theoretical Concepts', 'Theoretical'),
            ('Applications of Derivatives: Basic Rules & Properties', 'Theoretical'),
            ('Applications of Derivatives: Practical Skills', 'Practical'),
            ('Applications of Derivatives: Concept Understanding', 'Theoretical'),
            ('Applications of Derivatives: Fundamental Properties', 'Theoretical'),
            ('Applications of Derivatives: Advanced Practice', 'Practical'),
            ('Derivatives: Chain Rule Mixed Practice', 'Practical'),
        ]
        
        # Delete quizzes not in the seed file
        for quiz in Quiz.objects.all():
            quiz_key = (quiz.title, quiz.quiz_type)
            if quiz_key not in expected_quizzes:
                quiz_title = quiz.title
                quiz.delete()
                self.stdout.write(f'Deleted quiz not in seed file: {quiz_title}')

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

        # Delete all existing questions to ensure database matches seed file
        quiz.question_set.all().delete()
        
        # Create all questions
        for order, text, answer in questions_data:
            Question.objects.create(
                quiz=quiz,
                question_order=order,
                question_text=text,
                model_answer=answer,
                accepted_answers=[]
            )
        self.stdout.write(f'Successfully created {len(questions_data)} questions for Quiz 1.')
        
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
        else:
             self.stdout.write('Quiz 2 already exists.')
             
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

        # Delete all existing questions to ensure database matches seed file
        quiz2.question_set.all().delete()
        
        # Create all questions
        for order, text, answer, accepted in questions_data_2:
            Question.objects.create(
                quiz=quiz2,
                question_order=order,
                question_text=text,
                model_answer=answer,
                accepted_answers=accepted
            )
        self.stdout.write(f'Successfully created {len(questions_data_2)} questions for Quiz 2.')

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

        # Delete all existing questions to ensure database matches seed file
        quiz3.question_set.all().delete()
        
        # Create all questions
        for order, text, answer, explanation in questions_data_3:
            Question.objects.create(
                quiz=quiz3,
                question_order=order,
                question_text=text,
                model_answer=answer,
                explanation=explanation,
                accepted_answers=[]
            )
        self.stdout.write(f'Successfully created {len(questions_data_3)} questions for Quiz 3.')

        # ==========================================
        # Quiz 4: Limits: Concept Understanding (Theoretical / Self-Eval)
        # ==========================================
        description_4 = "Write your answer in your own words, then compare it to the model answer. Remember, this exercise is built on trust and personal responsibility. Marking incorrect answers as right mimics progress but hinders true understanding. Embrace the learning process—honesty here is the foundation of your growth."
        
        # Cleanup duplicates for Quiz 4 (search by title + quiz_type only)
        qs4 = Quiz.objects.filter(
            title='Limits: Concept Understanding',
            quiz_type=Quiz.QuizType.THEORETICAL
        )
        if qs4.count() > 1:
            qs4.exclude(pk=qs4.first().pk).delete()
            self.stdout.write('Removed duplicate Quiz 4 entries.')

        # Use title + quiz_type for lookup to avoid duplicates
        quiz4, created4 = Quiz.objects.get_or_create(
            title='Limits: Concept Understanding',
            quiz_type=Quiz.QuizType.THEORETICAL,
            defaults={
                'subject': Quiz.Subject.CALCULUS_1,
                'topic': 'Limits',
                'evaluation_method': Quiz.EvaluationMethod.SELF_EVAL,  # Self-Eval from the start
                'description': description_4,
                'created_at': timezone.now()
            }
        )

        # Update description and ensure evaluation_method is correct
        if not created4:
            if quiz4.description != description_4 or quiz4.evaluation_method != Quiz.EvaluationMethod.SELF_EVAL:
                quiz4.description = description_4
                quiz4.evaluation_method = Quiz.EvaluationMethod.SELF_EVAL
                quiz4.save()
                self.stdout.write('Updated Quiz 4.')
            self.stdout.write('Quiz 4 already exists.')
        else:
            self.stdout.write(f'Created Quiz: {quiz4.title}')

        # Questions for Quiz 4
        # Note: Using LaTeX for math terms
        questions_data_4 = [
            (1, 'Define what it means for a function to be **differentiable** at $x=c$ in relation to continuity.', 'Differentiability is a stronger condition than continuity. If a function is differentiable at $x=c$, it MUST be continuous there. However, a function can be continuous but NOT differentiable (for example, at a sharp corner like $|x|$ at 0).', None),

            (2, 'Explain why the limit of a constant function, like $f(x) = 7$, is always the constant itself as $x$ approaches any value.', 'Because the function value never changes regardless of what $x$ is doing. The "gap" between $f(x)$ and 7 is always zero, so the limit is 7.', None),

            (3, 'If $\lim_{x \\to c} f(x) = 5$ and $\lim_{x \\to c} g(x) = -2$, what is the limit of $[f(x) \cdot g(x)]$? Which Limit Law applies?', '-10. The Product Law applies: The limit of a product is the product of the limits, provided both individual limits exist.', None),

            (4, 'Describe the "Infinite Limit" behavior. If $\lim_{x \\to c} f(x) = \infty$, is the limit considered to "exist" in the strict sense?', 'Strictly speaking, the limit does not exist (DNE) because it does not settle on a single real number. However, we describe it as "infinity" to be specific about the way in which it fails to exist (unbounded growth).', None),

            (5, 'What is the specific geometric interpretation of the limit: $\lim_{h \\to 0} \\frac{f(x+h) - f(x)}{h}$?', 'This limit represents the slope of the tangent line to the graph of $f$ at the point $x$. It is the definition of the derivative.', None),

            (6, 'Explain how to determine horizontal asymptotes for a rational function where the degree of the numerator is LARGER than the denominator.', 'If the numerator degree > denominator degree, there is no horizontal asymptote. The function goes to positive or negative infinity (or follows a slant asymptote).', None),
            
            (7, 'If $f(x)$ is squeezed between $y = -|x|$ and $y = |x|$, what is the limit of $f(x)$ as $x \\to 0$?', 'The limit is 0. Both $-|x|$ and $|x|$ approach 0 as $x \\to 0$. By the Squeeze Theorem, $f(x)$ must also approach 0.', None),

            (8, 'Why can we not just plug in $x=0$ to evaluate $\lim_{x \\to 0} (\\frac{\\sin x}{x})$?', 'Because $\\sin(0)$ is 0 and $x$ is 0, leading to the indeterminate form $0/0$. Direct substitution fails to give a valid result, requiring geometric proof or L\'Hopital\'s Rule.', None),

            (9, 'Does the Intermediate Value Theorem apply to the function $f(x) = 1/x$ on the interval $[-1, 1]$? Why or why not?', 'No. The IVT requires the function to be continuous on the entire closed interval. $f(x) = 1/x$ has an infinite discontinuity at $x=0$, which is inside $[-1, 1]$, so the theorem fails.', None),

            (10, 'Describe a "Jump Discontinuity".', 'A jump discontinuity occurs when the Left-Hand Limit and Right-Hand Limit both exist as finite numbers, but they are not equal to each other (the graph physically breaks and jumps to a new height).', None)
        ]

        # Delete all existing questions to ensure database matches seed file
        quiz4.question_set.all().delete()
        
        # Create all questions
        for order, text, answer, _ignored in questions_data_4:
            Question.objects.create(
                quiz=quiz4,
                question_order=order,
                question_text=text,
                model_answer=answer,
                accepted_answers=[]
            )
        self.stdout.write(f'Successfully created {len(questions_data_4)} questions for Quiz 4.')


        # ==========================================
        # Quiz 5: Limits: Basic Rules & Properties (Theoretical / Automated)
        # ==========================================
        # Description matches Quiz 2 (Automated)
        description_5 = "Type in the answer directly. These questions are automatically graded to test your precision and recall."

        # Cleanup duplicates for Quiz 5
        qs5 = Quiz.objects.filter(
            title='Limits: Basic Rules & Properties',
            quiz_type=Quiz.QuizType.THEORETICAL,
            evaluation_method=Quiz.EvaluationMethod.AUTOMATED
        )
        if qs5.count() > 1:
            qs5.exclude(pk=qs5.first().pk).delete()
            self.stdout.write('Removed duplicate Quiz 5 entries.')

        quiz5, created5 = Quiz.objects.get_or_create(
            title='Limits: Basic Rules & Properties',
            quiz_type=Quiz.QuizType.THEORETICAL,
            evaluation_method=Quiz.EvaluationMethod.AUTOMATED,
            defaults={
                'subject': Quiz.Subject.CALCULUS_1,
                'topic': 'Limits',
                'description': description_5,
                'created_at': timezone.now()
            }
        )
        
        # Update description for existing quizzes
        if not created5 and quiz5.description != description_5:
            quiz5.description = description_5
            quiz5.save()
            self.stdout.write('Updated description for Quiz 5.')

        if created5:
            self.stdout.write(f'Created Quiz: {quiz5.title}')
        else:
            self.stdout.write('Quiz 5 already exists.')

        # Questions for Quiz 5
        questions_data_5 = [
            (1, 'If the degree of the numerator equals the degree of the denominator, the Horizontal Asymptote is found by dividing the ______ coefficients.', 'leading', ["leading", "front", "first"]),
            
            (2, 'A function is said to be ______ at $x=c$ if you can draw the graph through $x=c$ without lifting your pen.', 'continuous', ["continuous", "connected"]),
            
            (3, 'The limit of $\\frac{\\sin x}{x}$ as $x \\to \\infty$ is ______.', '0', ["0", "zero"]), 
            
            (4, 'If a function oscillates between -1 and 1 as $x \\to 0$ (like $\\sin(1/x)$), the limit ______.', 'does not exist', ["does not exist", "dne", "undefined"]),
            
            (5, 'To remove a rational discontinuity where both top and bottom are zero, we typically ______ the numerator and denominator and cancel terms.', 'factor', ["factor", "factoring"]),
            
            (6, 'The notation $x \\to c^-$ means $x$ is approaching $c$ from the ______ side.', 'left', ["left", "negative", "lesser"]),
            
            (7, 'If $\lim f(x) = L$ and $\lim g(x) = M$, then the limit of $[f(x) + g(x)]$ is equal to ______.', 'L+M', ["l+m", "l + m", "sum", "sum of limits"]),
            
            (8, 'A ______ asymptote occurs when $x$ approaches a finite value $c$ but the function goes to infinity.', 'vertical', ["vertical"]),
            
            (9, 'True or False: The limit of a function at $x=c$ depends on the value of $f(c)$.', 'false', ["false", "no", "f"]),
            
            (10, 'The expression $\\frac{f(x) - f(a)}{x - a}$ is known as the ______ quotient.', 'difference', ["difference"])
        ]

        # Delete all existing questions to ensure database matches seed file
        quiz5.question_set.all().delete()
        
        # Create all questions
        for order, text, answer, accepted in questions_data_5:
            Question.objects.create(
                quiz=quiz5,
                question_order=order,
                question_text=text,
                model_answer=answer,
                accepted_answers=accepted
            )
        self.stdout.write(f'Successfully created {len(questions_data_5)} questions for Quiz 5.')


        # ==========================================
        # Quiz 6: Limits: Advanced Practice (Practical / Self-Eval)
        # ==========================================
        # Description matches Quiz 3 (Practical Self-Eval)
        description_6 = "Solve the problems below. For each question, type your final answer. After submitting, you will see the detailed step-by-step solution. Compare your work honestly and mark yourself correct only if your process and answer align."

        # Cleanup duplicates for Quiz 6
        qs6 = Quiz.objects.filter(
            title='Limits: Advanced Practice',
            quiz_type=Quiz.QuizType.PRACTICAL,
            evaluation_method=Quiz.EvaluationMethod.SELF_EVAL
        )
        if qs6.count() > 1:
            qs6.exclude(pk=qs6.first().pk).delete()
            self.stdout.write('Removed duplicate Quiz 6 entries.')

        quiz6, created6 = Quiz.objects.get_or_create(
            title='Limits: Advanced Practice',
            quiz_type=Quiz.QuizType.PRACTICAL,
            evaluation_method=Quiz.EvaluationMethod.SELF_EVAL,
            defaults={
                'subject': Quiz.Subject.CALCULUS_1,
                'topic': 'Limits',
                'description': description_6,
                'created_at': timezone.now()
            }
        )

        # Update description for existing quizzes
        if not created6 and quiz6.description != description_6:
            quiz6.description = description_6
            quiz6.save()
            self.stdout.write('Updated description for Quiz 6.')

        if created6:
            self.stdout.write(f'Created Quiz: {quiz6.title}')
        else:
            self.stdout.write('Quiz 6 already exists.')

        # Questions for Quiz 6
        questions_data_6 = [
            (1, 
                'Evaluate the limit: $\lim_{x \\to -2} (3x^3 - 5x + 1)$', 
                '-13', 
                'Since this is a polynomial, use Direct Substitution.\n\nCalculation:\n1. $3(-2)^3 - 5(-2) + 1$\n2. $3(-8) + 10 + 1$\n3. $-24 + 11 = -13$.'),
            
            (2, 
                'Evaluate the limit: $\lim_{x \\to 5} \\frac{x^2 - 25}{x - 5}$', 
                '10', 
                'Plugging in 5 gives $0/0$. We must factor.\n\nSteps:\n1. Factor numerator (Difference of Squares): $(x-5)(x+5)$.\n2. Cancel $(x-5)$ from top and bottom.\n3. Limit becomes $\lim_{x \\to 5} (x+5)$.\n4. Substitute 5: $5 + 5 = 10$.'),
            
            (3, 
                'Evaluate the limit: $\lim_{x \\to 9} \\frac{\\sqrt{x} - 3}{x - 9}$', 
                '1/6', 
                'Plugging in 9 gives $0/0$. Use the conjugate.\n\nSteps:\n1. Multiply by $\\frac{\\sqrt{x} + 3}{\\sqrt{x} + 3}$.\n2. Numerator becomes $x - 9$.\n3. Denominator becomes $(x-9)(\\sqrt{x}+3)$.\n4. Cancel $(x-9)$: Limit is $\\frac{1}{\\sqrt{x}+3}$.\n5. Plug in 9: $\\frac{1}{\\sqrt{9}+3} = \\frac{1}{3+3} = 1/6$.'),
            
            (4, 
                'Evaluate the limit at infinity: $\lim_{x \\to \\infty} \\frac{10x^3 - 2}{5x^3 + x^2 + 100}$', 
                '2', 
                'Degrees are equal (both are $x^3$).\n\nMethod:\n1. Identify leading coefficients: 10 for numerator, 5 for denominator.\n2. Divide: $10 / 5 = 2$.\n3. (Alternatively divide every term by $x^3$ and observe smaller terms go to 0).'),
            
            (5, 
                'Evaluate the trig limit: $\lim_{x \\to 0} \\frac{\\sin(2x)}{\\sin(3x)}$', 
                '2/3', 
                'Use the identity $\lim \\frac{\\sin(kx)}{kx} = 1$.\n\nSteps:\n1. Rewrite as $\\frac{\\sin(2x)}{2x} \\cdot 2x \\cdot \\frac{3x}{\\sin(3x)} \\cdot \\frac{1}{3x}$.\n2. The trig parts go to 1.\n3. The $x$s cancel, leaving $2/3$.'),
            
            (6, 
                'Find the Right-Hand Limit: $\lim_{x \\to 0^+} \\frac{1}{x}$', 
                'Positive Infinity', 
                'As $x$ approaches 0 from the positive side (e.g., $x=0.1, x=0.01$), the fraction $1/x$ becomes very large (10, 100). The values grow without bound towards positive infinity.'),
            
            (7, 
                'Evaluate the limit: $\lim_{x \\to 1} \\frac{\\frac{1}{x+1} - \\frac{1}{2}}{x - 1}$', 
                '-1/4', 
                'Common denominator strategy.\n\nSteps:\n1. Combine top fractions: $\\frac{2 - (x+1)}{2(x+1)} = \\frac{1-x}{2(x+1)}$.\n2. Note that $1-x = -(x-1)$.\n3. Cancel $(x-1)$ with denominator.\n4. Result is $\\frac{-1}{2(x+1)}$.\n5. Plug in $x=1$: $\\frac{-1}{2(2)} = -1/4$.'),
            
            (8, 
                'Evaluate the limit at infinity: $\lim_{x \\to \\infty} \\frac{\\sin(x)}{x}$', 
                '0', 
                'Squeeze Theorem application.\n\nReasoning:\n1. We know $-1 \\le \\sin(x) \\le 1$.\n2. Divide by $x$: $-\\frac{1}{x} \\le \\frac{\\sin(x)}{x} \\le \\frac{1}{x}$.\n3. As $x \\to \\infty$, both $-\\frac{1}{x}$ and $\\frac{1}{x}$ go to 0.\n4. Therefore, the middle term must go to 0.'),
            
            (9, 
                'Evaluate the limit: $\lim_{x \\to 0} \\frac{1 - \\cos(x)}{x}$', 
                '0', 
                'This is a standard trigonometric limit, often proven using conjugates.\n\nSteps:\n1. Multiply by $(1+\\cos x)$.\n2. Numerator becomes $1-\\cos^2 x = \\sin^2 x$.\n3. Rewrite as $(\\frac{\\sin x}{x}) \\cdot \\sin x \\cdot \\frac{1}{1+\\cos x}$.\n4. Limit is $1 \\cdot 0 \\cdot (1/2) = 0$.'),
            
            (10, 
                'Given $f(x) = x^2$ for $x \\neq 2$ and $f(2) = 10$. What is $\lim_{x \\to 2} f(x)$?', 
                '4', 
                'The limit depends on the values approaching 2, not the value AT 2.\n\nReasoning:\n1. As $x$ gets close to 2 (but is not 2), $f(x) = x^2$.\n2. $2^2 = 4$.\n3. The fact that $f(2)=10$ is a discontinuity, but it does not change the limit.')
        ]

        # Delete all existing questions to ensure database matches seed file
        quiz6.question_set.all().delete()
        
        # Create all questions
        for order, text, answer, explanation in questions_data_6:
            Question.objects.create(
                quiz=quiz6,
                question_order=order,
                question_text=text,
                model_answer=answer,
                explanation=explanation,
                accepted_answers=[]
            )
        self.stdout.write(f'Successfully created {len(questions_data_6)} questions for Quiz 6.')

        # ==========================================
        # Quiz 7: Derivatives: Theoretical Concepts (Theoretical / Self-Eval)
        # ==========================================
        # Description matches Quiz 1 (Self-Eval Theoretical)
        description_7 = "Write your answer in your own words, then compare it to the model answer. Remember, this exercise is built on trust and personal responsibility. Marking incorrect answers as right mimics progress but hinders true understanding. Embrace the learning process—honesty here is the foundation of your growth."

        qs7 = Quiz.objects.filter(
            title='Derivatives: Theoretical Concepts',
            quiz_type=Quiz.QuizType.THEORETICAL,
            evaluation_method=Quiz.EvaluationMethod.SELF_EVAL
        )
        if qs7.count() > 1:
            qs7.exclude(pk=qs7.first().pk).delete()
            self.stdout.write('Removed duplicate Quiz 7 entries.')

        quiz7, created7 = Quiz.objects.get_or_create(
            title='Derivatives: Theoretical Concepts',
            quiz_type=Quiz.QuizType.THEORETICAL,
            evaluation_method=Quiz.EvaluationMethod.SELF_EVAL,
            defaults={
                'subject': Quiz.Subject.CALCULUS_1,
                'topic': 'Derivatives',
                'description': description_7,
                'created_at': timezone.now()
            }
        )
        
        if not created7 and quiz7.description != description_7:
            quiz7.description = description_7
            quiz7.save()
            self.stdout.write('Updated description for Quiz 7.')

        if created7:
            self.stdout.write(f'Created Quiz: {quiz7.title}')
        else:
            self.stdout.write('Quiz 7 already exists.')

        questions_data_7 = [
            (1, 'State the formal **Limit Definition of the Derivative** of a function $f(x)$.', 
             '$f\'(x) = \lim_{h \\to 0} \\frac{f(x+h) - f(x)}{h}$. (Alternatively, the alternate form using $x \\to a$ is also acceptable).', None),

            (2, 'Explain the geometric relationship between a **Secant Line** and a **Tangent Line**.', 
             'A secant line connects two distinct points on a curve. A tangent line is the limiting position of the secant line as the two points get infinitely close to each other. The slope of the secant approaches the slope of the tangent.', None),

            (3, 'If a function is **Differentiable** at a point, must it be **Continuous** at that point? Explain why.', 
             'Yes. For the derivative to exist, the graph must be smooth and connected. If there were a break (discontinuity), the "rise" would be non-zero while the "run" approaches zero, or the limits wouldn\'t match, making the derivative undefined.', None),

            (4, 'Give two examples of visual features on a graph where a function is **Continuous but NOT Differentiable**.', 
             '1. A sharp corner or "cusp" (like $|x|$ at 0).\n2. A vertical tangent line (where the slope is infinite).', None),
            
            # Interleaving: Limits
            (5, 'Explain why the limit $\lim_{x \to 0} \frac{1}{x}$ does not exist.', 
             'As $x$ approaches 0 from the right, the value goes to positive infinity. As $x$ approaches 0 from the left, it goes to negative infinity. Since the left and right behaviors do not match (and are unbounded), the limit DNE.', None),

            (6, 'If the derivative $f\'(x)$ is **positive** over an interval, what does this tell you about the behavior of the original function $f(x)$?', 
             'It means the function $f(x)$ is increasing (going up from left to right) over that interval.', None),

            (7, 'What does the **Second Derivative** $f\'\'(x)$ tell us about the shape of the graph of $f(x)$?', 
             'It describes the concavity. If $f\'\' > 0$, the graph is concave up (like a cup). If $f\'\' < 0$, the graph is concave down (like a frown).', None),

            (8, 'Explain the difference between **Average Rate of Change** and **Instantaneous Rate of Change**.', 
             'Average Rate of Change is calculated over a time interval (slope of secant). Instantaneous Rate of Change is calculated at a single specific moment (slope of tangent, using a limit).', None),

            # INTERLEAVING: LIMITS
            (9, 'What is the primary difference between evaluating a limit and evaluating a function value?', 
             'The function value $f(c)$ depends on what happens exactly AT $x=c$. The limit depends on what happens NEAR $x=c$. They can be completely different (e.g., if there is a hole).', None),

            (10, 'In the Leibniz notation $\\frac{dy}{dx}$, is this symbol literally a fraction? Explain.', 
             'Not literally. It represents the limit of the fraction $\\frac{\\Delta y}{\\Delta x}$ as $\\Delta x$ approaches zero. However, in methods like separation of variables or differentials, we often treat it algebraically *like* a fraction.', None),

            (11, 'Conceptually, why is the derivative of a **Constant Function** equal to zero?', 
             'Geometrically, a constant function is a horizontal line. Horizontal lines have a slope of 0 everywhere, so the rate of change is always 0.', None),

            (12, 'Why do we need the **Chain Rule**? What specific type of functions does it apply to?', 
             'We need it to differentiate **composite functions** (functions inside other functions, like $f(g(x))$). It allows us to multiply the rate of change of the outer function by the rate of change of the inner function.', None),
        ]

        # Delete all existing questions to ensure database matches seed file
        quiz7.question_set.all().delete()
        
        # Create all questions
        for order, text, answer, _ignored in questions_data_7:
            Question.objects.create(
                quiz=quiz7,
                question_order=order,
                question_text=text,
                model_answer=answer,
                accepted_answers=[]
            )
        self.stdout.write(f'Successfully created {len(questions_data_7)} questions for Quiz 7.')


        # ==========================================
        # Quiz 8: Derivatives: Basic Rules & Properties (Theoretical / Automated)
        # ==========================================
        # Description matches Quiz 2 (Automated)
        description_8 = "Type in the answer directly. These questions are automatically graded to test your precision and recall."

        qs8 = Quiz.objects.filter(
            title='Derivatives: Basic Rules & Properties',
            quiz_type=Quiz.QuizType.THEORETICAL,
            evaluation_method=Quiz.EvaluationMethod.AUTOMATED
        )
        if qs8.count() > 1:
            qs8.exclude(pk=qs8.first().pk).delete()
            self.stdout.write('Removed duplicate Quiz 8 entries.')

        quiz8, created8 = Quiz.objects.get_or_create(
            title='Derivatives: Basic Rules & Properties',
            quiz_type=Quiz.QuizType.THEORETICAL,
            evaluation_method=Quiz.EvaluationMethod.AUTOMATED,
            defaults={
                'subject': Quiz.Subject.CALCULUS_1,
                'topic': 'Derivatives',
                'description': description_8,
                'created_at': timezone.now()
            }
        )
        
        if not created8 and quiz8.description != description_8:
            quiz8.description = description_8
            quiz8.save()
            self.stdout.write('Updated description for Quiz 8.')

        if created8:
            self.stdout.write(f'Created Quiz: {quiz8.title}')
        else:
            self.stdout.write('Quiz 8 already exists.')

        questions_data_8 = [
            (1, 'The line that best approximates the slope of a curve at a single point is called the ______ line.', 'tangent', ["tangent"]),
            
            (2, 'The process of finding a derivative is called ______.', 'differentiation', ["differentiation", "differentiating"]),
            
            (3, 'If the graph of $f(x)$ has a sharp corner (like the letter V) at $x=c$, then $f\'(c)$ is ______.', 'undefined', ["undefined", "dne", "does not exist", "non-existent"]),
            
            (4, 'The Power Rule states that the derivative of $x^n$ is ______.', 'nx^(n-1)', ["nx^(n-1)", "nx^n-1", "n*x^(n-1)"]),
            
            (5, 'If $f(x)$ represents position, then $f\'(x)$ represents ______.', 'velocity', ["velocity", "speed"]),
            
            (6, 'If $f(x)$ represents velocity, then $f\'(x)$ (the derivative of velocity) represents ______.', 'acceleration', ["acceleration"]),
            
            # INTERLEAVING: LIMITS
            (7, 'To prove that the limit of sin(x)/x is 0 as x approaches infinity (since sine is bounded), we must use the ______ Theorem.', 'squeeze', ["squeeze", "sandwich", "pinching"]),
            
            (8, 'Differentiation of a function defined by an equation where $y$ cannot be easily isolated (e.g., $x^2 + y^2 = 25$) is called ______ differentiation.', 'implicit', ["implicit"]),
            
            (9, 'If the derivative f\'(c) exists (is a real number), then the function f must be ______ at x=c.', 'continuous', ["continuous"]),
            
            (10, 'The theorem that guarantees a point where the instantaneous velocity equals the average velocity (assuming smoothness) is called the ______ Value Theorem.', 'mean', ["mean", "mvt"]),

            (11, 'A line perpendicular to the tangent line at the point of tangency is called the ______ line.', 'normal', ["normal"]),
            
            # INTERLEAVING: LIMITS
            (12, 'If the degree of the numerator is exactly one greater than the degree of the denominator, the function approaches a ______ asymptote.', 'slant', ["slant", "oblique"]),
        ]

        # Delete all existing questions to ensure database matches seed file
        quiz8.question_set.all().delete()
        
        # Create all questions
        for order, text, answer, accepted in questions_data_8:
            Question.objects.create(
                quiz=quiz8,
                question_order=order,
                question_text=text,
                model_answer=answer,
                accepted_answers=accepted
            )
        self.stdout.write(f'Successfully created {len(questions_data_8)} questions for Quiz 8.')


        # ==========================================
        # Quiz 9: Derivatives: Practical Skills (Practical / Self-Eval)
        # ==========================================
        description_9 = "Solve the problems below. For each question, type your final answer. After submitting, you will see the detailed step-by-step solution. Compare your work honestly and mark yourself correct only if your process and answer align."
        
        qs9 = Quiz.objects.filter(
            title='Derivatives: Practical Skills',
            quiz_type=Quiz.QuizType.PRACTICAL,
            evaluation_method=Quiz.EvaluationMethod.SELF_EVAL
        )
        if qs9.count() > 1:
            qs9.exclude(pk=qs9.first().pk).delete()
            self.stdout.write('Removed duplicate Quiz 9 entries.')

        quiz9, created9 = Quiz.objects.get_or_create(
            title='Derivatives: Practical Skills',
            quiz_type=Quiz.QuizType.PRACTICAL,
            evaluation_method=Quiz.EvaluationMethod.SELF_EVAL,
            defaults={
                'subject': Quiz.Subject.CALCULUS_1,
                'topic': 'Derivatives',
                'description': description_9,
                'created_at': timezone.now()
            }
        )

        if not created9 and quiz9.description != description_9:
            quiz9.description = description_9
            quiz9.save()
            self.stdout.write('Updated description for Quiz 9.')

        if created9:
            self.stdout.write(f'Created Quiz: {quiz9.title}')
        else:
            self.stdout.write('Quiz 9 already exists.')

        
        questions_data_9 = [
            (1, 
             'Evaluate the limit: $\\lim_{x \\to 3} \\frac{x^2 - 9}{x - 3}$', 
             '6', 
             'Direct substitution gives 0/0. Factor the numerator: $(x-3)(x+3)$. Cancel the $(x-3)$ terms. Evaluate $x+3$ at $x=3$, which gives $3+3=6$.'),

            (2, 
             'Find the derivative $f\'(x)$ for the function $f(x) = 5x^3 - 2x + 10$.', 
             '15x^2 - 2', 
             'Use the Power Rule $\\frac{d}{dx}(ax^n) = anx^{n-1}$.\n1. For $5x^3$: $3 \\cdot 5x^{2} = 15x^2$.\n2. For $-2x$: The derivative is $-2$.\n3. For $10$: The derivative of a constant is 0.'),

            (3, 
             'Evaluate this limit by recognizing it as the definition of a derivative: $\\lim_{h \\to 0} \\frac{(x+h)^2 - x^2}{h}$', 
             '2x', 
             'Do not expand the algebra. Recognize that this structure is the Limit Definition of the Derivative for the function $f(x) = x^2$. The derivative of $x^2$ is simply $2x$.'),

            (4, 
             'Find the derivative of $y = x^2 \\sin(x)$.', 
             '2x sin(x) + x^2 cos(x)', 
             'Use the Product Rule: $(uv)\' = u\'v + uv\'$.\nHere $u=x^2$ (so $u\'=2x$) and $v=\\sin(x)$ (so $v\'=\\cos(x)$).\nCombine: $(2x)(\\sin x) + (x^2)(\\cos x)$.'),

            (5, 
             'What is the slope of the tangent line to the curve $y = \\sqrt{x}$ at the point where $x = 4$?', 
             '1/4', 
             '1. Find the derivative: $y = x^{1/2}$, so $y\' = \\frac{1}{2}x^{-1/2} = \\frac{1}{2\\sqrt{x}}$.\n2. Plug in $x=4$: $\\frac{1}{2\\sqrt{4}} = \\frac{1}{2(2)} = 1/4$.'),

            (6, 
             'Differentiate using the Chain Rule: $y = (3x^2 + 1)^5$.', 
             '30x(3x^2 + 1)^4', 
             'Identify Outer function $(\\dots)^5$ and Inner function $(3x^2+1)$.\n1. Deriv of Outer: $5(3x^2+1)^4$.\n2. Deriv of Inner: $6x$.\n3. Multiply: $5(3x^2+1)^4 \\cdot 6x = 30x(3x^2+1)^4$.'),

            (7, 
             'Evaluate $\\lim_{x \\to \\infty} \\frac{4x^2 - x}{2x^2 + 5}$.', 
             '2', 
             'Compare degrees. Both are $x^2$. Therefore, the limit is the ratio of the leading coefficients: $4/2 = 2$.'),

            (8, 
             'Find the derivative of the quotient: $y = \\frac{x}{x+1}$.', 
             '1 / (x+1)^2', 
             'Use Quotient Rule: $\\frac{u\'v - uv\'}{v^2}$.\n$u=x, u\'=1$. $v=x+1, v\'=1$.\nNumerator: $1(x+1) - x(1) = x + 1 - x = 1$.\nDenominator: $(x+1)^2$.'),

            (9, 
             'A particle\'s position is given by $s(t) = t^2 - 4t + 3$. What is its **velocity** at $t = 5$?', 
             '6', 
             'Velocity is the derivative of position.\n1. $v(t) = s\'(t) = 2t - 4$.\n2. Evaluate at $t=5$: $2(5) - 4 = 10 - 4 = 6$.'),

            (10, 
             'Find the derivative of $y = \sin^3(2x)$.', 
             '6sin^2(2x)cos(2x)', 
             'Use Chain Rule twice.\nOuter: $u^3 \\to 3u^2$.\nInner 1: $\\sin(v) \\to \\cos(v)$.\nInner 2: $2x \\to 2$.\n\nMultiply: $3(\\sin(2x))^2 \\cdot \\cos(2x) \\cdot 2 = 6\\sin^2(2x)\\cos(2x)$.'),

            (11, 
             'At which x-value is the function $f(x) = |x - 2|$ **NOT** differentiable? Why?', 
             '2', 
             'The graph of $|x-2|$ is a V-shape shifted to $x=2$. At the tip of the V ($x=2$), there is a sharp corner (cusp). Derivatives are undefined at sharp corners.'),

            # Interleaving
            (12, 
             'If $f(x) = e^x$, what is the value of $\\lim_{h \\to 0} \\frac{e^{(0+h)} - e^0}{h}$?', 
             '1', 
             'This limit represents the derivative of $e^x$ at $x=0$.\n1. We know $f\'(x) = e^x$.\n2. Evaluate at $0$: $e^0 = 1$.')
        ]

        quiz9.question_set.all().delete()
        for order, text, answer, explanation in questions_data_9:
            Question.objects.create(
                quiz=quiz9,
                question_order=order,
                question_text=text,
                model_answer=answer,
                explanation=explanation,
                accepted_answers=[]
            )
        self.stdout.write(f'Successfully created {len(questions_data_9)} questions for Quiz 9.')


        # ==========================================
        # Quiz 10: Derivatives: Chain Rule Concepts (Theoretical / Self-Eval)
        # ==========================================
        description_10 = "Write your answer in your own words, then compare it to the model answer. Remember, this exercise is built on trust and personal responsibility. Marking incorrect answers as right mimics progress but hinders true understanding. Embrace the learning process—honesty here is the foundation of your growth."
        
        qs10 = Quiz.objects.filter(
            title='Derivatives: Chain Rule Concepts',
            quiz_type=Quiz.QuizType.THEORETICAL,
            evaluation_method=Quiz.EvaluationMethod.SELF_EVAL
        )
        if qs10.count() > 1:
            qs10.exclude(pk=qs10.first().pk).delete()
            self.stdout.write('Removed duplicate Quiz 10 entries.')

        quiz10, created10 = Quiz.objects.get_or_create(
            title='Derivatives: Chain Rule Concepts',
            quiz_type=Quiz.QuizType.THEORETICAL,
            evaluation_method=Quiz.EvaluationMethod.SELF_EVAL,
            defaults={
                'subject': Quiz.Subject.CALCULUS_1,
                'topic': 'Derivatives',
                'description': description_10,
                'created_at': timezone.now()
            }
        )

        if not created10 and quiz10.description != description_10:
            quiz10.description = description_10
            quiz10.save()
            self.stdout.write('Updated description for Quiz 10.')

        if created10:
            self.stdout.write(f'Created Quiz: {quiz10.title}')
        else:
            self.stdout.write('Quiz 10 already exists.')

        # Original interleaved questions are 11 and 12. 
        # Moving Q11 (Interleaving) to position 6 to separate them.
        questions_data_10 = [
            (1, 
             'Explain the intuitive logic behind the Chain Rule using a "rates of change" analogy (e.g., gears or conversion rates).', 
             'If y changes 3 times as fast as u, and u changes 2 times as fast as x, then y changes 3 * 2 = 6 times as fast as x. We multiply the rates because the effects compound.', None),

            (2, 
             'In the Chain Rule formula $\\frac{dy}{dx} = \\frac{dy}{du} \\cdot \\frac{du}{dx}$, what does the variable $u$ represent?', 
             'The variable $u$ represents the "inner" function. It acts as the output of the first function and the input for the second function.', None),

            (3, 
             'Why is $\\sin(x^2)$ structurally different from $\\sin^2(x)$? How does this change the differentiation process?', 
             'In $\\sin(x^2)$, the squaring happens *inside* to the angle (Outer: sin, Inner: x^2). In $\\sin^2(x)$, the squaring happens *outside* to the whole result (Outer: x^2, Inner: sin). You must peel the layers in the correct order.', None),

            (4, 
             'When applying the Chain Rule to $f(g(h(x)))$, how many derivatives will you end up multiplying together?', 
             'Three. You differentiate the outer layer f, multiply by the derivative of the middle layer g, and multiply by the derivative of the inner layer h.', None),

            (5, 
             'What is the difference between "Implicit Differentiation" and the "Chain Rule"?', 
             'They are actually the same thing. Implicit differentiation is just applying the Chain Rule to the variable y (treating y as an unknown function y(x)) whenever we differentiate a term containing y.', None),

            # Interleaving
            (6, 
             'If $f(x)$ is continuous at $x=c$, does that guarantee that $\\lim_{x \\to c} f(x)$ exists? Why?', 
             'Yes. By definition of continuity, the limit must exist and it must equal the function value f(c).', None),

            (7, 
             'If you know the derivative of $f(x)$ is $f\'(x)$, how do you find the derivative of the inverse function $f^{-1}(x)$ using the Chain Rule?', 
             'You differentiate the identity $f(f^{-1}(x)) = x$. Applying the Chain Rule gives $f\'(f^{-1}(x)) \\cdot (f^{-1})\'(x) = 1$. Then solve for the inverse derivative.', None),

            (8, 
             'In Machine Learning, gradients are calculated "backwards". How does this relate to the Chain Rule?', 
             'The Chain Rule calculates the total rate of change by multiplying local derivatives. Backpropagation computes these products from the last layer (output) back to the first layer (input) to update weights.', None),

            (9, 
             'Why does the derivative of $e^{kx}$ equal $k \\cdot e^{kx}$ instead of just $e^{kx}$?', 
             'Because of the Chain Rule. The outer function is $e^u$ (deriv is $e^u$) and the inner function is $u=kx$ (deriv is k). Multiplying them gives $k e^{kx}$.', None),

            (10, 
             'Describe a "cusp" on a graph. Why does the derivative fail to exist there?', 
             'A cusp is a sharp point where the tangent line becomes vertical or the left-hand slope and right-hand slope are not equal. The limit of the difference quotient does not exist.', None),

            (11, 
             'What is the "Linear Approximation" of a function $f(x)$ at a point $a$?', 
             'It is the equation of the tangent line: $L(x) = f(a) + f\'(a)(x-a)$. It estimates the function values near $x=a$ using the derivative.', None),

            # Interleaving
            (12, 
             'Evaluate the limit of a composite function $\\lim_{x \\to c} f(g(x))$ if both are continuous.', 
             'You can move the limit inside. The result is simply $f(\\lim_{x \\to c} g(x))$, which equals $f(g(c))$.', None)
        ]

        quiz10.question_set.all().delete()
        for order, text, answer, _ignored in questions_data_10:
            Question.objects.create(
                quiz=quiz10,
                question_order=order,
                question_text=text,
                model_answer=answer,
                accepted_answers=[]
            )
        self.stdout.write(f'Successfully created {len(questions_data_10)} questions for Quiz 10.')


        # ==========================================
        # Quiz 11: Derivatives: Chain Rule Practice (Theoretical / Automated)
        # ==========================================
        description_11 = "Type in the answer directly. These questions are automatically graded to test your precision and recall."
        
        qs11 = Quiz.objects.filter(
            title='Derivatives: Chain Rule Practice',
            quiz_type=Quiz.QuizType.THEORETICAL,
            evaluation_method=Quiz.EvaluationMethod.AUTOMATED
        )
        if qs11.count() > 1:
            qs11.exclude(pk=qs11.first().pk).delete()
            self.stdout.write('Removed duplicate Quiz 11 entries.')

        quiz11, created11 = Quiz.objects.get_or_create(
            title='Derivatives: Chain Rule Practice',
            quiz_type=Quiz.QuizType.THEORETICAL,
            evaluation_method=Quiz.EvaluationMethod.AUTOMATED,
            defaults={
                'subject': Quiz.Subject.CALCULUS_1,
                'topic': 'Derivatives',
                'description': description_11,
                'created_at': timezone.now()
            }
        )

        if not created11 and quiz11.description != description_11:
            quiz11.description = description_11
            quiz11.save()
            self.stdout.write('Updated description for Quiz 11.')

        if created11:
            self.stdout.write(f'Created Quiz: {quiz11.title}')
        else:
            self.stdout.write('Quiz 11 already exists.')

        # Original interleaved questions are 11 and 12. 
        # Moving Q11 to position 6.
        questions_data_11 = [
            (1, 'The rule used to differentiate a composite function f(g(x)) is called the ______ Rule.', 'chain', ["chain"]),
            
            (2, 'In the function y = cos(3x), the function "3x" is referred to as the ______ function.', 'inner', ["inner", "inside"]),
            
            (3, 'If y = f(u) and u = g(x), then dy/dx is the ______ of dy/du and du/dx.', 'product', ["product", "multiplication"]),
            
            (4, 'The derivative of ln(u) with respect to x is (1/u) multiplied by ______.', 'u\'', ["u'", "du/dx", "derivative of u"]),
            
            (5, 'The notation f\'(g(x)) * g\'(x) represents the derivative of the ______ function f(g(x)).', 'composite', ["composite", "composition"]),

            # Interleaving
            (6, 'If a limit evaluates to infinity/infinity, we can often simplify the limit by dividing by the highest ______ of x.', 'power', ["power", "degree", "exponent"]),
            
            (7, 'When differentiating sin^3(x), the first rule you apply is the ______ Rule.', 'power', ["power"]),
            
            (8, 'If f(x) and g(x) are inverses, their graphs are reflections of each other across the line y = ______.', 'x', ["x"]),
            
            (9, 'The derivative of the natural exponential function e^x is ______.', 'e^x', ["e^x", "ex", "itself"]),
            
            (10, 'A function is strictly ______ on an interval if its derivative is always positive there.', 'increasing', ["increasing"]),
            
            (11, 'Linear approximation uses the tangent line to estimate function values ______ the point of tangency.', 'near', ["near", "close to", "around"]),

            # Interleaving
            (12, 'The limit of a constant k as x approaches infinity is ______.', 'k', ["k", "constant"])
        ]

        quiz11.question_set.all().delete()
        for order, text, answer, accepted in questions_data_11:
            Question.objects.create(
                quiz=quiz11,
                question_order=order,
                question_text=text,
                model_answer=answer,
                accepted_answers=accepted
            )
        self.stdout.write(f'Successfully created {len(questions_data_11)} questions for Quiz 11.')

        # ==========================================
        # Quiz 12: Applications of Derivatives: Theoretical Concepts (Theoretical / Self-Eval)
        # ==========================================
        description_12 = "Write your answer in your own words, then compare it to the model answer. Remember, this exercise is built on trust and personal responsibility. Marking incorrect answers as right mimics progress but hinders true understanding. Embrace the learning process—honesty here is the foundation of your growth."
        
        qs12 = Quiz.objects.filter(
            title='Applications of Derivatives: Theoretical Concepts',
            quiz_type=Quiz.QuizType.THEORETICAL,
            evaluation_method=Quiz.EvaluationMethod.SELF_EVAL
        )
        if qs12.count() > 1:
            qs12.exclude(pk=qs12.first().pk).delete()
            self.stdout.write('Removed duplicate Quiz 12 entries.')

        quiz12, created12 = Quiz.objects.get_or_create(
            title='Applications of Derivatives: Theoretical Concepts',
            quiz_type=Quiz.QuizType.THEORETICAL,
            evaluation_method=Quiz.EvaluationMethod.SELF_EVAL,
            defaults={
                'subject': Quiz.Subject.CALCULUS_1,
                'topic': 'Applications of Derivatives',
                'description': description_12,
                'created_at': timezone.now()
            }
        )

        if not created12 and quiz12.description != description_12:
            quiz12.description = description_12
            quiz12.save()
            self.stdout.write('Updated description for Quiz 12.')

        if created12:
            self.stdout.write(f'Created Quiz: {quiz12.title}')
        else:
            self.stdout.write('Quiz 12 already exists.')

        questions_data_12 = [
            (1, 
             'Explain why a **Critical Point** (where f\'(c)=0) is a *candidate* for a local maximum or minimum, but not a guarantee. Give a counter-example.', 
             'A derivative of zero means the tangent is horizontal, but the function could flatten out and then continue going up (like y = x^3 at x=0). This is called a "saddle point" or inflection point, not a max/min.', None),

            (2, 
             'State **Rolle\'s Theorem**. How is it a special case of the Mean Value Theorem?', 
             'Rolle\'s Theorem states that if f(a) = f(b), there must be a point between them where f\'(c) = 0. This is just the MVT where the average rate of change is zero (the secant line is horizontal).', None),

            # Interleaved 3 -> Position 3
            (3, 
             'Interleaving: Explain why the derivative of ln(x) cannot exist for x < 0.', 
             'Because the natural logarithm ln(x) is not defined for negative numbers (domain restriction). You cannot have a slope where the graph does not exist.', None),

            (4, 
             'Explain the **First Derivative Test**. How do you use the *signs* of f\'(x) to classify a critical point?', 
             'You check the sign of f\'(x) on both sides of the critical point. If f\' changes from Positive to Negative, it\'s a Peak (Max). If it changes from Negative to Positive, it\'s a Valley (Min).', None),

            (5, 
             'Geometrically, what does it mean for a function to be **Concave Up**? Relate this to the tangent lines.', 
             'Concave Up means the graph opens upward (like a cup). Geometrically, the graph lies *above* its tangent lines, and the slopes of the tangent lines are increasing.', None),

            # Interleaved 6 -> Position 6
            (6, 
             'Interleaving: Differentiate y = sin(x) * cos(x) using two different methods (Product Rule vs. Identity).', 
             'Method 1 (Product): cos(x)cos(x) - sin(x)sin(x) = cos(2x). Method 2 (Identity): Rewrite as 0.5sin(2x). Deriv is 0.5 * cos(2x) * 2 = cos(2x).', None),

            (7, 
             'Why does the **Second Derivative Test** work? (i.e., Why does f\'\'(c) < 0 imply a Maximum?)', 
             'If f\'\'(c) < 0, the function is Concave Down (frowning). A horizontal tangent (f\'=0) at the top of a frown must be a Peak (Maximum).', None),

            (8, 
             'What is an **Inflection Point**? strictly in terms of the second derivative.', 
             'An inflection point is a point where the second derivative f\'\'(x) *changes sign* (from positive to negative or vice versa). It is not enough for f\'\' to just be zero.', None),

            # Interleaved 9 -> Position 9
            (9, 
             'Interleaving: If lim_{x->inf} f(x) = 5, what does this tell us about the graph of f\'(x) (the derivative) as x approaches infinity?', 
             'If the function flattens out to a horizontal asymptote y=5, the slope (derivative) must approach 0.', None),

            (10, 
             'When applying **L\'Hôpital\'s Rule**, why must we check that the limit is an "Indeterminate Form" first?', 
             'Because if the limit is determinate (like 5/0 or 0/5), L\'Hôpital\'s Rule gives the wrong answer. It only works when there is a "struggle" between numerator and denominator (0/0 or inf/inf).', None),

            (11, 
             'What does the "+ C" represent when finding the **General Antiderivative**? Why is it geometrically necessary?', 
             'It represents the "Constant of Integration." Geometrically, it means a family of vertically shifted curves. Since the derivative (slope) is the same regardless of vertical height, we must account for all possible vertical starting positions.', None),

            (12, 
             'How does **Optimization** (finding global max/min) on a *closed* interval [a, b] differ from an *open* interval?', 
             'On a closed interval, you MUST check the endpoints (f(a) and f(b)) in addition to the critical points. The absolute max/min could occur at the very edge of the domain.', None)
        ]

        quiz12.question_set.all().delete()
        for order, text, answer, _ignored in questions_data_12:
            Question.objects.create(
                quiz=quiz12,
                question_order=order,
                question_text=text,
                model_answer=answer,
                accepted_answers=[]
            )
        self.stdout.write(f'Successfully created {len(questions_data_12)} questions for Quiz 12.')


        # ==========================================
        # Quiz 13: Applications of Derivatives: Basic Rules & Properties (Theoretical / Automated)
        # ==========================================
        description_13 = "Type in the answer directly. These questions are automatically graded to test your precision and recall."
        
        qs13 = Quiz.objects.filter(
            title='Applications of Derivatives: Basic Rules & Properties',
            quiz_type=Quiz.QuizType.THEORETICAL,
            evaluation_method=Quiz.EvaluationMethod.AUTOMATED
        )
        if qs13.count() > 1:
            qs13.exclude(pk=qs13.first().pk).delete()
            self.stdout.write('Removed duplicate Quiz 13 entries.')

        quiz13, created13 = Quiz.objects.get_or_create(
            title='Applications of Derivatives: Basic Rules & Properties',
            quiz_type=Quiz.QuizType.THEORETICAL,
            evaluation_method=Quiz.EvaluationMethod.AUTOMATED,
            defaults={
                'subject': Quiz.Subject.CALCULUS_1,
                'topic': 'Applications of Derivatives',
                'description': description_13,
                'created_at': timezone.now()
            }
        )

        if not created13 and quiz13.description != description_13:
            quiz13.description = description_13
            quiz13.save()
            self.stdout.write('Updated description for Quiz 13.')

        if created13:
            self.stdout.write(f'Created Quiz: {quiz13.title}')
        else:
            self.stdout.write('Quiz 13 already exists.')

        questions_data_13 = [
            (1, 'A point in the domain of f where f\'(x) = 0 or f\'(x) is undefined is called a ______ point.', 'critical', ["critical"]),

            (2, 'According to the Mean Value Theorem, there is a point c where the instantaneous rate of change equals the ______ rate of change.', 'average', ["average"]),

            (3, 'Interleaving: Implicit differentiation is required when y is not explicitly defined as a function of ______.', 'x', ["x"]),

            (4, 'If f\'(x) > 0 on an interval, then f(x) is strictly ______ on that interval.', 'increasing', ["increasing"]),

            (5, 'The graph of f is Concave Down on intervals where the second derivative f\'\'(x) is ______.', 'negative', ["negative", "less than zero", "< 0"]),

            (6, 'Interleaving: The derivative of arcsin(x) involves a square ______ in the denominator.', 'root', ["root", "radical"]),

            (7, 'A point where the concavity of a function changes is called a point of ______.', 'inflection', ["inflection"]),

            (8, 'To apply L\'Hôpital\'s Rule to a limit of the form 0 * infinity, you must first rewrite it as a ______.', 'fraction', ["fraction", "ratio", "quotient"]),

            (9, 'Interleaving: A vertical asymptote at x=c implies that the limit as x approaches c is ______.', 'infinity', ["infinity", "infinite", "inf"]),

            (10, 'If f\'(c) = 0 and f\'\'(c) > 0, then f(c) is a local ______.', 'minimum', ["minimum", "min"]),

            (11, 'The family of all functions F(x) such that F\'(x) = f(x) is called the ______ integral of f.', 'indefinite', ["indefinite"]),

            (12, 'A function that is continuous on a closed interval [a, b] is guaranteed to have an absolute maximum and minimum by the ______ Value Theorem.', 'extreme', ["extreme", "evt"])
        ]

        quiz13.question_set.all().delete()
        for order, text, answer, accepted in questions_data_13:
            Question.objects.create(
                quiz=quiz13,
                question_order=order,
                question_text=text,
                model_answer=answer,
                accepted_answers=accepted
            )
        self.stdout.write(f'Successfully created {len(questions_data_13)} questions for Quiz 13.')


        # ==========================================
        # Quiz 14: Applications of Derivatives: Practical Skills (Practical / Self-Eval)
        # ==========================================
        description_14 = "Solve the problems below. For each question, type your final answer. After submitting, you will see the detailed step-by-step solution. Compare your work honestly and mark yourself correct only if your process and answer align."
        
        qs14 = Quiz.objects.filter(
            title='Applications of Derivatives: Practical Skills',
            quiz_type=Quiz.QuizType.PRACTICAL,
            evaluation_method=Quiz.EvaluationMethod.SELF_EVAL
        )
        if qs14.count() > 1:
            qs14.exclude(pk=qs14.first().pk).delete()
            self.stdout.write('Removed duplicate Quiz 14 entries.')

        quiz14, created14 = Quiz.objects.get_or_create(
            title='Applications of Derivatives: Practical Skills',
            quiz_type=Quiz.QuizType.PRACTICAL,
            evaluation_method=Quiz.EvaluationMethod.SELF_EVAL,
            defaults={
                'subject': Quiz.Subject.CALCULUS_1,
                'topic': 'Applications of Derivatives',
                'description': description_14,
                'created_at': timezone.now()
            }
        )

        if not created14 and quiz14.description != description_14:
            quiz14.description = description_14
            quiz14.save()
            self.stdout.write('Updated description for Quiz 14.')

        if created14:
            self.stdout.write(f'Created Quiz: {quiz14.title}')
        else:
            self.stdout.write('Quiz 14 already exists.')

        questions_data_14 = [
            (1, 
             'Find the critical points of $f(x) = 2x^3 - 9x^2 + 12x$.', 
             'x = 1 and x = 2', 
             '1. Find $f\'(x) = 6x^2 - 18x + 12$.\n2. Set to 0: $6(x^2 - 3x + 2) = 0$.\n3. Factor: $6(x-1)(x-2) = 0$.\n4. Critical points at $x=1, x=2$.'),

            (2, 
             'Determine the intervals where $f(x) = x^3 - 12x$ is **Decreasing**.', 
             '(-2, 2)', 
             '1. $f\'(x) = 3x^2 - 12$.\n2. Critical points: $3(x^2 - 4) = 0 \\to x = \\pm 2$.\n3. Test intervals: For $x=0$ (between -2 and 2), $f\'(0) = -12$ (Negative).\n4. Since $f\' < 0$, it is decreasing on $(-2, 2)$.'),

            (3, 
             'Interleaving: Find the slope of the tangent line to $x^2 + y^2 = 25$ at $(3, 4)$ using Implicit Differentiation.', 
             '-3/4', 
             '1. Differentiate: $2x + 2y y\' = 0$.\n2. Solve for $y\': y\' = -x/y$.\n3. Plug in $(3,4): -3/4$.'),

            (4, 
             'Apply the Mean Value Theorem to $f(x) = x^2$ on $[0, 4]$. Find the value $c$.', 
             'c = 2', 
             '1. Average slope: $(f(4)-f(0))/(4-0) = (16-0)/4 = 4$.\n2. Instantaneous slope: $f\'(c) = 2c$.\n3. Set equal: $2c = 4 \\to c = 2$.'),

            (5, 
             'Use the **Second Derivative Test** to classify the critical point $x=0$ for $f(x) = 1 - x^2$.', 
             'Local Maximum', 
             '1. $f\'(x) = -2x$. Critical point at $x=0$.\n2. $f\'\'(x) = -2$.\n3. Evaluate: $f\'\'(0) = -2$ (Negative).\n4. Negative concavity means a frown, so it is a Maximum.'),

            (6, 
             'Interleaving: Differentiate $y = x^x$ (Hint: Use Logarithmic Differentiation).', 
             'x^x (1 + ln(x))', 
             '1. $\\ln y = x \\ln x$.\n2. $y\'/y = 1 \\cdot \\ln x + x(1/x) = \\ln x + 1$.\n3. $y\' = y(\\ln x + 1) = x^x(1 + \\ln x)$.'),

            (7, 
             'Evaluate using L\'Hôpital\'s Rule: $\\lim_{x \\to 0} \\frac{e^x - 1 - x}{x^2}$.', 
             '1/2', 
             '1. Check: $e^0 - 1 - 0 = 0$ and $0^2 = 0$. Form 0/0.\n2. L\'Hopital 1: $\\frac{e^x - 1}{2x}$. Check: $0/0$ again.\n3. L\'Hopital 2: $\\frac{e^x}{2}$.\n4. Evaluate: $e^0 / 2 = 1/2$.'),

            (8, 
             'Find the general antiderivative of: $3x^2 + \\sin x$.', 
             'x^3 - cos(x) + C', 
             '1. Power rule reversed for $3x^2$: $\\frac{3x^3}{3} = x^3$.\n2. Trig rule reversed for $\\sin x$: The deriv of $-\\cos x$ is $\\sin x$, so antideriv is $-\\cos x$.\n3. Add + C.'),

            (9, 
             'Interleaving: Evaluate $\\lim_{x \\to \\infty} \\frac{\\ln x}{x}$ using L\'Hôpital\'s Rule concepts.', 
             '0', 
             'Logarithms grow much slower than polynomials. Using L\'Hopital: Deriv top is $1/x$, Deriv bottom is 1. Limit $(1/x)/1$ as $x \\to \\infty$ is 0.'),

            (10, 
             'Find the point of **inflection** for $f(x) = x^3 - 6x^2$.', 
             'x = 2', 
             '1. $f\'(x) = 3x^2 - 12x$.\n2. $f\'\'(x) = 6x - 12$.\n3. Set $f\'\' = 0 \\to 6x = 12 \\to x = 2$.\n4. Check sign change: $f\'\'(1) = -6$, $f\'\'(3) = +6$. Signs change, so it is an inflection point.'),

            (11, 
             'Find the absolute maximum of $f(x) = x^2 - 4x$ on the interval $[0, 5]$.', 
             '5 (at x=5)', 
             '1. Critical pt: $2x - 4 = 0 \\to x=2$.\n2. Check Endpoints and Critical pt:\n   f(0) = 0\n   f(2) = 4 - 8 = -4\n   f(5) = 25 - 20 = 5\n3. Max is 5.'),

            (12, 
             'Find $f(x)$ if $f\'(x) = 4x + 1$ and $f(0) = 3$.', 
             '2x^2 + x + 3', 
             '1. Integrate $4x + 1$ to get $2x^2 + x + C$.\n2. Use condition $f(0) = 3$: $2(0)^2 + 0 + C = 3 \\to C = 3$.\n3. Final: $2x^2 + x + 3$.')
        ]

        quiz14.question_set.all().delete()
        for order, text, answer, explanation in questions_data_14:
            Question.objects.create(
                quiz=quiz14,
                question_order=order,
                question_text=text,
                model_answer=answer,
                explanation=explanation,
                accepted_answers=[]
            )
        self.stdout.write(f'Successfully created {len(questions_data_14)} questions for Quiz 14.')


        # ==========================================
        # Quiz 15: Applications of Derivatives: Concept Understanding (Theoretical / Self-Eval)
        # ==========================================
        description_15 = "Write your answer in your own words, then compare it to the model answer. Remember, this exercise is built on trust and personal responsibility. Marking incorrect answers as right mimics progress but hinders true understanding. Embrace the learning process—honesty here is the foundation of your growth."
        
        qs15 = Quiz.objects.filter(
            title='Applications of Derivatives: Concept Understanding',
            quiz_type=Quiz.QuizType.THEORETICAL,
            evaluation_method=Quiz.EvaluationMethod.SELF_EVAL
        )
        if qs15.count() > 1:
            qs15.exclude(pk=qs15.first().pk).delete()
            self.stdout.write('Removed duplicate Quiz 15 entries.')

        quiz15, created15 = Quiz.objects.get_or_create(
            title='Applications of Derivatives: Concept Understanding',
            quiz_type=Quiz.QuizType.THEORETICAL,
            evaluation_method=Quiz.EvaluationMethod.SELF_EVAL,
            defaults={
                'subject': Quiz.Subject.CALCULUS_1,
                'topic': 'Applications of Derivatives',
                'description': description_15,
                'created_at': timezone.now()
            }
        )

        if not created15 and quiz15.description != description_15:
            quiz15.description = description_15
            quiz15.save()
            self.stdout.write('Updated description for Quiz 15.')

        if created15:
            self.stdout.write(f'Created Quiz: {quiz15.title}')
        else:
            self.stdout.write('Quiz 15 already exists.')

        questions_data_15 = [
            (1, 
             'Can a function have an Absolute Maximum but NO Local Maximums? Explain.', 
             'Yes. Consider a straight line $y=x$ on the closed interval $[0, 1]$. The Absolute Max is at $x=1$ (an endpoint). Endpoints are not typically considered "local" extrema because the function doesn\'t exist on both sides.', None),

            (2, 
             'What is the difference between a function being "strictly increasing" and "non-decreasing"?', 
             'Strictly increasing means $f(b) > f(a)$ always. Non-decreasing allows for flat spots (f(b) >= f(a)), meaning the slope can be zero for a while, but never negative.', None),

            (3, 
             'Interleaving: Differentiate the inverse trig function $y = \\arctan(x)$.', 
             '$1 / (1 + x^2)$', None),

            (4, 
             'Why does L\'Hôpital\'s Rule **fail** for the limit $\\lim_{x \\to \\infty} \\frac{x + \\sin x}{x}$? Explain structurally.', 
             'Because the derivative of the top is $1 + \\cos x$. As $x \\to \\infty$, this oscillates and has no limit. L\'Hôpital requires the limit of the derivatives to exist. (You must solve this by dividing by x instead).', None),

            (5, 
             'If $f\'(x)$ represents velocity, what physical concept corresponds to an **Inflection Point** on the position graph?', 
             'An inflection point on position is where Concavity changes. Concavity corresponds to Acceleration. So, it is the moment where acceleration changes from positive to negative (jerk), or maximum speed.', None),

            (6, 
             'Interleaving: State the derivative of $a^x$ (where a is a constant, $a>0$).', 
             '$a^x \\ln(a)$. (Common mistake is forgetting the ln(a)).', None),

            (7, 
             'Connection: How is the Mean Value Theorem used to prove that a function with a zero derivative everywhere ($f\'(x)=0$) must be a Constant function?', 
             'If $f\'(x)=0$ always, then for any two points $a, b$, the MVT says $(f(b)-f(a))/(b-a) = 0$. This implies $f(b)-f(a) = 0$, or $f(b)=f(a)$ for all points. Thus, constant.', None),

            (8, 
             'Explain why we cannot simplify the antiderivative of $x \\cdot \\cos(x)$ into the antiderivative of $x$ times the antiderivative of $\\cos(x)$.', 
             'There is no "Product Rule for Integration" that simple. The integral of a product is NOT the product of integrals. You would need "Integration by Parts" (the reverse of the product rule).', None),

            (9, 
             'Interleaving: Explain the behavior of $e^{-x}$ as $x \\to \\infty$.', 
             'It approaches 0. Negative exponents mean "1 over e^x". As denominator gets huge, fraction goes to 0.', None),

            (10, 
             'Visually, if f\'(x) is an **Odd Function** (symmetric origin), what symmetry does the graph of f(x) likely have?', 
             'If the slopes are symmetric odd (like $x^2$ slopes are linear), the function is often Even (symmetric Y-axis). (e.g., antideriv of $x$ is $x^2/2$).', None),

            (11, 
             'If we use Linear Approximation to estimate $\\sqrt{4.1}$ using the tangent at $x=4$, will our estimate be an Overestimate or Underestimate? Why?', 
             'Overestimate. The graph of $\\sqrt{x}$ is Concave Down. Tangent lines to concave down curves sit *above* the actual curve.', None),

            (12, 
             'In Optimization, if you find a single critical point in an open interval, how can you confirm it is the Absolute Max without checking endpoints?', 
             'If it is the *only* critical point and it is a Local Max (by 1st/2nd deriv test), and the function is continuous, it must be the Absolute Max because the graph can never turn around to go higher.', None)
        ]

        quiz15.question_set.all().delete()
        for order, text, answer, _ignored in questions_data_15:
            Question.objects.create(
                quiz=quiz15,
                question_order=order,
                question_text=text,
                model_answer=answer,
                accepted_answers=[]
            )
        self.stdout.write(f'Successfully created {len(questions_data_15)} questions for Quiz 15.')


        # ==========================================
        # Quiz 16: Applications of Derivatives: Fundamental Properties (Theoretical / Automated)
        # ==========================================
        description_16 = "Type in the answer directly. These questions are automatically graded to test your precision and recall."
        
        qs16 = Quiz.objects.filter(
            title='Applications of Derivatives: Fundamental Properties',
            quiz_type=Quiz.QuizType.THEORETICAL,
            evaluation_method=Quiz.EvaluationMethod.AUTOMATED
        )
        if qs16.count() > 1:
            qs16.exclude(pk=qs16.first().pk).delete()
            self.stdout.write('Removed duplicate Quiz 16 entries.')

        quiz16, created16 = Quiz.objects.get_or_create(
            title='Applications of Derivatives: Fundamental Properties',
            quiz_type=Quiz.QuizType.THEORETICAL,
            evaluation_method=Quiz.EvaluationMethod.AUTOMATED,
            defaults={
                'subject': Quiz.Subject.CALCULUS_1,
                'topic': 'Applications of Derivatives',
                'description': description_16,
                'created_at': timezone.now()
            }
        )

        if not created16 and quiz16.description != description_16:
            quiz16.description = description_16
            quiz16.save()
            self.stdout.write('Updated description for Quiz 16.')

        if created16:
            self.stdout.write(f'Created Quiz: {quiz16.title}')
        else:
            self.stdout.write('Quiz 16 already exists.')

        questions_data_16 = [
            (1, 'If f\'\'(x) is positive for all x, the graph of f is always Concave ______.', 'up', ["up"]),

            (2, 'A "Corner" or "Cusp" on a graph produces a critical point where the derivative is ______.', 'undefined', ["undefined", "dne"]),

            (3, 'Interleaving: The derivative of ln(u) is u\' divided by ______.', 'u', ["u"]),

            (4, 'L\'Hôpital\'s rule can be used if the limit approaches zero divided by ______.', 'zero', ["zero", "0"]),

            (5, 'If the velocity of an object is increasing, its acceleration must be ______.', 'positive', ["positive"]),

            (6, 'Interleaving: The Chain Rule is used to differentiate ______ functions.', 'composite', ["composite", "nested"]),

            (7, 'The process of finding the maximum or minimum values of a function in a real-world context is called ______.', 'optimization', ["optimization"]),

            (8, 'If f\'(x) changes from negative to positive at c, then f(c) is a Local ______.', 'minimum', ["minimum", "min"]),

            (9, 'Interleaving: If a function is continuous, the limit as x approaches c can be found by ______ substitution.', 'direct', ["direct"]),

            (10, 'The antiderivative of f(x) = 1/x is ln(|x|) + ______.', 'c', ["c", "constant"]),

            (11, 'The equation of the tangent line L(x) used for approximation is L(x) = f(a) + f\'(a) * ______.', '(x-a)', ["(x-a)", "x-a"]),

            (12, 'A function f(x) has a horizontal asymptote y=L if the limit of f(x) as x approaches ______ is L.', 'infinity', ["infinity", "inf"])
        ]

        quiz16.question_set.all().delete()
        for order, text, answer, accepted in questions_data_16:
            Question.objects.create(
                quiz=quiz16,
                question_order=order,
                question_text=text,
                model_answer=answer,
                accepted_answers=accepted
            )
        self.stdout.write(f'Successfully created {len(questions_data_16)} questions for Quiz 16.')


        # ==========================================
        # Quiz 17: Applications of Derivatives: Advanced Practice (Practical / Self-Eval)
        # ==========================================
        description_17 = "Solve the problems below. For each question, type your final answer. After submitting, you will see the detailed step-by-step solution. Compare your work honestly and mark yourself correct only if your process and answer align."
        
        qs17 = Quiz.objects.filter(
            title='Applications of Derivatives: Advanced Practice',
            quiz_type=Quiz.QuizType.PRACTICAL,
            evaluation_method=Quiz.EvaluationMethod.SELF_EVAL
        )
        if qs17.count() > 1:
            qs17.exclude(pk=qs17.first().pk).delete()
            self.stdout.write('Removed duplicate Quiz 17 entries.')

        quiz17, created17 = Quiz.objects.get_or_create(
            title='Applications of Derivatives: Advanced Practice',
            quiz_type=Quiz.QuizType.PRACTICAL,
            evaluation_method=Quiz.EvaluationMethod.SELF_EVAL,
            defaults={
                'subject': Quiz.Subject.CALCULUS_1,
                'topic': 'Applications of Derivatives',
                'description': description_17,
                'created_at': timezone.now()
            }
        )

        if not created17 and quiz17.description != description_17:
            quiz17.description = description_17
            quiz17.save()
            self.stdout.write('Updated description for Quiz 17.')

        if created17:
            self.stdout.write(f'Created Quiz: {quiz17.title}')
        else:
            self.stdout.write('Quiz 17 already exists.')

        # (Order, Text, Model Answer, Explanation)
        questions_data_17 = [
            (1, 
             'Find the open intervals where $f(x) = xe^{-x}$ is **Increasing**.', 
             '(-infinity, 1)', 
             '1. Product Rule: $f\'(x) = 1 \\cdot e^{-x} + x(-e^{-x})$.\n2. Factor: $e^{-x}(1 - x)$.\n3. Critical pt at $x=1$ (since $e^{-x}$ is never 0).\n4. Test $x=0$: $1(1) = +$. Test $x=2$: $e^{-2}(-1) = -$.\n5. Increasing where positive: $(-\\infty, 1)$.'),

            (2, 
             'Evaluate limit using L\'Hôpital: $\\lim_{x \\to \\infty} \\frac{\\ln(x)}{x^{0.5}}$.', 
             '0', 
             '1. Form $\\infty/\\infty$. Apply L\'H.\n2. Deriv top: $1/x$. Deriv bot: $0.5x^{-0.5}$.\n3. Simplify: $(1/x) / (0.5/\\sqrt{x}) = \\frac{\\sqrt{x}}{0.5x} = \\frac{2}{\\sqrt{x}}$.\n4. As $x \\to \\infty$, $2/\\sqrt{x} \\to 0$.'),

            (3, 
             'Interleaving: Find the derivative of $y = 5^{x^2}$.', 
             '5^{x^2} * ln(5) * 2x', 
             '1. Rule for $a^u$: $a^u \\ln(a) u\'$.\n2. $u=x^2, u\'=2x$.\n3. Combine: $5^{x^2} \\ln(5) 2x$.'),

            (4, 
             'Analyze Concavity: Determine where $f(x) = x^4 - 4x^3$ is Concave Down.', 
             '(0, 2)', 
             '1. $f\'(x) = 4x^3 - 12x^2$.\n2. $f\'\'(x) = 12x^2 - 24x$.\n3. Set $f\'\'=0$: $12x(x-2)=0$. Inflection pts at 0, 2.\n4. Test interval $(0, 2)$ with $x=1$: $12(1)(-1) = -12$. Negative means Concave Down.'),

            (5, 
             'Optimization Setup: You have 100m of fence to build a rectangular rectangular pen against a barn (no fence needed on that side). Write the Area function $A(x)$ in terms of the width x.', 
             'A(x) = 100x - 2x^2', 
             '1. Let width = x. Let length = y.\n2. Constraint: $2x + y = 100 \\to y = 100 - 2x$.\n3. Area = $x \\cdot y = x(100 - 2x) = 100x - 2x^2$.'),

            (6, 
             'Interleaving: If $x^2 + y^2 = 1$, show that $y\'\' = -1/y^3$. (Harder)', 
             'See Steps.', 
             '1. $y\' = -x/y$.\n2. Quotient Rule for $y\'\'$: $\\frac{y(-1) - (-x)y\'}{y^2}$.\n3. Sub $y\'$: $\\frac{-y + x(-x/y)}{y^2} = \\frac{-y^2 - x^2}{y^3}$.\n4. Since $x^2+y^2=1$, numerator is $-1$. Result: $-1/y^3$.'),

            (7, 
             'Find the critical points of the function $y = |x - 3|$ and classify them.', 
             'x=3, Absolute Minimum', 
             '1. This is a V-shape shifted to 3.\n2. Derivative is undefined at x=3 (sharp corner), so it IS a critical point.\n3. Graph shows it is the bottom of the V, so it is a Minimum.'),

            (8, 
             'Evaluate $\\lim_{x \\to 0} (1 + 2x)^{1/x}$. (Hint: Use Logarithms or recognition of *e*).', 
             'e^2', 
             '1. Let $y = (1+2x)^{1/x}$. $\\ln y = \\frac{1}{x} \\ln(1+2x)$.\n2. Limit is $\\frac{\\ln(1+2x)}{x}$ (0/0 form).\n3. L\'Hopital: $\\frac{2/(1+2x)}{1}$.\n4. Evaluate at 0: $2/1 = 2$.\n5. $\\ln y = 2 \\to y = e^2$.'),

            (9, 
             'Interleaving: Determine the horizontal asymptote of $y = \\frac{5x^3 - 2}{10 - x^3}$.', 
             'y = -5', 
             '1. Highest powers are both $x^3$.\n2. Ratio of coefficients: $5 / (-1) = -5$.\n3. Asymptote is $y = -5$.'),

            (10, 
             'Find the general antiderivative of $f(x) = \\sec^2(x) + e^{2x}$.', 
             'tan(x) + 0.5e^{2x} + C', 
             '1. Know pairs: Deriv of $\\tan x$ is $\\sec^2 x$. So integral is $\\tan x$.\n2. Reverse Chain Rule: Deriv of $e^{2x}$ is $2e^{2x}$. So integral is $\\frac{1}{2}e^{2x}$.\n3. Add C.'),

            (11, 
             'Use the MVT to prove that $f(x) = \\sin(x) + 2x$ has NO horizontal tangent lines.', 
             'Derivative is cos(x) + 2, which is never 0.', 
             '1. Find $f\'(x) = \\cos(x) + 2$.\n2. Since $\\cos(x)$ is always between -1 and 1, $f\'(x)$ is always between 1 and 3.\n3. Since $f\'$ is never 0, there are no horizontal tangents.'),

            (12, 
             'Find the global minimum of $f(x) = x + \\frac{1}{x}$ for $x > 0$.', 
             '2', 
             '1. $f\'(x) = 1 - x^{-2} = 1 - 1/x^2$.\n2. Set to 0: $1 = 1/x^2 \\to x^2 = 1$. Since $x>0$, $x=1$.\n3. Check Concavity: $f\'\'(x) = 2/x^3$. At $x=1$, $f\'\' > 0$ (Concave Up). So it is a Min.\n4. Value: $1 + 1/1 = 2$.')
        ]

        quiz17.question_set.all().delete()
        for order, text, answer, explanation in questions_data_17:
            Question.objects.create(
                quiz=quiz17,
                question_order=order,
                question_text=text,
                model_answer=answer,
                explanation=explanation,
                accepted_answers=[]
            )
        self.stdout.write(f'Successfully created {len(questions_data_17)} questions for Quiz 17.')


        # ==========================================
        # Quiz 18: Derivatives: Chain Rule Mixed Practice (Practical)
        # ==========================================
        description_18 = "Solve the problems below. For each question, type your final answer. After submitting, you will see the detailed step-by-step solution. Compare your work honestly and mark yourself correct only if your process and answer align."

        qs18 = Quiz.objects.filter(
            title='Derivatives: Chain Rule Mixed Practice',
            quiz_type=Quiz.QuizType.PRACTICAL,
            evaluation_method=Quiz.EvaluationMethod.SELF_EVAL
        )
        if qs18.count() > 1:
            qs18.exclude(pk=qs18.first().pk).delete()
            self.stdout.write('Removed duplicate Quiz 18 entries.')

        quiz18, created18 = Quiz.objects.get_or_create(
            title='Derivatives: Chain Rule Mixed Practice',
            quiz_type=Quiz.QuizType.PRACTICAL,
            evaluation_method=Quiz.EvaluationMethod.SELF_EVAL,
            defaults={
                'subject': Quiz.Subject.CALCULUS_1,
                'topic': 'Derivatives',
                'description': description_18,
                'created_at': timezone.now()
            }
        )

        if not created18 and quiz18.description != description_18:
            quiz18.description = description_18
            quiz18.save()
            self.stdout.write('Updated description for Quiz 18.')

        if created18:
            self.stdout.write(f'Created Quiz: {quiz18.title}')
        else:
            self.stdout.write('Quiz 18 already exists.')

        # (Order, Text, Model Answer, Explanation)
        questions_data_18 = [
            (1, 
             'Differentiate: $y = (5x^3 + 2)^4$', 
             '60x^2(5x^3 + 2)^3', 
             'Chain Rule + Power Rule.\n1. Outer: $4(\\dots)^3$. Inner: $5x^3+2$.\n2. Deriv of Inner: $15x^2$.\n3. Multiply: $4(5x^3+2)^3 \\cdot 15x^2 = 60x^2(5x^3+2)^3$.'),

            (2, 
             'Differentiate the "Sigmoid-style" function: $y = \\frac{1}{1 + e^{-x}}$.', 
             'e^{-x} / (1 + e^{-x})^2', 
             'Rewrite as $(1 + e^{-x})^{-1}$ and use Chain Rule.\n1. Outer (Power): $-1(1+e^{-x})^{-2}$.\n2. Inner ($1+e^{-x}$): Deriv is $-e^{-x}$.\n3. Multiply: $-1 \\cdot (-e^{-x}) \\cdot (1+e^{-x})^{-2}$.'),

            (3, 
             'Differentiate: $y = \\sin(\\cos(x))$', 
             '-cos(cos(x)) * sin(x)', 
             'Chain Rule.\n1. Outer (sin): $\\cos(\\dots)$. Keep inner same: $\\cos(\\cos(x))$.\n2. Inner (cos): $-\\sin(x)$.\n3. Multiply: $\\cos(\\cos(x)) \\cdot [-\\sin(x)]$.'),

            (4, 
             'Differentiate: $y = e^{3x^2}$', 
             '6x * e^{3x^2}', 
             'Chain Rule with Exponential.\n1. Outer ($e^u$): stays $e^{3x^2}$.\n2. Inner ($3x^2$): deriv is $6x$.\n3. Multiply: $6x e^{3x^2}$.'),

            (5, 
             'Differentiate: $y = \\ln(x^2 + 1)$', 
             '2x / (x^2 + 1)', 
             'Chain Rule with Logarithm ($d/dx \\ln(u) = u\'/u$).\n1. $u = x^2+1$. $u\' = 2x$.\n2. Result: $\\frac{2x}{x^2+1}$.'),

            (6, 
             'Double Chain Rule: Differentiate $y = \\cos^4(2x)$', 
             '-8cos^3(2x)sin(2x)', 
             'Rewrite as $[\cos(2x)]^4$. Three layers.\n1. Power: $4[\cos(2x)]^3$.\n2. Trig: deriv of $\\cos(2x)$ is $-\\sin(2x)$.\n3. Inside arg: deriv of $2x$ is $2$.\n4. Multiply all: $4 \\cdot [-\\sin(2x)] \\cdot 2 \\cdot \\cos^3(2x)$.'),

            (7, 
             'Product and Chain Mixed: Differentiate $y = x \\cdot e^{-x}$', 
             'e^{-x}(1 - x)', 
             'Product Rule first, then Chain.\n1. $u=x, v=e^{-x}$.\n2. $u\'=1$. $v\'=-e^{-x}$ (Chain Rule).\n3. $u\'v + uv\' = 1(e^{-x}) + x(-e^{-x})$.\n4. Factor out $e^{-x}$.'),

            (8, 
             'Find the tangent line slope for $y = (2x-1)^3$ at $x=1$.', 
             '6', 
             '1. Differentiate: $3(2x-1)^2 \\cdot 2 = 6(2x-1)^2$.\n2. Evaluate at $x=1$: $6(2(1)-1)^2 = 6(1)^2 = 6$.'),

            (9, 
             'Differentiate the square root: $y = \\sqrt{x^2 + 5}$', 
             'x / sqrt(x^2 + 5)', 
             'Rewrite as $(x^2+5)^{1/2}$.\n1. Power rule: $\\frac{1}{2}(x^2+5)^{-1/2}$.\n2. Inner deriv: $2x$.\n3. Multiply: $\\frac{1}{2} \\cdot 2x \\cdot \\frac{1}{\\sqrt{x^2+5}} = \\frac{x}{\\sqrt{x^2+5}}$.'),

            (10, 
             'Differentiate: $y = \\tan(5x)$', 
             '5sec^2(5x)', 
             'Know your trig rules.\n1. Deriv of $\\tan(u)$ is $\\sec^2(u)$.\n2. Inner deriv of $5x$ is 5.\n3. Result: $5\\sec^2(5x)$.'),

            (11, 
             'Interleaving Limits: Evaluate $\\lim_{x \\to 0} \\frac{\\sin(2x)}{3x}$', 
             '2/3', 
             'Adjust the fraction to match $\\sin(u)/u$.\n1. Rewrite as $\\frac{\\sin(2x)}{2x} \\cdot \\frac{2x}{3x}$.\n2. Limit of $\\sin(2x)/2x$ is 1.\n3. Limit of $2x/3x$ is $2/3$.'),

            (12, 
             'Interleaving Limits: Evaluate $\\lim_{x \\to \\infty} \\frac{e^x}{x^2}$', 
             'Infinity', 
             'Hierarchy of Growth.\n1. Exponentials ($e^x$) grow much faster than polynomials ($x^2$).\n2. The numerator overwhelms the denominator.\n3. The limit is positive infinity.')
        ]

        quiz18.question_set.all().delete()
        for order, text, answer, explanation in questions_data_18:
            Question.objects.create(
                quiz=quiz18,
                question_order=order,
                question_text=text,
                model_answer=answer,
                explanation=explanation,
                accepted_answers=[]
            )
        self.stdout.write(f'Successfully created {len(questions_data_18)} questions for Quiz 18.')

        self.stdout.write(f'Seeding complete.')
