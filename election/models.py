from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    ADMIN = 'admin'
    STUDENT = 'student'
    CANDIDATE = 'candidate'
    
    ROLE_CHOICES = [
        (ADMIN, 'Admin'),
        (STUDENT, 'Student'),
        (CANDIDATE, 'Candidate'),
    ]
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=STUDENT)
    student_id = models.CharField(max_length=20, unique=True, null=True, blank=True)
    email = models.EmailField(unique=True)
    
    def is_admin(self):
        return self.role == self.ADMIN
    
    def is_candidate(self):
        return self.role == self.CANDIDATE

class Election(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    notification_sent = models.BooleanField(default=False)

    def is_ongoing(self):
        now = timezone.now()
        return self.start_date <= now <= self.end_date and self.is_active

    def can_vote(self, user):
        if not self.is_ongoing():
            return False
        return not Vote.objects.filter(voter=user, election=self).exists()

    def get_results(self):
        results = {}
        for position in self.positions.all():
            candidates = position.candidates.all()
            vote_counts = []
            total_votes = Vote.objects.filter(
                candidate__position=position
            ).count()
            
            for candidate in candidates:
                votes = Vote.objects.filter(candidate=candidate).count()
                percentage = (votes / total_votes * 100) if total_votes > 0 else 0
                vote_counts.append({
                    'candidate': candidate,
                    'votes': votes,
                    'percentage': round(percentage, 1)
                })
            results[position] = {
                'vote_counts': vote_counts,
                'total_votes': total_votes
            }
        return results

    def __str__(self):
        return self.title

class Position(models.Model):
    election = models.ForeignKey(Election, on_delete=models.CASCADE, related_name='positions')
    title = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return f"{self.title} - {self.election.title}"

class Candidate(models.Model):
    position = models.ForeignKey(Position, on_delete=models.CASCADE, related_name='candidates')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bio = models.TextField()
    photo = models.ImageField(upload_to='candidate_photos/', null=True, blank=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.position.title}"

class Vote(models.Model):
    voter = models.ForeignKey(User, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    election = models.ForeignKey(Election, on_delete=models.CASCADE)
    position = models.ForeignKey(Position, on_delete=models.CASCADE, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [
            ('voter', 'election', 'position'),
        ]

    def save(self, *args, **kwargs):
        if not self.position:
            self.position = self.candidate.position
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.voter.username} - {self.candidate.position.title}"

# ... rest of your models ... 