from django.db import models
from django.conf import settings

class Quiz(models.Model):
    class Subject(models.TextChoices):
        CALCULUS_1 = 'Calculus I', 'Calculus I'
        CALCULUS_2 = 'Calculus II', 'Calculus II'
        CALCULUS_3 = 'Calculus III', 'Calculus III'

    class QuizType(models.TextChoices):
        PRACTICAL = 'Practical', 'Practical'
        THEORETICAL = 'Theoretical', 'Theoretical'

    class EvaluationMethod(models.TextChoices):
        SELF_EVAL = 'Self-Eval', 'Self-Eval'
        AUTOMATED = 'Automated', 'Automated'

    quiz_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    subject = models.CharField(max_length=100, choices=Subject.choices)
    topic = models.CharField(max_length=100)
    quiz_type = models.CharField(max_length=50, choices=QuizType.choices)
    evaluation_method = models.CharField(max_length=50, choices=EvaluationMethod.choices)
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
    question_order = models.IntegerField()

    class Meta:
        db_table = 'questions'
