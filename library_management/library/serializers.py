from rest_framework import serializers
from .models import Book, Borrower, Loan 

''' Serializer for the Book model
    This serializer converts the Book model instances into JSON format and vice versa.'''
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

    ''' Serializer for the Borrower model
    This serializer converts the Borrower model instances into JSON format and vice versa.'''
class BorrowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrower
        fields = '__all__'

    ''' Serializer for the Loan model
    This serializer converts the Loan model instances into JSON format and vice versa.
    It also includes additional read-only fields for book title and borrower name.'''
class LoanSerializer(serializers.ModelSerializer):
    book_title = serializers.CharField(source='book.title', read_only=True) # Read-only field for the book's title
    borrowed_by = serializers.CharField(source='borrower.name', read_only=True)  # Read-only field for the borrower's name
    is_returned = serializers.BooleanField(read_only=True) # Read-only field indicating if the book is returned

    class Meta:
        model = Loan
        fields = ['id', 'book_title', 'borrowed_by', 'borrowed_date', 'returned_date', 'is_returned']
