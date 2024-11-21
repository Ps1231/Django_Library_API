from django.urls import path
from .views import BookListCreate, BorrowBook, ReturnBook, BorrowerBorrowedBooks, LoanHistory, BorrowerListCreate

urlpatterns = [
    path('books/', BookListCreate.as_view(), name='book-list-create'),
    path('borrow/', BorrowBook.as_view(), name='borrow-book'),
    path('return/', ReturnBook.as_view(), name='return-book'),
    path('loans/active/<int:borrower_id>/', BorrowerBorrowedBooks.as_view(), name='active-loans'),
    path('loans/history/<int:borrower_id>/', LoanHistory.as_view(), name='loan-history'),
    path('borrowers/', BorrowerListCreate.as_view()),  
]