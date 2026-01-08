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
            # Calculus 2: Integrals
            ('Integrals: Basic Forms & Rules', 'Theoretical'),
            ('Integrals: FTC Mechanics', 'Theoretical'),
            ('Integrals: Conceptual Understanding', 'Theoretical'),
            ('Integrals: The Net Change Theorem', 'Theoretical'),
            ('Integrals: Antiderivative Skills', 'Practical'),
            ('Integrals: Definite Integral Practice', 'Practical'),
            # Calculus 2: Techniques
            ('Techniques: Substitution & Parts Rules', 'Theoretical'),
            ('Techniques: Trig & Partial Fractions Setup', 'Theoretical'),
            ('Techniques: Strategy & Recognition', 'Theoretical'),
            ('Techniques: Improper Integrals Concepts', 'Theoretical'),
            ('Techniques: Solving Integrals', 'Practical'),
            ('Techniques: Advanced Integration', 'Practical'),
            # Calculus 2: Sequences & Series
            ('Sequences: Definitions & Basic Limits', 'Theoretical'),
            ('Series: Convergence Test Rules', 'Theoretical'),
            ('Sequences: Conceptual Convergence', 'Theoretical'),
            ('Series: Theory of Power Series', 'Theoretical'),
            ('Sequences: Limit Calculations', 'Practical'),
            ('Series: Convergence Testing', 'Practical'),
            # Linear Algebra (Mechanics)
            ('Vectors: Dot Products & Lengths', 'Practical'),
            ('Vectors: Theoretical Concepts', 'Theoretical'),
            ('Matrices: Multiplication & Operations', 'Practical'),
            ('Matrices: Algebra & Properties', 'Theoretical'),
            ('Gaussian Elimination & Pivots', 'Theoretical'),
            ('Inverses & Singular Matrices', 'Theoretical'),
            ('LU Factorization & Transposes', 'Theoretical'),
            ('Advanced Factorization (PA=LU)', 'Theoretical'),
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
                'domain': Quiz.Domain.CALCULUS,
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
                'domain': Quiz.Domain.CALCULUS,
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
                'domain': Quiz.Domain.CALCULUS,
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
                'domain': Quiz.Domain.CALCULUS,
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
            (1, 'Define what it means for a function to be **differentiable** at $x=c$ in relation to continuity.', 'Differentiability is a stronger condition than continuity. If a function is differentiable at $x=c$, it MUST be continuous there. However, a function can be continuous but NOT differentiable (for example, at a sharp corner like $|x|$ at 0).', []),

            (2, 'Explain why the limit of a constant function, like $f(x) = 7$, is always the constant itself as $x$ approaches any value.', 'Because the function value never changes regardless of what $x$ is doing. The "gap" between $f(x)$ and 7 is always zero, so the limit is 7.', []),

            (3, 'If $\lim_{x \\to c} f(x) = 5$ and $\lim_{x \\to c} g(x) = -2$, what is the limit of $[f(x) \cdot g(x)]$? Which Limit Law applies?', '-10. The Product Law applies: The limit of a product is the product of the limits, provided both individual limits exist.', []),

            (4, 'Describe the "Infinite Limit" behavior. If $\lim_{x \\to c} f(x) = \infty$, is the limit considered to "exist" in the strict sense?', 'Strictly speaking, the limit does not exist (DNE) because it does not settle on a single real number. However, we describe it as "infinity" to be specific about the way in which it fails to exist (unbounded growth).', []),

            (5, 'What is the specific geometric interpretation of the limit: $\lim_{h \\to 0} \\frac{f(x+h) - f(x)}{h}$?', 'This limit represents the slope of the tangent line to the graph of $f$ at the point $x$. It is the definition of the derivative.', []),

            (6, 'Explain how to determine horizontal asymptotes for a rational function where the degree of the numerator is LARGER than the denominator.', 'If the numerator degree > denominator degree, there is no horizontal asymptote. The function goes to positive or negative infinity (or follows a slant asymptote).', []),
            
            (7, 'If $f(x)$ is squeezed between $y = -|x|$ and $y = |x|$, what is the limit of $f(x)$ as $x \\to 0$?', 'The limit is 0. Both $-|x|$ and $|x|$ approach 0 as $x \\to 0$. By the Squeeze Theorem, $f(x)$ must also approach 0.', []),

            (8, 'Why can we not just plug in $x=0$ to evaluate $\lim_{x \\to 0} (\\frac{\\sin x}{x})$?', 'Because $\\sin(0)$ is 0 and $x$ is 0, leading to the indeterminate form $0/0$. Direct substitution fails to give a valid result, requiring geometric proof or L\'Hopital\'s Rule.', []),

            (9, 'Does the Intermediate Value Theorem apply to the function $f(x) = 1/x$ on the interval $[-1, 1]$? Why or why not?', 'No. The IVT requires the function to be continuous on the entire closed interval. $f(x) = 1/x$ has an infinite discontinuity at $x=0$, which is inside $[-1, 1]$, so the theorem fails.', []),

            (10, 'Describe a "Jump Discontinuity".', 'A jump discontinuity occurs when the Left-Hand Limit and Right-Hand Limit both exist as finite numbers, but they are not equal to each other (the graph physically breaks and jumps to a new height).', [])
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
                'domain': Quiz.Domain.CALCULUS,
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
                'domain': Quiz.Domain.CALCULUS,
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
                'domain': Quiz.Domain.CALCULUS,
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
             '$f\'(x) = \lim_{h \\to 0} \\frac{f(x+h) - f(x)}{h}$. (Alternatively, the alternate form using $x \\to a$ is also acceptable).', []),

            (2, 'Explain the geometric relationship between a **Secant Line** and a **Tangent Line**.', 
             'A secant line connects two distinct points on a curve. A tangent line is the limiting position of the secant line as the two points get infinitely close to each other. The slope of the secant approaches the slope of the tangent.', []),

            (3, 'If a function is **Differentiable** at a point, must it be **Continuous** at that point? Explain why.', 
             'Yes. For the derivative to exist, the graph must be smooth and connected. If there were a break (discontinuity), the "rise" would be non-zero while the "run" approaches zero, or the limits wouldn\'t match, making the derivative undefined.', []),

            (4, 'Give two examples of visual features on a graph where a function is **Continuous but NOT Differentiable**.', 
             '1. A sharp corner or "cusp" (like $|x|$ at 0).\n2. A vertical tangent line (where the slope is infinite).', []),
            
            # Interleaving: Limits
            (5, r'Explain why the limit $\lim_{x \to 0} \frac{1}{x}$ does not exist.', 
             'As $x$ approaches 0 from the right, the value goes to positive infinity. As $x$ approaches 0 from the left, it goes to negative infinity. Since the left and right behaviors do not match (and are unbounded), the limit DNE.', []),

            (6, 'If the derivative $f\'(x)$ is **positive** over an interval, what does this tell you about the behavior of the original function $f(x)$?', 
             'It means the function $f(x)$ is increasing (going up from left to right) over that interval.', []),

            (7, 'What does the **Second Derivative** $f\'\'(x)$ tell us about the shape of the graph of $f(x)$?', 
             'It describes the concavity. If $f\'\' > 0$, the graph is concave up (like a cup). If $f\'\' < 0$, the graph is concave down (like a frown).', []),

            (8, 'Explain the difference between **Average Rate of Change** and **Instantaneous Rate of Change**.', 
             'Average Rate of Change is calculated over a time interval (slope of secant). Instantaneous Rate of Change is calculated at a single specific moment (slope of tangent, using a limit).', []),

            # INTERLEAVING: LIMITS
            (9, 'What is the primary difference between evaluating a limit and evaluating a function value?', 
             'The function value $f(c)$ depends on what happens exactly AT $x=c$. The limit depends on what happens NEAR $x=c$. They can be completely different (e.g., if there is a hole).', []),

            (10, 'In the Leibniz notation $\\frac{dy}{dx}$, is this symbol literally a fraction? Explain.', 
             'Not literally. It represents the limit of the fraction $\\frac{\\Delta y}{\\Delta x}$ as $\\Delta x$ approaches zero. However, in methods like separation of variables or differentials, we often treat it algebraically *like* a fraction.', []),

            (11, 'Conceptually, why is the derivative of a **Constant Function** equal to zero?', 
             'Geometrically, a constant function is a horizontal line. Horizontal lines have a slope of 0 everywhere, so the rate of change is always 0.', []),

            (12, 'Why do we need the **Chain Rule**? What specific type of functions does it apply to?', 
             'We need it to differentiate **composite functions** (functions inside other functions, like $f(g(x))$). It allows us to multiply the rate of change of the outer function by the rate of change of the inner function.', []),
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
                'domain': Quiz.Domain.CALCULUS,
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
                'domain': Quiz.Domain.CALCULUS,
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
                'domain': Quiz.Domain.CALCULUS,
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
             'If y changes 3 times as fast as u, and u changes 2 times as fast as x, then y changes 3 * 2 = 6 times as fast as x. We multiply the rates because the effects compound.', []),

            (2, 
             'In the Chain Rule formula $\\frac{dy}{dx} = \\frac{dy}{du} \\cdot \\frac{du}{dx}$, what does the variable $u$ represent?', 
             'The variable $u$ represents the "inner" function. It acts as the output of the first function and the input for the second function.', []),

            (3, 
             'Why is $\\sin(x^2)$ structurally different from $\\sin^2(x)$? How does this change the differentiation process?', 
             'In $\\sin(x^2)$, the squaring happens *inside* to the angle (Outer: sin, Inner: x^2). In $\\sin^2(x)$, the squaring happens *outside* to the whole result (Outer: x^2, Inner: sin). You must peel the layers in the correct order.', []),

            (4, 
             'When applying the Chain Rule to $f(g(h(x)))$, how many derivatives will you end up multiplying together?', 
             'Three. You differentiate the outer layer f, multiply by the derivative of the middle layer g, and multiply by the derivative of the inner layer h.', []),

            (5, 
             'What is the difference between "Implicit Differentiation" and the "Chain Rule"?', 
             'They are actually the same thing. Implicit differentiation is just applying the Chain Rule to the variable y (treating y as an unknown function y(x)) whenever we differentiate a term containing y.', []),

            # Interleaving
            (6, 
             'If $f(x)$ is continuous at $x=c$, does that guarantee that $\\lim_{x \\to c} f(x)$ exists? Why?', 
             'Yes. By definition of continuity, the limit must exist and it must equal the function value f(c).', []),

            (7, 
             'If you know the derivative of $f(x)$ is $f\'(x)$, how do you find the derivative of the inverse function $f^{-1}(x)$ using the Chain Rule?', 
             'You differentiate the identity $f(f^{-1}(x)) = x$. Applying the Chain Rule gives $f\'(f^{-1}(x)) \\cdot (f^{-1})\'(x) = 1$. Then solve for the inverse derivative.', []),

            (8, 
             'In Machine Learning, gradients are calculated "backwards". How does this relate to the Chain Rule?', 
             'The Chain Rule calculates the total rate of change by multiplying local derivatives. Backpropagation computes these products from the last layer (output) back to the first layer (input) to update weights.', []),

            (9, 
             'Why does the derivative of $e^{kx}$ equal $k \\cdot e^{kx}$ instead of just $e^{kx}$?', 
             'Because of the Chain Rule. The outer function is $e^u$ (deriv is $e^u$) and the inner function is $u=kx$ (deriv is k). Multiplying them gives $k e^{kx}$.', []),

            (10, 
             'Describe a "cusp" on a graph. Why does the derivative fail to exist there?', 
             'A cusp is a sharp point where the tangent line becomes vertical or the left-hand slope and right-hand slope are not equal. The limit of the difference quotient does not exist.', []),

            (11, 
             'What is the "Linear Approximation" of a function $f(x)$ at a point $a$?', 
             'It is the equation of the tangent line: $L(x) = f(a) + f\'(a)(x-a)$. It estimates the function values near $x=a$ using the derivative.', []),

            # Interleaving
            (12, 
             'Evaluate the limit of a composite function $\\lim_{x \\to c} f(g(x))$ if both are continuous.', 
             'You can move the limit inside. The result is simply $f(\\lim_{x \\to c} g(x))$, which equals $f(g(c))$.', [])
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
                'domain': Quiz.Domain.CALCULUS,
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
                'domain': Quiz.Domain.CALCULUS,
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
             'A derivative of zero means the tangent is horizontal, but the function could flatten out and then continue going up (like y = x^3 at x=0). This is called a "saddle point" or inflection point, not a max/min.', []),

            (2, 
             'State **Rolle\'s Theorem**. How is it a special case of the Mean Value Theorem?', 
             'Rolle\'s Theorem states that if f(a) = f(b), there must be a point between them where f\'(c) = 0. This is just the MVT where the average rate of change is zero (the secant line is horizontal).', []),

            # Interleaved 3 -> Position 3
            (3, 
             'Explain why the derivative of ln(x) cannot exist for x < 0.', 
             'Because the natural logarithm ln(x) is not defined for negative numbers (domain restriction). You cannot have a slope where the graph does not exist.', []),

            (4, 
             'Explain the **First Derivative Test**. How do you use the *signs* of f\'(x) to classify a critical point?', 
             'You check the sign of f\'(x) on both sides of the critical point. If f\' changes from Positive to Negative, it\'s a Peak (Max). If it changes from Negative to Positive, it\'s a Valley (Min).', []),

            (5, 
             'Geometrically, what does it mean for a function to be **Concave Up**? Relate this to the tangent lines.', 
             'Concave Up means the graph opens upward (like a cup). Geometrically, the graph lies *above* its tangent lines, and the slopes of the tangent lines are increasing.', []),

            # Interleaved 6 -> Position 6
            (6, 
             'Differentiate y = sin(x) * cos(x) using two different methods (Product Rule vs. Identity).', 
             'Method 1 (Product): cos(x)cos(x) - sin(x)sin(x) = cos(2x). Method 2 (Identity): Rewrite as 0.5sin(2x). Deriv is 0.5 * cos(2x) * 2 = cos(2x).', []),

            (7, 
             'Why does the **Second Derivative Test** work? (i.e., Why does f\'\'(c) < 0 imply a Maximum?)', 
             'If f\'\'(c) < 0, the function is Concave Down (frowning). A horizontal tangent (f\'=0) at the top of a frown must be a Peak (Maximum).', []),

            (8, 
             'What is an **Inflection Point**? strictly in terms of the second derivative.', 
             'An inflection point is a point where the second derivative f\'\'(x) *changes sign* (from positive to negative or vice versa). It is not enough for f\'\' to just be zero.', []),

            # Interleaved 9 -> Position 9
            (9, 
             'If lim_{x->inf} f(x) = 5, what does this tell us about the graph of f\'(x) (the derivative) as x approaches infinity?', 
             'If the function flattens out to a horizontal asymptote y=5, the slope (derivative) must approach 0.', []),

            (10, 
             'When applying **L\'Hôpital\'s Rule**, why must we check that the limit is an "Indeterminate Form" first?', 
             'Because if the limit is determinate (like 5/0 or 0/5), L\'Hôpital\'s Rule gives the wrong answer. It only works when there is a "struggle" between numerator and denominator (0/0 or inf/inf).', []),

            (11, 
             'What does the "+ C" represent when finding the **General Antiderivative**? Why is it geometrically necessary?', 
             'It represents the "Constant of Integration." Geometrically, it means a family of vertically shifted curves. Since the derivative (slope) is the same regardless of vertical height, we must account for all possible vertical starting positions.', []),

            (12, 
             'How does **Optimization** (finding global max/min) on a *closed* interval [a, b] differ from an *open* interval?', 
             'On a closed interval, you MUST check the endpoints (f(a) and f(b)) in addition to the critical points. The absolute max/min could occur at the very edge of the domain.', [])
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
                'domain': Quiz.Domain.CALCULUS,
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

            (3, 'Implicit differentiation is required when y is not explicitly defined as a function of ______.', 'x', ["x"]),

            (4, 'If f\'(x) > 0 on an interval, then f(x) is strictly ______ on that interval.', 'increasing', ["increasing"]),

            (5, 'The graph of f is Concave Down on intervals where the second derivative f\'\'(x) is ______.', 'negative', ["negative", "less than zero", "< 0"]),

            (6, 'The derivative of arcsin(x) involves a square ______ in the denominator.', 'root', ["root", "radical"]),

            (7, 'A point where the concavity of a function changes is called a point of ______.', 'inflection', ["inflection"]),

            (8, 'To apply L\'Hôpital\'s Rule to a limit of the form 0 * infinity, you must first rewrite it as a ______.', 'fraction', ["fraction", "ratio", "quotient"]),

            (9, 'A vertical asymptote at x=c implies that the limit as x approaches c is ______.', 'infinity', ["infinity", "infinite", "inf"]),

            (10, 'If f\'(c) = 0 and f\'\'(c) > 0, then f(c) is a local ______.', 'minimum', ["minimum", "min"]),

            (11, 'Any function F such that F\'(x) = f(x) is called an ______ of f.', 'antiderivative', ["antiderivative"]),

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
                'domain': Quiz.Domain.CALCULUS,
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
             'Find the slope of the tangent line to $x^2 + y^2 = 25$ at $(3, 4)$ using Implicit Differentiation.', 
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
             'Differentiate $y = x^x$ (Hint: Use Logarithmic Differentiation).', 
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
             'Evaluate $\\lim_{x \\to \\infty} \\frac{\\ln x}{x}$ using L\'Hôpital\'s Rule concepts.', 
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
                'domain': Quiz.Domain.CALCULUS,
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
             'Yes. Consider a straight line $y=x$ on the closed interval $[0, 1]$. The Absolute Max is at $x=1$ (an endpoint). Endpoints are not typically considered "local" extrema because the function doesn\'t exist on both sides.', []),

            (2, 
             'What is the difference between a function being "strictly increasing" and "non-decreasing"?', 
             'Strictly increasing means $f(b) > f(a)$ always. Non-decreasing allows for flat spots (f(b) >= f(a)), meaning the slope can be zero for a while, but never negative.', []),

            (3, 
             'Differentiate the inverse trig function $y = \\arctan(x)$.', 
             '$1 / (1 + x^2)$', []),

            (4, 
             'Why does L\'Hôpital\'s Rule **fail** for the limit $\\lim_{x \\to \\infty} \\frac{x + \\sin x}{x}$? Explain structurally.', 
             'Because the derivative of the top is $1 + \\cos x$. As $x \\to \\infty$, this oscillates and has no limit. L\'Hôpital requires the limit of the derivatives to exist. (You must solve this by dividing by x instead).', []),

            (5, 
             'If $f\'(x)$ represents velocity, what physical concept corresponds to an **Inflection Point** on the position graph?', 
             'An inflection point on position is where Concavity changes. Concavity corresponds to Acceleration. So, it is the moment where acceleration changes from positive to negative (jerk), or maximum speed.', []),

            (6, 
             'State the derivative of $a^x$ (where a is a constant, $a>0$).', 
             '$a^x \\ln(a)$. (Common mistake is forgetting the ln(a)).', []),

            (7, 
             'How is the Mean Value Theorem used to prove that a function with a zero derivative everywhere ($f\'(x)=0$) must be a Constant function?', 
             'If $f\'(x)=0$ always, then for any two points $a, b$, the MVT says $(f(b)-f(a))/(b-a) = 0$. This implies $f(b)-f(a) = 0$, or $f(b)=f(a)$ for all points. Thus, constant.', []),

            (8, 
             'Explain why we cannot simplify the antiderivative of $x \\cdot \\cos(x)$ into the antiderivative of $x$ times the antiderivative of $\\cos(x)$.', 
             'There is no "Product Rule for Integration" that simple. The integral of a product is NOT the product of integrals. You would need "Integration by Parts" (the reverse of the product rule).', []),

            (9, 
             'Explain the behavior of $e^{-x}$ as $x \\to \\infty$.', 
             'It approaches 0. Negative exponents mean "1 over e^x". As denominator gets huge, fraction goes to 0.', []),

            (10, 
             'Visually, if f\'(x) is an **Odd Function** (symmetric origin), what symmetry does the graph of f(x) likely have?', 
             'If the slopes are symmetric odd (like $x^2$ slopes are linear), the function is often Even (symmetric Y-axis). (e.g., antideriv of $x$ is $x^2/2$).', []),

            (11, 
             'If we use Linear Approximation to estimate $\\sqrt{4.1}$ using the tangent at $x=4$, will our estimate be an Overestimate or Underestimate? Why?', 
             'Overestimate. The graph of $\\sqrt{x}$ is Concave Down. Tangent lines to concave down curves sit *above* the actual curve.', []),

            (12, 
             'In Optimization, if you find a single critical point in an open interval, how can you confirm it is the Absolute Max without checking endpoints?', 
             'If it is the *only* critical point and it is a Local Max (by 1st/2nd deriv test), and the function is continuous, it must be the Absolute Max because the graph can never turn around to go higher.', [])
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
                'domain': Quiz.Domain.CALCULUS,
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

            (3, 'The derivative of ln(u) is u\' divided by ______.', 'u', ["u"]),

            (4, 'L\'Hôpital\'s rule can be used if the limit approaches zero divided by ______.', 'zero', ["zero", "0"]),

            (5, 'If the velocity of an object is increasing, its acceleration must be ______.', 'positive', ["positive"]),

            (6, 'The Chain Rule is used to differentiate ______ functions.', 'composite', ["composite", "nested"]),

            (7, 'The process of finding the maximum or minimum values of a function in a real-world context is called ______.', 'optimization', ["optimization"]),

            (8, 'If f\'(x) changes from negative to positive at c, then f(c) is a Local ______.', 'minimum', ["minimum", "min"]),

            (9, 'If a function is continuous, the limit as x approaches c can be found by ______ substitution.', 'direct', ["direct"]),

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
                'domain': Quiz.Domain.CALCULUS,
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
             'Find the derivative of $y = 5^{x^2}$.', 
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
             'If $x^2 + y^2 = 1$, show that $y\'\' = -1/y^3$. (Harder)', 
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
             'Determine the horizontal asymptote of $y = \\frac{5x^3 - 2}{10 - x^3}$.', 
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
                'domain': Quiz.Domain.CALCULUS,
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
             'Limits: Evaluate $\\lim_{x \\to 0} \\frac{\\sin(2x)}{3x}$', 
             '2/3', 
             'Adjust the fraction to match $\\sin(u)/u$.\n1. Rewrite as $\\frac{\\sin(2x)}{2x} \\cdot \\frac{2x}{3x}$.\n2. Limit of $\\sin(2x)/2x$ is 1.\n3. Limit of $2x/3x$ is $2/3$.'),

            (12, 
             'Evaluate $\\lim_{x \\to \\infty} \\frac{e^x}{x^2}$', 
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

        # ==============================================================================
        # CALCULUS 2: INTEGRALS
        # ==============================================================================

        # --- Quiz 19: Integrals: Basic Forms & Rules (Theoretical / Automated) ---
        desc_19 = "Test your memory of the basic anti-derivative formulas. These are the building blocks for all integration."
        quiz19, _ = Quiz.objects.get_or_create(
            title='Integrals: Basic Forms & Rules',
            quiz_type=Quiz.QuizType.THEORETICAL,
            evaluation_method=Quiz.EvaluationMethod.AUTOMATED,
            defaults={'domain': Quiz.Domain.CALCULUS, 'subject': Quiz.Subject.CALCULUS_2, 'topic': 'Integrals', 'description': desc_19}
        )
        if quiz19.description != desc_19: quiz19.description = desc_19; quiz19.save()
        
        q_data_19 = [
            (1, 'The indefinite integral of $x^n$ (for $n \\neq -1$) is $\\frac{x^{n+1}}{n+1} + C$. This is known as the ______ Rule for Integration.', 'power', ['power', 'power rule']),
            (2, 'The indefinite integral $\\int \\frac{1}{x} dx$ is equal to ______.', 'ln|x|+C', ['ln|x|+c', 'ln|x|', 'natural log', 'ln(x)']),
            (3, 'The indefinite integral of $e^x$ is ______.', 'e^x+C', ['e^x+c', 'e^x']),
            (4, 'The indefinite integral of $\\cos(x)$ is ______.', 'sin(x)+C', ['sin(x)+c', 'sin(x)', 'sine']),
            (5, 'The derivative of $\\sin(x)$ is ______.', 'cos(x)', ['cos(x)', 'cosine']),
            (6, 'The indefinite integral of $\\sin(x)$ is ______.', '-cos(x)+C', ['-cos(x)+c', '-cos(x)', 'negative cosine']),
            (7, 'The indefinite integral of $\\sec^2(x)$ is ______.', 'tan(x)+C', ['tan(x)+c', 'tan(x)', 'tangent']),
            (8, 'True or False: $\\int [f(x) + g(x)] dx = \\int f(x) dx + \\int g(x) dx$.', 'true', ['true', 't']),
            (9, '$\\frac{d}{dx}(x^3) = $ ______.', '3x^2', ['3x^2']),
            (10, 'True or False: $\\int f(x)g(x) dx = \\int f(x) dx \\cdot \\int g(x) dx$.', 'false', ['false', 'f']),
            (11, 'The arbitrary constant added to an indefinite integral is usually denoted by the letter ______.', 'C', ['c', 'k']),
            (12, 'Integration is the ______ process of differentiation.', 'reverse', ['reverse', 'inverse', 'opposite'])
        ]
        quiz19.question_set.all().delete()
        for o, t, a, acc in q_data_19: Question.objects.create(quiz=quiz19, question_order=o, question_text=t, model_answer=a, accepted_answers=acc)
        self.stdout.write(f'Created Quiz: {quiz19.title}')

        # --- Quiz 20: Integrals: FTC Mechanics (Theoretical / Automated) ---
        desc_20 = "Focused review of the Fundamental Theorem of Calculus equations and immediate consequences."
        quiz20, _ = Quiz.objects.get_or_create(
            title='Integrals: FTC Mechanics',
            quiz_type=Quiz.QuizType.THEORETICAL,
            evaluation_method=Quiz.EvaluationMethod.AUTOMATED,
            defaults={'domain': Quiz.Domain.CALCULUS, 'subject': Quiz.Subject.CALCULUS_2, 'topic': 'Integrals', 'description': desc_20}
        )
        if quiz20.description != desc_20: quiz20.description = desc_20; quiz20.save()

        q_data_20 = [
            (1, 'FTC Part 1 states that if $g(x) = \\int_a^x f(t) dt$, then $g\'(x) = $ ______.', 'f(x)', ['f(x)']),
            (2, 'FTC Part 2 states that $\\int_a^b f(x) dx = F(b) - $ ______.', 'F(a)', ['f(a)']),
            (3, 'The limit of $\\frac{\\sin x}{x}$ as $x \\to 0$ is ______.', '1', ['1', 'one']),
            (4, 'To use the Fundamental Theorem of Calculus on $[a, b]$, the function $f$ must be ______ on that interval.', 'continuous', ['continuous']),
            (5, 'If we differentiate an integral with the upper limit $x$, we get the integrand back. This shows diff and int are ______ processes.', 'inverse', ['inverse', 'reverse']),
            (6, 'Evaluate $\\frac{d}{dx} \\int_1^x t^3 dt$.', 'x^3', ['x^3']),
            (7, 'The integral from $a$ to $a$ of any functions is always ______.', '0', ['0', 'zero']),
            (8, 'If $f\'(c)=0$ and $f\'\'(c)>0$, then $f$ has a local ______ at c.', 'minimum', ['minimum', 'min']),
            (9, 'If you switch the limits of integration (from $a$ to $b$ -> $b$ to $a$), the sign of the integral ______.', 'changes', ['changes', 'flips', 'reverses', 'becomes negative']),
            (10, '$\\int_a^b f(x) dx + \\int_b^c f(x) dx = \\int_a^c f(x) dx$. This is the ______ Property of intervals.', 'additive', ['additive', 'additivity', 'addition']),
            (11, 'If $F(x)$ is an antiderivative of $f(x)$, then $F\'(x)$ must equal ______.', 'f(x)', ['f(x)']),
            (12, 'In the definite integral notation, $a$ and $b$ are called the ______ of integration.', 'limits', ['limits', 'bounds'])
        ]
        quiz20.question_set.all().delete()
        for o, t, a, acc in q_data_20: Question.objects.create(quiz=quiz20, question_order=o, question_text=t, model_answer=a, accepted_answers=acc)
        self.stdout.write(f'Created Quiz: {quiz20.title}')

        # --- Quiz 21: Integrals: Conceptual Understanding (Theoretical / Self-Eval) ---
        desc_21 = "Deep dive into the 'why' of integration. Focus on the area interpretation and the connection between rate limits and sums."
        quiz21, _ = Quiz.objects.get_or_create(
            title='Integrals: Conceptual Understanding',
            quiz_type=Quiz.QuizType.THEORETICAL,
            evaluation_method=Quiz.EvaluationMethod.SELF_EVAL,
            defaults={'domain': Quiz.Domain.CALCULUS, 'subject': Quiz.Subject.CALCULUS_2, 'topic': 'Integrals', 'description': desc_21}
        )
        if quiz21.description != desc_21: quiz21.description = desc_21; quiz21.save()

        q_data_21 = [
            (1, 'Explain the geometric meaning of the definite integral $\\int_a^b f(x) dx$ if $f(x)$ takes on both positive and negative values.', 'It applies to the "Net Signed Area". Area above the x-axis is positive, and area below is negative. The integral sums these signed values.', []),
            (2, 'Why do we add a "+ C" to indefinite integrals but not definite integrals?', 'An indefinite integral represents a FAMILY of functions (all vertical shifts). A definite integral represents a specific number (area/accumulation), and the C\'s cancel out during the subtraction $F(b) - F(a)$.', []),
            (3, 'If $\\lim_{x \\to a} f(x)$ exists but does not equal $f(a)$, what type of discontinuity is this?', 'Removable (Hole).', []),
            (4, 'If $v(t)$ is velocity, what does the area under the curve from $t=a$ to $t=b$ represent?', 'It represents the Displacement (change in position) of the object between time $a$ and $b$.', []),
            (5, 'Explain why $\\int_{-a}^a f(x) dx = 0$ if $f(x)$ is an Odd function.', 'An odd function has rotational symmetry about the origin. The area from $-a$ to $0$ is the exact negative of the area from $0$ to $a$, so they cancel each other out perfectly.', []),
            (6, 'What does the Mean Value Theorem for Integrals say geometrically?', 'It says there is at least one rectangle with height $f(c)$ and width $b-a$ that has the exact same area as the area under the curve.', []),
            (7, 'True or False: If $f$ is continuous on $[a,b]$, it must have a max and min.', 'True (Extreme Value Theorem).', []),
            (8, 'Visualize $\\int_0^1 \\sqrt{1-x^2} dx$. What geometric shape is this, and what is its value?', 'This is the upper right quarter of the unit circle. The area is $\\frac{1}{4}(\\pi r^2) = \\frac{\\pi}{4}$.', []),
            (9, 'Why CAN\'T we use the Power Rule for $\\int x^{-1} dx$?', 'Because the Power Rule $\\frac{x^{n+1}}{n+1}$ would result in division by zero ($n+1 = 0$). That\'s why we have the special $\\ln|x|$ rule.', []),
            (10, 'Explain the relationship between the units of $f(x)$, $x$, and $\\int f(x) dx$.', 'The unit of the integral is the product of the unit of $f(x)$ and the unit of $x$. (e.g., Velocity (m/s) * Time (s) = Distance (m)).', []),
            (11, 'Conceptually, what happens to the Riemann Sum as the number of rectangles ($n$) goes to infinity?', 'The width of each rectangle ($\Delta x$) approaches zero, and the approximation error vanishes. The sum converges to the exact area under the curve.', []),
            (12, 'If $\\int_a^b f(x) dx > 0$, does this mean $f(x)$ is always positive on $[a,b]$?', 'No. It just means the area above the x-axis is greater than the area below the x-axis. $f(x)$ could be negative for parts of the interval.', []),
        ]
        quiz21.question_set.all().delete()
        for o, t, a, acc in q_data_21: Question.objects.create(quiz=quiz21, question_order=o, question_text=t, model_answer=a, accepted_answers=acc)
        self.stdout.write(f'Created Quiz: {quiz21.title}')

        # --- Quiz 22: Integrals: The Net Change Theorem (Theoretical / Self-Eval) ---
        desc_22 = "Applying integration to real-world rates of change."
        quiz22, _ = Quiz.objects.get_or_create(
            title='Integrals: The Net Change Theorem',
            quiz_type=Quiz.QuizType.THEORETICAL,
            evaluation_method=Quiz.EvaluationMethod.SELF_EVAL,
            defaults={'domain': Quiz.Domain.CALCULUS, 'subject': Quiz.Subject.CALCULUS_2, 'topic': 'Integrals', 'description': desc_22}
        )
        if quiz22.description != desc_22: quiz22.description = desc_22; quiz22.save()

        q_data_22 = [
            (1, 'State the Net Change Theorem in words.', 'The integral of a rate of change is the net change in the collected quantity over that interval.', []),
            (2, 'Explain the difference between $\\int_a^b v(t) dt$ and $\\int_a^b |v(t)| dt$.', 'The first is Displacement (net change in position, can be 0 if you return to start). The second is Total Distance Traveled (adds up all movement regardless of direction).', []),
            (3, 'If $C\'(x)$ is the marginal cost of producing $x$ units, what does $\\int_{100}^{200} C\'(x) dx$ represent?', 'It represents the increase in Total Cost required to increase production from 100 units to 200 units.', []),
            (4, 'The derivative of slope is ______.', 'Concavity (or second derivative).', []),
            (5, 'If a population growth rate is negative for a time period, what does that mean for the net change integral?', 'It means the integral will be negative, indicating a decrease in total population size.', []),
            (6, 'Why is the integral of acceleration $\\int v\'(t) dt$ equal to the change in velocity?', 'Because acceleration is the rate of change of velocity. Summing the changes in velocity gives the total net change in velocity.', []),
            (7, 'If $P(t)$ is power (rate of energy use), what does $\\int P(t) dt$ represent?', 'It represents the total Energy consumed over that time period.', []),
            (8, 'How do you calculate the final position of a particle if you know its initial position $s(0)$ and velocity $v(t)$?', '$s(t) = s(0) + \\int_0^t v(x) dx$. Final = Initial + Net Change.', []),
            (9, 'If velocity is constant, what does the position graph look like?', 'A straight line with slope equal to that constant velocity.', []),
            (10, 'In the context of Net Change, why is it important to distinguish between "rate of flow into" and "rate of flow out" of a tank?', 'Often the Net Rate = (Rate In) - (Rate Out). You must integrate this Net Rate to find the change in volume inside the tank.', []),
            (11, 'If water flows into a tank at rate $r(t)$, what does $\\int_{0}^{60} r(t) dt$ represent?', 'The total volume of water that entered the tank in the first 60 minutes (or seconds, depending on unit).', []),
            (12, 'What rule helps find limits of indeterminate forms 0/0?', 'L\'Hopital\'s Rule.', [])
        ]
        quiz22.question_set.all().delete()
        for o, t, a, acc in q_data_22: Question.objects.create(quiz=quiz22, question_order=o, question_text=t, model_answer=a, accepted_answers=acc)
        self.stdout.write(f'Created Quiz: {quiz22.title}')

        # --- Quiz 23: Integrals: Antiderivative Skills (Practical / Self-Eval) ---
        desc_23 = "Practice finding indefinite integrals. Do the work on paper, then check."
        quiz23, _ = Quiz.objects.get_or_create(
            title='Integrals: Antiderivative Skills',
            quiz_type=Quiz.QuizType.PRACTICAL,
            evaluation_method=Quiz.EvaluationMethod.SELF_EVAL,
            defaults={'domain': Quiz.Domain.CALCULUS, 'subject': Quiz.Subject.CALCULUS_2, 'topic': 'Integrals', 'description': desc_23}
        )
        if quiz23.description != desc_23: quiz23.description = desc_23; quiz23.save()

        q_data_23 = [
            (1, 'Find $\\int (3x^2 + 4x - 5) dx$', '$x^3 + 2x^2 - 5x + C$', 'Power Rule: Integrals are $x^3$, $2x^2$, and $-5x$. Add C.'),
            (2, 'Find $\\int (\\sqrt{x} + \\frac{1}{\\sqrt{x}}) dx$', '$\\frac{2}{3}x^{3/2} + 2\\sqrt{x} + C$', 'Rewrite as $x^{1/2} + x^{-1/2}$. Power rule: Add 1 to exponents and divide.'),
            (3, 'Find $\\int (\\sin x - 2\\cos x) dx$', '$-\\cos x - 2\\sin x + C$', 'Integral of sin is -cos. Integral of cos is sin.'),
            (4, 'Find $\\int e^{3x} dx$', '$\\frac{1}{3}e^{3x} + C$', 'Reverse chain rule (or u-sub). Divide by the constant derivative of the exponent.'),
            (5, 'Solve the Differential Equation: $f\'(x) = 6x$, $f(0) = 4$.', '$f(x) = 3x^2 + 4$', '1. Integrate $6x$ to get $3x^2 + C$. 2. Plug in $x=0, y=4$. 3. $3(0)^2 + C = 4 \\implies C=4$.'),
            (6, 'Differentiate $y = \\sqrt{x}$.', '$1/(2\\sqrt{x})$', 'Power rule x^(1/2).'),
            (7, 'Find $\\int (2 + \\tan^2 x) dx$', '2x + (\\tan x - x) + C = x + \\tan x + C$', 'Recall $\\tan^2 x = \\sec^2 x - 1$. Integral becomes $\\int (2 + \\sec^2 x - 1) dx = \\int (1 + \\sec^2 x) dx$.'),
            (8, 'Find $\\int \\frac{1}{\\cos^2 x} dx$', '$\\tan x + C$', 'Rewrite $1/\\cos^2 x$ as $\\sec^2 x$. The antiderivative is $\\tan x$.'),
            (9, 'Find $\\int 2^x dx$', '$\\frac{2^x}{\\ln 2} + C$', 'General Exponential Rule: $\\int a^x dx = \\frac{a^x}{\\ln a}$.'),
            (10, 'Find $\\int (x^2 - 1)^2 dx$', '$\\frac{x^5}{5} - \\frac{2x^3}{3} + x + C$', 'Expand first: $(x^2-1)^2 = x^4 - 2x^2 + 1$. Then integrate.'),
            (11, 'Find $\\int \\frac{3x^2 + 2}{x} dx$', '$\\frac{3}{2}x^2 + 2\\ln|x| + C$', 'Divide first: $3x + \\frac{2}{x}$. Then integrate term by term.'),
            (12, 'Differentiate $y = e^{5x}$.', '$5e^{5x}$', 'Chain rule.')
        ]
        quiz23.question_set.all().delete()
        for o, t, a, exp in q_data_23: Question.objects.create(quiz=quiz23, question_order=o, question_text=t, model_answer=a, explanation=exp, accepted_answers=[])
        self.stdout.write(f'Created Quiz: {quiz23.title}')

        # --- Quiz 24: Integrals: Definite Integral Practice (Practical / Self-Eval) ---
        desc_24 = "Practice evaluating definite integrals using FTC Part 2."
        quiz24, _ = Quiz.objects.get_or_create(
            title='Integrals: Definite Integral Practice',
            quiz_type=Quiz.QuizType.PRACTICAL,
            evaluation_method=Quiz.EvaluationMethod.SELF_EVAL,
            defaults={'domain': Quiz.Domain.CALCULUS, 'subject': Quiz.Subject.CALCULUS_2, 'topic': 'Integrals', 'description': desc_24}
        )
        if quiz24.description != desc_24: quiz24.description = desc_24; quiz24.save()

        q_data_24 = [
            (1, 'Evaluate $\\int_0^3 (2x) dx$', '9', 'Antiderivative is $x^2$. $[x^2]_0^3 = 3^2 - 0^2 = 9$.'),
            (2, 'Differentiate sin(x^2).', '2x cos(x^2)', 'Chain rule.'),
            (3, 'Evaluate $\\int_0^{\\pi} \\sin x dx$', '2', 'Antiderivative is $-\\cos x$. $[-\\cos(\\pi)] - [-\\cos(0)] = -(-1) - (-1) = 1 + 1 = 2$.'),
            (4, 'Evaluate $\\int_0^1 e^x dx$', '$e - 1$', 'Antiderivative is $e^x$. $e^1 - e^0 = e - 1$.'),
            (5, 'Evaluate $\\int_{-1}^1 x^3 dx$', '0', 'Odd function on symmetric interval is 0. Or calc: $[x^4/4]_{-1}^1 = 1/4 - 1/4 = 0$.'),
            (6, 'Find the area under $y=x^2$ from $x=0$ to $x=2$.', '8/3', 'Evaluate $\\int_0^2 x^2 dx = [\\frac{x^3}{3}]_0^2 = \\frac{8}{3} - 0 = 8/3$.'),
            (7, 'Evaluate $\\int_1^4 \\sqrt{x} dx$', '14/3', '$x^{1/2} \\to \\frac{2}{3}x^{3/2}$. Limits 1 to 4. $\\frac{2}{3}(4^{3/2} - 1^{3/2}) = \\frac{2}{3}(8 - 1) = 14/3$.'),
            (8, 'Evaluate $\\int_0^{\\pi/4} \\sec^2 x dx$', '1', 'Antiderivative is $\\tan x$. $\\tan(\\pi/4) - \\tan(0) = 1 - 0 = 1$.'),
            (9, 'Evaluate $\\int_0^1 (e^x + x) dx$', '$e - 0.5$', '$[e^x + x^2/2]_0^1 = (e + 1/2) - (1 + 0) = e - 0.5$.'),
            (10, 'Find the average value of $f(x) = x$ on $[0, 5]$.', '2.5', 'Avg = $\\frac{1}{b-a}\\int_a^b f(x)dx$. $\\frac{1}{5}\\int_0^5 x dx = \\frac{1}{5}[12.5] = 2.5$.'),
            (11, 'Limit x->3 of (x-3)/(x^2-9).', '1/6', 'Factor: 1/(x+3) -> 1/6.'),
            (12, 'Evaluate $\\int_1^2 \\frac{1}{x} dx$', '$\\ln 2$ (approx 0.693)', 'Antiderivative is $\\ln|x|$. $\\ln(2) - \\ln(1) = \\ln 2 - 0 = \\ln 2$.'),
        ]
        quiz24.question_set.all().delete()
        for o, t, a, exp in q_data_24: Question.objects.create(quiz=quiz24, question_order=o, question_text=t, model_answer=a, explanation=exp, accepted_answers=[])
        self.stdout.write(f'Created Quiz: {quiz24.title}')

        # ==============================================================================
        # CALCULUS 2: TECHNIQUES OF INTEGRATION
        # ==============================================================================

        # --- Quiz 25: Techniques: Substitution & Parts Rules (Theoretical / Automated) ---
        desc_25 = "Tests the core rules behind substitution and integration by parts."
        quiz25, _ = Quiz.objects.get_or_create(
            title='Techniques: Substitution & Parts Rules',
            quiz_type=Quiz.QuizType.THEORETICAL,
            evaluation_method=Quiz.EvaluationMethod.AUTOMATED,
            defaults={'domain': Quiz.Domain.CALCULUS, 'subject': Quiz.Subject.CALCULUS_2, 'topic': 'Techniques', 'description': desc_25}
        )
        if quiz25.description != desc_25: quiz25.description = desc_25; quiz25.save()

        q_data_25 = [
            (1, 'Integration by Substitution is the reverse of the ______ Rule for differentiation.', 'chain', ['chain']),
            (2, 'Integration by Parts is the reverse of the ______ Rule for differentiation.', 'product', ['product']),
            (3, 'The formula for Integration by Parts is $\\int u dv = uv - $ ______.', 'int v du', ['int v du', 'integral v du']),
            (4, 'The derivative of $\\ln(x)$ is ______.', '1/x', ['1/x']),
            (5, 'In the LIATE rule for choosing u, the L stands for ______.', 'logarithmic', ['logarithmic', 'log', 'logs']),
            (6, 'In the LIATE rule, the E stands for ______.', 'exponential', ['exponential']),
            (7, 'For $\\sqrt{a^2 - x^2}$, the recommended trig substitution is $x = $ ______.', 'a sin(theta)', ['a sin(theta)', 'asin(theta)', 'sine']),
            (8, 'If $f\'\'(x) > 0$, the graph of $f$ is concave ______.', 'up', ['up']),
            (9, 'For $\\sqrt{a^2 + x^2}$, the recommended trig substitution is $x = $ ______.', 'a tan(theta)', ['a tan(theta)', 'atan(theta)', 'tangent']),
            (10, 'Partial Fraction Decomposition is used to integrate ______ functions.', 'rational', ['rational']),
            (11, 'An Improper Integral of Type 1 has an ______ interval of integration.', 'infinite', ['infinite']),
            (12, 'An Improper Integral of Type 2 has a ______ integrand at some point in the interval.', 'discontinuous', ['discontinuous', 'undefined'])
        ]
        quiz25.question_set.all().delete()
        for o, t, a, acc in q_data_25: Question.objects.create(quiz=quiz25, question_order=o, question_text=t, model_answer=a, accepted_answers=acc)
        self.stdout.write(f'Created Quiz: {quiz25.title}')

        # --- Quiz 26: Techniques: Trig & Partial Fractions Setup (Theoretical / Automated) ---
        desc_26 = "Test your ability to set up complex integrals for solving."
        quiz26, _ = Quiz.objects.get_or_create(
            title='Techniques: Trig & Partial Fractions Setup',
            quiz_type=Quiz.QuizType.THEORETICAL,
            evaluation_method=Quiz.EvaluationMethod.AUTOMATED,
            defaults={'domain': Quiz.Domain.CALCULUS, 'subject': Quiz.Subject.CALCULUS_2, 'topic': 'Techniques', 'description': desc_26}
        )
        if quiz26.description != desc_26: quiz26.description = desc_26; quiz26.save()

        q_data_26 = [
            (1, 'The partial fraction decomposition of $\\frac{1}{(x-1)(x+2)}$ is $\\frac{A}{x-1} + $ ______.', 'B/(x+2)', ['b/(x+2)']),
            (2, 'For a repeated linear factor $(x-1)^2$, you need terms $\\frac{A}{x-1}$ and ______.', 'B/(x-1)^2', ['b/(x-1)^2']),
            (3, 'The limit at infinity for a rational function with equal degree numerator and denominator is the ratio of their ______ coefficients.', 'leading', ['leading']),
            (4, 'For an irreducible quadratic factor $x^2+1$, the numerator should be ______.', 'Ax+B', ['ax+b']),
            (5, 'The half-angle identity for $\\cos^2(x)$ is $\\frac{1 + \\cos(2x)}{2}$. What is the identity for $\\sin^2(x)$?', '(1-cos(2x))/2', ['(1-cos(2x))/2', '1-cos(2x)/2']),
            (6, 'To integrate $\\sin^3(x)$, you should save one factor of $\\sin(x)$ and convert the rest to ______.', 'cosines', ['cosines', 'cos', 'cos(x)']),
            (7, 'To integrate $\\tan(x)$, rewrite it as ______.', 'sin(x)/cos(x)', ['sin(x)/cos(x)']),
            (8, 'The derivative of $e^{2x}$ is ______.', '2e^{2x}', ['2e^{2x}']),
            (9, 'The integral $\\int \\frac{1}{x^2+1} dx$ is ______.', 'arctan(x)', ['arctan(x)', 'tan^-1(x)', 'inverse tan']),
            (10, 'The integral $\\int \\tan(x) dx$ involves the natural log of absolute ______.', 'sec(x)', ['sec(x)', 'secant']),
            (11, 'Simpson\'s Rule for approximation requires the number of subintervals $n$ to be ______.', 'even', ['even']),
            (12, 'When using the Trapezoidal Rule, we approximate the area using ______.', 'trapezoids', ['trapezoids'])
        ]
        quiz26.question_set.all().delete()
        for o, t, a, acc in q_data_26: Question.objects.create(quiz=quiz26, question_order=o, question_text=t, model_answer=a, accepted_answers=acc)
        self.stdout.write(f'Created Quiz: {quiz26.title}')

        # --- Quiz 27: Techniques: Strategy & Recognition (Theoretical / Self-Eval) ---
        desc_27 = "Develop the instinct for choosing the right method."
        quiz27, _ = Quiz.objects.get_or_create(
            title='Techniques: Strategy & Recognition',
            quiz_type=Quiz.QuizType.THEORETICAL,
            evaluation_method=Quiz.EvaluationMethod.SELF_EVAL,
            defaults={'domain': Quiz.Domain.CALCULUS, 'subject': Quiz.Subject.CALCULUS_2, 'topic': 'Techniques', 'description': desc_27}
        )
        if quiz27.description != desc_27: quiz27.description = desc_27; quiz27.save()

        q_data_27 = [
            (1, 'How do you decide between using U-Substitution and Integration by Parts?', 'Use U-Sub if you see a composite function and its derivative (chain rule pattern). Use Parts if you see a product of unrelated functions (like x*e^x) that doesn\'t fit the chain rule.', []),
            (2, 'What is the visual indicator that you should use Trigonometric Substitution?', 'The presence of terms like $\\sqrt{a^2-x^2}$, $\\sqrt{x^2-a^2}$, or $\\sqrt{x^2+a^2}$ inside an integral that cannot be solved by simple u-sub.', []),
            (3, 'Why does integrating $\\sin^2(x)$ require a half-angle formula while $\\sin^3(x)$ does not?', '$\\sin^3(x)$ has an odd power, so we can peal off one sine and convert the rest to cosine to use u-sub. $\\sin^2(x)$ has no "spare" sine to be the derivative, so we must reduce the power using the identity.', []),
            (4, 'Explain why proper rational functions are easier to integrate than improper ones.', 'Proper rational functions can be directly decomposed into partial fractions. Improper ones require polynomial long division first to separate the polynomial part from the proper rational part.', []),
            (5, 'Why do we need to split an integral like $\\int_{-1}^{1} \\frac{1}{x} dx$ at zero?', 'Because there is an infinite discontinuity at $x=0$. The integral is improper, and we must define it as the sum of limits approaching 0 from left and right. (In this case, it diverges).', []),
            (6, 'What creates an "Indeterminate Form" in an improper integral?', 'When evaluating the limit (e.g., at infinity), if you get $\\infty - \\infty$ or $0 \\cdot \\infty$, you have to use L\'Hopital\'s Rule or algebra to resolve the true value.', []),
            (7, 'If you see $\\int x^2e^{x^3} dx$, what method should you use?', 'U-Substitution. Let $u=x^3$. Then $du=3x^2 dx$, which matches the factor outside.', []),
            (8, 'If you see $\\int x^2e^x dx$, what method should you use?', 'Integration by Parts (twice). You need to reduce the power of $x$ until it disappears.', []),
            (9, 'How do you find the critical numbers of a function $f$?', 'Find all $x$ in the domain where $f\'(x) = 0$ or $f\'(x)$ is undefined.', []),
            (10, 'What is the first step for integrating $\\int \\frac{x^3 + x}{x-1} dx$?', 'Polynomial Long Division. The numerator degree (3) is higher than denominator degree (1), so it is improper.', []),
            (11, 'If $f\'(x) < 0$ and $f\'\'(x) < 0$, describe the shape.', 'Decreasing and Concave Down.', []),
            (12, 'Differentiate $\\ln(x^2)$.', '$2/x$', '2ln(x) -> 2/x.')
        ]
        quiz27.question_set.all().delete()
        for o, t, a, acc in q_data_27: Question.objects.create(quiz=quiz27, question_order=o, question_text=t, model_answer=a, accepted_answers=acc)
        self.stdout.write(f'Created Quiz: {quiz27.title}')

        # --- Quiz 28: Techniques: Improper Integrals Concepts (Theoretical / Self-Eval) ---
        desc_28 = "Understanding infinity in integration."
        quiz28, _ = Quiz.objects.get_or_create(
            title='Techniques: Improper Integrals Concepts',
            quiz_type=Quiz.QuizType.THEORETICAL,
            evaluation_method=Quiz.EvaluationMethod.SELF_EVAL,
            defaults={'domain': Quiz.Domain.CALCULUS, 'subject': Quiz.Subject.CALCULUS_2, 'topic': 'Techniques', 'description': desc_28}
        )
        if quiz28.description != desc_28: quiz28.description = desc_28; quiz28.save()

        q_data_28 = [
            (1, 'What does it mean for an improper integral to "Diverge"?', 'It means the limit of the partial integral does not exist as a finite number (it goes to infinity or oscillates).', []),
            (2, 'Explain the P-Test for integrals of type $\\int_1^\\infty \\frac{1}{x^p} dx$.', 'The integral converges if $p > 1$ and diverges if $p \\le 1$.', []),
            (3, 'How does the Comparison Test help determine determining convergence without solving?', 'If you find a larger function that converges, your function must converge. If you find a smaller function that diverges, your function must diverge.', []),
            (4, 'True or False: If a limit is $0/0$, it does not exist.', 'False. It is indeterminate.', []),
            (5, 'Why is $\\int_1^\\infty \\frac{1}{x} dx$ (Harmonic area) divergent even though the curve goes to zero?', 'Although the height goes to zero, it doesn\'t go to zero "fast enough." The area accumulates slowly but endlessly without bound.', []),
            (6, 'Does $\\int_{-\\infty}^{\\infty} x dx$ equal zero? Why or why not?', 'No, strictly speaking, it diverges. You must evaluate $\\int_{-\\infty}^0$ and $\\int_0^{\\infty}$ separately. Both diverge to infinity, so you cannot cancel them out (unless using Principal Value, but standard calc says diverges).', []),
            (7, 'What condition must be met for a function to be differentiable at a point?', 'The limit of the difference quotient must exist (and be the same from both sides). It implies the function must be continuous and "smooth" (no sharp corners).', []),
            (8, 'Evaluating $\\int_0^1 \\frac{1}{x^2} dx$: What happens?', 'It diverges. The antiderivative is $-1/x$. Limit as $x \\to 0$ is infinity.', []),
            (9, 'Can an improper integral be negative?', 'Yes. If the function is below the x-axis, the "area" will be negative.', []),
            (10, 'Why is $\\int_{-\\infty}^\infty \\frac{1}{1+x^2} dx$ a famous convergent integral?', 'Because the antiderivative is $\\arctan(x)$. $\\arctan(\infty) - \\arctan(-\\infty) = \\pi/2 - (-\\pi/2) = \\pi$.', []),
            (11, 'Is $\\int_1^\\infty e^{-x} dx$ convergent? Explain geometrically.', 'Yes, it is convergent. The graph of $e^{-x}$ decays very quickly, so the "infinite tail" encloses a finite amount of area (specifically, area = 1).', []),
            (12, 'The derivative of constant c is?', '0', [])
        ]
        quiz28.question_set.all().delete()
        for o, t, a, acc in q_data_28: Question.objects.create(quiz=quiz28, question_order=o, question_text=t, model_answer=a, accepted_answers=acc)
        self.stdout.write(f'Created Quiz: {quiz28.title}')

        # --- Quiz 29: Techniques: Solving Integrals (Practical / Self-Eval) ---
        desc_29 = "Practice standard integration techniques."
        quiz29, _ = Quiz.objects.get_or_create(
            title='Techniques: Solving Integrals',
            quiz_type=Quiz.QuizType.PRACTICAL,
            evaluation_method=Quiz.EvaluationMethod.SELF_EVAL,
            defaults={'domain': Quiz.Domain.CALCULUS, 'subject': Quiz.Subject.CALCULUS_2, 'topic': 'Techniques', 'description': desc_29}
        )
        if quiz29.description != desc_29: quiz29.description = desc_29; quiz29.save()

        q_data_29 = [
            (1, 'Solve $\\int x e^x dx$', '$x e^x - e^x + C$', 'Integration by Parts. $u=x, dv=e^x dx$.'),
            (2, 'Solve $\\int \\sin^3(x) dx$', '$-\\cos x + \\frac{\\cos^3 x}{3} + C$', 'Save $\\sin x$. Change $\\sin^2 x$ to $1-\\cos^2 x$. Let $u=\\cos x$.'),
            (3, 'Solve $\\int \\frac{1}{x^2 - 1} dx$', '$\\frac{1}{2}\\ln|x-1| - \\frac{1}{2}\\ln|x+1| + C$', 'Partial Fractions. $\\frac{1}{(x-1)(x+1)} = \\frac{1/2}{x-1} - \\frac{1/2}{x+1}$.'),
            (4, 'Solve $\\int x \\sqrt{x^2+1} dx$', '$\\frac{1}{3}(x^2+1)^{3/2} + C$', 'U-Sub. $u=x^2+1, du=2x dx$. Integral becomes $\\frac{1}{2} \\int u^{1/2} du$.'),
            (5, 'Differentiate $\\frac{1}{x^2}$.', '$-2x^{-3}$ or $-2/x^3$', 'Power rule.'),
            (6, 'Solve $\\int_0^{\\pi/2} \\cos^3 x dx$', '2/3', 'Rewrite $(1-\\sin^2 x)\\cos x$. U-sub $u=\\sin x$. $\\int_0^1 (1-u^2) du = [u - u^3/3]_0^1 = 1 - 1/3 = 2/3$.'),
            (7, 'Solve $\\int x^2 \\ln x dx$', '$\\frac{x^3}{3}\\ln x - \\frac{x^3}{9} + C$', 'Parts. $u=\\ln x, dv=x^2 dx$.'),
            (8, 'Solve $\\int \\frac{2x}{x^2+1} dx$', '$\\ln(x^2+1) + C$', 'Simple U-Sub. $u=x^2+1, du=2x dx$.'),
            (9, 'Solve $\\int \\cos^2 x dx$', '$\\frac{x}{2} + \\frac{\\sin(2x)}{4} + C$', 'Use half-angle identity: $\\frac{1+\\cos(2x)}{2}$.'),
            (10, 'Solve $\\int \\frac{1}{x^2+4} dx$', '$\\frac{1}{2}\\arctan(x/2) + C$', 'Standard formula $\\int \\frac{1}{x^2+a^2} = \\frac{1}{a}\\arctan(x/a)$.'),
            (11, 'Differentiate $x \\sin x$.', '$x\\cos x + \\sin x$', 'Product rule.'),
            (12, 'Solve $\\int \\ln(x) dx$', '$x\\ln(x) - x + C$', 'Integration by Parts. $u=\\ln x, dv=1dx$.'),
        ]
        quiz29.question_set.all().delete()
        for o, t, a, exp in q_data_29: Question.objects.create(quiz=quiz29, question_order=o, question_text=t, model_answer=a, explanation=exp, accepted_answers=[])
        self.stdout.write(f'Created Quiz: {quiz29.title}')

        # --- Quiz 30: Techniques: Advanced Integration (Practical / Self-Eval) ---
        desc_30 = "Advanced problems involving trig substitution and improper integrals."
        quiz30, _ = Quiz.objects.get_or_create(
            title='Techniques: Advanced Integration',
            quiz_type=Quiz.QuizType.PRACTICAL,
            evaluation_method=Quiz.EvaluationMethod.SELF_EVAL,
            defaults={'domain': Quiz.Domain.CALCULUS, 'subject': Quiz.Subject.CALCULUS_2, 'topic': 'Techniques', 'description': desc_30}
        )
        if quiz30.description != desc_30: quiz30.description = desc_30; quiz30.save()

        q_data_30 = [
            (1, 'Use Trig Sub to find $\\int \\frac{1}{x^2\\sqrt{9-x^2}} dx$', '$-\\frac{\\sqrt{9-x^2}}{9x} + C$', 'Let $x=3\\sin\\theta$. Reduces to $\\int \\frac{1}{9}\\csc^2\\theta d\\theta$.'),
            (2, 'Evaluate Improper Integral: $\\int_1^\\infty \\frac{1}{x^2} dx$', '1', 'Limit as $t\\to\\infty$ of $[-1/x]_1^t = 0 - (-1) = 1$. Converges.'),
            (3, 'Evaluate $\\int e^x \\sin x dx$', '$\\frac{e^x(\\sin x - \\cos x)}{2} + C$', 'Use Integration by Parts twice and solve for the integral ("Boomerang" or "Phoenix" method).'),
            (4, 'Evaluate $\\int_0^1 \\frac{1}{\\sqrt{x}} dx$', '2', 'Improper at 0. Limit $t\\to0^+$ of $[2\\sqrt{x}]_t^1 = 2 - 0 = 2$. Converges.'),
            (5, 'Solve $\\int \\arctan(x) dx$', '$x\\arctan(x) - \\frac{1}{2}\\ln(1+x^2) + C$', 'Parts. $u=\\arctan x, dv=dx$. Then simple u-sub.'),
            (6, 'Approximate $\\int_0^4 x^2 dx$ using Trapezoidal Rule with $n=2$.', '24', 'Points: 0, 2, 4. $\\Delta x=2$. $T = \\frac{2}{2} [0^2 + 2(2^2) + 4^2] = 1 [0 + 8 + 16] = 24$. (Exact is 21.33).'),
            (7, 'Solve $\\int \\frac{x+1}{(x-1)^2} dx$', '$\\ln|x-1| - \\frac{2}{x-1} + C$', 'Partial Fractions. $\\frac{A}{x-1} + \\frac{B}{(x-1)^2}$. $A=1, B=2$.'),
            (8, 'Differentiate $\\cos^3(x)$.', '$-3\\cos^2(x)\\sin(x)$', 'Chain rule.'),
            (9, 'Evaluate $\\int_2^\\infty \\frac{1}{x \\ln x} dx$', 'Diverges', 'U-Sub $u=\\ln x$. Integral becomes $\\int \\frac{1}{u} du = \\ln|u|$. Limit is $\\ln(\\infty)$.'),
            (10, 'Find extrema of $y=x^2$.', 'Min at x=0', 'Deriv 2x=0.'),
            (11, 'Solve $\\int \\cot^3 x dx$', '$-\\frac{\\cot^2 x}{2} - \\ln|\\sin x| + C$', 'Rewrite $\\cot x (\\csc^2 x - 1)$. Split into two integrals.'),
            (12, 'Find $\\int \\sin(\\sqrt{x}) dx$', '$-2\\sqrt{x}\\cos\\sqrt{x} + 2\\sin\\sqrt{x} + C$', 'Sub $w=\\sqrt{x \\implies} w^2=x, 2w dw = dx$. Then use Integration by Parts on $2w \\sin w dw$.'),
        ]
        quiz30.question_set.all().delete()
        for o, t, a, exp in q_data_30: Question.objects.create(quiz=quiz30, question_order=o, question_text=t, model_answer=a, explanation=exp, accepted_answers=[])
        self.stdout.write(f'Created Quiz: {quiz30.title}')

        # ==============================================================================
        # CALCULUS 2: SEQUENCES & SERIES
        # ==============================================================================

        # --- Quiz 31: Sequences: Definitions & Basic Limits (Theoretical / Automated) ---
        desc_31 = "Foundational definitions for sequences and simple series behavior."
        quiz31, _ = Quiz.objects.get_or_create(
            title='Sequences: Definitions & Basic Limits',
            quiz_type=Quiz.QuizType.THEORETICAL,
            evaluation_method=Quiz.EvaluationMethod.AUTOMATED,
            defaults={'domain': Quiz.Domain.CALCULUS, 'subject': Quiz.Subject.CALCULUS_2, 'topic': 'Sequences & Series', 'description': desc_31}
        )
        if quiz31.description != desc_31: quiz31.description = desc_31; quiz31.save()

        q_data_31 = [
            (1, 'A ______ is an ordered list of numbers.', 'sequence', ['sequence']),
            (2, 'A ______ is the sum of the terms of a sequence.', 'series', ['series', 'infinite series']),
            (3, 'The limit of the sequence $a_n = \\frac{1}{n}$ as $n \\to \\infty$ is ______.', '0', ['0', 'zero']),
            (4, 'The limit of the sequence $a_n = (-1)^n$ ______.', 'does not exist', ['does not exist', 'dne']),
            (5, 'A sequence is called ______ if it is either always increasing or always decreasing.', 'monotonic', ['monotonic', 'monotone']),
            (6, 'If $f\'(x) > 0$ for all x, then f is ______.', 'increasing', ['increasing']),
            (7, 'A Geometric Series with ratio $r$ converges if $|r| < $ ______.', '1', ['1', 'one']),
            (8, 'The sum of a convergent geometric series starting at $a$ is given by the formula ______.', 'a/(1-r)', ['a/(1-r)', 'a/1-r']),
            (9, 'The derivative of $\\tan(x)$ is ______.', 'sec^2(x)', ['sec^2(x)', 'secant squared']),
            (10, 'The P-series $\\sum \\frac{1}{n^p}$ converges if $p > $ ______.', '1', ['1', 'one']),
            (11, 'The Harmonic Series $\\sum \\frac{1}{n}$ is known to ______.', 'diverge', ['diverge']),
            (12, 'The Alternating Harmonic Series $\\sum \\frac{(-1)^{n+1}}{n}$ is known to ______.', 'converge', ['converge'])
        ]
        quiz31.question_set.all().delete()
        for o, t, a, acc in q_data_31: Question.objects.create(quiz=quiz31, question_order=o, question_text=t, model_answer=a, accepted_answers=acc)
        self.stdout.write(f'Created Quiz: {quiz31.title}')

        # --- Quiz 32: Series: Convergence Test Rules (Theoretical / Automated) ---
        desc_32 = "Test your memory of the conditions for various convergence tests."
        quiz32, _ = Quiz.objects.get_or_create(
            title='Series: Convergence Test Rules',
            quiz_type=Quiz.QuizType.THEORETICAL,
            evaluation_method=Quiz.EvaluationMethod.AUTOMATED,
            defaults={'domain': Quiz.Domain.CALCULUS, 'subject': Quiz.Subject.CALCULUS_2, 'topic': 'Sequences & Series', 'description': desc_32}
        )
        if quiz32.description != desc_32: quiz32.description = desc_32; quiz32.save()

        q_data_32 = [
            (1, 'The Divergence Test states: If $\\lim a_n \\neq 0$, then the series ______.', 'diverges', ['diverges', 'must diverge']),
            (2, 'For the Integral Test, the function $f(x)$ must be continuous, positive, and ______.', 'decreasing', ['decreasing']),
            (3, 'In the Ratio Test, if the limit $L < 1$, the series ______.', 'converges', ['converges', 'converges absolutely']),
            (4, 'At a vertical asymptote $x=a$, the limit as $x \\to a$ is usually plus or minus ______.', 'infinity', ['infinity']),
            (5, 'In the Ratio Test, if the limit $L > 1$, the series ______.', 'diverges', ['diverges']),
            (6, 'In the Ratio Test, if the limit $L = 1$, the test is ______.', 'inconclusive', ['inconclusive', 'unknown']),
            (7, 'The Limit Comparison Test requires the limit of the ratio of terms to be a positive ______ number.', 'finite', ['finite', 'real']),
            (8, 'The set of all input values for which a function is defined is called its ______.', 'domain', ['domain']),
            (9, 'If a series converges locally but the series of absolute values diverges, it is called ______ convergence.', 'conditional', ['conditional']),
            (10, 'If $\\sum |a_n|$ converges, then $\\sum a_n$ is said to be ______ convergent.', 'absolutely', ['absolutely', 'absolute']),
            (11, 'A Taylor Series centered at $a=0$ is specifically called a ______ Series.', 'maclaurin', ['maclaurin']),
            (12, 'The Root Test is most useful when terms involve ______ powers of $n$.', 'nth', ['nth', 'n', 'n-th'])
        ]
        quiz32.question_set.all().delete()
        for o, t, a, acc in q_data_32: Question.objects.create(quiz=quiz32, question_order=o, question_text=t, model_answer=a, accepted_answers=acc)
        self.stdout.write(f'Created Quiz: {quiz32.title}')

        # --- Quiz 33: Sequences: Conceptual Convergence (Theoretical / Self-Eval) ---
        desc_33 = "Understand the subtle difference between sequences and series convergence."
        quiz33, _ = Quiz.objects.get_or_create(
            title='Sequences: Conceptual Convergence',
            quiz_type=Quiz.QuizType.THEORETICAL,
            evaluation_method=Quiz.EvaluationMethod.SELF_EVAL,
            defaults={'domain': Quiz.Domain.CALCULUS, 'subject': Quiz.Subject.CALCULUS_2, 'topic': 'Sequences & Series', 'description': desc_33}
        )
        if quiz33.description != desc_33: quiz33.description = desc_33; quiz33.save()

        q_data_33 = [
            (1, 'Explain the difference between $\{a_n\}$ converging and $\\sum a_n$ converging.', '$\{a_n\}$ converges if the terms approach a single number. $\\sum a_n$ converges if the SUM of the terms approaches a single number. (e.g., $1, 1, 1...$ converges as a sequence, but the sum diverges).', []),
            (2, 'Why does the Harmonic Series diverge even though the terms get smaller?', 'The terms $1/n$ approach zero, but they do so very slowly. The sum "piles up" effectively infinite area (like calculating $\\int 1/x$).', []),
            (3, 'Interpret the Ratio Test logic: Why does $L<1$ imply convergence?', 'If the ratio of successive terms is less than 1, the series eventually behaves like a Geometric Series with $r < 1$, which is known to converge.', []),
            (4, 'What is the "Radius of Convergence"?', 'It is the distance R from the center $a$ such that the power series converges for all $|x-a| < R$.', []),
            (5, 'Explain "Conditional Convergence" using the Alternating Harmonic Series.', 'The series $1 - 1/2 + 1/3 - ...$ converges (sums to ln 2). However, if you make all signs positive ($1 + 1/2 + ...$), it diverges. Thus, it only converges "on the condition" that the signs alternate.', []),
            (6, 'If $\\lim_{n \\to \\infty} a_n = 0$, does the series $\\sum a_n$ automatically converge? Give a counter-example.', 'No. The Harmonic Series ($1/n$) has terms going to 0, but the sum is infinite.', []),
            (7, 'Can a series sum to a negative number?', 'Yes. If the terms are negative, or if it is an alternating series dominated by negative terms.', []),
            (8, 'Why is the Integral Test valid?', 'Because the sum $\\sum f(n)$ can be bounded by the integral $\\int f(x) dx$ (using left and right Riemann sums methodology). If the area is finite, the sum is finite.', []),
            (9, 'What is the definition of a horizontal asymptote?', 'The line $y=L$ is a horizontal asymptote if $\\lim_{x \\to \\infty} f(x) = L$ or $\\lim_{x \\to -\\infty} f(x) = L$.', []),
            (10, 'True or False: If $\\sum a_n$ converges, then $\\lim_{n \\to \\infty} a_n$ must be 0.', 'True. This is the logic behind the Divergence Test (contrapositive).', []),
            (11, 'Does $f(x)=|x|$ have a derivative at 0?', 'No', 'Corner point.')
        ]
        quiz33.question_set.all().delete()
        for o, t, a, acc in q_data_33: Question.objects.create(quiz=quiz33, question_order=o, question_text=t, model_answer=a, accepted_answers=acc)
        self.stdout.write(f'Created Quiz: {quiz33.title}')

        # --- Quiz 34: Series: Theory of Power Series (Theoretical / Self-Eval) ---
        desc_34 = "Deep dive into power series representation of functions."
        quiz34, _ = Quiz.objects.get_or_create(
            title='Series: Theory of Power Series',
            quiz_type=Quiz.QuizType.THEORETICAL,
            evaluation_method=Quiz.EvaluationMethod.SELF_EVAL,
            defaults={'domain': Quiz.Domain.CALCULUS, 'subject': Quiz.Subject.CALCULUS_2, 'topic': 'Sequences & Series', 'description': desc_34}
        )
        if quiz34.description != desc_34: quiz34.description = desc_34; quiz34.save()

        q_data_34 = [
            (1, 'Does a Power Series always converge at its center $x=a$?', 'Yes. At $x=a$, all terms involving $(x-a)$ become 0. The sum is just the first constant term, so it trivially converges.', []),
            (2, 'What do we check at the "endpoints" of the Interval of Convergence?', 'We must manually plug in the endpoint values ($x = a-R$ and $x = a+R$) into the original series to see if it converges at those specific points, because the Ratio Test is inconclusive there.', []),
            (3, 'What is the Taylor Series formula for $f(x)$ centered at $a$?', '$f(x) = \\sum_{n=0}^\\infty \\frac{f^{(n)}(a)}{n!} (x-a)^n$.', []),
            (4, 'Write the Maclaurin Series for $e^x$.', '$1 + x + \\frac{x^2}{2!} + \\frac{x^3}{3!} + ... = \\sum \\frac{x^n}{n!}$.', []),
            (5, 'Write the Maclaurin Series for $\\sin(x)$.', '$x - \\frac{x^3}{3!} + \\frac{x^5}{5!} - ... = \\sum (-1)^n \\frac{x^{2n+1}}{(2n+1)!}$.', []),
            (6, 'How can you find the power series deriviative of a function?', 'You can differentiate the power series term-by-term. The radius of convergence remains the same.', []),
            (7, 'Derivative of $\\arctan(x)$.', '$1/(1+x^2)$', []),
            (8, 'What is the series for $\\frac{1}{1-x}$?', '$1 + x + x^2 + x^3 + ... = \\sum x^n$, for $|x| < 1$.', []),
            (9, 'How do you find the Maclaurin series for $e^{-x^2}$?', 'Take the series for $e^u$ and substitute $u = -x^2$.', []),
            (10, 'What is the Binomial Series expansion for $(1+x)^k$?', '$1 + kx + \\frac{k(k-1)}{2!}x^2 + \\frac{k(k-1)(k-2)}{3!}x^3 + ...$', []),
            (11, 'Linear approximation of $\\sqrt{x}$ at $x=1$.', 'L(x) = 1 + 1/2(x-1)', []),
            (12, 'Write the Maclaurin Series for $\\cos(x)$.', '$1 - \\frac{x^2}{2!} + \\frac{x^4}{4!} - ... = \\sum (-1)^n \\frac{x^{2n}}{(2n)!}$.', []),
        ]
        quiz34.question_set.all().delete()
        for o, t, a, acc in q_data_34: Question.objects.create(quiz=quiz34, question_order=o, question_text=t, model_answer=a, accepted_answers=acc)
        self.stdout.write(f'Created Quiz: {quiz34.title}')

        # --- Quiz 35: Sequences: Limit Calculations (Practical / Self-Eval) ---
        desc_35 = "Practice finding limits of sequences and sums of geometric series."
        quiz35, _ = Quiz.objects.get_or_create(
            title='Sequences: Limit Calculations',
            quiz_type=Quiz.QuizType.PRACTICAL,
            evaluation_method=Quiz.EvaluationMethod.SELF_EVAL,
            defaults={'domain': Quiz.Domain.CALCULUS, 'subject': Quiz.Subject.CALCULUS_2, 'topic': 'Sequences & Series', 'description': desc_35}
        )
        if quiz35.description != desc_35: quiz35.description = desc_35; quiz35.save()

        q_data_35 = [
            (1, 'Find the limit of sequence $a_n = \\frac{n+1}{3n-1}$.', '1/3', 'Divide by n: $\\frac{1 + 1/n}{3 - 1/n} \\to 1/3$.'),
            (2, 'Find $\\lim_{n \\to \\infty} (1 + \\frac{1}{n})^n$.', 'e (approx 2.718)', 'definition of e.'),
            (3, 'Does sequence $a_n = \\cos(n\\pi)$ converge?', 'No', 'It alternates $1, -1, 1, -1$. It oscillates and never settles on one value.'),
            (4, 'Limit x->0 of (sin 3x)/x.', '3', '3 * (sin 3x)/3x -> 3*1 = 3.'),
            (5, 'Find sum of $\\sum_{n=1}^\\infty \\frac{1}{n(n+1)}$ (Telescoping).', '1', 'Partial Frac: $\\frac{1}{n} - \\frac{1}{n+1}$. Sums to $(1 - 1/2) + (1/2 - 1/3) ... = 1$.'),
            (6, 'Find limit of $a_n = \\frac{\\ln n}{\\sqrt{n}}$.', '0', 'L\'Hopital or growth rates. $\\sqrt{n}$ grows faster than $\\ln n$.'),
            (7, 'Find limit of $a_n = \\frac{(-1)^n}{n}$.', '0', 'Squeeze Theorem. $-1/n \\le a_n \\le 1/n$. Both bounds go to 0.'),
            (8, 'Limit x->2 of x^2.', '4', 'Plug in.'),
            (9, 'Find limit of $a_n = \\sqrt{n+1} - \\sqrt{n}$.', '0', 'Multiply by conjugate $\\frac{\\sqrt{n+1}+\\sqrt{n}}{\\sqrt{n+1}+\\sqrt{n}}$. Becomes $\\frac{1}{\\sqrt{n+1}+\\sqrt{n}} \\to 0$.'),
            (10, 'Find sum of $0.999...$ as a series.', '1', '$\\sum_{n=1}^\\infty 9(1/10)^n$. $a=0.9, r=0.1$. Sum = $0.9 / (1-0.1) = 0.9/0.9 = 1$.'),
            (11, 'Find the sum of series $\\sum_{n=1}^\\infty 3(\\frac{1}{2})^{n-1}$.', '6', 'Geometric. $a=3, r=1/2$. Sum = $3 / (1 - 1/2) = 3 / (1/2) = 6$.'),
            (12, 'Find sum of $\\sum_{n=0}^\\infty \\frac{2^{n+1}}{5^n}$.', '10/3', 'Geometric. Rewrite as $2 \\sum (2/5)^n$. $a=2, r=2/5$. Sum = $2 / (1 - 2/5) = 2 / (3/5) = 10/3$.'),
        ]
        quiz35.question_set.all().delete()
        for o, t, a, exp in q_data_35: Question.objects.create(quiz=quiz35, question_order=o, question_text=t, model_answer=a, explanation=exp, accepted_answers=[])
        self.stdout.write(f'Created Quiz: {quiz35.title}')

        # --- Quiz 36: Series: Convergence Testing (Practical / Self-Eval) ---
        desc_36 = "Determine if the following series converge or diverge."
        quiz36, _ = Quiz.objects.get_or_create(
            title='Series: Convergence Testing',
            quiz_type=Quiz.QuizType.PRACTICAL,
            evaluation_method=Quiz.EvaluationMethod.SELF_EVAL,
            defaults={'domain': Quiz.Domain.CALCULUS, 'subject': Quiz.Subject.CALCULUS_2, 'topic': 'Sequences & Series', 'description': desc_36}
        )
        if quiz36.description != desc_36: quiz36.description = desc_36; quiz36.save()

        q_data_36 = [
            (1, 'Test $\\sum \\frac{1}{n^3}$.', 'Converges', 'P-Series with $p=3 > 1$.'),
            (2, 'Test $\\sum \\frac{n}{2n+1}$.', 'Diverges', 'Divergence Test. limit is $1/2 \\neq 0$.'),
            (3, 'Test $\\sum \\frac{(-1)^n}{n}$.', 'Converges', 'Alternating Harmonic Series converges.'),
            (4, 'Test $\\sum \\frac{n}{2^n}$.', 'Converges', 'Ratio Test. ratio $\\to 1/2 < 1$.'),
            (5, 'Test $\\sum \\frac{1}{\\sqrt{n}}$.', 'Diverges', 'P-Series with $p=1/2 \\le 1$.'),
            (6, 'If f\'(x) changes + to -, that x is a ______.', 'Local Max', None),
            (7, 'Test $\\sum \\frac{\\sin^2(n)}{n^2}$.', 'Converges', 'Direct Comparison with $\\frac{1}{n^2}$ (which converges). $\\sin^2 n \\le 1$.'),
            (8, 'Test $\\sum \\frac{1}{n \\ln n}$.', 'Diverges', 'Integral Test. $\\int \\frac{1}{x \\ln x} dx = \\ln(\\ln x) \\to \\infty$.'),
            (9, 'Test $\\sum \\frac{n^n}{n!}$.', 'Converges (Actually Diverges!)', 'Ratio Test. $\\lim (1+1/n)^n = e > 1$. Wait, careful! $n^n$ grows faster. It DIVERGES.'),
            (10, 'Test $\\sum (-1)^n \\frac{n}{\\sqrt{n^3 + 2}}$.', 'Converges', 'Alternating Series Test. Terms decrease to 0. (Be careful with absolute convergence check).'),
            (11, 'Find Radius of Convergence for $\\sum \\frac{x^n}{n}$.', '1', 'Ratio Test. $|x| < 1$, so R=1. (Converges on $[-1, 1)$).'),
            (12, 'Integral of 0 dx.', 'C', 'Constant.')
        ]
        quiz36.question_set.all().delete()
        for o, t, a, exp in q_data_36: Question.objects.create(quiz=quiz36, question_order=o, question_text=t, model_answer=a, explanation=exp, accepted_answers=[])
        self.stdout.write(f'Created Quiz: {quiz36.title}')

        self.stdout.write(f'Created Quiz: {quiz36.title}')

        # ==========================================
        # Linear Algebra Quizzes (Subject: Mechanics)
        # ==========================================
        
        # Quiz 1: Vectors: Dot Products & Lengths (Automated)
        quiz_la_1, created_la_1 = Quiz.objects.get_or_create(
            title='Vectors: Dot Products & Lengths',
            quiz_type=Quiz.QuizType.THEORETICAL,
            evaluation_method=Quiz.EvaluationMethod.AUTOMATED,
            defaults={
                'domain': Quiz.Domain.LINEAR_ALGEBRA,
                'subject': Quiz.Subject.MECHANICS,
                'topic': 'Vectors & Matrices',
                'description': "Practice with dot products, norms, and vector properties. Automatically graded.",
                'created_at': timezone.now()
            }
        )
        if created_la_1: self.stdout.write(f'Created Quiz: {quiz_la_1.title}')
        
        quiz_1_data = [
            {
                "question_text": "If v = (1, 1) and w = (2, -1), what is the value of the dot product v · w?",
                "model_answer": "1",
                "accepted_answers": ["1", "one"],
                "explanation": "The dot product is (1)(2) + (1)(-1) = 2 - 1 = 1."
            },
            {
                "question_text": "Vectors whose dot product equals zero are called what?",
                "model_answer": "Orthogonal",
                "accepted_answers": ["orthogonal", "perpendicular", "normal"],
                "explanation": "If v · w = 0, the angle between them is 90 degrees."
            },
            {
                "question_text": "Calculate the length (norm) of the vector v = (3, 4).",
                "model_answer": "5",
                "accepted_answers": ["5", "five"],
                "explanation": "Length is the square root of (3^2 + 4^2) = sqrt(9+16) = sqrt(25) = 5."
            },
            {
                "question_text": "A unit vector is a vector whose length equals what number?",
                "model_answer": "1",
                "accepted_answers": ["1", "one"],
                "explanation": "Unit vectors are u = v / ||v||, resulting in a length of 1."
            },
            {
                "question_text": "In the linear combination c(1, 0) + d(0, 1), if the result is vector (5, 2), what is the value of c?",
                "model_answer": "5",
                "accepted_answers": ["5", "five"],
                "explanation": "c(1, 0) + d(0, 1) = (c, d). Therefore c=5 and d=2."
            },
            {
                "question_text": "Complete the inequality name: The Cauchy-_______ Inequality states that |v · w| ≤ ||v|| ||w||.",
                "model_answer": "Schwarz",
                "accepted_answers": ["Schwarz", "Bunyakovsky", "Schwarz inequality"],
                "explanation": "The Cauchy-Schwarz inequality connects geometry (lengths) to algebra (dot products)."
            },
            {
                "question_text": "If vector v is in 3-dimensional space (R3), how many components does it have?",
                "model_answer": "3",
                "accepted_answers": ["3", "three"],
                "explanation": "R3 denotes a space with 3 dimensions (x, y, z)."
            },
            {
                "question_text": "What is the result of the dot product of a vector with itself (v · v)?",
                "model_answer": "Length squared",
                "accepted_answers": ["length squared", "norm squared", "magnitude squared", "||v||^2", "|v|^2"],
                "explanation": "v · v = ||v||^2."
            },
            {
                "question_text": "If w = 2v, what is the angle between vector v and vector w in degrees?",
                "model_answer": "0",
                "accepted_answers": ["0", "zero", "0 degrees"],
                "explanation": "One is a positive scalar multiple of the other, so they point in the exact same direction."
            },
            {
                "question_text": "If you divide a non-zero vector v by its length ||v||, what property does the resulting vector u have?",
                "model_answer": "It has length 1",
                "accepted_answers": ["length 1", "unit vector", "norm 1", "magnitude 1"],
                "explanation": "This process is called 'Normalization'. The direction remains the same, but the length becomes 1. This is crucial in ML for feature scaling."
            }
        ]
        
        quiz_la_1.question_set.all().delete()
        for idx, q in enumerate(quiz_1_data, 1):
            Question.objects.create(
                quiz=quiz_la_1,
                question_order=idx,
                question_text=q['question_text'],
                model_answer=q['model_answer'],
                accepted_answers=q['accepted_answers'],
                explanation=q.get('explanation', '')
            )

        # Quiz 2: Vectors: Theoretical Concepts (Self-Eval)
        quiz_la_2, created_la_2 = Quiz.objects.get_or_create(
            title='Vectors: Theoretical Concepts',
            quiz_type=Quiz.QuizType.THEORETICAL,
            evaluation_method=Quiz.EvaluationMethod.SELF_EVAL,
            defaults={
                'domain': Quiz.Domain.LINEAR_ALGEBRA,
                'subject': Quiz.Subject.MECHANICS,
                'topic': 'Vectors & Matrices',
                'description': "Conceptual understanding of vector geometry and linear combinations. Self-graded.",
                'created_at': timezone.now()
            }
        )
        if created_la_2: self.stdout.write(f'Created Quiz: {quiz_la_2.title}')

        quiz_2_data = [
            {
                "question_text": "Describe the geometric shape formed by all linear combinations of two non-zero, non-parallel vectors, v and w, in 3D space (R3).",
                "model_answer": "A plane passing through the origin.",
                "accepted_answers": [],
                "explanation": "The set of all c*v + d*w generates a 2D plane. It must pass through the origin because c=0, d=0 gives the zero vector."
            },
            {
                "question_text": "Explain why the dot product v · w is negative if the angle between them is obtuse (greater than 90 degrees).",
                "model_answer": "The formula for dot product is ||v|| ||w|| cos(theta). Lengths are always positive. Cosine is negative for angles between 90 and 180 degrees, making the total product negative.",
                "accepted_answers": [],
                "explanation": "This geometric link relies on the cosine behavior."
            },
            {
                "question_text": "Using the Triangle Inequality ||v + w|| ≤ ||v|| + ||w||, explain when the equality holds (when is the 'less than' actually 'equal to')?",
                "model_answer": "Equality holds only when v and w are in the same direction (parallel and pointing the same way).",
                "accepted_answers": [],
                "explanation": "Geometrically, this means the triangle flattens into a straight line."
            },
            {
                "question_text": "How do you algebraically determine if three vectors in R3 lie on the same plane?",
                "model_answer": "They lie on the same plane if one vector can be written as a linear combination of the other two (linearly dependent). Or, if their volume/determinant is zero.",
                "accepted_answers": [],
                "explanation": "If u = c*v + d*w, then u adds no new dimension; it stays in the plane defined by v and w."
            },
            {
                "question_text": "Describe the difference between v = (1, 2, 3) as a point and v = (1, 2, 3) as a vector.",
                "model_answer": "As a point, it is a specific location in space. As a vector, it is an arrow (magnitude and direction) starting at the origin (0,0,0) and ending at that point.",
                "accepted_answers": [],
                "explanation": "Vectors represent displacement; points represent position."
            },
            {
                "question_text": "Why is the zero vector (0,0) orthogonal to every other vector?",
                "model_answer": "Because the dot product of the zero vector with any vector v is 0 (0*x + 0*y = 0). By definition, dot product = 0 implies orthogonality.",
                "accepted_answers": [],
                "explanation": "It creates a unique geometric edge case where the angle is technically undefined, but orthogonality holds algebraically."
            },
            {
                "question_text": "Explain the concept of a 'Linear Combination' in your own words.",
                "model_answer": "It is the process of taking vectors, scaling them by constant numbers (scalars), and adding the results together (cv + dw).",
                "accepted_answers": [],
                "explanation": "This is the fundamental operation of linear algebra."
            },
            {
                "question_text": "If ||v|| = 3 and ||w|| = 4, what are the maximum and minimum possible values for ||v - w||?",
                "model_answer": "Max: 7, Min: 1",
                "accepted_answers": [],
                "explanation": "Max occurs when they point in opposite directions (3 - (-4) distance = 7). Min occurs when they point in same direction (4 - 3 = 1)."
            },
            {
                "question_text": "What does the equation cos(theta) = (v · w) / (||v|| ||w||) tell us about the relationship between vector algebra and geometry?",
                "model_answer": "It links the algebraic calculation of coordinates (dot product) to geometric intuition (angles).",
                "accepted_answers": [],
                "explanation": "This allows us to find angles in high-dimensional spaces where we cannot visualize them."
            },
            {
                "question_text": "Visually, how do you find v + w using the parallelogram rule?",
                "model_answer": "Place the tail of w at the head of v. The vector from the start of v to the end of w is the sum.",
                "accepted_answers": [],
                "explanation": "Alternatively, draw both from the origin and complete the parallelogram; the diagonal is the sum."
            }
        ]

        quiz_la_2.question_set.all().delete()
        for idx, q in enumerate(quiz_2_data, 1):
            Question.objects.create(
                quiz=quiz_la_2,
                question_order=idx,
                question_text=q['question_text'],
                model_answer=q['model_answer'],
                accepted_answers=q['accepted_answers'],
                explanation=q.get('explanation', '')
            )

        # Quiz 3: Matrices: Multiplication & Operations (Automated)
        quiz_la_3, created_la_3 = Quiz.objects.get_or_create(
            title='Matrices: Multiplication & Operations',
            quiz_type=Quiz.QuizType.THEORETICAL,
            evaluation_method=Quiz.EvaluationMethod.AUTOMATED,
            defaults={
                'domain': Quiz.Domain.LINEAR_ALGEBRA,
                'subject': Quiz.Subject.MECHANICS,
                'topic': 'Vectors & Matrices',
                'description': "Matrix operations check.",
                'created_at': timezone.now()
            }
        )
        if created_la_3: self.stdout.write(f'Created Quiz: {quiz_la_3.title}')

        quiz_3_data = [
            {
                "question_text": "If A is a 3x2 matrix and B is a 2x5 matrix, what are the dimensions of the product AB?",
                "model_answer": "3x5",
                "accepted_answers": ["3x5", "3 by 5", "3 * 5"],
                "explanation": "(m x n) * (n x p) results in (m x p)."
            },
            {
                "question_text": "Is Matrix Multiplication commutative? (Yes/No)",
                "model_answer": "No",
                "accepted_answers": ["No", "no", "false"],
                "explanation": "In general, AB does not equal BA. Dimensions might not even match."
            },
            {
                "question_text": "Strang's 'Column View': The product Ax is a linear combination of the _______ of A.",
                "model_answer": "Columns",
                "accepted_answers": ["columns", "column vectors"],
                "explanation": "Ax = x1(col1) + x2(col2) + ... This is the most important concept in Chapter 1."
            },
            {
                "question_text": "If A is a 3x3 Identity matrix (I) and v is a vector, what is I*v?",
                "model_answer": "v",
                "accepted_answers": ["v", "vector v", "the same vector"],
                "explanation": "The identity matrix acts like the number 1 in scalar multiplication."
            },
            {
                "question_text": "In the multiplication AB, the entry in row i and column j comes from the dot product of Row i of A and _______ of B.",
                "model_answer": "Column j",
                "accepted_answers": ["column j", "Column j", "col j"],
                "explanation": "This is the standard 'Row-Column' rule for matrix multiplication."
            },
            {
                "question_text": "The transpose of a matrix A (denoted A^T) transforms the rows of A into the _______ of A^T.",
                "model_answer": "Columns",
                "accepted_answers": ["columns", "cols"],
                "explanation": "Rows become columns and columns become rows."
            },
            {
                "question_text": "If Matrix A has dependent columns, is the matrix invertible? (Yes/No)",
                "model_answer": "No",
                "accepted_answers": ["No", "no"],
                "explanation": "Dependent columns mean the matrix is singular (not invertible)."
            },
            {
                "question_text": "Calculate the inner product (dot product) of row vector [1, 2] and column vector [3; 4].",
                "model_answer": "11",
                "accepted_answers": ["11", "eleven"],
                "explanation": "1*3 + 2*4 = 3 + 8 = 11."
            },
            {
                "question_text": "If A is a 2x1 matrix (column) and B is a 1x2 matrix (row), the product AB is what size matrix?",
                "model_answer": "2x2",
                "accepted_answers": ["2x2", "2 by 2"],
                "explanation": "This is an 'Outer Product', which creates a matrix of rank 1."
            },
            {
                "question_text": "If A is invertible, what is the unique solution to Ax = b?",
                "model_answer": "x = A^-1 b",
                "accepted_answers": ["x = A^-1 b", "A^-1 b", "A inverse b"],
                "explanation": "Multiply both sides by A inverse on the left."
            }
        ]

        quiz_la_3.question_set.all().delete()
        for idx, q in enumerate(quiz_3_data, 1):
            Question.objects.create(
                quiz=quiz_la_3,
                question_order=idx,
                question_text=q['question_text'],
                model_answer=q['model_answer'],
                accepted_answers=q['accepted_answers'],
                explanation=q.get('explanation', '')
            )

        # Quiz 4: Matrices: Column Space & Rules (Self-Eval)
        quiz_la_4, created_la_4 = Quiz.objects.get_or_create(
            title='Matrices: Algebra & Properties',
            quiz_type=Quiz.QuizType.THEORETICAL,
            evaluation_method=Quiz.EvaluationMethod.SELF_EVAL,
            defaults={
                'domain': Quiz.Domain.LINEAR_ALGEBRA,
                'subject': Quiz.Subject.MECHANICS,
                'topic': 'Vectors & Matrices',
                'description': "Understanding matrix algebra, inverses, and partitions.",
                'created_at': timezone.now()
            }
        )
        if created_la_4: self.stdout.write(f'Created Quiz: {quiz_la_4.title}')

        quiz_4_data = [
            {
                "question_text": "Explain the difference between the Row-Column rule (dot products) and the Column-Row rule (sum of outer products) for matrix multiplication AB.",
                "model_answer": "Row-Col rule calculates one number at a time (inner products). Col-Row rule sums up full matrices (Column k of A multiplied by Row k of B). Both give the same result.",
                "accepted_answers": [],
                "explanation": "Strang emphasizes the Col-Row rule (outer products) for understanding the structure of the data."
            },
            {
                "question_text": "What is the formula for the inverse of a product (AB)^-1?",
                "model_answer": "B^-1 A^-1",
                "accepted_answers": [],
                "explanation": "The order must be reversed: shoes and socks rule."
            },
            {
                "question_text": "If det(A) = 0 for a square matrix A, is the matrix invertible (non-singular)?",
                "model_answer": "No",
                "accepted_answers": [],
                "explanation": "A determinant of zero indicates the matrix collapses space and cannot be reversed."
            },
            {
                "question_text": "What is the transpose of the product (AB)^T?",
                "model_answer": "B^T A^T",
                "accepted_answers": [],
                "explanation": "Like the inverse, the transpose of a product reverses the order of multiplication."
            },
            {
                "question_text": "Why does (AB)C = A(BC)? (Associativity). Explain conceptually, not just by writing the property name.",
                "model_answer": "Matrix multiplication represents applying linear transformations sequentially. Applying transformation C, then B, then A is the same sequence regardless of how we group the calculations.",
                "accepted_answers": [],
                "explanation": "Matrices are functions acting on vectors."
            },
            {
                "question_text": "In the CR decomposition (A = CR), if A is a matrix of rank 1, what are the dimensions of C and R?",
                "model_answer": "C is a single column (m x 1) and R is a single row (1 x n).",
                "accepted_answers": [],
                "explanation": "Every rank 1 matrix is the outer product of one column and one row."
            },
            {
                "question_text": "How does multiplying a matrix A by a diagonal matrix D on the right (AD) affect the columns of A?",
                "model_answer": "It scales the columns of A. The first column is multiplied by d1, the second by d2, etc.",
                "accepted_answers": [],
                "explanation": "Multiplying on the Right affects Columns. Multiplying on the Left affects Rows."
            },
            {
                "question_text": "If A and B are both Upper Triangular matrices, what is true about their product AB?",
                "model_answer": "AB is also Upper Triangular.",
                "accepted_answers": [],
                "explanation": "The linear combinations of triangular columns preserve the triangular structure."
            },
            {
                "question_text": "Explain why the columns of the Identity Matrix are important.",
                "model_answer": "They are the standard basis vectors (1,0,0...), (0,1,0)... Any vector v can be written as a combination of these columns simply by using the components of v as the weights.",
                "accepted_answers": [],
                "explanation": "This is why I*v = v."
            },
            {
                "question_text": "If you view matrix multiplication AB as A acting on the columns of B, what is the result?",
                "model_answer": "The result is a matrix where the columns are A * (col 1 of B), A * (col 2 of B), etc.",
                "accepted_answers": [],
                "explanation": "This allows us to treat matrix multiplication as a collection of matrix-vector products."
            }
        ]

        quiz_la_4.question_set.all().delete()
        for idx, q in enumerate(quiz_4_data, 1):
            Question.objects.create(
                quiz=quiz_la_4,
                question_order=idx,
                question_text=q['question_text'],
                model_answer=q['model_answer'],
                accepted_answers=q['accepted_answers'],
                explanation=q.get('explanation', '')
            )
        self.stdout.write(f'Created Quiz: {quiz_la_4.title}')

        # Quiz 5: Gaussian Elimination & Pivots (Theoretical)
        quiz_la_5, created_la_5 = Quiz.objects.get_or_create(
            title='Gaussian Elimination & Pivots',
            quiz_type=Quiz.QuizType.THEORETICAL,
            evaluation_method=Quiz.EvaluationMethod.SELF_EVAL,
            defaults={
                'domain': Quiz.Domain.LINEAR_ALGEBRA,
                'subject': Quiz.Subject.MECHANICS,
                'topic': 'Vectors & Matrices',
                'description': "Understanding pivots, multipliers, and elimination steps.",
                'created_at': timezone.now()
            }
        )
        if created_la_5: self.stdout.write(f'Created Quiz: {quiz_la_5.title}')

        quiz_5_data = [
            {
                "question_text": "In Gaussian elimination, the first non-zero entry in a row used to eliminate entries below it is called the _______.",
                "model_answer": "Pivot",
                "accepted_answers": ["pivot", "pivot element"],
                "explanation": "Pivots are the crucial diagonal entries that must not be zero to proceed without row exchanges."
            },
            {
                "question_text": "If we subtract 3 times Row 1 from Row 2, what is the 'multiplier' ($l_{21}$) associated with this operation?",
                "model_answer": "3",
                "accepted_answers": ["3", "three"],
                "explanation": "The multiplier is the number you multiply the pivot row by to cancel the entry below it."
            },
            {
                "question_text": "Elimination converts matrix A into an ______ Triangular matrix U.",
                "model_answer": "Upper",
                "accepted_answers": ["upper", "Upper"],
                "explanation": "The result of forward elimination is U, where all entries below the diagonal are zero."
            },
            {
                "question_text": "A matrix that has no inverse is technically called _______.",
                "model_answer": "Singular",
                "accepted_answers": ["singular", "non-invertible", "degenerate"],
                "explanation": "A singular matrix has a determinant of 0 and fewer than n pivots."
            },
            {
                "question_text": "What is the inverse of the matrix product AB? (Write in terms of A^-1 and B^-1)",
                "model_answer": "B^-1 A^-1",
                "accepted_answers": ["B^-1 A^-1", "B^-1A^-1", "inverse of B times inverse of A", "Binv Ainv"],
                "explanation": "The 'Shoes and Socks' rule: to undo the operation AB, you must unwrap B first, then A."
            },
            {
                "question_text": "For a 2x2 matrix [[a, b], [c, d]], the quantity (ad - bc) is known as the _______.",
                "model_answer": "Determinant",
                "accepted_answers": ["determinant", "det"],
                "explanation": "If ad - bc = 0, the matrix is singular."
            },
            {
                "question_text": "The Gauss-Jordan method solves for A inverse by applying elimination to the augmented matrix [A  _ ]. Fill in the blank.",
                "model_answer": "I",
                "accepted_answers": ["I", "Identity", "Identity matrix"],
                "explanation": "We transform [A I] into [I A^-1]."
            },
            {
                "question_text": "If a matrix A has a row of all zeros, can it be invertible? (Yes/No)",
                "model_answer": "No",
                "accepted_answers": ["No", "no", "false"],
                "explanation": "A row of zeros implies the pivots cannot fill the diagonal, meaning the matrix is singular."
            },
            {
                "question_text": "What matrix E would you multiply A by to subtract 2 * Row 1 from Row 2? (Describe the entry E_21)",
                "model_answer": "-2",
                "accepted_answers": ["-2", "negative 2"],
                "explanation": "Elementary matrices have the negative of the multiplier in the position being eliminated (off-diagonal)."
            },
            {
                "question_text": "Once we have Ux = c, we solve for x using _______ substitution.",
                "model_answer": "Back",
                "accepted_answers": ["back", "backward"],
                "explanation": "We solve the equations from bottom to top."
            }
        ]
        
        quiz_la_5.question_set.all().delete()
        for idx, q in enumerate(quiz_5_data, 1):
            Question.objects.create(
                quiz=quiz_la_5,
                question_order=idx,
                question_text=q['question_text'],
                model_answer=q['model_answer'],
                accepted_answers=q['accepted_answers'],
                explanation=q.get('explanation', '')
            )

        # Quiz 6: Inverses & Singular Matrices (Theoretical)
        quiz_la_6, created_la_6 = Quiz.objects.get_or_create(
            title='Inverses & Singular Matrices',
            quiz_type=Quiz.QuizType.THEORETICAL,
            evaluation_method=Quiz.EvaluationMethod.SELF_EVAL,
            defaults={
                'domain': Quiz.Domain.LINEAR_ALGEBRA,
                'subject': Quiz.Subject.MECHANICS,
                'topic': 'Vectors & Matrices',
                'description': "Understanding invertibility, failure cases, and geometric interpretations.",
                'created_at': timezone.now()
            }
        )
        if created_la_6: self.stdout.write(f'Created Quiz: {quiz_la_6.title}')

        quiz_6_data = [
            {
                "question_text": "Explain the difference between a 'Temporary Failure' and a 'Permanent Failure' in Gaussian elimination.",
                "model_answer": "Temporary failure occurs when a 0 appears in a pivot position, but a non-zero entry exists below it (fixed by row exchange). Permanent failure occurs when a 0 is in the pivot position and all entries below it are also 0 (matrix is singular/not invertible).",
                "accepted_answers": [],
                "explanation": "This distinguishes between needing a permutation and the system having no unique solution."
            },
            {
                "question_text": "Why is the inverse of an Elementary Matrix (one that does a row subtraction) easy to find without calculation?",
                "model_answer": "Because the operation is just 'adding back' what was subtracted. If E subtracts 5*Row1 from Row2, E^-1 adds 5*Row1 to Row2.",
                "accepted_answers": [],
                "explanation": "In the matrix, you simply flip the sign of the off-diagonal multiplier."
            },
            {
                "question_text": "Why do we say that Matrix Multiplication is 'Associative' and how does this help in understanding LU factorization?",
                "model_answer": "Associativity means (AB)C = A(BC). This allows us to group all the elementary elimination matrices (E) together into one matrix L without worrying about the vector x. E(Ax) = (EA)x.",
                "accepted_answers": [],
                "explanation": "It justifies why we can talk about factoring the matrix A itself, separate from the specific equations."
            },
            {
                "question_text": "Visually/Geometrically, what does a singular matrix (2x2) represent in terms of the row equations?",
                "model_answer": "The two lines defined by the rows are parallel (and distinct) or the exact same line. They do not intersect at a unique single point.",
                "accepted_answers": [],
                "explanation": "In 3D, the planes would not intersect at a point (they might form a line, a tunnel, or be parallel)."
            },
            {
                "question_text": "Explain the 'Shoes and Socks' analogy for the inverse of a product (AB)^-1.",
                "model_answer": "You put on socks (A) then shoes (B). To reverse this, you must take off shoes (B^-1) first, then socks (A^-1). Hence (AB)^-1 = B^-1 A^-1.",
                "accepted_answers": [],
                "explanation": "Order of operations reverses when inverting."
            },
            {
                "question_text": "If A is invertible, what must be true about the equation Ax = b?",
                "model_answer": "It has exactly one unique solution x for every vector b.",
                "accepted_answers": [],
                "explanation": "Invertibility <-> Nonsingularity <-> Unique Solution."
            },
            {
                "question_text": "Describe the diagonal entries of the inverse of a Diagonal Matrix D.",
                "model_answer": "The entries are the reciprocals (1/d_ii) of the original diagonal entries.",
                "accepted_answers": [],
                "explanation": "If D has 2 and 5 on diagonal, D^-1 has 1/2 and 1/5."
            },
            {
                "question_text": "Why is it computationally expensive to calculate A^-1 explicitly compared to just solving Ax=b?",
                "model_answer": "Finding A^-1 is equivalent to solving Ax=e for n different columns. It effectively triples the work (or more) compared to a single elimination pass for one b.",
                "accepted_answers": [],
                "explanation": "Strang emphasizes: Don't compute the inverse unless you have to! Solve the system instead."
            },
            {
                "question_text": "If A and B are square and invertible, why is A + B not necessarily invertible?",
                "model_answer": "There is no formula for (A+B)^-1. Example: A=I and B=-I. Both are invertible, but sum is 0 (singular).",
                "accepted_answers": [],
                "explanation": "Inverses handle multiplication well, but addition poorly."
            },
            {
                "question_text": "In the Gauss-Jordan method, we go from [A I] to [I A^-1]. What is happening to the matrix representing the row operations during this process?",
                "model_answer": "The matrix of row operations accumulates to become A^-1. Effectively, (Row Ops Matrix) * [A I] = [I A^-1].",
                "accepted_answers": [],
                "explanation": "The operations that turn A into I are exactly the operations that turn I into A^-1."
            }
        ]

        quiz_la_6.question_set.all().delete()
        for idx, q in enumerate(quiz_6_data, 1):
            Question.objects.create(
                quiz=quiz_la_6,
                question_order=idx,
                question_text=q['question_text'],
                model_answer=q['model_answer'],
                accepted_answers=q['accepted_answers'],
                explanation=q.get('explanation', '')
            )

        # Quiz 7: LU Factorization & Transposes (Theoretical)
        quiz_la_7, created_la_7 = Quiz.objects.get_or_create(
            title='LU Factorization & Transposes',
            quiz_type=Quiz.QuizType.THEORETICAL,
            evaluation_method=Quiz.EvaluationMethod.SELF_EVAL,
            defaults={
                'domain': Quiz.Domain.LINEAR_ALGEBRA,
                'subject': Quiz.Subject.MECHANICS,
                'topic': 'Vectors & Matrices',
                'description': "LU decomposition, permutation matrices, and symmetric rules.",
                'created_at': timezone.now()
            }
        )
        if created_la_7: self.stdout.write(f'Created Quiz: {quiz_la_7.title}')

        quiz_7_data = [
            {
                "question_text": "In the factorization A = LU, L stands for _______ Triangular matrix.",
                "model_answer": "Lower",
                "accepted_answers": ["Lower", "lower"],
                "explanation": "L contains the multipliers used during elimination."
            },
            {
                "question_text": "What number is always on the main diagonal of the standard L matrix in A = LU?",
                "model_answer": "1",
                "accepted_answers": ["1", "one"],
                "explanation": "The diagonals of L are 1s; the pivots appear on the diagonal of U."
            },
            {
                "question_text": "A matrix P that exchanges rows of another matrix is called a _______ matrix.",
                "model_answer": "Permutation",
                "accepted_answers": ["permutation", "Permutation"],
                "explanation": "P is the identity matrix with rows reordered."
            },
            {
                "question_text": "If A is a Symmetric matrix, then A must equal what?",
                "model_answer": "A Transpose",
                "accepted_answers": ["A Transpose", "A^T", "transpose of A", "A_T"],
                "explanation": "Symmetric means a_ij = a_ji."
            },
            {
                "question_text": "What is the Transpose of the product (AB)?",
                "model_answer": "B^T A^T",
                "accepted_answers": ["B^T A^T", "B' A'", "B transpose A transpose"],
                "explanation": "Like inverses, transposes reverse the order of multiplication."
            },
            {
                "question_text": "For a Permutation matrix P, P inverse is always equal to P _______.",
                "model_answer": "Transpose",
                "accepted_answers": ["Transpose", "transpose", "T", "^T"],
                "explanation": "P^T P = I. This is a special property of orthogonal matrices."
            },
            {
                "question_text": "The computational cost of elimination for an n by n matrix is proportional to n to the power of _______.",
                "model_answer": "3",
                "accepted_answers": ["3", "three"],
                "explanation": "The operation count is approximately n^3 / 3."
            },
            {
                "question_text": "In the Symmetric Factorization A = LDL^T, D stands for what kind of matrix?",
                "model_answer": "Diagonal",
                "accepted_answers": ["diagonal", "Diagonal"],
                "explanation": "We separate the pivots out of U, leaving U with 1s on diagonal, becoming L^T for symmetric matrices."
            },
            {
                "question_text": "Is the matrix product R^T R always symmetric? (Yes/No)",
                "model_answer": "Yes",
                "accepted_answers": ["Yes", "yes", "true"],
                "explanation": "(R^T R)^T = R^T (R^T)^T = R^T R. It returns to itself."
            },
            {
                "question_text": "How many 3x3 Permutation matrices exist?",
                "model_answer": "6",
                "accepted_answers": ["6", "six"],
                "explanation": "n factorial (3! = 3*2*1 = 6)."
            }
        ]

        quiz_la_7.question_set.all().delete()
        for idx, q in enumerate(quiz_7_data, 1):
            Question.objects.create(
                quiz=quiz_la_7,
                question_order=idx,
                question_text=q['question_text'],
                model_answer=q['model_answer'],
                accepted_answers=q['accepted_answers'],
                explanation=q.get('explanation', '')
            )

        # Quiz 8: Advanced Factorization (PA=LU) (Theoretical)
        quiz_la_8, created_la_8 = Quiz.objects.get_or_create(
            title='Advanced Factorization (PA=LU)',
            quiz_type=Quiz.QuizType.THEORETICAL,
            evaluation_method=Quiz.EvaluationMethod.SELF_EVAL,
            defaults={
                'domain': Quiz.Domain.LINEAR_ALGEBRA,
                'subject': Quiz.Subject.MECHANICS,
                'topic': 'Vectors & Matrices',
                'description': "Advanced logic behind elimination, L, U, P, and symmetry.",
                'created_at': timezone.now()
            }
        )
        if created_la_8: self.stdout.write(f'Created Quiz: {quiz_la_8.title}')

        quiz_8_data = [
            {
                "question_text": "Why is the factorization A = LU more useful than just running elimination from scratch every time?",
                "model_answer": "If you have to solve Ax = b for many different vectors b, you factor A once (n^3 cost), then use L and U to solve each b very quickly (n^2 cost) via substitution.",
                "accepted_answers": [],
                "explanation": "It separates the coefficient matrix processing from the specific right-hand side."
            },
            {
                "question_text": "Describe the structure of the matrix L compared to the elimination matrices E. Why is L 'cleaner'?",
                "model_answer": "L contains the multipliers exactly in their positions below the diagonal. The product of E's mixes terms, but the inverse of E's (which forms L) places the multipliers perfectly without mixing.",
                "accepted_answers": [],
                "explanation": "This is a minor miracle of linear algebra that makes A=LU so elegant."
            },
            {
                "question_text": "If we need row exchanges to solve Ax=b, the factorization becomes PA = LU. What is P and why is it needed?",
                "model_answer": "P is a Permutation Matrix. It reorders the rows of A beforehand so that pivots are in the correct non-zero positions, allowing the standard LU process to proceed.",
                "accepted_answers": [],
                "explanation": "Elimination fails if a zero is in the pivot spot; P fixes this logic."
            },
            {
                "question_text": "Why does the operation count decrease from n^3/3 (Elimination) to n^2 (Back Substitution)?",
                "model_answer": "Elimination works on the whole 3D block of the matrix (rows * cols * steps). Substitution only works on the 2D triangle of the matrix. One dimension lower.",
                "accepted_answers": [],
                "explanation": "Integration analogy: Integral of x^2 is x^3/3."
            },
            {
                "question_text": "Show/Explain why (Ax) · y = x · (A^T y). (Dot Product Transpose Property)",
                "model_answer": "The dot product (Ax) · y is (Ax)^T y = x^T A^T y. This is the same as x · (A^T y).",
                "accepted_answers": [],
                "explanation": "This property effectively defines the transpose: it moves the matrix across the dot product."
            },
            {
                "question_text": "What is the relationship between symmetric matrices and elimination? (Hint: LDL^T)",
                "model_answer": "If A is symmetric (and no row exchanges needed), U is the transpose of L (scaled by pivots). We write A = LDL^T, saving half the storage/work.",
                "accepted_answers": [],
                "explanation": "Symmetry is preserved during elimination."
            },
            {
                "question_text": "Why is the inverse of a Permutation Matrix equal to its transpose?",
                "model_answer": "Permutations are orthogonal matrices. The rows are unit vectors and orthogonal to each other. Thus P^T P = I.",
                "accepted_answers": [],
                "explanation": "Swapping rows back is the same as swapping columns in the reverse order."
            },
            {
                "question_text": "Explain the concept of 'Band Matrices' and why they are computationally efficient.",
                "model_answer": "Band matrices only have non-zero entries near the diagonal (within a bandwidth w). Elimination only affects this band, reducing cost from n^3 to n*w^2.",
                "accepted_answers": [],
                "explanation": "This is crucial for engineering applications with sparse connections."
            },
            {
                "question_text": "If A is invertible and symmetric, is A^-1 symmetric? Why?",
                "model_answer": "Yes. (A^-1)^T = (A^T)^-1 = A^-1. Since A is symmetric, transposing the inverse gets you back the inverse.",
                "accepted_answers": [],
                "explanation": "Symmetry is robust; it survives inversion."
            },
            {
                "question_text": "What happens to the L and U factors if you multiply A by 2?",
                "model_answer": "L remains the same (multipliers are ratios, so 2x/2y = x/y). U is multiplied by 2 (the pivots double).",
                "accepted_answers": [],
                "explanation": "L depends on the ratio of rows; U contains the actual scale of the numbers."
            }
        ]

        quiz_la_8.question_set.all().delete()
        for idx, q in enumerate(quiz_8_data, 1):
            Question.objects.create(
                quiz=quiz_la_8,
                question_order=idx,
                question_text=q['question_text'],
                model_answer=q['model_answer'],
                accepted_answers=q['accepted_answers'],
                explanation=q.get('explanation', '')
            )


        self.stdout.write(f'Seeding complete.')

