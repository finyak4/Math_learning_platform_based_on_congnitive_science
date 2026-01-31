from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Quiz, Question, QuizAttempt, TopicState
from django.utils import timezone
from datetime import timedelta
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

from django.db.models import Count

def quiz_list(request, subject_slug='calculus'):
    # Separate standard quizzes and revision quizzes based on title
    all_quizzes = Quiz.objects.annotate(question_count=Count('question')).order_by('created_at')

    # Domain Filtering
    current_domain = None
    if subject_slug == 'linear-algebra':
        current_domain = Quiz.Domain.LINEAR_ALGEBRA
        all_quizzes = all_quizzes.filter(domain=Quiz.Domain.LINEAR_ALGEBRA)
    elif subject_slug == 'statistics':
        current_domain = Quiz.Domain.STATISTICS
        all_quizzes = all_quizzes.filter(domain=Quiz.Domain.STATISTICS)
    else:
        # Default to Calculus
        current_domain = Quiz.Domain.CALCULUS
        all_quizzes = all_quizzes.filter(domain=Quiz.Domain.CALCULUS)

    # 1. Standard Quizzes
    quizzes = all_quizzes.exclude(title__icontains='Revision')

    # Exclude quizzes the user has already taken if they are authenticated
    if request.user.is_authenticated:
        quizzes = quizzes.exclude(quizattempt__user=request.user)
    
    # Filters (Subject, Type, Eval)
    subject_filter = request.GET.get('subject')
    type_filter = request.GET.get('quiz_type')
    eval_filter = request.GET.get('evaluation_method')
    
    if subject_filter:
        quizzes = quizzes.filter(subject=subject_filter)
    if type_filter:
        quizzes = quizzes.filter(quiz_type=type_filter)
    if eval_filter:
        quizzes = quizzes.filter(evaluation_method=eval_filter)

    # 2. SRS / Revision Quizzes Logic
    srs_cards = []
    if request.user.is_authenticated:
        # Get all TopicStates for the user
        topic_states = TopicState.objects.filter(user=request.user)
        
        for state in topic_states:
            # Determine which revision is next based on current_level
            target_level = state.current_level + 1
            if target_level > 4:
                continue # All done for this proof of concept

            # Find the specific revision quiz
            # Format: "{Topic}: Revision {Level}..."
            # Ensure we only pick revision quizzes from the current domain
            rev_quiz = all_quizzes.filter(
                topic=state.topic, 
                title__icontains=f'Revision {target_level}'
            ).first()

            if rev_quiz:
                is_locked = True
                unlock_date = state.next_review_at
                
                # Check if it's time to review
                if unlock_date and timezone.now() >= unlock_date:
                    is_locked = False
                
                srs_cards.append({
                    'quiz': rev_quiz,
                    'is_locked': is_locked,
                    'unlock_date': unlock_date,
                    'topic': state.topic
                })

    # Filter Subject Choices based on Domain
    visible_subjects = []
    if subject_slug == 'linear-algebra':
        visible_subjects = [
            (Quiz.Subject.MECHANICS, 'Mechanics')
        ]
    elif subject_slug == 'statistics':
        visible_subjects = [
            (Quiz.Subject.PROBABILITY, 'Probability')
        ]
    else:
        visible_subjects = [
            (Quiz.Subject.CALCULUS_1, 'Calculus 1'),
            (Quiz.Subject.CALCULUS_2, 'Calculus 2'),
            (Quiz.Subject.CALCULUS_3, 'Calculus 3'),
        ]

    context = {
        'quizzes': quizzes,
        'srs_cards': srs_cards, # Pass SRS data
        'subjects': visible_subjects,
        'quiz_types': Quiz.QuizType.choices,
        'eval_methods': Quiz.EvaluationMethod.choices,
        
        # Pass current filters back to template
        'current_subject': subject_filter,
        'current_type': type_filter,
        'current_eval': eval_filter,
        'active_tab': subject_slug, # 'calculus' or 'linear-algebra'
    }
    return render(request, 'quizzes/quiz_list.html', context)

@login_required
def take_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    
    # Check if already attempted
    if QuizAttempt.objects.filter(user=request.user, quiz=quiz).exists():
        # Redirect to results or profile (for now, simply redirect to list)
        return redirect('quizzes:quiz_list')

    # Get questions ordered by sequence
    questions = quiz.question_set.all().order_by('question_order')
    
    context = {
        'quiz': quiz,
        'questions': questions,
    }

@login_required
def submit_quiz(request, quiz_id):
    if request.method != 'POST':
        return redirect('quizzes:take_quiz', quiz_id=quiz_id)
        
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    questions = quiz.question_set.all().order_by('question_order')
    
    score = 0
    total = questions.count()
    
    for q in questions:
        # Assuming input name is 'answer_QUESTIONID' or similar?
        # Let's check quiz_take.html? No time. Standardize on question_{id}
        user_answer = request.POST.get(f'question_{q.question_id}')
        
        if user_answer:
            # Check against model answer / accepted answers
            candidates = [q.model_answer] + (q.accepted_answers if q.accepted_answers else [])
            if is_similar(user_answer, candidates):
                 score += 1
    
    percentage = (score / total) * 100 if total > 0 else 0
    
    # Save Attempt
    QuizAttempt.objects.create(
        user=request.user,
        quiz=quiz,
        score=score,
        percentage=percentage
    )
    
    # Render Result
    context = {
        'quiz': quiz,
        'score': score,
        'total': total,
        'percentage': percentage,
        'questions': questions # Might be useful for review
    }
    return render(request, 'quizzes/quiz_result.html', context)

