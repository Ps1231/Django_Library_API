from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    available = models.BooleanField(default=True)
    borrow_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

class Borrower(models.Model):
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

# class Loan(models.Model):
#     book = models.ForeignKey(Book, on_delete=models.CASCADE)
#     borrower = models.ForeignKey(Borrower, on_delete=models.CASCADE)
#     is_returned = models.BooleanField(default=False)

#     def __str__(self):
#         return f"{self.borrower.name} borrowed {self.book.title}"


class Loan(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrower = models.ForeignKey(Borrower, on_delete=models.CASCADE)
    borrowed_date = models.DateTimeField(auto_now_add=True)
    returned_date = models.DateTimeField(null=True, blank=True)
    is_returned = models.BooleanField(default=False)  # Add this field

    # def is_returned(self):
    #     return self.returned_date is not None
    def __str__(self):
        return f"{self.borrower.name} borrowed {self.book.title}"


# class BorrowedBook(models.Model):
#     book = models.ForeignKey(Book, on_delete=models.CASCADE)
#     borrower = models.ForeignKey(Borrower, on_delete=models.CASCADE)
#     borrowed_date = models.DateTimeField(auto_now_add=True)
#     returned_date = models.DateTimeField(null=True, blank=True)

#     def is_returned(self):
#         return self.returned_date is not None