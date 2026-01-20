from django.db import models
from django.conf import settings

class Quiz(models.Model):
    class Domain(models.TextChoices):
        CALCULUS = 'Calculus', 'Calculus'
        LINEAR_ALGEBRA = 'Linear Algebra', 'Linear Algebra'
        STATISTICS = 'Statistics', 'Statistics'

    class Subject(models.TextChoices):
        CALCULUS_1 = 'Calculus I', 'Calculus I'
        CALCULUS_2 = 'Calculus II', 'Calculus II'
        CALCULUS_3 = 'Calculus III', 'Calculus III'
        
        PROBABILITY = 'Probability', 'Probability'

        MECHANICS = 'Mechanics', 'Mechanics'
        # Focus: The basics of how matrices work and how to solve systems.

    class QuizType(models.TextChoices):
        PRACTICAL = 'Practical', 'Practical'
        THEORETICAL = 'Theoretical', 'Theoretical'
        REVISION = 'Revision', 'Revision'

    class EvaluationMethod(models.TextChoices):
        SELF_EVAL = 'Self-Eval', 'Self-Eval'
        AUTOMATED = 'Automated', 'Automated'

    quiz_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    domain = models.CharField(max_length=100, choices=Domain.choices)
    subject = models.CharField(max_length=100, choices=Subject.choices)
    topic = models.CharField(max_length=100)
    quiz_type = models.CharField(max_length=50, choices=QuizType.choices)
    evaluation_method = models.CharField(max_length=50, choices=EvaluationMethod.choices)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'quizzes'

class QuizAttempt(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.IntegerField()
    percentage = models.FloatField()
    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-completed_at']

    def __str__(self):
        return f"{self.user} - {self.quiz.title}"

class Question(models.Model):
    question_id = models.AutoField(primary_key=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question_text = models.TextField()
    model_answer = models.TextField()
    accepted_answers = models.JSONField(default=list, blank=True)
    explanation = models.TextField(blank=True, null=True, help_text="Process/Explanation for the solution")
    question_order = models.IntegerField()

    class Meta:
        db_table = 'questions'

class TopicState(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    topic = models.CharField(max_length=100)
    current_level = models.IntegerField(default=0)  # 0=Ready for Rev1, 1=Rev1 Done/Ready for Rev2, etc.
    last_reviewed_at = models.DateTimeField(null=True, blank=True)
    next_review_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ['user', 'topic']
