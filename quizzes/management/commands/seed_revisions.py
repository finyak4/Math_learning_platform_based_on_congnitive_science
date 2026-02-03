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
            
            # Derivatives Revisions
            (1, 'Derivatives: Revision 1', 'Derivatives'),
            (2, 'Derivatives: Revision 2', 'Derivatives'),
            (3, 'Derivatives: Revision 3', 'Derivatives'),
            (4, 'Derivatives: Revision 4', 'Derivatives'),

            # Applications Revisions
            (1, 'Applications of Derivatives: Revision 1', 'Applications of Derivatives'),
            (2, 'Applications of Derivatives: Revision 2', 'Applications of Derivatives'),
            (3, 'Applications of Derivatives: Revision 3', 'Applications of Derivatives'),
            (4, 'Applications of Derivatives: Revision 4', 'Applications of Derivatives'),
            
            # Calculus 2 Revisions
            # Integrals
            (1, 'Integrals: Revision 1', 'Integrals'),
            (2, 'Integrals: Revision 2', 'Integrals'),
            (3, 'Integrals: Revision 3', 'Integrals'),
            (4, 'Integrals: Revision 4', 'Integrals'),
            
            # Techniques
            (1, 'Techniques: Revision 1', 'Techniques'),
            (2, 'Techniques: Revision 2', 'Techniques'),
            (3, 'Techniques: Revision 3', 'Techniques'),
            (4, 'Techniques: Revision 4', 'Techniques'),
            
            # Sequences
            (1, 'Sequences & Series: Revision 1', 'Sequences & Series'),
            (2, 'Sequences & Series: Revision 2', 'Sequences & Series'),
            (3, 'Sequences & Series: Revision 3', 'Sequences & Series'),
            (4, 'Sequences & Series: Revision 4', 'Sequences & Series'),
            
            # Linear Algebra: Vectors & Matrices
            (1, 'Vectors & Matrices: Revision 1', 'Vectors & Matrices'),
            (2, 'Vectors & Matrices: Revision 2', 'Vectors & Matrices'),
            (3, 'Vectors & Matrices: Revision 3', 'Vectors & Matrices'),
            (4, 'Vectors & Matrices: Revision 4', 'Vectors & Matrices'),
            
            
            # Probability
            (1, 'Probability: Revision 1', 'Probability and Counting'),
            (2, 'Probability: Revision 2', 'Probability and Counting'),
            (3, 'Probability: Revision 3', 'Probability and Counting'),
            (4, 'Probability: Revision 4', 'Probability and Counting'),
            # Linear Algebra: Solving Linear Equations
            (1, 'Solving Linear Equations: Revision 1', 'Solving Linear Equations'),
            (2, 'Solving Linear Equations: Revision 2', 'Solving Linear Equations'),
            (3, 'Solving Linear Equations: Revision 3', 'Solving Linear Equations'),
            (4, 'Solving Linear Equations: Revision 4', 'Solving Linear Equations'),

            # Linear Algebra: Vector Spaces
            (1, 'Vector Spaces: Revision 1', 'Vector Spaces'),
            (2, 'Vector Spaces: Revision 2', 'Vector Spaces'),
            (3, 'Vector Spaces: Revision 3', 'Vector Spaces'),
            (4, 'Vector Spaces: Revision 4', 'Vector Spaces'),
        ]

        # Common description for all revision quizzes
        rev_description = "Spaced Repetition Review. This quiz is automatically scheduled to strengthen your long-term retention. Please answer honestly."

        for level, title, topic in revisions:
            # Create Quiz
            quiz, created = Quiz.objects.get_or_create(
                title=title,
                defaults={
                    'domain': Quiz.Domain.LINEAR_ALGEBRA if topic in ['Vectors & Matrices', 'Solving Linear Equations', 'Vector Spaces'] else (Quiz.Domain.STATISTICS if topic == 'Probability and Counting' else Quiz.Domain.CALCULUS),
                    'subject': Quiz.Subject.MECHANICS if topic in ['Vectors & Matrices', 'Solving Linear Equations', 'Vector Spaces'] 
                               else (Quiz.Subject.PROBABILITY if topic == 'Probability and Counting' else (Quiz.Subject.CALCULUS_2 if topic in ['Integrals', 'Techniques', 'Sequences & Series'] else Quiz.Subject.CALCULUS_1)),
                    'topic': topic,
                    'quiz_type': Quiz.QuizType.REVISION,
                    'evaluation_method': Quiz.EvaluationMethod.SELF_EVAL,
                    'description': rev_description,
                    'created_at': timezone.now()
                }
            )
            
            if not created:
                self.stdout.write(f'Revision Quiz "{title}" already exists. Ensuring description/mode/domain.')
                quiz.description = rev_description
                quiz.evaluation_method = Quiz.EvaluationMethod.SELF_EVAL
                
                # Ensure Domain/Subject are correct for existing quizzes
                if topic in ['Vectors & Matrices', 'Solving Linear Equations', 'Vector Spaces']:
                    quiz.domain = Quiz.Domain.LINEAR_ALGEBRA
                    quiz.subject = Quiz.Subject.MECHANICS
                elif topic == 'Probability and Counting':
                    quiz.domain = Quiz.Domain.STATISTICS
                    quiz.subject = Quiz.Subject.PROBABILITY
                else:
                     quiz.domain = Quiz.Domain.CALCULUS
                     # Re-apply Calculus subject logic if needed, but usually domain is the critical fix
                
                quiz.save()
            else:
                self.stdout.write(f'Created Revision Quiz: {title}')

            # Clear old questions to ensure fresh seed
            quiz.question_set.all().delete()

            # Define Questions based on Topic and Level
            questions_data = []

            # ================= LIMITS =================
            if topic == 'Limits':
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

            # ================= DERIVATIVES =================
            elif topic == 'Derivatives':
                if level == 1:
                    questions_data = [
                        (1, 'Power Rule: Derivative of x^5?', '5x^4', None),
                        (2, 'Derivative of sin(x)?', 'cos(x)', None),
                        (3, 'Derivative of a constant?', '0', None),
                        (4, 'State Product Rule for u*v.', "u'v + uv'", None),
                        (5, 'Geometric meaning of derivative at a point?', 'Slope of the tangent line.', None),
                        (6, 'Find f\'(x) for f(x) = 2x + 1.', '2', 'Slope of line 2x+1 is 2.'),
                    ]
                elif level == 2:
                    questions_data = [
                        (1, 'Derivative of e^x?', 'e^x', None),
                        (2, 'Derivative of ln(x)?', '1/x', None),
                        (3, 'Chain Rule for f(g(x))?', "f'(g(x)) * g'(x)", None),
                        (4, 'Quotient rule rhyme (or formula).', "Lo d-Hi minus Hi d-Lo, over Lo Lo.", None),
                        (5, 'Derivative of cos(x)?', '-sin(x)', None),
                        (6, 'Differentiate y = (2x+1)^2.', '4(2x+1) or 8x+4', 'Chain: 2(2x+1)*2 = 4(2x+1).'),
                    ]
                elif level == 3:
                    questions_data = [
                        (1, 'Derivative of tan(x)?', 'sec^2(x)', None),
                        (2, 'Implicit differentiation: derivative of y^2 w.r.t x?', "2y * y'", None),
                        (3, 'Derivative of position is ______?', 'Velocity', None),
                        (4, 'Derivative of velocity is ______?', 'Acceleration', None),
                        (5, 'Meaning of f\'(x) > 0?', 'Function is increasing.', None),
                        (6, 'Find slope of tangent to y=x^2 at x=3.', '6', "f'(x)=2x, f'(3)=6."),
                    ]
                elif level == 4:
                    questions_data = [
                        (1, 'Derivative of sec(x)?', 'sec(x)tan(x)', None),
                        (2, 'Derivative of arcsin(x)?', '1/sqrt(1-x^2)', None),
                        (3, 'If f is differentiable at c, is it continuous at c?', 'Yes.', None),
                        (4, 'Give an example of a function continuous but not differentiable at x=0.', '|x|', None),
                        (5, 'Derivative of a^x?', "a^x * ln(a)", None),
                        (6, 'Differentiate y = x * e^x.', 'e^x(x+1)', "Product rule: 1*e^x + x*e^x."),
                    ]

            # ================= APPLICATIONS OF DERIVATIVES =================
            elif topic == 'Applications of Derivatives':
                if level == 1:
                    questions_data = [
                        (1, 'Definition of a Critical Point?', "f'(x) = 0 or Undefined", None),
                        (2, 'If f\'(x) goes from + to - at c, what is c?', 'Local Maximum', None),
                        (3, 'If f\'\'(x) > 0, the graph is Concave ______.', 'Up', None),
                        (4, 'Rolle\'s Theorem condition: f(a) must equal ______.', 'f(b)', None),
                        (5, 'MVT guarantees a point where instantaneous rate equals ______ rate.', 'Average', None),
                        (6, 'Find critical points of f(x) = x^2 - 4x.', 'x = 2', "2x - 4 = 0 -> x=2"),
                    ]
                elif level == 2:
                    questions_data = [
                        (1, 'Indeterminate forms for L\'Hopital?', '0/0 or inf/inf', None),
                        (2, 'Point where concavity changes is called ______.', 'Inflection Point', None),
                        (3, 'General antiderivative of x?', 'x^2/2 + C', None),
                        (4, 'If f\'(x) < 0, f is ______.', 'Decreasing', None),
                        (5, 'Second derivative test: If f\'\'(c) < 0 at critical pt, it\'s a ______.', 'Local Max', None),
                        (6, 'Find inflection pt of f(x) = x^3.', 'x = 0', "f'' = 6x, 6x=0 -> x=0."),
                    ]
                elif level == 3:
                    questions_data = [
                        (1, 'L\'Hopital: Derivative of top divided by derivative of ______.', 'Bottom', None),
                        (2, 'Optimization on closed interval [a,b]: Check critical pts and ______.', 'Endpoints', None),
                        (3, 'Linear Approximation formula L(x)?', "f(a) + f'(a)(x-a)", None),
                        (4, 'Antiderivative of 1/x?', 'ln(|x|) + C', None),
                        (5, 'If velocity > 0 and acceleration < 0, speed is ______.', 'Decreasing', None),
                        (6, 'Max of y = -x^2 on [-1, 1]?', '0', 'Vertex at 0 is max.'),
                    ]
                elif level == 4:
                    questions_data = [
                        (1, 'Derivative of integral from a to x of f(t)dt?', 'f(x)  (FTC 1)', None),
                        (2, 'Newton\'s Method formula: x_{n+1} = x_n - ______?', "f(x_n)/f'(x_n)", None),
                        (3, 'Related Rates: If x^2+y^2=r^2, derivative w.r.t time?', "2x(dx/dt) + 2y(dy/dt) = 2r(dr/dt)", None),
                        (4, 'Antiderivative of sec^2(x)?', 'tan(x) + C', None),
                        (5, 'Explain why f\'(x)=0 is not enough for an extrema.', 'Could be an inflection point (like x^3 at 0).', None),
                        (6, 'Evaluate lim x->inf (ln x / x).', '0', 'L\'Hopital -> (1/x)/1 -> 0.'),
                    ]

            # ================= CALCULUS 2: INTEGRALS =================
            elif topic == 'Integrals':
                if level == 1:
                    questions_data = [
                        (1, 'Antiderivative of x^n where n != -1?', 'x^(n+1)/(n+1) + C', None),
                        (2, 'Integral of 1/x dx?', 'ln|x| + C', None),
                        (3, 'Integral of sin(x) dx?', '-cos(x) + C', None),
                        (4, 'FTC Part 1 says d/dx of Integral from a to x of f(t) is?', 'f(x)', None),
                        (5, 'FTC Part 2 says Integral from a to b is F(b) - F(?)', 'F(a)', None),
                        (6, 'Integral of e^x?', 'e^x + C', None),
                    ]
                elif level == 2:
                    questions_data = [
                        (1, 'Integral of sec^2(x)?', 'tan(x) + C', None),
                        (2, 'Net Change Theorem: Integral of rate of change gives ______.', 'Net Change', None),
                        (3, 'If velocity is positive, displacement equals ______.', 'Distance Traveled', None),
                        (4, 'Integral of 1/(1+x^2)?', 'arctan(x) + C', None),
                        (5, 'Evaluate Integral from 0 to 1 of 2x.', '1', '[x^2] from 0 to 1 = 1-0 = 1.'),
                        (6, 'True or False: Integral of product is product of integrals.', 'False', None),
                    ]
                elif level == 3:
                    questions_data = [
                        (1, 'Integral of tan(x)?', 'ln|sec x| or -ln|cos x|', None),
                        (2, 'Geometric meaning of Integral from a to b?', 'Net signed area under curve.', None),
                        (3, 'Average value of f on [a,b] formula?', '1/(b-a) * Integral(a to b) f(x) dx', None),
                        (4, 'If f is odd, Integral from -a to a is?', '0', None),
                        (5, 'If f is even, Integral from -a to a is?', '2 * Integral from 0 to a', None),
                        (6, 'Evaluate Integral 0 to pi of sin(x).', '2', '-cos(pi) - (-cos(0)) = 1 - (-1) = 2.'),
                    ]
                elif level == 4:
                    questions_data = [
                        (1, 'Integral of sec(x)?', 'ln|sec x + tan x|', None),
                        (2, 'Integral of 1/sqrt(1-x^2)?', 'arcsin(x)', None),
                        (3, 'Explain substitution rule in reverse.', 'Chain rule reversed.', None),
                        (4, 'Displacement vs Distance? Integral of v vs Integral of |v|.', 'Displacement vs Distance', None),
                        (5, 'Evaluate d/dx Integral from 1 to x^2 of sin(t)dt.', '2x sin(x^2)', 'Chain rule extension of FTC 1.'),
                        (6, 'Find area between y=x and y=x^2 from 0 to 1.', '1/6', 'Int(x - x^2) = 1/2 - 1/3 = 1/6.'),
                    ]

            # ================= CALCULUS 2: TECHNIQUES =================
            elif topic == 'Techniques':
                if level == 1:
                    questions_data = [
                        (1, 'Integration by Parts formula.', 'uv - Int v du', None),
                        (2, 'LIATE - L stands for?', 'Logarithmic', None),
                        (3, 'Type of substitution for sqrt(a^2 - x^2)?', 'x = a sin(theta)', None),
                        (4, 'Partial Fractions: Break down (2x+1)/((x-1)(x+2)).', 'A/(x-1) + B/(x+2)', None),
                        (5, 'If integral limit is infinity, it is called ______.', 'Improper', None),
                        (6, 'Identity for sin^2(x)?', '(1-cos(2x))/2', None),
                    ]
                elif level == 2:
                    questions_data = [
                        (1, 'Integral of ln(x)?', 'x ln(x) - x + C', 'By parts.'),
                        (2, 'Substitution for sqrt(x^2 + a^2)?', 'x = a tan(theta)', None),
                        (3, 'Partial Fractions: Term for repeated factor (x-1)^2?', 'A/(x-1) + B/(x-1)^2', None),
                        (4, 'Strategy for Integral sin^3(x)?', 'Save one sin(x), convert rest to cos.', None),
                        (5, 'Evaluate Integral 1 to infinity of 1/x^2.', '1', 'Converges.'),
                        (6, 'Trapezoidal Rule approximates curve with ______.', 'Trapezoids (straight lines).', None),
                    ]
                elif level == 3:
                    questions_data = [
                        (1, 'Integral of arctan(x)?', 'x arctan(x) - 1/2 ln(1+x^2)', 'By parts.'),
                        (2, 'Substitution for sqrt(x^2 - a^2)?', 'x = a sec(theta)', None),
                        (3, 'Partial fractions for irreducible quadratic?', 'Ax + B', None),
                        (4, 'Evaluate Integral 1 to infinity of 1/x.', 'Diverges', 'Limit is ln(inf).'),
                        (5, 'Identity for cos^2(x)?', '(1+cos(2x))/2', None),
                        (6, 'Simpson\'s Rule uses what shape?', 'Parabolas', None),
                    ]
                elif level == 4:
                    questions_data = [
                        (1, 'Integral of e^x sin(x)?', 'Boomerang / Phoenix method (Parts twice).', None),
                        (2, 'P-test: Integral 1 to inf of 1/x^p converges if?', 'p > 1', None),
                        (3, 'Comparison Test: If f < g and Integral g converges, then?', 'Integral f converges.', None),
                        (4, 'What if limit of Improper Integral oscillates?', 'Diverges.', None),
                        (5, 'Weierstrass Substitution (half-angle) is for?', 'Rational trig functions.', None),
                        (6, 'Evaluate Integral 0 to 1 of 1/sqrt(x).', '2', 'Converges (p=1/2 < 1).'),
                    ]
            
            elif topic == 'Sequences & Series':
                if level == 1:
                    questions_data = [
                        (1, 'Definition of a Sequence.', 'Ordered list of numbers.', None),
                        (2, 'Definition of a Series.', 'Sum of sequence terms.', None),
                        (3, 'Limit of 1/n?', '0', None),
                        (4, 'Geometric Series converges if |r| < ?', '1', None),
                        (5, 'Harmonic Series converges or diverges?', 'Diverges', None),
                        (6, 'Test for Divergence: If limit a_n is not 0, series ______.', 'Diverges', None),
                    ]
                elif level == 2:
                    questions_data = [
                        (1, 'Sum of geometric series a + ar + ...?', 'a / (1-r)', None),
                        (2, 'P-series: Sum 1/n^p converges if?', 'p > 1', None),
                        (3, 'Integral Test conditions?', 'Positive, Continuous, Decreasing.', None),
                        (4, 'Ratio Test: Limit < 1 implies?', 'Convergence', None),
                        (5, 'Ratio Test: Limit > 1 implies?', 'Divergence', None),
                        (6, 'Alternating Series Test conditions?', 'Alternates, Decreases, Limit is 0.', None),
                    ]
                elif level == 3:
                    questions_data = [
                        (1, 'What is Absolute Convergence?', 'Sum of |a_n| converges.', None),
                        (2, 'What is Conditional Convergence?', 'Converges, but Sum of |a_n| diverges.', None),
                        (3, 'Maclaurin Series for e^x?', '1 + x + x^2/2! + ...', None),
                        (4, 'Radius of Convergence definition.', 'Distance from center where series converges.', None),
                        (5, 'Power series for 1/(1-x)?', '1 + x + x^2 + ...', None),
                        (6, 'Limit Comparison Test: If limit of ratio is finite positive?', 'Both behave same.', None),
                    ]
                elif level == 4:
                    questions_data = [
                        (1, 'Maclaurin Series for sin(x)?', 'x - x^3/3! + x^5/5! ...', None),
                        (2, 'Maclaurin Series for cos(x)?', '1 - x^2/2! + x^4/4! ...', None),
                        (3, 'Taylor Series formula.', 'Sum f^(n)(a)/n! * (x-a)^n', None),
                        (4, 'Interval of convergence check endpoints?', 'Yes, manually.', None),
                        (5, 'Binomial Series for (1+x)^k start?', '1 + kx + ...', None),
                        (6, 'Sum of Alternating Harmonic Series?', 'ln(2)', None),
                    ]

            # ================= LIN ALG: VECTORS & MATRICES =================
            elif topic == 'Vectors & Matrices':
                if level == 1:
                    questions_data = [
                        (1, 'Dot product of $v=(1,2)$ and $w=(3,-1)$?', '1', '$1(3) + 2(-1) = 3 - 2 = 1$.'),
                        (2, 'Length of vector $(3,4)$?', '5', '$\\sqrt{3^2+4^2} = \\sqrt{25} = 5$.'),
                        (3, 'Unit vector definition?', 'Vector with length $(\\|v\\|) = 1$.', None),
                        (4, 'Angle if dot product is 0?', '$90^\\circ$ (Orthogonal)', None),
                        (5, 'Linear combination of $v$ and $w$?', '$cv + dw$', None),
                        (6, 'Schwarz Inequality?', '$|v \\cdot w| \\le \\|v\\| \\|w\\|$', None),
                    ]
                elif level == 2:
                    questions_data = [
                        (1, 'Triangle Inequality?', '$\\|v+w\\| \\le \\|v\\| + \\|w\\|$', None),
                        (2, 'When does Triangle Inequality become equality?', 'Vectors are parallel (same direction).', None),
                        (3, 'Column Space $C(A)$ consists of all linear combinations of...?', 'The columns of $A$.', None),
                        (4, 'Matrix multiplication $AB$: entry $(i,j)$ is dot product of?', 'Row $i$ of $A$ and Column $j$ of $B$.', None),
                        (5, 'Is matrix multiplication commutative?', 'No usually not ($AB \\neq BA$).', None),
                        (6, 'Outer product of $(2 \\times 1)$ and $(1 \\times 2)$ size?', '$2 \\times 2$', None),
                    ]
                elif level == 3:
                    questions_data = [
                        (1, 'Rank 1 matrix can be written as?', '$uv^T$ (Column times Row)', None),
                        (2, 'Associative Property means?', '$(AB)C = A(BC)$', None),
                        (3, 'If $A$ has dependent columns, is it invertible?', 'No', None),
                        (4, '$Ax=b$ solvable only if $b$ is in...?', 'Column Space $C(A)$.', None),
                        (5, 'Inner product rule $(Ax)\\cdot y = ?$ ', '$x \\cdot (A^T y)$', None),
                        (6, 'How many components in $R^4$?', '4', None),
                    ]
                elif level == 4:
                    questions_data = [
                        (1, 'Condition for Independent Columns?', '$Ax=0$ has only $x=0$ solution.', None),
                        (2, 'Matrices acting on vectors: $Ax$ is a combination of columns, $xA$ is combination of?', 'Rows', None),
                        (3, 'Why $C(A)$ is a subspace?', 'Closed under addition and scalar multiplication.', None),
                        (4, 'Geometric shape of $C(A)$ for $3 \\times 3$ singular matrix?', 'Plane or Line (through origin).', None),
                        (5, 'Effect of multiplying by Diagonal matrix on Right ($AD$)?', 'Scales the columns.', None),
                        (6, 'Effect of multiplying by Permutation matrix on Left ($PA$)?', 'Reorders the rows.', None),
                    ]
            
            # ================= LIN ALG: SOLVING LINEAR EQUATIONS =================
            elif topic == 'Solving Linear Equations':
                if level == 1:
                    questions_data = [
                        (1, 'Purpose of Elimination?', 'To transform $A$ into Upper Triangular $U$.', None),
                        (2, 'What is a Pivot?', 'First non-zero entry in a row.', None),
                        (3, 'Singular matrix means?', 'Not invertible (Determinant 0).', None),
                        (4, 'Inverse of $(AB)$?', '$B^{-1} A^{-1}$', None),
                        (5, 'Determinant of $2 \\times 2$ $\\begin{bmatrix} a & b \\\\ c & d \\end{bmatrix}$?', '$ad - bc$', None),
                        (6, 'Identity matrix $I$ property?', '$IA = A$ and $AI = A$.', None),
                    ]
                elif level == 2:
                    questions_data = [
                        (1, 'Breakdown of elimination (Pivot=0) is fixed by?', 'Row Exchange', None),
                        (2, 'Multiplier $l_{21}$ formula?', 'Entry to kill / Pivot', None),
                        (3, 'Inverse of Elementary Matrix $E$ (subtraction)?', 'Add back (flip sign of multiplier).', None),
                        (4, 'Gauss-Jordan method transforms $[A|I]$ into?', '$[I|A^{-1}]$', None),
                        (5, 'Does $A+B$ have nice inverse formula?', 'No.', None),
                        (6, 'If row of zeros appears, is $A$ invertible?', 'No.', None),
                    ]
                elif level == 3:
                    questions_data = [
                        (1, '$A = LU$ factorization: $L$ is?', 'Lower Triangular (multipliers).', None),
                        (2, 'Diagonals of $L$ are?', '1s', None),
                        (3, 'Symmetric Matrix definition?', '$A = A^T$', None),
                        (4, 'Transpose of $(AB)$?', '$B^T A^T$', None),
                        (5, 'Permutation Matrix Inverse $P^{-1} = ?$', '$P^T$', None),
                        (6, 'Inverse of Diagonal Matrix $D$?', 'Diagonal matrix with $1/d_{ii}$', None),
                    ]
                elif level == 4:
                    questions_data = [
                        (1, 'Operation count for Elimination ($n \\times n$)?', '$n^3 / 3$', None),
                        (2, 'Symmetric Factorization $A = ?$', '$LDL^T$', None),
                        (3, 'Why solve $Ax=b$ instead of finding $A^{-1}$?', 'Faster/More stable ($n^3$ vs $3n^3$).', None),
                        (4, '$PA = LU$ is used when?', 'Row exchanges are required.', None),
                        (5, 'Is $R^T R$ always symmetric?', 'Yes.', None),
                        (6, 'Band Matrix efficiency?', 'Operations proportional to $n$ (not $n^3$).', None),
                    ]


            # ================= PROBABILITY =================
            elif topic == 'Probability and Counting':
                if level == 1:
                    questions_data = [
                        (1, "Define 'Sample Space'.", "The set of all possible outcomes of an experiment.", None),
                        (2, "What does $nPk$ represent?", "The number of ways to choose and arrange $k$ items from $n$ distinct items.", None),
                        (3, "Explain $P(A^c) = 1 - P(A)$.", "The probability of an event NOT happening is 1 minus the probability it DOES happen, because total probability is 1.", None),
                        (4, "How many rearrangements of 'LEVEL'?", "$5! / (2! 2!) = 30$.", None),
                        (5, "When do you multiply probabilities?", "When the events are independent (or using conditional probability logic $P(A)P(B|A)$).", None),
                        (6, "What is a 'disjoint' event?", "Two events that share no outcomes (Intersection is empty).", None),
                    ]
                elif level == 2:
                    questions_data = [
                        (1, "What is $\\binom{n}{n}$?", "1. There is only one way to choose everyone.", None),
                        (2, "Does $n!$ grow faster than $2^n$?", "Yes, much faster.", None),
                        (3, "Solve $x_1 + x_2 + x_3 = 10$ for non-negative integers.", "Stars/Bars: $\\binom{10+3-1}{3-1} = \\binom{12}{2}$.", None),
                        (4, "What is the Pigeonhole Principle?", "If $n+1$ items go into $n$ boxes, one box has $>1$ item.", None),
                        (5, "Difference between Set and Sequence?", "Sequence has order; Set does not.", None),
                        (6, "How many subsets of $\{1, 2, 3\}$?", "$2^3 = 8$.", None),
                    ]
                elif level == 3:
                     questions_data = [
                        (1, "State the 1st Axiom of Probability.", "$P(A) \\ge 0$ for any event $A$.", None),
                        (2, "In the Birthday Problem ($n=23$), is prob > 50%?", "Yes, approx 50.7%.", None),
                        (3, "If $P(A)=0$, is it impossible?", "Discrete: Yes. Continuous: No (point mass is 0 but exists).", None),
                        (4, "What is a Bernoulli Trial?", "An experiment with 2 outcomes (Success/Failure).", None),
                        (5, "Outcomes of 10 coin flips?", "$2^{10} = 1024$.", None),
                        (6, "What is $P(A|B)$ if $A$ and $B$ are independent?", "$P(A)$.", None),
                     ]
                elif level == 4:
                     questions_data = [
                        (1, "Explain 'Adjusting for Overcounting'.", "If your counting method produces each valid outcome $c$ times, divide the total by $c$.", None),
                        (2, "Binomial Theorem expansion of $(x+y)^n$?", "Sum of $(\\binom{n}{k} x^k y^{n-k})$.", None),
                        (3, "Vandermonde's Identity concept?", "Summing committee possibilities across gender splits.", None),
                        (4, "Can Probability be negative?", "No.", None),
                        (5, "Why divide by $n$ for circular arrangements?", "To account for $n$ rotations being identical.", None),
                        (6, "Complement of 'All heads'?", "At least one tail.", None),
                     ]
            # ================= LIN ALG: VECTOR SPACES =================
            elif topic == 'Vector Spaces':
                if level == 1:
                    questions_data = [
                        (1, "Is the set of all polynomials of degree exactly 2 a subspace?", "No", "Not closed under addition (x^2 + x - x^2 = x, degree 1)."),
                        (2, "Is the set of integer vectors a subspace of R^2?", "No", "Not closed under scalar multiplication (e.g. 0.5 * v)."),
                        (3, "True/False: Intersection of two subspaces is a subspace.", "True", "If u,v in both, their combination is in both."),
                        (4, "True/False: Union of two subspaces is a subspace.", "False", "Sum of elements from each might not be in either."),
                        (5, "Does every subspace contain the zero vector?", "Yes", "Required property."),
                        (6, "Is the line y=3x+1 a subspace of R^2?", "No", "It does not pass through the origin (0,0)."),
                    ]
                elif level == 2:
                    questions_data = [
                        (1, "Can a basis contain the zero vector?", "No", "Zero vector creates dependence."),
                        (2, "Max number of independent vectors in n-dim space?", "n", None),
                        (3, "Can n-1 vectors span an n-dim space?", "No", "Not enough vectors."),
                        (4, "A basis is a ______ generating set.", "Minimal", "Removing any vector breaks the span."),
                        (5, "Is the basis for a vector space unique?", "No", "Infinitely many bases exist."),
                        (6, "Is the dimension of a vector space unique?", "Yes", "All bases have the same count."),
                    ]
                elif level == 3:
                     questions_data = [
                        (1, "Row Space is orthogonal complement to Nullspace in...?", "R^n", "Input space."),
                        (2, "Column Space is orthogonal complement to Left Nullspace in...?", "R^m", "Output space."),
                        (3, "Dim(Column Space) + Dim(Left Nullspace) = ?", "m", "Rank + (m-r) = m."),
                        (4, "Dim(Row Space) + Dim(Nullspace) = ?", "n", "Rank + (n-r) = n."),
                        (5, "For symmetric matrix, Row Space equals ______?", "Column Space", "A = A^T."),
                        (6, "Which subspace contains the error term e = b - Ax?", "Left Nullspace", "Error is orthogonal to C(A)."),
                     ]
                elif level == 4:
                     questions_data = [
                        (1, "Does Rank(A) always equal Rank(A^T)?", "Yes", "Fundamental Theorem."),
                        (2, "If Rank r=n, what is the Nullspace?", "{0}", "Zero vector only."),
                        (3, "If Rank r=m, what is the Column Space?", "R^m", "Full row rank."),
                        (4, "SVD sum of rank-______ matrices?", "1", "sigma * u * v^T."),
                        (5, "Dimension of Column Space is also known as ______.", "Rank", None),
                        (6, "If A is 4x3 and rank is 3, dimension of Nullspace?", "0", "3 - 3 = 0."),
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
