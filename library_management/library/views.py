from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound
from .models import Book, Borrower, Loan
from .serializers import BookSerializer, BorrowerSerializer, LoanSerializer
from rest_framework import generics
from django.utils import timezone

class BookListCreate(APIView):
    """
    API view to retrieve list of books or create a new book.

    - GET: Returns a list of all books. If 'available' query parameter is provided,
           it filters the books based on their availability.
    - POST: Creates a new book with the provided data.
            Returns the created book data if successful, otherwise returns errors.
    """
    def post(self, request):
        # Handles POST requests to create a new book.
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        # Handles GET requests to retrieve books.
        # Filters books by availability if the 'available' query parameter is provided.
        available = request.query_params.get('available', None)
        books = Book.objects.all()
        if available is not None:
            books = books.filter(available=available.lower() == 'true')
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

class BorrowBook(APIView):
    """
    API view to handle borrowing a book.

    Methods:
        post: Allows a borrower to borrow a book if eligible.
    """
    def post(self, request):
        """
        Handles POST requests to borrow a book.
        Ensures the book and borrower exist, checks eligibility, and creates a loan record.
        """
        book_id = request.data.get('book_id')
        borrower_id = request.data.get('borrower_id')

        # Handle the case where book_id or borrower_id are missing
        if not book_id or not borrower_id:
            return Response({"error": "book_id and borrower_id are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Fetch the book and borrower from the database
            book = Book.objects.get(id=book_id)
            borrower = Borrower.objects.get(id=borrower_id)

            # Check if borrower is active
            if not borrower.is_active:
                return Response({"error": "Borrower is not active."}, status=status.HTTP_400_BAD_REQUEST)

            # Check if book is available
            if not book.available:
                return Response({"error": "Book is not available."}, status=status.HTTP_400_BAD_REQUEST)

            # Check if the borrower has already borrowed 3 books
            if Loan.objects.filter(borrower=borrower, returned_date__isnull=True).count() >= 3:
                return Response({"error": "Borrowing limit reached."}, status=status.HTTP_400_BAD_REQUEST)

            # Create a new loan entry
            Loan.objects.create(book=book, borrower=borrower)

            # Update the book's status
            book.available = False
            book.borrow_count += 1
            book.save()

            return Response({"message": "Book borrowed successfully."}, status=status.HTTP_201_CREATED)

        except Book.DoesNotExist:
            return Response({"error": "Book not found."}, status=status.HTTP_404_NOT_FOUND)
        except Borrower.DoesNotExist:
            return Response({"error": "Borrower not found."}, status=status.HTTP_404_NOT_FOUND)
        

class ReturnBook(APIView):
    """
    API view to handle returning a borrowed book.

    Methods:
        post: Marks a book as returned and updates its availability status.
    """
    def post(self, request):
        """
        Handles POST requests to return a borrowed book.
        Finds the active loan for the book, marks it as returned, and updates the book's availability.
        """
        book_id = request.data.get('book_id')
        
        # Check if book_id is provided
        if not book_id:
            return Response({"error": "book_id is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Fetch all loans for the book that are not returned
        loans = Loan.objects.filter(book_id=book_id, is_returned=False)

        if not loans.exists():
            return Response({"error": "No active loan found for this book."}, status=status.HTTP_404_NOT_FOUND)

        # Assuming you want to return the most recent loan
        loan = loans.last()  # Get the most recent loan

        # Mark the loan as returned
        loan.is_returned = True
        loan.returned_date = timezone.now()  # Set the returned date
        loan.save()

        # Update the book's availability
        book = loan.book
        book.available = True
        book.save()

        return Response({"message": "Book returned successfully."}, status=status.HTTP_200_OK)


class BorrowerBorrowedBooks(generics.ListAPIView):
    """
    API view to retrieve all active loans for a specific borrower.

    This view returns a list of borrowed books along with the count of currently borrowed books
    that have not been returned.

    Methods:-
    get_queryset(): Returns a queryset of loans that are not returned for the specified borrower.
    get(): Returns a response containing the count of borrowed books and the list of borrowed books.
    """
    serializer_class = LoanSerializer

    def get_queryset(self):
        """
        Returns a queryset of loans that are not returned for the specified borrower.
        Raises NotFound if the borrower does not exist.
        """
        borrower_id = self.kwargs['borrower_id']
        
        # Check if the borrower exists
        if not Borrower.objects.filter(id=borrower_id).exists():
            raise NotFound(detail="Borrower not found.")
        
        # Return loans that are not returned
        return Loan.objects.filter(borrower_id=borrower_id, is_returned=False)

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests to retrieve borrowed books and their count for a borrower.

        Returns:
            Response: A response containing the count of borrowed books and the list of borrowed books.
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        
        # Count the number of borrowed books
        borrowed_books_count = queryset.count()
        
        return Response({
            "borrowed_books_count": borrowed_books_count,
            "borrowed_books": serializer.data
        })


class LoanHistory(generics.ListAPIView):
    """
    API view to retrieve the loan history for a borrower.

    Methods:
        get_queryset: Returns all loans (past and current) for a borrower.
    """
    serializer_class = LoanSerializer

    def get_queryset(self):
        """
        Retrieves all loans for the specified borrower.
        Raises NotFound if the borrower does not exist.
        """
        borrower_id = self.kwargs['borrower_id']
        # Check if the borrower exists
        if not Borrower.objects.filter(id=borrower_id).exists():
            raise NotFound(detail="Borrower not found.")
        
        return Loan.objects.filter(borrower_id=borrower_id)
        
class BorrowerListCreate(generics.ListCreateAPIView):
    queryset = Borrower.objects.all()
    serializer_class = BorrowerSerializer