from quizzes.models import Quiz
from django.utils import timezone

def get_linear_algebra_quizzes():
    return [
        {
            'title': 'Vectors: Dot Products & Lengths',
            'type': Quiz.QuizType.THEORETICAL,
            'eval_method': Quiz.EvaluationMethod.AUTOMATED,
            'domain': Quiz.Domain.LINEAR_ALGEBRA,
            'subject': Quiz.Subject.FOUNDATIONS,
            'topic': 'Vectors & Matrices',
            'description': "Practice with dot products, norms, and vector properties. Automatically graded.",
            'questions': [
                {
                    "question_order": 1,
                    "question_text": "If v = (1, 1) and w = (2, -1), what is the value of the dot product v · w?",
                    "model_answer": "1",
                    "accepted_answers": ["1", "one"],
                    "explanation": "The dot product is (1)(2) + (1)(-1) = 2 - 1 = 1."
                },
                {
                    "question_order": 2,
                    "question_text": "Vectors whose dot product equals zero are called what?",
                    "model_answer": "Orthogonal",
                    "accepted_answers": ["orthogonal", "perpendicular", "normal"],
                    "explanation": "If v · w = 0, the angle between them is 90 degrees."
                },
                {
                    "question_order": 3,
                    "question_text": "Calculate the length (norm) of the vector v = (3, 4).",
                    "model_answer": "5",
                    "accepted_answers": ["5", "five"],
                    "explanation": "Length is the square root of (3^2 + 4^2) = sqrt(9+16) = sqrt(25) = 5."
                },
                {
                    "question_order": 4,
                    "question_text": "A unit vector is a vector whose length equals what number?",
                    "model_answer": "1",
                    "accepted_answers": ["1", "one"],
                    "explanation": "Unit vectors are u = v / ||v||, resulting in a length of 1."
                },
                {
                    "question_order": 5,
                    "question_text": "In the linear combination c(1, 0) + d(0, 1), if the result is vector (5, 2), what is the value of c?",
                    "model_answer": "5",
                    "accepted_answers": ["5", "five"],
                    "explanation": "c(1, 0) + d(0, 1) = (c, d). Therefore c=5 and d=2."
                },
                {
                    "question_order": 6,
                    "question_text": "Complete the inequality name: The Cauchy-_______ Inequality states that |v · w| ≤ ||v|| ||w||.",
                    "model_answer": "Schwarz",
                    "accepted_answers": ["Schwarz", "Bunyakovsky", "Schwarz inequality"],
                    "explanation": "The Cauchy-Schwarz inequality connects geometry (lengths) to algebra (dot products)."
                },
                {
                    "question_order": 7,
                    "question_text": "If vector v is in 3-dimensional space (R3), how many components does it have?",
                    "model_answer": "3",
                    "accepted_answers": ["3", "three"],
                    "explanation": "R3 denotes a space with 3 dimensions (x, y, z)."
                },
                {
                    "question_order": 8,
                    "question_text": "What is the result of the dot product of a vector with itself (v · v)?",
                    "model_answer": "Length squared",
                    "accepted_answers": ["length squared", "norm squared", "magnitude squared", "||v||^2", "|v|^2"],
                    "explanation": "v · v = ||v||^2."
                },
                {
                    "question_order": 9,
                    "question_text": "If w = 2v, what is the angle between vector v and vector w in degrees?",
                    "model_answer": "0",
                    "accepted_answers": ["0", "zero", "0 degrees"],
                    "explanation": "One is a positive scalar multiple of the other, so they point in the exact same direction."
                },
                {
                    "question_order": 10,
                    "question_text": "If you divide a non-zero vector v by its length ||v||, what property does the resulting vector you have?",
                    "model_answer": "It has length 1",
                    "accepted_answers": ["length 1", "unit vector", "norm 1", "magnitude 1", "unit"],
                    "explanation": "This process is called 'Normalization'. The direction remains the same, but the length becomes 1. This is crucial in ML for feature scaling."
                }
            ]
        },
        {
            'title': 'Vectors: Theoretical Concepts',
            'type': Quiz.QuizType.THEORETICAL,
            'eval_method': Quiz.EvaluationMethod.SELF_EVAL,
            'domain': Quiz.Domain.LINEAR_ALGEBRA,
            'subject': Quiz.Subject.FOUNDATIONS,
            'topic': 'Vectors & Matrices',
            'description': "Conceptual understanding of vector geometry and linear combinations. Self-graded.",
            'questions': [
                {
                    "question_order": 1,
                    "question_text": "Describe the geometric shape formed by all linear combinations of two non-zero, non-parallel vectors, v and w, in 3D space (R3).",
                    "model_answer": "A plane passing through the origin.",
                    "accepted_answers": [],
                    "explanation": "The set of all c*v + d*w generates a 2D plane. It must pass through the origin because c=0, d=0 gives the zero vector."
                },
                {
                    "question_order": 2,
                    "question_text": "Explain why the dot product v · w is negative if the angle between them is obtuse (greater than 90 degrees).",
                    "model_answer": "The formula for dot product is ||v|| ||w|| cos(theta). Lengths are always positive. Cosine is negative for angles between 90 and 180 degrees, making the total product negative.",
                    "accepted_answers": [],
                    "explanation": "This geometric link relies on the cosine behavior."
                },
                {
                    "question_order": 3,
                    "question_text": "Using the Triangle Inequality ||v + w|| ≤ ||v|| + ||w||, explain when the equality holds (when is the 'less than' actually 'equal to')?",
                    "model_answer": "Equality holds only when v and w are in the same direction (parallel and pointing the same way).",
                    "accepted_answers": [],
                    "explanation": "Geometrically, this means the triangle flattens into a straight line."
                },
                {
                    "question_order": 4,
                    "question_text": "How do you algebraically determine if three vectors in R3 lie on the same plane?",
                    "model_answer": "They lie on the same plane if one vector can be written as a linear combination of the other two (linearly dependent). Or, if their volume/determinant is zero.",
                    "accepted_answers": [],
                    "explanation": "If u = c*v + d*w, then u adds no new dimension; it stays in the plane defined by v and w."
                },
                {
                    "question_order": 5,
                    "question_text": "Describe the difference between v = (1, 2, 3) as a point and v = (1, 2, 3) as a vector.",
                    "model_answer": "As a point, it is a specific location in space. As a vector, it is an arrow (magnitude and direction) starting at the origin (0,0,0) and ending at that point.",
                    "accepted_answers": [],
                    "explanation": "Vectors represent displacement; points represent position."
                },
                {
                    "question_order": 6,
                    "question_text": "Why is the zero vector (0,0) orthogonal to every other vector?",
                    "model_answer": "Because the dot product of the zero vector with any vector v is 0 (0*x + 0*y = 0). By definition, dot product = 0 implies orthogonality.",
                    "accepted_answers": [],
                    "explanation": "It creates a unique geometric edge case where the angle is technically undefined, but orthogonality holds algebraically."
                },
                {
                    "question_order": 7,
                    "question_text": "Explain the concept of a 'Linear Combination' in your own words.",
                    "model_answer": "It is the process of taking vectors, scaling them by constant numbers (scalars), and adding the results together (cv + dw).",
                    "accepted_answers": [],
                    "explanation": "This is the fundamental operation of linear algebra."
                },
                {
                    "question_order": 8,
                    "question_text": "If ||v|| = 3 and ||w|| = 4, what are the maximum and minimum possible values for ||v - w||?",
                    "model_answer": "Max: 7, Min: 1",
                    "accepted_answers": [],
                    "explanation": "Max occurs when they point in opposite directions (3 - (-4) distance = 7). Min occurs when they point in same direction (4 - 3 = 1)."
                },
                {
                    "question_order": 9,
                    "question_text": "What does the equation cos(theta) = (v · w) / (||v|| ||w||) tell us about the relationship between vector algebra and geometry?",
                    "model_answer": "It links the algebraic calculation of coordinates (dot product) to geometric intuition (angles).",
                    "accepted_answers": [],
                    "explanation": "This allows us to find angles in high-dimensional spaces where we cannot visualize them."
                },
                {
                    "question_order": 10,
                    "question_text": "Visually, how do you find v + w using the parallelogram rule?",
                    "model_answer": "Place the tail of w at the head of v. The vector from the start of v to the end of w is the sum.",
                    "accepted_answers": [],
                    "explanation": "Alternatively, draw both from the origin and complete the parallelogram; the diagonal is the sum."
                }
            ]
        },
        {
            'title': 'Matrices: Multiplication & Operations',
            'type': Quiz.QuizType.THEORETICAL,
            'eval_method': Quiz.EvaluationMethod.AUTOMATED,
            'domain': Quiz.Domain.LINEAR_ALGEBRA,
            'subject': Quiz.Subject.FOUNDATIONS,
            'topic': 'Vectors & Matrices',
            'description': "Matrix operations check.",
            'questions': [
                {
                    "question_order": 1,
                    "question_text": "If A is a 3x2 matrix and B is a 2x5 matrix, what are the dimensions of the product AB?",
                    "model_answer": "3x5",
                    "accepted_answers": ["3x5", "3 by 5", "3 * 5"],
                    "explanation": "(m x n) * (n x p) results in (m x p)."
                },
                {
                    "question_order": 2,
                    "question_text": "Is Matrix Multiplication commutative? (Yes/No)",
                    "model_answer": "No",
                    "accepted_answers": ["No", "no", "false"],
                    "explanation": "In general, AB does not equal BA. Dimensions might not even match."
                },
                {
                    "question_order": 3,
                    "question_text": "Strang's 'Column View': The product Ax is a linear combination of the _______ of A.",
                    "model_answer": "Columns",
                    "accepted_answers": ["columns", "column vectors"],
                    "explanation": "Ax = x1(col1) + x2(col2) + ... This is the most important concept in Chapter 1."
                },
                {
                    "question_order": 4,
                    "question_text": "If A is a 3x3 Identity matrix (I) and v is a vector, what is I*v?",
                    "model_answer": "v",
                    "accepted_answers": ["v", "vector v", "the same vector"],
                    "explanation": "The identity matrix acts like the number 1 in scalar multiplication."
                },
                {
                    "question_order": 5,
                    "question_text": "In the multiplication AB, the entry in row i and column j comes from the dot product of Row i of A and _______ of B.",
                    "model_answer": "Column j",
                    "accepted_answers": ["column j", "Column j", "col j"],
                    "explanation": "This is the standard 'Row-Column' rule for matrix multiplication."
                },
                {
                    "question_order": 6,
                    "question_text": "The transpose of a matrix A (denoted A^T) transforms the rows of A into the _______ of A^T.",
                    "model_answer": "Columns",
                    "accepted_answers": ["columns", "cols"],
                    "explanation": "Rows become columns and columns become rows."
                },
                {
                    "question_order": 7,
                    "question_text": "If Matrix A has dependent columns, is the matrix invertible? (Yes/No)",
                    "model_answer": "No",
                    "accepted_answers": ["No", "no"],
                    "explanation": "Dependent columns mean the matrix is singular (not invertible)."
                },
                {
                    "question_order": 8,
                    "question_text": "Calculate the inner product (dot product) of row vector [1, 2] and column vector [3; 4].",
                    "model_answer": "11",
                    "accepted_answers": ["11", "eleven"],
                    "explanation": "1*3 + 2*4 = 3 + 8 = 11."
                },
                {
                    "question_order": 9,
                    "question_text": "If A is a 2x1 matrix (column) and B is a 1x2 matrix (row), the product AB is what size matrix?",
                    "model_answer": "2x2",
                    "accepted_answers": ["2x2", "2 by 2"],
                    "explanation": "This is an 'Outer Product', which creates a matrix of rank 1."
                },
                {
                    "question_order": 10,
                    "question_text": "If A is invertible, what is the unique solution to Ax = b?",
                    "model_answer": "x = A^-1 b",
                    "accepted_answers": ["x = A^-1 b", "A^-1 b", "A inverse b"],
                    "explanation": "Multiply both sides by A inverse on the left."
                }
            ]
        },
        {
            'title': 'Matrices: Algebra & Properties',
            'type': Quiz.QuizType.THEORETICAL,
            'eval_method': Quiz.EvaluationMethod.SELF_EVAL,
            'domain': Quiz.Domain.LINEAR_ALGEBRA,
            'subject': Quiz.Subject.FOUNDATIONS,
            'topic': 'Vectors & Matrices',
            'description': "Understanding matrix algebra, inverses, and partitions.",
            'questions': [
                {
                    "question_order": 1,
                    "question_text": "Explain the difference between the Row-Column rule (dot products) and the Column-Row rule (sum of outer products) for matrix multiplication AB.",
                    "model_answer": "Row-Col rule calculates one number at a time (inner products). Col-Row rule sums up full matrices (Column k of A multiplied by Row k of B). Both give the same result.",
                    "accepted_answers": [],
                    "explanation": "Strang emphasizes the Col-Row rule (outer products) for understanding the structure of the data."
                },
                {
                    "question_order": 2,
                    "question_text": "What is the formula for the inverse of a product (AB)^-1?",
                    "model_answer": "B^-1 A^-1",
                    "accepted_answers": [],
                    "explanation": "The order must be reversed: shoes and socks rule."
                },
                {
                    "question_order": 3,
                    "question_text": "If det(A) = 0 for a square matrix A, is the matrix invertible (non-singular)?",
                    "model_answer": "No",
                    "accepted_answers": [],
                    "explanation": "A determinant of zero indicates the matrix collapses space and cannot be reversed."
                },
                {
                    "question_order": 4,
                    "question_text": "What is the transpose of the product (AB)^T?",
                    "model_answer": "B^T A^T",
                    "accepted_answers": [],
                    "explanation": "Like the inverse, the transpose of a product reverses the order of multiplication."
                },
                {
                    "question_order": 5,
                    "question_text": "Why does (AB)C = A(BC)? (Associativity). Explain conceptually, not just by writing the property name.",
                    "model_answer": "Matrix multiplication represents applying linear transformations sequentially. Applying transformation C, then B, then A is the same sequence regardless of how we group the calculations.",
                    "accepted_answers": [],
                    "explanation": "Matrices are functions acting on vectors."
                },
                {
                    "question_order": 6,
                    "question_text": "In the CR decomposition (A = CR), if A is a matrix of rank 1, what are the dimensions of C and R?",
                    "model_answer": "C is a single column (m x 1) and R is a single row (1 x n).",
                    "accepted_answers": [],
                    "explanation": "Every rank 1 matrix is the outer product of one column and one row."
                },
                {
                    "question_order": 7,
                    "question_text": "How does multiplying a matrix A by a diagonal matrix D on the right (AD) affect the columns of A?",
                    "model_answer": "It scales the columns of A. The first column is multiplied by d1, the second by d2, etc.",
                    "accepted_answers": [],
                    "explanation": "Multiplying on the Right affects Columns. Multiplying on the Left affects Rows."
                },
                {
                    "question_order": 8,
                    "question_text": "If A and B are both Upper Triangular matrices, what is true about their product AB?",
                    "model_answer": "AB is also Upper Triangular.",
                    "accepted_answers": [],
                    "explanation": "The linear combinations of triangular columns preserve the triangular structure."
                },
                {
                    "question_order": 9,
                    "question_text": "Explain why the columns of the Identity Matrix are important.",
                    "model_answer": "They are the standard basis vectors (1,0,0...), (0,1,0)... Any vector v can be written as a combination of these columns simply by using the components of v as the weights.",
                    "accepted_answers": [],
                    "explanation": "This is why I*v = v."
                },
                {
                    "question_order": 10,
                    "question_text": "If you view matrix multiplication AB as A acting on the columns of B, what is the result?",
                    "model_answer": "The result is a matrix where the columns are A * (col 1 of B), A * (col 2 of B), etc.",
                    "accepted_answers": [],
                    "explanation": "This allows us to treat matrix multiplication as a collection of matrix-vector products."
                }
            ]
        },
        {
            'title': 'Gaussian Elimination & Pivots',
            'type': Quiz.QuizType.THEORETICAL,
            'eval_method': Quiz.EvaluationMethod.AUTOMATED,
            'domain': Quiz.Domain.LINEAR_ALGEBRA,
            'subject': Quiz.Subject.FOUNDATIONS,
            'topic': 'Solving Linear Equations',
            'description': "Understanding pivots, multipliers, and elimination steps.",
            'questions': [
                {
                    "question_order": 1,
                    "question_text": "In Gaussian elimination, the first non-zero entry in a row used to eliminate entries below it is called the ______.",
                    "model_answer": "Pivot",
                    "accepted_answers": ["pivot", "pivot element"],
                    "explanation": "Pivots are the crucial diagonal entries that must not be zero to proceed without row exchanges."
                },
                {
                    "question_order": 2,
                    "question_text": "If we subtract $3$ times Row 1 from Row 2, what is the 'multiplier' ($l_{21}$) associated with this operation?",
                    "model_answer": "3",
                    "accepted_answers": ["3", "three"],
                    "explanation": "The multiplier is the number you multiply the pivot row by to cancel the entry below it."
                },
                {
                    "question_order": 3,
                    "question_text": "Elimination converts matrix $A$ into an ______ Triangular matrix $U$.",
                    "model_answer": "Upper",
                    "accepted_answers": ["upper", "Upper"],
                    "explanation": "The result of forward elimination is $U$, where all entries below the diagonal are zero."
                },
                {
                    "question_order": 4,
                    "question_text": "A matrix that has no inverse is technically called _______.",
                    "model_answer": "Singular",
                    "accepted_answers": ["singular", "non-invertible", "degenerate"],
                    "explanation": "A singular matrix has a determinant of $0$ and fewer than $n$ pivots."
                },
                {
                    "question_order": 5,
                    "question_text": "What is the inverse of the matrix product $AB$? (Write in terms of $A^{-1}$ and $B^{-1}$)",
                    "model_answer": "B^-1 A^-1",
                    "accepted_answers": ["B^-1 A^-1", "B^-1A^-1", "inverse of B times inverse of A", "Binv Ainv"],
                    "explanation": "The 'Shoes and Socks' rule: to undo the operation $AB$, you must unwrap $B$ first, then $A$."
                },
                {
                    "question_order": 6,
                    "question_text": "For a $2 \\times 2$ matrix $\\begin{bmatrix} a & b \\\\ c & d \\end{bmatrix}$, the quantity $(ad - bc)$ is known as the _______.",
                    "model_answer": "Determinant",
                    "accepted_answers": ["determinant", "det"],
                    "explanation": "If $ad - bc = 0$, the matrix is singular."
                },
                {
                    "question_order": 7,
                    "question_text": "The Gauss-Jordan method solves for $A$ inverse by applying elimination to the augmented matrix $[A \\ | \\ ...]$. Fill in the blank.",
                    "model_answer": "I",
                    "accepted_answers": ["I", "Identity", "Identity matrix"],
                    "explanation": "We transform $[A \\ | \\ I]$ into $[I \\ | \\ A^{-1}]$."
                },
                {
                    "question_order": 8,
                    "question_text": "If a matrix $A$ has a row of all zeros, can it be invertible? (Yes/No)",
                    "model_answer": "No",
                    "accepted_answers": ["No", "no", "false"],
                    "explanation": "A row of zeros implies the pivots cannot fill the diagonal, meaning the matrix is singular."
                },
                {
                    "question_order": 9,
                    "question_text": "What matrix $E$ would you multiply $A$ by to subtract $2 \\times \\text{Row 1}$ from $\\text{Row 2}$? (Describe the entry $E_{21}$)",
                    "model_answer": "-2",
                    "accepted_answers": ["-2", "negative 2"],
                    "explanation": "Elementary matrices have the negative of the multiplier in the position being eliminated (off-diagonal)."
                },
                {
                    "question_order": 10,
                    "question_text": "Once we have $Ux = c$, we solve for $x$ using _______ substitution.",
                    "model_answer": "Back",
                    "accepted_answers": ["back", "backward"],
                    "explanation": "We solve the equations from bottom to top."
                }
            ]
        },
        {
            'title': 'Inverses & Singular Matrices',
            'type': Quiz.QuizType.THEORETICAL,
            'eval_method': Quiz.EvaluationMethod.SELF_EVAL,
            'domain': Quiz.Domain.LINEAR_ALGEBRA,
            'subject': Quiz.Subject.FOUNDATIONS,
            'topic': 'Solving Linear Equations',
            'description': "Understanding invertibility, failure cases, and geometric interpretations.",
            'questions': [
                {
                    "question_order": 1,
                    "question_text": "Explain the difference between a 'Temporary Failure' and a 'Permanent Failure' in Gaussian elimination.",
                    "model_answer": "Temporary failure occurs when a $0$ appears in a pivot position, but a non-zero entry exists below it (fixed by row exchange). Permanent failure occurs when a $0$ is in the pivot position and all entries below it are also $0$ (matrix is singular/not invertible).",
                    "accepted_answers": [],
                    "explanation": "This distinguishes between needing a permutation and the system having no unique solution."
                },
                {
                    "question_order": 2,
                    "question_text": "Why is the inverse of an Elementary Matrix (one that does a row subtraction) easy to find without calculation?",
                    "model_answer": "Because the operation is just 'adding back' what was subtracted. If $E$ subtracts $5 \\times \\text{Row 1}$ from $\\text{Row 2}$, $E^{-1}$ adds $5 \\times \\text{Row 1}$ to $\\text{Row 2}$.",
                    "accepted_answers": [],
                    "explanation": "In the matrix, you simply flip the sign of the off-diagonal multiplier."
                },
                {
                    "question_order": 3,
                    "question_text": "Why do we say that Matrix Multiplication is 'Associative' and how does this help in understanding LU factorization?",
                    "model_answer": "Associativity means $(AB)C = A(BC)$. This allows us to group all the elementary elimination matrices ($E$) together into one matrix $L$ without worrying about the vector $x$. $E(Ax) = (EA)x$.",
                    "accepted_answers": [],
                    "explanation": "It justifies why we can talk about factoring the matrix A itself, separate from the specific equations."
                },
                {
                    "question_order": 4,
                    "question_text": "Visually/Geometrically, what does a singular matrix ($2 \\times 2$) represent in terms of the row equations?",
                    "model_answer": "The two lines defined by the rows are parallel (and distinct) or the exact same line. They do not intersect at a unique single point.",
                    "accepted_answers": [],
                    "explanation": "In 3D, the planes would not intersect at a point (they might form a line, a tunnel, or be parallel)."
                },
                {
                    "question_order": 5,
                    "question_text": "Explain the 'Shoes and Socks' analogy for the inverse of a product $(AB)^{-1}$.",
                    "model_answer": "You put on socks ($A$) then shoes ($B$). To reverse this, you must take off shoes ($B^{-1}$) first, then socks ($A^{-1}$). Hence $(AB)^{-1} = B^{-1} A^{-1}$.",
                    "accepted_answers": [],
                    "explanation": "Order of operations reverses when inverting."
                },
                {
                    "question_order": 6,
                    "question_text": "If $A$ is invertible, what must be true about the equation $Ax = b$?",
                    "model_answer": "It has exactly one unique solution $x$ for every vector $b$.",
                    "accepted_answers": [],
                    "explanation": "Invertibility $\\leftrightarrow$ Nonsingularity $\\leftrightarrow$ Unique Solution."
                },
                {
                    "question_order": 7,
                    "question_text": "Describe the diagonal entries of the inverse of a Diagonal Matrix $D$.",
                    "model_answer": "The entries are the reciprocals ($1/d_{ii}$) of the original diagonal entries.",
                    "accepted_answers": [],
                    "explanation": "If $D$ has 2 and 5 on diagonal, $D^{-1}$ has $1/2$ and $1/5$."
                },
                {
                    "question_order": 8,
                    "question_text": "Why is it computationally expensive to calculate $A^{-1}$ explicitly compared to just solving $Ax=b$?",
                    "model_answer": "Finding $A^{-1}$ is equivalent to solving $Ax=e$ for $n$ different columns. It effectively triples the work (or more) compared to a single elimination pass for one $b$.",
                    "accepted_answers": [],
                    "explanation": "Strang emphasizes: Don't compute the inverse unless you have to! Solve the system instead."
                },
                {
                    "question_order": 9,
                    "question_text": "If $A$ and $B$ are square and invertible, why is $A + B$ not necessarily invertible?",
                    "model_answer": "There is no formula for $(A+B)^{-1}$. Example: $A=I$ and $B=-I$. Both are invertible, but sum is $0$ (singular).",
                    "accepted_answers": [],
                    "explanation": "Inverses handle multiplication well, but addition poorly."
                },
                {
                    "question_order": 10,
                    "question_text": "In the Gauss-Jordan method, we go from $[A \\ | \\ I]$ to $[I \\ | \\ A^{-1}]$. What is happening to the matrix representing the row operations during this process?",
                    "model_answer": "The matrix of row operations accumulates to become $A^{-1}$. Effectively, $(\\text{Row Ops}) [A \\ | \\ I] = [I \\ | \\ A^{-1}]$.",
                    "accepted_answers": [],
                    "explanation": "The operations that turn $A$ into $I$ are exactly the operations that turn $I$ into $A^{-1}$."
                }
            ]
        },
        {
            'title': 'LU Factorization & Transposes',
            'type': Quiz.QuizType.THEORETICAL,
            'eval_method': Quiz.EvaluationMethod.AUTOMATED,
            'domain': Quiz.Domain.LINEAR_ALGEBRA,
            'subject': Quiz.Subject.FOUNDATIONS,
            'topic': 'Solving Linear Equations',
            'description': "LU decomposition, permutation matrices, and symmetric rules.",
            'questions': [
                {
                    "question_order": 1,
                    "question_text": "In the factorization $A = LU$, $L$ stands for _______ Triangular matrix.",
                    "model_answer": "Lower",
                    "accepted_answers": ["Lower", "lower"],
                    "explanation": "$L$ contains the multipliers used during elimination."
                },
                {
                    "question_order": 2,
                    "question_text": "What number is always on the main diagonal of the standard $L$ matrix in $A = LU$?",
                    "model_answer": "1",
                    "accepted_answers": ["1", "one"],
                    "explanation": "The diagonals of $L$ are $1$s; the pivots appear on the diagonal of $U$."
                },
                {
                    "question_order": 3,
                    "question_text": "A matrix $P$ that exchanges rows of another matrix is called a _______ matrix.",
                    "model_answer": "Permutation",
                    "accepted_answers": ["permutation", "Permutation"],
                    "explanation": "$P$ is the identity matrix with rows reordered."
                },
                {
                    "question_order": 4,
                    "question_text": "If $A$ is a Symmetric matrix, then $A$ must equal what?",
                    "model_answer": "A Transpose",
                    "accepted_answers": ["A Transpose", "A^T", "transpose of A", "A_T"],
                    "explanation": "Symmetric means $a_{ij} = a_{ji}$."
                },
                {
                    "question_order": 5,
                    "question_text": "What is the Transpose of the product $(AB)$?",
                    "model_answer": "B^T A^T",
                    "accepted_answers": ["B^T A^T", "B' A'", "B transpose A transpose"],
                    "explanation": "Like inverses, transposes reverse the order of multiplication."
                },
                {
                    "question_order": 6,
                    "question_text": "For a Permutation matrix $P$, $P$ inverse is always equal to $P$ _______.",
                    "model_answer": "Transpose",
                    "accepted_answers": ["Transpose", "transpose", "T", "^T"],
                    "explanation": "$P^T P = I$. This is a special property of orthogonal matrices."
                },
                {
                    "question_order": 7,
                    "question_text": "The computational cost of elimination for an $n \\times n$ matrix is proportional to $n$ to the power of _______.",
                    "model_answer": "3",
                    "accepted_answers": ["3", "three"],
                    "explanation": "The operation count is approximately $n^3 / 3$."
                },
                {
                    "question_order": 8,
                    "question_text": "In the Symmetric Factorization $A = LDL^T$, $D$ stands for what kind of matrix?",
                    "model_answer": "Diagonal",
                    "accepted_answers": ["diagonal", "Diagonal"],
                    "explanation": "We separate the pivots out of $U$, leaving $U$ with $1$s on diagonal, becoming $L^T$ for symmetric matrices."
                },
                {
                    "question_order": 9,
                    "question_text": "Is the matrix product $R^T R$ always symmetric? (Yes/No)",
                    "model_answer": "Yes",
                    "accepted_answers": ["Yes", "yes", "true"],
                    "explanation": "$(R^T R)^T = R^T (R^T)^T = R^T R$. It returns to itself."
                },
                {
                    "question_order": 10,
                    "question_text": "How many $3 \\times 3$ Permutation matrices exist?",
                    "model_answer": "6",
                    "accepted_answers": ["6", "six"],
                    "explanation": "$n$ factorial ($3! = 3 \\times 2 \\times 1 = 6$)."
                }
            ]
        },
        {
            'title': 'Advanced Factorization (PA=LU)',
            'type': Quiz.QuizType.THEORETICAL,
            'eval_method': Quiz.EvaluationMethod.SELF_EVAL,
            'domain': Quiz.Domain.LINEAR_ALGEBRA,
            'subject': Quiz.Subject.FOUNDATIONS,
            'topic': 'Solving Linear Equations',
            'description': "Advanced logic behind elimination, L, U, P, and symmetry.",
            'questions': [
                {
                    "question_order": 1,
                    "question_text": "Why is the factorization $A = LU$ more useful than just running elimination from scratch every time?",
                    "model_answer": "If you have to solve $Ax = b$ for many different vectors $b$, you factor $A$ once ($n^3$ cost), then use $L$ and $U$ to solve each $b$ very quickly ($n^2$ cost) via substitution.",
                    "accepted_answers": [],
                    "explanation": "It separates the coefficient matrix processing from the specific right-hand side."
                },
                {
                    "question_order": 2,
                    "question_text": "Describe the structure of the matrix $L$ compared to the elimination matrices $E$. Why is $L$ 'cleaner'?",
                    "model_answer": "$L$ contains the multipliers exactly in their positions below the diagonal. The product of $E$'s mixes terms, but the inverse of $E$'s (which forms $L$) places the multipliers perfectly without mixing.",
                    "accepted_answers": [],
                    "explanation": "This is a minor miracle of linear algebra that makes $A=LU$ so elegant."
                },
                {
                    "question_order": 3,
                    "question_text": "If we need row exchanges to solve $Ax=b$, the factorization becomes $PA = LU$. What is $P$ and why is it needed?",
                    "model_answer": "$P$ is a Permutation Matrix. It reorders the rows of $A$ beforehand so that pivots are in the correct non-zero positions, allowing the standard $LU$ process to proceed.",
                    "accepted_answers": [],
                    "explanation": "Elimination fails if a zero is in the pivot spot; $P$ fixes this logic."
                },
                {
                    "question_order": 4,
                    "question_text": "Why does the operation count decrease from $n^3/3$ (Elimination) to $n^2$ (Back Substitution)?",
                    "model_answer": "Elimination works on the whole 3D block of the matrix (rows * cols * steps). Substitution only works on the 2D triangle of the matrix. One dimension lower.",
                    "accepted_answers": [],
                    "explanation": "Integration analogy: Integral of $x^2$ is $x^3/3$."
                },
                {
                    "question_order": 5,
                    "question_text": "Show/Explain why $(Ax) \\cdot y = x \\cdot (A^T y)$. (Dot Product Transpose Property)",
                    "model_answer": "The dot product $(Ax) \\cdot y$ is $(Ax)^T y = x^T A^T y$. This is the same as $x \\cdot (A^T y)$.",
                    "accepted_answers": [],
                    "explanation": "This property effectively defines the transpose: it moves the matrix across the dot product."
                },
                {
                    "question_order": 6,
                    "question_text": "What is the relationship between symmetric matrices and elimination? (Hint: $LDL^T$)",
                    "model_answer": "If $A$ is symmetric (and no row exchanges needed), $U$ is the transpose of $L$ (scaled by pivots). We write $A = LDL^T$, saving half the storage/work.",
                    "accepted_answers": [],
                    "explanation": "Symmetry is preserved during elimination."
                },
                {
                    "question_order": 7,
                    "question_text": "Why is the inverse of a Permutation Matrix equal to its transpose?",
                    "model_answer": "Permutations are orthogonal matrices. The rows are unit vectors and orthogonal to each other. Thus $P^T P = I$.",
                    "accepted_answers": [],
                    "explanation": "Swapping rows back is the same as swapping columns in the reverse order."
                },
                {
                    "question_order": 8,
                    "question_text": "Explain the concept of 'Band Matrices' and why they are computationally efficient.",
                    "model_answer": "Band matrices only have non-zero entries near the diagonal (within a bandwidth $w$). Elimination only affects this band, reducing cost from $n^3$ to $n \\cdot w^2$.",
                    "accepted_answers": [],
                    "explanation": "This is crucial for engineering applications with sparse connections."
                },
                {
                    "question_order": 9,
                    "question_text": "If $A$ is invertible and symmetric, is $A^{-1}$ symmetric? Why?",
                    "model_answer": "Yes. $(A^{-1})^T = (A^T)^{-1} = A^{-1}$. Since $A$ is symmetric, transposing the inverse gets you back the inverse.",
                    "accepted_answers": [],
                    "explanation": "Symmetry is robust; it survives inversion."
                },
                {
                    "question_order": 10,
                    "question_text": "What happens to the $L$ and $U$ factors if you multiply $A$ by $2$?",
                    "model_answer": "$L$ remains the same (multipliers are ratios, so $2x/2y = x/y$). $U$ is multiplied by $2$ (the pivots double).",
                    "accepted_answers": [],
                    "explanation": "$L$ depends on the ratio of rows; $U$ contains the actual scale of the numbers."
                }
            ]
        },
        {
            'title': 'Vector Subspaces & Nullspace',
            'type': Quiz.QuizType.THEORETICAL,
            'eval_method': Quiz.EvaluationMethod.AUTOMATED,
            'domain': Quiz.Domain.LINEAR_ALGEBRA,
            'subject': Quiz.Subject.FOUNDATIONS,
            'topic': 'Vector Spaces',
            'description': "Concepts of subspaces, nullspace, and rank. Automatically graded.",
            'questions': [
                {
                    "question_order": 1,
                    "question_text": "To be a valid Subspace, a set of vectors must be closed under addition and ______.",
                    "model_answer": "scalar multiplication",
                    "accepted_answers": ["scalar multiplication", "multiplication by scalars", "multiplication"],
                    "explanation": "Linear combinations (c*v + d*w) must stay within the space."
                },
                {
                    "question_order": 2,
                    "question_text": "Which specific vector MUST be present in every subspace?",
                    "model_answer": "zero vector",
                    "accepted_answers": ["zero vector", "0 vector", "zero", "0", "(0,0)"],
                    "explanation": "If you multiply any vector by the scalar 0, you get the zero vector. If the origin isn't included, it's not a subspace."
                },
                {
                    "question_order": 3,
                    "question_text": "The Nullspace of a matrix A consists of all vectors x such that Ax = ______.",
                    "model_answer": "0",
                    "accepted_answers": ["0", "zero", "zero vector"],
                    "explanation": "The Nullspace is the solution set to the homogeneous equation."
                },
                {
                    "question_order": 4,
                    "question_text": "In the Reduced Row Echelon Form (R), the variables corresponding to columns WITHOUT pivots are called ______ variables.",
                    "model_answer": "free",
                    "accepted_answers": ["free", "free variables"],
                    "explanation": "We can assign any value to these variables to find the special solutions."
                },
                {
                    "question_order": 5,
                    "question_text": "If a matrix A has m rows and n columns, the Nullspace is a subspace of R to the power of ______.",
                    "model_answer": "n",
                    "accepted_answers": ["n", "columns", "col count"],
                    "explanation": "The vector x multiplies the rows, so x must have n components."
                },
                {
                    "question_order": 6,
                    "question_text": "The number of pivots in a matrix is called its ______.",
                    "model_answer": "rank",
                    "accepted_answers": ["rank", "r"],
                    "explanation": "The rank (r) measures the true dimension of the information in the matrix."
                },
                {
                    "question_order": 7,
                    "question_text": "Is the union of two subspaces (all vectors in S OR in T) usually a subspace? (Yes/No)",
                    "model_answer": "No",
                    "accepted_answers": ["No", "no", "false"],
                    "explanation": "Imagine two lines crossing. If you add a vector from line A and a vector from line B, the result is NOT on either line."
                },
                {
                    "question_order": 8,
                    "question_text": "To find the special solutions to Ax=0, we set one free variable to ______ and the others to 0, then solve.",
                    "model_answer": "1",
                    "accepted_answers": ["1", "one"],
                    "explanation": "This allows us to isolate the effect of each free variable."
                },
                {
                    "question_order": 9,
                    "question_text": "If rank r = n (number of cols), then the only vector in the nullspace is ______.",
                    "model_answer": "0",
                    "accepted_answers": ["0", "zero", "zero vector", "the zero vector"],
                    "explanation": "There are no free variables, so there are no non-zero solutions."
                },
                {
                    "question_order": 10,
                    "question_text": "The Column Space C(A) is a subspace of R^m, while the Nullspace N(A) is a subspace of ______.",
                    "model_answer": "R^n",
                    "accepted_answers": ["R^n", "Rn", "n dimensional space"],
                    "explanation": "C(A) lives in the output space; N(A) lives in the input space."
                }
            ]
        },
        {
            'title': 'Solvability & Basis',
            'type': Quiz.QuizType.THEORETICAL,
            'eval_method': Quiz.EvaluationMethod.AUTOMATED,
            'domain': Quiz.Domain.LINEAR_ALGEBRA,
            'subject': Quiz.Subject.FOUNDATIONS,
            'topic': 'Vector Spaces',
            'description': "Understanding basis vectors, dimension, and solvability conditions. Automatically graded.",
            'questions': [
                {
                    "question_order": 1,
                    "question_text": "The complete solution to Ax = b is written as x_particular + ______.",
                    "model_answer": "x_nullspace",
                    "accepted_answers": ["x_nullspace", "xn", "homogeneous solution", "x_n", "nullspace solution"],
                    "explanation": "The particular solution gets you to the solution plane; the nullspace solution lets you move around on that plane."
                },
                {
                    "question_order": 2,
                    "question_text": "Ax = b is solvable if and only if b lies in the ______ Space of A.",
                    "model_answer": "Column",
                    "accepted_answers": ["Column", "column", "Col", "C(A)"],
                    "explanation": "b must be a linear combination of the columns."
                },
                {
                    "question_order": 3,
                    "question_text": "A set of vectors is Linearly Independent if the only linear combination that gives the zero vector is when all scalars are ______.",
                    "model_answer": "0",
                    "accepted_answers": ["0", "zero"],
                    "explanation": "If c1*v1 + ... + cn*vn = 0 implies all c=0, they are independent."
                },
                {
                    "question_order": 4,
                    "question_text": "A 'Basis' for a vector space is a set of vectors that are linearly independent and ______ the space.",
                    "model_answer": "span",
                    "accepted_answers": ["span", "spans", "generate"],
                    "explanation": "A basis is a minimal generating set."
                },
                {
                    "question_order": 5,
                    "question_text": "The number of vectors in every basis of a vector space is the same. This number is called the ______ of the space.",
                    "model_answer": "dimension",
                    "accepted_answers": ["dimension", "dim"],
                    "explanation": "This is the definition of dimension."
                },
                {
                    "question_order": 6,
                    "question_text": "If a matrix A has full column rank (r = n), then Ax = b has either 0 or ______ solution(s).",
                    "model_answer": "1",
                    "accepted_answers": ["1", "one", "unique"],
                    "explanation": "There are no free variables to create infinite solutions."
                },
                {
                    "question_order": 7,
                    "question_text": "If a matrix A has full row rank (r = m), then Ax = b is solvable for ______ right-hand side b.",
                    "model_answer": "every",
                    "accepted_answers": ["every", "all", "any"],
                    "explanation": "The columns span the entire output space R^m."
                },
                {
                    "question_order": 8,
                    "question_text": "The columns of the Matrix A generally span the column space, but do they form a basis for it? (Yes/No)",
                    "model_answer": "No",
                    "accepted_answers": ["No", "no"],
                    "explanation": "They only form a basis if they are linearly independent. If there are dependent columns, they are redundant."
                },
                {
                    "question_order": 9,
                    "question_text": "In the reduced echelon form R, the columns containing the ______ form a basis for the column space of A.",
                    "model_answer": "pivots",
                    "accepted_answers": ["pivots", "pivot", "leading 1s"],
                    "explanation": "Note: You must pick the columns from the ORIGINAL matrix A, not R."
                },
                {
                    "question_order": 10,
                    "question_text": "If A is a 3x3 invertible matrix, what is the dimension of its Nullspace?",
                    "model_answer": "0",
                    "accepted_answers": ["0", "zero"],
                    "explanation": "An invertible matrix has rank 3. Dim(N(A)) = n - r = 3 - 3 = 0."
                }
            ]
        },
        {
            'title': 'The Four Subspaces (Conceptual)',
            'type': Quiz.QuizType.THEORETICAL,
            'eval_method': Quiz.EvaluationMethod.SELF_EVAL,
            'domain': Quiz.Domain.LINEAR_ALGEBRA,
            'subject': Quiz.Subject.FOUNDATIONS,
            'topic': 'Vector Spaces',
            'description': "Deep dive into Column Space, Nullspace, spanning, and independence.",
            'questions': [
                {
                    "question_order": 1,
                    "question_text": "Why does the general solution to $Ax=b$ equal $x_p + x_n$? Why can we add the nullspace vector?",
                    "model_answer": "Because $A(x_p + x_n) = Ax_p + Ax_n = b + 0 = b$. Adding a vector from the nullspace doesn't change the result of the multiplication, so it's still a valid solution.",
                    "accepted_answers": [],
                    "explanation": "This is why the solution set is a 'flat' (a shifted subspace)."
                },
                {
                    "question_order": 2,
                    "question_text": "Explain why row operations (elimination) change the Column Space but DO NOT change the Nullspace.",
                    "model_answer": "Elimination takes linear combinations of rows. This changes the columns (and thus the Column Space). However, the Nullspace is the set of $x$ such that $Ax=0$. Since row ops are just combining the equations, any $x$ that satisfied the original system still satisfies the new system.",
                    "accepted_answers": [],
                    "explanation": "Row ops preserve the relationship between the variables."
                },
                {
                    "question_order": 3,
                    "question_text": "Provide a geometric description of the solution to $Ax=b$ for a $3 \\times 3$ matrix of rank 2.",
                    "model_answer": "Since $r=2$, the nullspace is 1-dimensional (a line). The solution is a line in $\\mathbb{R}^3$ that does not pass through the origin (unless $b=0$). It is parallel to the nullspace line, shifted by the particular solution $x_p$.",
                    "accepted_answers": [],
                    "explanation": "Rank 2 means a plane of column space; n-r=1 means a line of nullspace."
                },
                {
                    "question_order": 4,
                    "question_text": "Why can't we have more basis vectors than the dimension of the space? (e.g. 4 basis vectors in $\\mathbb{R}^3$)",
                    "model_answer": "If you have more vectors than the dimension (n), they must be linearly dependent. At least one will be a combination of the others, so it's not a basis.",
                    "accepted_answers": [],
                    "explanation": "There are only 3 pivot positions available in $R^3$."
                },
                {
                    "question_order": 5,
                    "question_text": "Explain the difference between 'Spanning a Space' and 'Being a Basis for a Space'.",
                    "model_answer": "Spanning means you have *enough* vectors to cover the space (existence). Basis means you have enough vectors AND no extras (existence + uniqueness/independence).",
                    "accepted_answers": [],
                    "explanation": "A basis is a spanning set with no redundancy."
                },
                {
                    "question_order": 6,
                    "question_text": "How do we find the basis for the Column Space of $A$ using the reduced matrix $R$?",
                    "model_answer": "Identify the columns in $R$ that have pivots. Then, go back to the ORIGINAL matrix $A$ and pick the corresponding columns. Those columns form the basis.",
                    "accepted_answers": [],
                    "explanation": "Important: The columns of R span C(R), NOT C(A)."
                },
                {
                    "question_order": 7,
                    "question_text": "Why is the rank of a matrix the same as the dimension of its Column Space?",
                    "model_answer": "The rank is the number of pivots. The pivot columns form the basis of the Column Space. Therefore, the number of basis vectors (dimension) equals the rank.",
                    "accepted_answers": [],
                    "explanation": "Rank counts the number of independent columns."
                },
                {
                    "question_order": 8,
                    "question_text": "If $A$ is $5 \\times 7$ with rank 4, what is the dimension of the Nullspace?",
                    "model_answer": "$n - r = 7 - 4 = 3$. There are 3 free variables.",
                    "accepted_answers": [],
                    "explanation": "The logic is: Total variables - Pivot variables = Free variables."
                },
                {
                    "question_order": 9,
                    "question_text": "What is the 'Condition for Solvability' for $Ax=b$ in terms of the zero rows of the reduced matrix $R$?",
                    "model_answer": "If elimination produces a row of zeros on the left side (in $R$), the corresponding entry on the right side (in $d$) must also be zero. Otherwise, $0 = \\text{non-zero}$, which is impossible.",
                    "accepted_answers": [],
                    "explanation": "This algebraic condition confirms if $b$ is in the column space."
                },
                {
                    "question_order": 10,
                    "question_text": "Why is the vector space of all $3 \\times 3$ matrices having dimension 9?",
                    "model_answer": "Because we can treat the matrix as a long vector with 9 components. A basis would be 9 matrices, each with a 1 in a single spot and 0 elsewhere.",
                    "accepted_answers": [],
                    "explanation": "Vector spaces don't have to be arrows; they can be matrices or functions."
                }
            ]
        },
        {
            'title': 'Fundamental Theorem of Linear Algebra',
            'type': Quiz.QuizType.THEORETICAL,
            'eval_method': Quiz.EvaluationMethod.SELF_EVAL,
            'domain': Quiz.Domain.LINEAR_ALGEBRA,
            'subject': Quiz.Subject.FOUNDATIONS,
            'topic': 'Vector Spaces',
            'description': "Connecting dimensions, orthogonality, and the four subspaces.",
            'questions': [
                {
                    "question_order": 1,
                    "question_text": "State the Fundamental Theorem of Linear Algebra, Part 1 (Dimensions). List the 4 subspaces and their dimensions for an $m \\times n$ matrix of rank $r$.",
                    "model_answer": "Column Space C(A): r. Row Space C(A^T): r. Nullspace N(A): n-r. Left Nullspace N(A^T): m-r.",
                    "accepted_answers": [],
                    "explanation": "This shows the conservation of information. Row rank = Column rank."
                },
                {
                    "question_order": 2,
                    "question_text": "Why do the Row Space and the Column Space have the same dimension ($r$)?",
                    "model_answer": "Because row operations preserve the dependency relations. The number of independent rows equals the number of independent columns (the number of pivots).",
                    "accepted_answers": [],
                    "explanation": "This is non-obvious! A matrix with short fat rows has the same number of independent rows as independent columns."
                },
                {
                    "question_order": 3,
                    "question_text": "Explain the name 'Left Nullspace' for $N(A^T)$. Why 'Left'?",
                    "model_answer": "$N(A^T)$ contains vectors $y$ such that $A^T y = 0$. If we transpose this equation, we get $y^T A = 0^T$. Here, the vector $y$ multiplies $A$ on the LEFT.",
                    "accepted_answers": [],
                    "explanation": "It solves the row-combination problem."
                },
                {
                    "question_order": 4,
                    "question_text": "Why is the Nullspace perpendicular (orthogonal) to the Row Space? (Intuition check)",
                    "model_answer": "Since $Ax=0$, the dot product of every row of $A$ with $x$ is 0. If $x$ is orthogonal to every row, it is orthogonal to the whole Row Space (all combinations of rows).",
                    "accepted_answers": [],
                    "explanation": "Vectors in the nullspace are perpendicular to vectors in the row space."
                },
                {
                    "question_order": 5,
                    "question_text": "Describe the Left Nullspace in terms of Elimination and pivots.",
                    "model_answer": "The dimensions of the Left Nullspace ($m-r$) tell us how many rows of zeros appear in the reduced matrix $R$ (or $U$). These zero rows represent dependencies among the original rows.",
                    "accepted_answers": [],
                    "explanation": "Each zero row in U comes from a specific combination of rows in A."
                },
                {
                    "question_order": 6,
                    "question_text": "If $A$ is a $3 \\times 4$ matrix, what is the largest possible rank it can have? In that case, what is the dimension of the Nullspace?",
                    "model_answer": "Max rank is 3 (limited by rows). If $r=3$, then dim $N(A) = 4 - 3 = 1$.",
                    "accepted_answers": [],
                    "explanation": "Rank cannot exceed min(m, n)."
                },
                {
                    "question_order": 7,
                    "question_text": "Draw or describe the 'Big Picture' diagram. Where does the vector $x$ live? Where does $Ax$ live?",
                    "model_answer": "$x$ lives in $\\mathbb{R}^n$ (composed of Row Space + Nullspace). $Ax$ lives in $\\mathbb{R}^m$ (composed of Column Space + Left Nullspace). The matrix maps the Row Space to the Column Space.",
                    "accepted_answers": [],
                    "explanation": "This mapping is invertible between the Row Space and Column Space."
                },
                {
                    "question_order": 8,
                    "question_text": "Why do we say 'Rank is 1' matrices are the building blocks of all matrices?",
                    "model_answer": "Every rank $r$ matrix can be written as the sum of $r$ rank-1 matrices. (e.g., using Singular Value Decomposition or CR factorization).",
                    "accepted_answers": [],
                    "explanation": "A rank 1 matrix is just a column times a row."
                },
                {
                    "question_order": 9,
                    "question_text": "If $Ax=b$ has a solution, $b$ is in the Column Space. If it has NO solution, $b$ has a component in which other subspace?",
                    "model_answer": "The Left Nullspace ($N(A^T)$).",
                    "accepted_answers": [],
                    "explanation": "This is crucial for Least Squares approximations in Chapter 4."
                },
                {
                    "question_order": 10,
                    "question_text": "What is the dimension of the vector space of all symmetric $3 \\times 3$ matrices?",
                    "model_answer": "6. You can choose the 3 diagonal entries and the 3 upper-triangle entries freely. The lower entries are forced by symmetry.",
                    "accepted_answers": [],
                    "explanation": "3 (diagonal) + 3 (off-diagonal) = 6."
                }
            ]
        },
        {
            'title': 'Orthogonal Subspaces',
            'type': Quiz.QuizType.THEORETICAL,
            'eval_method': Quiz.EvaluationMethod.AUTOMATED,
            'domain': Quiz.Domain.LINEAR_ALGEBRA,
            'subject': Quiz.Subject.GEOMETRY_AND_VOLUME,
            'topic': 'Orthogonality',
            'description': "Ch 4.1: Orthogonality of the Four Fundamental Subspaces.",
            'questions': [
                {
                    "question_order": 1,
                    "question_text": "Two vectors $v$ and $w$ are orthogonal if their _______ product is zero.",
                    "model_answer": "dot",
                    "accepted_answers": ["dot", "inner", "scalar"],
                    "explanation": "Geometrically, $v^T w = 0$ means the angle between them is 90 degrees."
                },
                {
                    "question_order": 2,
                    "question_text": "The Nullspace $N(A)$ is the orthogonal complement of the _______ Space.",
                    "model_answer": "Row",
                    "accepted_answers": ["Row", "row", "Row Space", "row space", "C(A^T)"],
                    "explanation": "Every vector $x$ in the nullspace satisfies $Ax = 0$, meaning $x$ has a zero dot product with every row of $A$."
                },
                {
                    "question_order": 3,
                    "question_text": "The Left Nullspace $N(A^T)$ is the orthogonal complement of the _______ Space.",
                    "model_answer": "Column",
                    "accepted_answers": ["Column", "column", "Column Space", "column space", "C(A)"],
                    "explanation": " These two spaces exist in $\\mathbb{R}^m$ and are perpendicular to each other."
                },
                {
                    "question_order": 4,
                    "question_text": "If subspace $V$ and subspace $W$ are orthogonal complements in $\\mathbb{R}^n$, then $\\dim(V) + \\dim(W) = $ _______.",
                    "model_answer": "n",
                    "accepted_answers": ["n", "N"],
                    "explanation": "Their dimensions perfectly add up to the dimension of the whole space (e.g., a 1D line and a 2D plane in 3D space)."
                },
                {
                    "question_order": 5,
                    "question_text": "The squared length of a vector $v$, denoted as $\\|v\\|^2$, is algebraically calculated as $v^T$ times _______.",
                    "model_answer": "v",
                    "accepted_answers": ["v"],
                    "explanation": "This is the Pythagorean theorem in $n$-dimensions: $v_1^2 + v_2^2 + ... + v_n^2$."
                },
                {
                    "question_order": 6,
                    "question_text": "Review: If a $4 \\times 5$ matrix has a rank of $3$, what is the dimension of its Nullspace?",
                    "model_answer": "2",
                    "accepted_answers": ["2", "two"],
                    "explanation": "Dimension of $N(A) = n - r = 5 - 3 = 2$."
                },
                {
                    "question_order": 7,
                    "question_text": "If $x$ is in the nullspace of $A$ and $y$ is in the row space of $A$, then $x^T y = $ _______.",
                    "model_answer": "0",
                    "accepted_answers": ["0", "zero"],
                    "explanation": "Because they are orthogonal complements, any vector in one is perpendicular to any vector in the other."
                },
                {
                    "question_order": 8,
                    "question_text": "Review: Matrix multiplication $AB$ is only possible if the number of columns of $A$ equals the number of _______ of $B$.",
                    "model_answer": "rows",
                    "accepted_answers": ["rows"],
                    "explanation": "Inner dimensions must match: $(m \\times n) \\times (n \\times p)$."
                },
                {
                    "question_order": 9,
                    "question_text": "True or False: The zero vector is orthogonal to every vector in $\\mathbb{R}^n$.",
                    "model_answer": "True",
                    "accepted_answers": ["True", "true", "T", "t", "yes", "Yes"],
                    "explanation": "$0^T v = 0$ for any vector $v$."
                },
                {
                    "question_order": 10,
                    "question_text": "If $A$ is an $m \\times n$ matrix, its row space lives in $\\mathbb{R}^n$, and its column space lives in $\\mathbb{R}^?$. (Fill in the missing dimension)",
                    "model_answer": "m",
                    "accepted_answers": ["m", "M"],
                    "explanation": "The columns have $m$ components (one for each row)."
                }
            ]
        },
        {
            'title': 'Projections & Least Squares Fundamentals',
            'type': Quiz.QuizType.THEORETICAL,
            'eval_method': Quiz.EvaluationMethod.AUTOMATED,
            'domain': Quiz.Domain.LINEAR_ALGEBRA,
            'subject': Quiz.Subject.GEOMETRY_AND_VOLUME,
            'topic': 'Orthogonality',
            'description': "Ch 4.2-4.3: Projection matrices and the normal equations.",
            'questions': [
                {
                    "question_order": 1,
                    "question_text": "The error vector $e = b - p$ is _______ to the subspace we are projecting onto.",
                    "model_answer": "orthogonal",
                    "accepted_answers": ["orthogonal", "perpendicular", "normal"],
                    "explanation": " The shortest distance to a subspace is always the perpendicular line."
                },
                {
                    "question_order": 2,
                    "question_text": "A projection matrix $P$ has the property $P^2 = $ _______.",
                    "model_answer": "P",
                    "accepted_answers": ["P", "p"],
                    "explanation": "Projecting a vector a second time changes nothing. It is already in the subspace."
                },
                {
                    "question_order": 3,
                    "question_text": "Is a standard projection matrix $P$ always symmetric? (Yes/No)",
                    "model_answer": "Yes",
                    "accepted_answers": ["Yes", "yes", "true", "True"],
                    "explanation": "Orthogonal projections always result in symmetric matrices: $P^T = P$."
                },
                {
                    "question_order": 4,
                    "question_text": "The normal equations for solving least squares are $A^T A \\hat{x} = $ _______.",
                    "model_answer": "A^T b",
                    "accepted_answers": ["A^T b", "A^Tb", "A transpose b"],
                    "explanation": "We multiply both sides of $Ax = b$ by $A^T$ to move the problem into the row space."
                },
                {
                    "question_order": 5,
                    "question_text": "The matrix $A^T A$ is invertible if and only if $A$ has independent _______.",
                    "model_answer": "columns",
                    "accepted_answers": ["columns", "cols"],
                    "explanation": "Independent columns mean the nullspace of $A$ is just the zero vector, which guarantees $A^T A$ is non-singular."
                },
                {
                    "question_order": 6,
                    "question_text": "The projection matrix onto the entire space $\\mathbb{R}^n$ is the _______ matrix.",
                    "model_answer": "Identity",
                    "accepted_answers": ["Identity", "identity", "I"],
                    "explanation": "If the subspace is the whole space, every vector is already perfectly 'projected'."
                },
                {
                    "question_order": 7,
                    "question_text": "If $b$ is already in the column space of $A$, its projection $p$ onto $C(A)$ is exactly _______.",
                    "model_answer": "b",
                    "accepted_answers": ["b"],
                    "explanation": "There is no error ($e=0$) if the vector is already in the subspace."
                },
                {
                    "question_order": 8,
                    "question_text": "Review: The inverse of a matrix product $(AB)$ is equal to _______.",
                    "model_answer": "B^-1 A^-1",
                    "accepted_answers": ["B^-1 A^-1", "B^-1A^-1", "B inverse A inverse"],
                    "explanation": "The 'shoes and socks' rule: you must reverse the order to undo the operations."
                },
                {
                    "question_order": 9,
                    "question_text": "If $P$ is the projection matrix onto the column space, the projection onto the left nullspace is given by $( _______ - P)$.",
                    "model_answer": "I",
                    "accepted_answers": ["I", "Identity", "Identity matrix"],
                    "explanation": "Since the column space and left nullspace are orthogonal complements, $p + e = b$, so $Pb + (I-P)b = b$."
                },
                {
                    "question_order": 10,
                    "question_text": "In the 1D projection formula $p = x a$, the scalar $x$ is calculated as $(a^T b)$ divided by _______.",
                    "model_answer": "a^T a",
                    "accepted_answers": ["a^T a", "a^Ta", "a transpose a", "length of a squared", "norm of a squared"],
                    "explanation": "This scales the vector $a$ by the ratio of the dot product to the length squared of $a$."
                }
            ]
        },
        {
            'title': 'Least Squares & Best Fit',
            'type': Quiz.QuizType.THEORETICAL,
            'eval_method': Quiz.EvaluationMethod.SELF_EVAL,
            'domain': Quiz.Domain.LINEAR_ALGEBRA,
            'subject': Quiz.Subject.GEOMETRY_AND_VOLUME,
            'topic': 'Orthogonality',
            'description': "Ch 4.3: The deep concepts behind fitting data to linear models.",
            'questions': [
                {
                    "question_order": 1,
                    "question_text": "Explain algebraically *why* we multiply both sides of $Ax = b$ by $A^T$ to find the least squares solution.",
                    "model_answer": "The error vector $e = b - A\\hat{x}$ must be orthogonal to the column space of $A$. This means every column of $A$ has a zero dot product with $e$. Algebraically, $A^T e = 0$, so $A^T (b - A\\hat{x}) = 0$, which rearranges to $A^T A \\hat{x} = A^T b$.",
                    "accepted_answers": [],
                    "explanation": "This turns an unsolvable system into a solvable one by projecting the problem into the row space."
                },
                {
                    "question_order": 2,
                    "question_text": "When fitting a line $y = C + Dt$ to 3 data points, what do the columns of the matrix $A$ represent?",
                    "model_answer": "Column 1 is all 1s (representing the constant intercept $C$). Column 2 contains the time variables $t_1, t_2, t_3$ (representing the slope multiplier $D$).",
                    "accepted_answers": [],
                    "explanation": "The vector $\\hat{x}$ will contain the optimal values for $C$ and $D$."
                },
                {
                    "question_order": 3,
                    "question_text": "Geometrically, what does the least squares solution $\\hat{x}$ represent when $Ax=b$ has no exact solution?",
                    "model_answer": "It finds the combination of columns of $A$ that gets as close as geometrically possible to $b$. The result, $A\\hat{x}$, is the exact orthogonal projection $p$ of the vector $b$ onto the column space.",
                    "accepted_answers": [],
                    "explanation": "It minimizes the distance $\\|b - Ax\\|^2$."
                },
                {
                    "question_order": 4,
                    "question_text": "What happens to the general projection formula $P = A(A^T A)^{-1}A^T$ if $A$ is a square, invertible matrix?",
                    "model_answer": "It simplifies to the Identity matrix $I$. If $A$ is invertible, its columns already span the entire space $\\mathbb{R}^n$. Projecting a vector onto the entire space just returns the vector itself ($Pb = b$).",
                    "accepted_answers": [],
                    "explanation": "Algebraically: $A(A^{-1}(A^T)^{-1})A^T = (A A^{-1})((A^T)^{-1} A^T) = I \\cdot I = I$."
                },
                {
                    "question_order": 5,
                    "question_text": "Explain why the matrix $A^T A$ is always guaranteed to be a symmetric matrix.",
                    "model_answer": "A matrix is symmetric if it equals its own transpose. Taking the transpose of the product: $(A^T A)^T = A^T (A^T)^T = A^T A$. It returns exactly to itself.",
                    "accepted_answers": [],
                    "explanation": "This symmetric property is why normal equations are computationally well-behaved."
                },
                {
                    "question_order": 6,
                    "question_text": "If the columns of $A$ are completely orthogonal to each other, what special form does $A^T A$ take?",
                    "model_answer": "It becomes a diagonal matrix. The off-diagonal entries are the dot products of different columns, which are all zero. The diagonal entries are the squared lengths of each column.",
                    "accepted_answers": [],
                    "explanation": "This makes the least squares equations uncoupled—you can solve for each variable independently!"
                },
                {
                    "question_order": 7,
                    "question_text": "Review: If a matrix $A$ is singular, why can't we simply use $A^{-1}$ to solve $Ax=b$?",
                    "model_answer": "A singular matrix collapses space (determinant is 0). Multiple inputs map to the same output, so the mapping is not 1-to-1, and you cannot reverse it. $A^{-1}$ literally does not exist.",
                    "accepted_answers": [],
                    "explanation": "You can't un-crush a crushed dimension."
                },
                {
                    "question_order": 8,
                    "question_text": "Why do we minimize the *square* of the errors (Least Squares) rather than just the absolute errors?",
                    "model_answer": "1) Squaring makes the calculus easy because derivatives of squares are linear. 2) It connects directly to geometry and the Pythagorean theorem ($c^2 = a^2 + b^2$), defining orthogonal projections.",
                    "accepted_answers": [],
                    "explanation": "Absolute value functions have sharp corners and are hard to differentiate."
                },
                {
                    "question_order": 9,
                    "question_text": "If the error vector $e$ calculated in least squares is exactly the zero vector, what does that tell you about the original vector $b$?",
                    "model_answer": "It means $b$ was already perfectly inside the column space of $A$. The original system $Ax=b$ actually had an exact solution, and no 'approximation' was necessary.",
                    "accepted_answers": [],
                    "explanation": "$p + 0 = b$, meaning $p = b$."
                },
                {
                    "question_order": 10,
                    "question_text": "Describe the projection matrix onto the Left Nullspace of $A$, given that we already know $P$ (the projection matrix onto the Column Space).",
                    "model_answer": "It is simply $I - P$. Since the Column Space and Left Nullspace are orthogonal complements that make up the whole space $\\mathbb{R}^m$, any vector $b$ splits perfectly into $p$ (in the column space) and $e$ (in the left nullspace).",
                    "accepted_answers": [],
                    "explanation": "$e = b - Pb = (I - P)b$."
                }
            ]
        },
        {
            'title': 'Gram-Schmidt & Orthogonal Matrices',
            'type': Quiz.QuizType.THEORETICAL,
            'eval_method': Quiz.EvaluationMethod.SELF_EVAL,
            'domain': Quiz.Domain.LINEAR_ALGEBRA,
            'subject': Quiz.Subject.GEOMETRY_AND_VOLUME,
            'topic': 'Orthogonality',
            'description': "Ch 4.4: Creating orthonormal bases and the QR factorization.",
            'questions': [
                {
                    "question_order": 1,
                    "question_text": "What defines an 'orthogonal matrix' $Q$? Give the defining equation for its transpose/inverse.",
                    "model_answer": "A square matrix $Q$ is orthogonal if its columns are orthonormal (length 1, mutually perpendicular). Because of this, $Q^T Q = I$, which means its transpose is exactly its inverse: $Q^T = Q^{-1}$.",
                    "accepted_answers": [],
                    "explanation": "This makes calculating the inverse trivially easy."
                },
                {
                    "question_order": 2,
                    "question_text": "Explain the conceptual goal of the Gram-Schmidt process in your own words.",
                    "model_answer": "It takes a set of skewed, independent basis vectors and straightens them out into an orthonormal basis. It does this by taking each new vector, projecting it onto the already-straightened vectors, and subtracting that projection to leave only the pure, orthogonal 'new' direction.",
                    "accepted_answers": [],
                    "explanation": "It systematically scrapes away the overlap between vectors."
                },
                {
                    "question_order": 3,
                    "question_text": "In Gram-Schmidt, how do we find the second orthogonal vector $B$ from the original vectors $a$ and $b$?",
                    "model_answer": "$B = b - p$, where $p$ is the projection of $b$ onto the first vector $a$. Specifically, $B = b - \\frac{a^T b}{a^T a} a$.",
                    "accepted_answers": [],
                    "explanation": "We subtract the part of $b$ that goes in the direction of $a$."
                },
                {
                    "question_order": 4,
                    "question_text": "Why is calculating the projection matrix $P$ onto a subspace incredibly easy if the basis vectors of that matrix $Q$ are orthonormal?",
                    "model_answer": "The ugly formula $P = A(A^T A)^{-1}A^T$ simplifies beautifully. Since $Q^T Q = I$, the inverse part disappears, and the projection matrix is simply $P = Q Q^T$.",
                    "accepted_answers": [],
                    "explanation": "Orthonormal bases eliminate all the cross-talk between dimensions."
                },
                {
                    "question_order": 5,
                    "question_text": "What is the $QR$ factorization?",
                    "model_answer": "It factors a matrix $A$ into an orthogonal matrix $Q$ (containing the orthonormal vectors from Gram-Schmidt) and an upper triangular matrix $R$ (which records the dot products/coefficients used to do the orthogonalizing).",
                    "accepted_answers": [],
                    "explanation": "Like $A=LU$ simplifies solving equations, $A=QR$ simplifies least squares."
                },
                {
                    "question_order": 6,
                    "question_text": "Why does multiplying a vector $x$ by an orthogonal matrix $Q$ preserve its length perfectly?",
                    "model_answer": "Algebraically: $\\|Qx\\|^2 = (Qx)^T(Qx) = x^T Q^T Q x = x^T I x = x^T x = \\|x\\|^2$. Geometrically: $Q$ represents rigid transformations like rotations, which don't stretch space.",
                    "accepted_answers": [],
                    "explanation": "Orthogonal matrices are rigid."
                },
                {
                    "question_order": 7,
                    "question_text": "Review: What does it mean conceptually for a vector to be in the Nullspace of $A$?",
                    "model_answer": "It means the vector is a specific set of weights that linearly combines the columns of $A$ to perfectly cancel each other out, resulting in the zero vector. It indicates linear dependence among the columns.",
                    "accepted_answers": [],
                    "explanation": "If the columns are independent, only the zero vector does this."
                },
                {
                    "question_order": 8,
                    "question_text": "If $Q$ is a rectangular matrix (taller than it is wide) with orthonormal columns, is the product $QQ^T$ equal to the Identity matrix $I$?",
                    "model_answer": "No. $Q^T Q = I$, but $QQ^T$ is the projection matrix $P$ onto the column space of $Q$. It only equals $I$ if $Q$ is a square matrix (meaning it spans the whole space).",
                    "accepted_answers": [],
                    "explanation": "Order matters! $QQ^T$ is $m \\times m$, but only has rank $n$."
                },
                {
                    "question_order": 9,
                    "question_text": "How does the Gram-Schmidt factorization ($A=QR$) compare conceptually to Gaussian Elimination ($A=LU$)?",
                    "model_answer": "Both systematically strip away parts of the matrix to reveal its structure. $LU$ makes $A$ lower triangular by subtracting rows to get zeros. $QR$ makes $A$ orthogonal by subtracting projections to get 90-degree angles.",
                    "accepted_answers": [],
                    "explanation": "They are the two foundational factorizations in linear algebra."
                },
                {
                    "question_order": 10,
                    "question_text": "In $A=QR$, why is the matrix $R$ always upper triangular?",
                    "model_answer": "Because of the order of Gram-Schmidt. The $k$-th vector $q_k$ is formed only using the first $k$ vectors of $A$. Later vectors in $Q$ do not contribute to earlier vectors in $A$, meaning all entries below the diagonal in $R$ are zero.",
                    "accepted_answers": [],
                    "explanation": "Vector 1 only depends on Vector 1. Vector 2 depends on 1 and 2, etc."
                }
            ]
        }
    ]
