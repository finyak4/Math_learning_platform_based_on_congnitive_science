import os
import django
from django.utils import timezone
from datetime import timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from quizzes.models import Quiz, TopicState, QuizAttempt
from django.db.models import Max

def backfill():
    print("Starting SRS Backfill...")
    
    # group attempts by user and topic
    attempts = QuizAttempt.objects.values('user', 'quiz__topic').annotate(latest_attempt=Max('completed_at'))
    
    count = 0
    for entry in attempts:
        user_id = entry['user']
        topic = entry['quiz__topic']
        last_date = entry['latest_attempt']
        
        # We only care about standard quizzes for initialization (not Revisions, which supposedly don't exist yet)
        if 'Revision' in topic: 
            continue

        # Get or Create SRS State
        state, created = TopicState.objects.get_or_create(
            user_id=user_id, 
            topic=topic,
            defaults={
                'current_level': 0,
                'last_reviewed_at': last_date
            }
        )
        
        if created:
            # Set next review time based on when they took the quiz
            # If they took it > 1 day ago, it should be reviewable now.
            state.next_review_at = last_date + timedelta(days=1)
            state.save()
            print(f"Initialized SRS for User {user_id} - Topic '{topic}'. Next Review: {state.next_review_at}")
            count += 1
        else:
             print(f"SRS State already exists for User {user_id} - Topic '{topic}'.")

    print(f"Backfill complete. Created {count} TopicState records.")

if __name__ == '__main__':
    backfill()
