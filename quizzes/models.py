from django.db import models

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

class Question(models.Model):
    question_id = models.AutoField(primary_key=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question_text = models.TextField()
    model_answer = models.TextField()
    question_order = models.IntegerField()

    class Meta:
        db_table = 'questions'
