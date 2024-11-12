# INTRODUCTION

This documentation provides an overview and usage guide for the My Flask API, which serves as a RESTful interface for interaction with a collections of books

## Base URL

If you run the app locally it should run on port `http://127.0.0.1:5000`. This its base URI

## Endoints

### Books

#### `GET /api/books`

- Description: Retrieve a list of all books.
- Parameters:
  None
- Response:

```json
{
	"res": {
		"1": {
			"id": 1,
			"imgUrl": "https://cdn.kobo.com/book-images/7a557cb3-f72a-47c3-992b-951c9566e4d4/1200/1200/False/the-fellowship-of-the-ring-the-lord-of-the-rings-book-1-1.jpg",
			"title": "Lord Of The Rings",
			"year": "1978"
		},
		"2": {
			"id": 2,
			"imgUrl": "https://www.dunod.com/sites/default/files/styles/principal_desktop/public/thumbnails/image/9782100592586-X.jpg",
			"title": "Réseaux & télécoms",
			"year": "2013"
		}
	}
}
```

#### `GET /api/books/{book_id}`

- Description: Retrieve a list of all books.
- Parameters:
  - user_id (integer): The unique identifier of the book
- Response:

```json
{
	"res": {
		"id": 1,
		"imgUrl": "https://cdn.kobo.com/book-images/7a557cb3-f72a-47c3-992b-951c9566e4d4/1200/1200/False/the-fellowship-of-the-ring-the-lord-of-the-rings-book-1-1.jpg",
		"title": "Lord Of The Rings",
		"year": "1978"
	}
}
```

#### `POST /api/books`

- Description: Create a new book
- Parameters (Request Body):

```json
{
	"title": "the new title",
	"year": 2014,
	"imageUrl": "your_image_url"
}
```

- Response:
  - HTTP code 201

```json
{
	"res": {
		"imageUrl": "test 01",
		"title": "the new title",
		"year": 2014
	}
}
```

- "/" => welcoming message
- "/api/books" -> GET => get all the books
- "/api/books" -> POST => add a new respurce (book)
- "/api/books/:id" -> GET => get one book based on its id
- "/api/books/:id" -> PUT => update one book based on its id
- "/api/books/:id" -> DELETE => delete one book based on its id
