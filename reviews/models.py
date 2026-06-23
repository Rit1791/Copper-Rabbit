from django.db import models


class Review(models.Model):
    repository = models.CharField(max_length=255)

    pr_number = models.IntegerField()

    review_text = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return (
            f"{self.repository} "
            f"PR #{self.pr_number}"
        )