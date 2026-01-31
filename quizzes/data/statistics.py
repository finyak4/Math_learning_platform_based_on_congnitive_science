from quizzes.models import Quiz
from django.utils import timezone

def get_statistics_quizzes():
    return [
        {
            'title': 'Probability: Counting Fundamentals',
            'type': Quiz.QuizType.THEORETICAL,
            'eval_method': Quiz.EvaluationMethod.AUTOMATED,
            'domain': Quiz.Domain.STATISTICS,
            'subject': Quiz.Subject.PROBABILITY,
            'topic': 'Probability and Counting',
            'description': "Automated quiz on counting principles.",
            'questions': [
                (1, "If an experiment has $r$ steps with $n_1, n_2... n_r$ choices respectively, the total number of outcomes is the ______ of the choices.", "product", ["product", "multiplication"]),
                (2, "Sampling $k$ items from $n$ with replacement where order matters results in ______ possibilities.", "$n^k$", ["n^k", "n**k", "n to the power of k"]),
                (3, "The number of distinct permutations of 'MISSISSIPPI' involves dividing $11!$ by factorials of 4, 4, 2, and 1 to account for ______.", "overcounting", ["overcounting", "duplicates", "repetition", "indistinguishable letters"]),
                (4, "True or False: The binomial coefficient $\\binom{n}{k}$ counts subsets where order matters.", "False", ["False", "F", "no"]),
                (5, "How many subsets does a set with 5 elements have?", "32", ["32", "2^5"]),
                (6, "$0!$ (zero factorial) is defined to be equal to ______.", "1", ["1", "one"]),
                (7, "The number of ways to arrange $n$ distinct objects in a circle is $(n - ? )!$", "1", ["1", "one"]),
                (8, "For sampling $k$ items from $n$ WITHOUT replacement where order DOES matter, we use the formula for ______.", "permutations", ["permutations", "nPk"]),
                (9, "If you have 5 shirts and 3 pairs of pants, how many distinct outfits can you make?", "15", ["15", "fifteen"]),
                (10, "The coefficient of $x^k y^{n-k}$ in the expansion of $(x+y)^n$ is $n$ ______ $k$.", "choose", ["choose", "C"]),
            ]
        },
        {
            'title': 'Probability: Definitions & Logic',
            'type': Quiz.QuizType.THEORETICAL,
            'eval_method': Quiz.EvaluationMethod.AUTOMATED,
            'domain': Quiz.Domain.STATISTICS,
            'subject': Quiz.Subject.PROBABILITY,
            'topic': 'Probability and Counting',
            'description': "Automated quiz on probability definitions.",
            'questions': [
                (1, "The Naive Definition $P(A) = |A|/|S|$ assumes all outcomes in $S$ are ______.", "equally likely", ["equally likely", "uniform"]),
                (2, "$P(A \\cup B) = P(A) + P(B) - ?.$", "$P(A \\cap B)$", ["P(A n B)", "P(A intersection B)", "intersection"]),
                (3, "If $A$ and $B$ are disjoint (mutually exclusive), then $P(A \\cap B)$ equals ______.", "0", ["0", "zero"]),
                (4, "The probability of the sample space $P(S)$ must always equal ______.", "1", ["1", "one"]),
                (5, "If $P(A) = 0.3$, then $P(A^c)$ (the complement) is ______.", "0.7", ["0.7", ".7"]),
                (6, "In the Birthday Problem, it is easier to calculate the probability that ______ two people share a birthday.", "no", ["no", "zero"]),
                (7, "Counting $k$ indistinguishable items into $n$ distinguishable bins is called Stars and ______.", "Bars", ["Bars", "bars"]),
                (8, "If $A$ is a subset of $B$, is $P(A) \\le P(B)$? (Yes/No)", "Yes", ["Yes", "yes", "true", "True"]),
                (9, "Probability is a function that maps events to real numbers between 0 and ______.", "1", ["1", "one"]),
                (10, "The empty set is an event with probability ______.", "0", ["0", "zero"]),
            ]
        },
        {
            'title': 'Probability: Story Proofs',
            'type': Quiz.QuizType.THEORETICAL,
            'eval_method': Quiz.EvaluationMethod.SELF_EVAL,
            'domain': Quiz.Domain.STATISTICS,
            'subject': Quiz.Subject.PROBABILITY,
            'topic': 'Probability and Counting',
            'description': "Self-Evaluation quiz on combinatorial proofs.",
            'questions': [
                (1, "Explain the identity $\\binom{n}{k} = \\binom{n}{n-k}$ using a 'Team Selection' story.", "Choosing a team of $k$ people to play is exactly the same as choosing a group of $(n-k)$ people to sit on the bench. Every team choice defines a specific bench choice.", "Symmetry identity."),
                (2, "Give a story proof for $k \\cdot \\binom{n}{k} = n \\cdot \\binom{n-1}{k-1}$. (The 'President' Identity)", "LHS: Choose a committee of size $k$, then pick 1 president from them. RHS: Choose the president first from the $n$ people, then choose the remaining $k-1$ members from the remaining $n-1$ people.", "Both count the number of ways to have a committee with a leader."),
                (3, "Explain Vandermonde's Identity $\\binom{m+n}{k} = \\sum \\binom{m}{j} \\binom{n}{k-j}$ with a story.", "We are picking a committee of $k$ people from a group of $m$ men and $n$ women. We can break this down by cases: 0 men & $k$ women, 1 man & $k-1$ women... summing these cases gives the total.", "Counting by partitioning the group."),
                (4, "Why is $\\sum \\binom{n}{k} = 2^n$?", "LHS sums the counts of subsets of size 0, 1, ... $n$. RHS counts all subsets directly (each element is either IN or OUT). Both count the total number of subsets (Power Set).", "Sum of binomial coefficients."),
                (5, "Explain the recursion $\\binom{n}{k} = \\binom{n-1}{k} + \\binom{n-1}{k-1}$ using a 'Specific Person X' story.", "Focus on person X. To form a team of $k$, either X is NOT on the team (so pick all $k$ from the other $n-1$ people) OR X IS on the team (so pick the remaining $k-1$ from the other $n-1$ people).", "Pascal's Triangle logic."),
                (6, "Explain the 'Stars and Bars' logic for distributing 5 candies to 3 kids.", "Imagine the 5 candies as stars (*****). To divide them into 3 groups, we need 2 bars (|). Any arrangement like **|*|** represents a specific distribution. We count arrangements of 5 stars + 2 bars.", None),
                (7, "Why does $n(n-1)...(n-k+1)$ calculate permutations?", "For the 1st spot, we have $n$ choices. For the 2nd, we have $n-1$ left (since no replacement). We continue this $k$ times.", None),
                (8, "Why is $0!$ defined as 1?", "Combinatorially, asking 'How many ways can we arrange 0 items?' has one answer: The empty arrangement (doing nothing).", None),
                (9, "Explain why $\\binom{n}{2}$ appears in the Birthday Problem calculation.", "We are looking for a match between ANY pair of people. With $n$ people, there are $\\binom{n}{2}$ distinct pairs. The probability accumulates based on these interactions.", None),
                (10, "Provide a story for $n^2 = 2 \\binom{n}{2} + n$.", "We are picking a pair of people $(x, y)$ from $n$ people, where order matters and replacement is allowed ($n^2$). Case 1: $x \\neq y$ (nC2 pairs, times 2 for order). Case 2: $x = y$ (n people chosen twice).", "Decomposing the grid of size $n*n."),
            ]
        },
        {
            'title': 'Probability: Axioms & Intuition',
            'type': Quiz.QuizType.THEORETICAL,
            'eval_method': Quiz.EvaluationMethod.SELF_EVAL,
            'domain': Quiz.Domain.STATISTICS,
            'subject': Quiz.Subject.PROBABILITY,
            'topic': 'Probability and Counting',
            'description': "Self-Evaluation quiz on probability axioms.",
            'questions': [
                (1, "Why is $P(\\text{Union of disjoint events}) = \\text{Sum of probabilities}$?", "Axiom 3. If events don't overlap, their 'masses' in the sample space simply add up. If they overlapped, adding would double-count.", None),
                (2, "Explain the difference between 'Sampling with Replacement' and 'Sampling without Replacement' regarding independence.", "With replacement: Draws are independent (the deck resets). Without replacement: Draws are dependent (taking an Ace makes the next Ace less likely).", None),
                (3, "Why must $P(A) \\le 1$?", "Because the probability of the entire sample space $S$ is 1, and $A$ is contained within $S$. A part cannot be larger than the whole.", None),
                (4, "What is the 'Pebble World' analogy?", "In discrete probability, each outcome is a pebble with a specific mass. The total mass is 1. The probability of an event is the sum of the masses of the pebbles in that event.", None),
                (5, "Explain the 'Labeling' strategy to avoid mistakes.", "It is safer to treat objects (like coins or cards) as distinct (labeled 1, 2, 3) to ensure outcomes are equally likely, even if the problem says they are 'indistinguishable'.", None),
                (6, "Why is $P(A \\cup B) \\le P(A) + P(B)$? (Boole's Inequality)", "The sum $P(A)+P(B)$ counts the intersection twice. The union only counts it once. Therefore the sum is an upper bound.", None),
                (7, "What is the complement of 'At least one match'?", "Zero matches (Everyone is unique).", None),
                (8, "If outcomes are NOT equally likely, can we use $|A|/|S|$?", "No. That formula only works for uniform distributions. For non-uniform, we must sum the individual probabilities.", None),
                (9, "Explain 'Capture-Recapture' intuition.", "If you tag a random sample of fish, release them, and catch a new sample, the proportion of tagged fish in the new sample estimates the proportion of the total population.", "An application of Hypergeometric probabilities."),
                (10, "Why does $P(\\emptyset) = 0$?", "$S$ and Empty are disjoint, and their union is $S$. So $P(S) = P(S) + P(\\emptyset)$. Since $P(S)=1$, $P(\\emptyset)$ must be 0.", None),
            ]
        }
    ]
