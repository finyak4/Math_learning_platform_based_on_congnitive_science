from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Quiz, Question, QuizAttempt
import difflib

def is_similar(user_input, accepted_strings):
    """
    Checks if user_input is similar to any string in accepted_strings.
    Criteria: Exact match OR Levenshtein distance <= 1 OR Similarity ratio >= 0.9
    """
    s1 = user_input.lower().strip()
    
    for s2_raw in accepted_strings:
        s2 = s2_raw.lower().strip()
        if s1 == s2:
            return True
            
        # Check similarity ratio (covers simple typos and >90% similarity)
        matcher = difflib.SequenceMatcher(None, s1, s2)
        if matcher.ratio() >= 0.9:
            return True
            
        # Check Levenshtein distance roughly for short words where 90% is too strict
        # (e.g. "teh" vs "the" is 1 edit but ratio is 0.66)
        # For simplicity, we can rely on difflib's get_close_matches or implement simple distance
        # Custom simple distance check for length difference <= 1
        if abs(len(s1) - len(s2)) <= 1:
            # Check for single char substitution or simple transposition
            diff_count = 0
            for c1, c2 in zip(s1, s2):
                if c1 != c2:
                    diff_count += 1
            if diff_count <= 1: 
                 return True

    return False

def quiz_list(request):
    quizzes = Quiz.objects.all().order_by('-created_at')

    # Exclude quizzes the user has already taken if they are authenticated
    if request.user.is_authenticated:
        quizzes = quizzes.exclude(quizattempt__user=request.user)
    
    # Filters
    subject_filter = request.GET.get('subject')
    type_filter = request.GET.get('quiz_type')
    eval_filter = request.GET.get('evaluation_method')
    
    if subject_filter:
        quizzes = quizzes.filter(subject=subject_filter)
    if type_filter:
        quizzes = quizzes.filter(quiz_type=type_filter)
    if eval_filter:
        quizzes = quizzes.filter(evaluation_method=eval_filter)

    context = {
        'quizzes': quizzes,
        'subjects': Quiz.Subject.choices,
        'quiz_types': Quiz.QuizType.choices,
        'eval_methods': Quiz.EvaluationMethod.choices,
        
        # Pass current filters back to template
        'current_subject': subject_filter,
        'current_type': type_filter,
        'current_eval': eval_filter,
    }
    return render(request, 'quizzes/quiz_list.html', context)

@login_required
def take_quiz(request, quiz_id):
    # Double check if user already took this quiz
    if QuizAttempt.objects.filter(user=request.user, quiz_id=quiz_id).exists():
        # Redirect to results or profile (for now, simply redirect to list)
        return redirect('quiz_list')

    quiz = get_object_or_404(Quiz, pk=quiz_id)
    questions = quiz.question_set.order_by('question_order')
    return render(request, 'quizzes/quiz_take.html', {'quiz': quiz, 'questions': questions})

@login_required
def submit_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    
    # Check if already taken
    if QuizAttempt.objects.filter(user=request.user, quiz=quiz).exists():
        return redirect('quiz_list')

    questions = quiz.question_set.order_by('question_order')

    if request.method == 'POST':
        score = 0
        total_questions = questions.count()
        results = []

        if quiz.evaluation_method == Quiz.EvaluationMethod.AUTOMATED:
            for question in questions:
                user_answer = request.POST.get(f'question_{question.question_id}', '').strip()
                is_correct = False
                
                # Check against accepted answers using fuzzy matching
                if is_similar(user_answer, question.accepted_answers):
                    is_correct = True
                    score += 1
                
                results.append({
                    'question': question,
                    'user_answer': user_answer,
                    'is_correct': is_correct,
                    'accepted_answers': question.accepted_answers
                })
            
            percentage = (score / total_questions) * 100 if total_questions > 0 else 0

            # Save Attempt
            QuizAttempt.objects.create(
                user=request.user,
                quiz=quiz,
                score=score,
                percentage=percentage
            )

            return render(request, 'quizzes/quiz_result.html', {
                'quiz': quiz,
                'score': score,
                'total_questions': total_questions,
                'percentage': percentage,
                'results': results
            })

        elif quiz.evaluation_method == Quiz.EvaluationMethod.SELF_EVAL:
            # First step of Self-Eval: Show user their answers vs model answers
            # If this is the "final" submit from the self-eval page
            if 'final_submit' in request.POST:
                 # Calculate score based on user's self-evaluation checkboxes
                 measured_score = 0
                 for question in questions:
                     if request.POST.get(f'correct_{question.question_id}') == 'on':
                         measured_score += 1
                 
                 percentage = (measured_score / total_questions) * 100 if total_questions > 0 else 0
                 
                 # Save Attempt
                 QuizAttempt.objects.create(
                    user=request.user,
                    quiz=quiz,
                    score=measured_score,
                    percentage=percentage
                 )

                 return render(request, 'quizzes/quiz_result.html', {
                    'quiz': quiz,
                    'score': measured_score,
                    'total_questions': total_questions,
                    'percentage': percentage,
                    'is_self_eval': True
                })

            # Otherwise, render the self-eval page
            user_answers = {}
            for question in questions:
                user_answers[question.question_id] = request.POST.get(f'question_{question.question_id}', '')
            
            return render(request, 'quizzes/quiz_self_eval.html', {
                'quiz': quiz,
                'questions': questions,
                'user_answers': user_answers
            })

    return redirect('take_quiz', quiz_id=quiz_id)
