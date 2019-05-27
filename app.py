import json
from flask import Flask, Response, request

app = Flask(__name__)

JSON_MIME_TYPE = 'application/json'

LAST_ID = 0
books = []
"""books = [{
    'id': 35,
    'author': 'Irfan CAN',
    'title': 'API Testing'
}]"""

@app.route("/")
def hello():
    return "Hello World!"


@app.route("/api/books/", methods=['GET', 'POST'])
def f1():
    global LAST_ID
    if request.method == 'GET':
        return Response(json.dumps(books), 200, {'Content-Type': JSON_MIME_TYPE})
    elif request.method == 'POST':
        data = request.json
        if 'author' in data and 'title' in data:
            if data['author'] is "" and data['title'] is "":
                error = json.dumps({"error": "Field 'author' and 'title' cannot be empty."})
                return Response(error, 400, {'Content-Type': JSON_MIME_TYPE})
            elif data['author'] is "":
                error = json.dumps({"error": "Field 'author' cannot be empty."})
                return Response(error, 400, {'Content-Type': JSON_MIME_TYPE})
            elif data['title'] is "":
                error = json.dumps({"error": "Field 'title' cannot be empty."})
                return Response(error, 400, {'Content-Type': JSON_MIME_TYPE})
            else:
                if 'id' in data:
                    error = json.dumps({"error": "You cannot set 'id' field."})
                    return Response(error, 400, {'Content-Type': JSON_MIME_TYPE})
                else:
                    for book in books:
                        if data['author'] == book['author'] and data['title'] == book['title']:
                            error = json.dumps({"error": "Another book with similar title and author already exists."})
                            return Response(error, 400, {'Content-Type': JSON_MIME_TYPE})
                    book = {
                        'id': LAST_ID+1,
                        'author': data['author'],
                        'title': data['title']
                    }
                    books.append(book)
                    LAST_ID += 1
                    return Response(json.dumps(book), status=200, mimetype=JSON_MIME_TYPE)

        else:
            if 'author' not in data and 'title' not in data:
                error = json.dumps({"error": "Field 'author' and 'title' are required."})
                return Response(error, 400, {'Content-Type': JSON_MIME_TYPE})
            elif 'author' not in data:
                error = json.dumps({"error": "Field 'author' is required."})
                return Response(error, 400, {'Content-Type': JSON_MIME_TYPE})
            else:
                error = json.dumps({"error": "Field 'title' is required."})
                return Response(error, 400, {'Content-Type': JSON_MIME_TYPE})
        return Response(json.dumps(data), status=200, mimetype=JSON_MIME_TYPE)


@app.route("/api/books/<int:book_id>", methods=['GET'])
def update_user(book_id):
    book = search_book(books, book_id)
    if book is None:
        error = json.dumps({"error": "The book with the given 'id' does not exist."})
        return Response(error, 404)
    return Response(json.dumps(book), status=200, mimetype=JSON_MIME_TYPE)


def search_book(books, book_id):
    for book in books:
        if book['id'] == book_id:
            return book


if __name__ == "__main__":
    app.run(debug=True)
