from django.db import models


class Book(models.Model):
    """
    Represents a book in the library.

    Attributes:
        title (str): The title of the book.
        author (str): The name of the author of the book.
        available (bool): Indicates whether the book is available for borrowing.
        borrow_count (int): The number of times the book has been borrowed.
    """
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    available = models.BooleanField(default=True)
    borrow_count = models.PositiveIntegerField(default=0)

    # Returns the string representation of the book, which is its title.
    def __str__(self):
        return self.title

    
class Borrower(models.Model):
    """
    Represents a person who can borrow books.

    Attributes:
        name (str): The name of the borrower.
        is_active (bool): Indicates whether the borrower is active and can borrow books.
    """
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    # Returns the string representation of the borrower, which is their name.
    def __str__(self):
        return self.name

    
class Loan(models.Model):
    """
    Represents a loan record for when a borrower borrows a book.

    Attributes:
        book (Book): The book being borrowed.
        borrower (Borrower): The person borrowing the book.
        borrowed_date (datetime): The date and time when the book was borrowed.
        returned_date (datetime, optional): The date and time when the book was returned.
        is_returned (bool): Indicates whether the book has been returned.
    """
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrower = models.ForeignKey(Borrower, on_delete=models.CASCADE)
    borrowed_date = models.DateTimeField(auto_now_add=True)
    returned_date = models.DateTimeField(null=True, blank=True)
    is_returned = models.BooleanField(default=False)  # Add this field

    # Returns a string representation of the loan, showing which borrower borrowed which book.
    def __str__(self):
        return f"{self.borrower.name} borrowed {self.book.title}"

