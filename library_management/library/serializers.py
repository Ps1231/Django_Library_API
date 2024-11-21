from rest_framework import serializers
from .models import Book, Borrower, Loan 

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class BorrowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrower
        fields = '__all__'


class LoanSerializer(serializers.ModelSerializer):
    book_title = serializers.CharField(source='book.title', read_only=True)
    borrowed_by = serializers.CharField(source='borrower.name', read_only=True)
    is_returned = serializers.BooleanField(read_only=True)

    class Meta:
        model = Loan
        fields = ['id', 'book_title', 'borrowed_by', 'borrowed_date', 'returned_date', 'is_returned']
