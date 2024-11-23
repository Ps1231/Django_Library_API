# Library Management System API 

This is a Django-based RESTful API for managing a library system. It allows users to perform various operations such as managing books, borrowers, loans, borrowing books, and returning them.

## Features
1. Books Management: Add, list, and check the availability of books.
2. Borrowers Management: Add borrowers and manage their active status.
3. Loan Management: Borrow books, return books, view active loans, and loan history.
4. Borrowing Rules:
   - A borrower can borrow up to 3 books at a time.
   - Only active borrowers can borrow books.
   - Books must be returned to allow re-borrowing.

## Endpoints Overview

### Books 
1. Add a Book
   - POST /api/books/
   - Request Body:
```
    {
    "title": "Your_Title",
    "author": "Your_Author",
    "available": true
    }
```
2. List All Books
   - GET /api/books/
   - Optional Query Parameter: available (e.g., /api/books/?available=true)
  
### Borrowers
1. Add a Borrower
   - POST /api/borrowers/
   - Request Body:
```
    {
    "name": "Your_Borrower_Name",
    "is_active": true
    }
```
2. List All Borrowers
   - GET /api/borrowers/

### Loans
1. Borrow a Book
   - POST /api/borrow/
   - Request Body:
 ```
   {
   "book_id": <your_book_id>,
   "borrower_id": <your_borrower_id>
   }
```
3. Return a Book
   - POST /api/return/
   - Request Body:
```
    {
    "book_id": <your_book_id>
    }
```
4. Get Active Loans for a Borrower
   - GET /api/loans/active/<borrower_id>/
5. Get Loan History for a Borrower
   - GET /api/loans/history/<borrower_id>/

## Setup Instructions
1. Clone the repository:

``` 
git clone <repository_url>
cd <repository_directory>
```
2. Install dependencies:
```
pip install -r requirements.txt
```
3. Apply migrations:
```
python manage.py migrate
```
4. Start the server:
```
python manage.py runserver
```
## Usage Examples

### Add a Sample Book
```
curl -X POST http://127.0.0.1:8000/api/books/ -H "Content-Type: application/json" -d '{
    "title": "The Great Gatsby",
    "author": "F. Scott Fitzgerald",
    "available": true
}'
```
### Add a Sample Borrower
```
curl -X POST http://127.0.0.1:8000/api/borrowers/ -H "Content-Type: application/json" -d '{
    "name": "Alice",
    "is_active": true
}'
```
### Borrow a Book
```
curl -X POST http://127.0.0.1:8000/api/borrow/ -H "Content-Type: application/json" -d '{
   "book_id": 1,
   "borrower_id": 1
}'
```
### Return a Book
```
curl -X POST http://127.0.0.1:8000/api/return/ -H "Content-Type: application/json" -d '{
    "book_id": 1
}'
```
### Get Active Loans for a Borrower
```
curl -X GET http://127.0.0.1:8000/api/loans/active/1/
```
### Get Loan History for a Borrower
```
curl -X GET http://127.0.0.1:8000/api/loans/history/1/
```
## Models Overview
> Book
Attributes:
- title: The title of the book.
- author: The author of the book.
- available: Whether the book is available for borrowing.
- borrow_count: Number of times the book has been borrowed.

> Borrower
Attributes:
- name: The name of the borrower.
- is_active: Whether the borrower is active.

> Loan
Attributes:
- book: The borrowed book (foreign key).
- borrower: The borrower (foreign key).
- borrowed_date: The date the book was borrowed.
- returned_date: The date the book was returned.
- is_returned: Whether the book has been returned.

## Borrowing Rules
1. Borrowers must be active to borrow books.
2. Books must be available to be borrowed.
3. A borrower can borrow up to 3 books simultaneously.

## Contributing
1. Fork the repository.
2. Create a new feature branch.
3. Submit a pull request.

