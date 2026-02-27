import xml.etree.ElementTree as ET
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Book

def xml_response(data_dict, root_tag='response', status=200):
    root = ET.Element(root_tag)

    def build(parent, data):
        if isinstance(data, dict):
            for key, value in data.items():
                child = ET.SubElement(parent, key)
                build(child, value)
        elif isinstance(data, list):
            for item in data:
                item_el = ET.SubElement(parent, 'book')
                build(item_el, item)
        else:
            parent.text = str(data) if data is not None else ''

    build(root, data_dict)
    xml_str = ET.tostring(root, encoding='unicode')
    full_xml = f'<?xml version="1.0" encoding="UTF-8"?>\n{xml_str}'
    return HttpResponse(full_xml, content_type='application/xml', status=status)


def xml_error(message, status=400):
    return xml_response({'status': 'error', 'message': message}, status=status)


def parse_xml_body(request):
    try:
        body = request.body
        if not body:
            return None, xml_error('Request body is empty.', 400)
        return ET.fromstring(body), None
    except ET.ParseError as e:
        return None, xml_error(f'Invalid XML: {str(e)}', 400)


def get_text(element, tag, default=None):
    child = element.find(tag)
    if child is not None and child.text:
        return child.text.strip()
    return default


# ── ENDPOINT 1: /api/books/  (GET = list, POST = create) ─────

@csrf_exempt
def book_list_create(request):

    if request.method == 'GET':
        books = Book.objects.all()
        books_data = [b.to_dict() for b in books]
        return xml_response({'status': 'success', 'count': str(len(books_data)), 'books': books_data})

    elif request.method == 'POST':
        xml_root, err = parse_xml_body(request)
        if err:
            return err

        title  = get_text(xml_root, 'title')
        author = get_text(xml_root, 'author')
        year   = get_text(xml_root, 'year')
        genre  = get_text(xml_root, 'genre', default='Unknown')
        isbn   = get_text(xml_root, 'isbn')

        if not title:
            return xml_error('Field <title> is required.', 400)
        if not author:
            return xml_error('Field <author> is required.', 400)
        if not year:
            return xml_error('Field <year> is required.', 400)

        try:
            year_int = int(year)
        except ValueError:
            return xml_error('<year> must be an integer like 2024.', 400)

        if isbn and Book.objects.filter(isbn=isbn).exists():
            return xml_error(f'ISBN "{isbn}" already exists.', 409)

        book = Book.objects.create(
            title=title, author=author, year=year_int,
            genre=genre, isbn=isbn if isbn else None
        )
        return xml_response({'status': 'success', 'message': 'Book created.', **book.to_dict()}, status=201)

    return xml_error(f'Method {request.method} not allowed.', 405)


# ── ENDPOINT 2: /api/books/<id>/  (GET / PUT / DELETE) ───────

@csrf_exempt
def book_detail(request, book_id):
    try:
        book = Book.objects.get(pk=book_id)
    except Book.DoesNotExist:
        return xml_error(f'Book with id={book_id} not found.', 404)

    if request.method == 'GET':
        return xml_response({'status': 'success', **book.to_dict()})

    elif request.method == 'PUT':
        xml_root, err = parse_xml_body(request)
        if err:
            return err

        title  = get_text(xml_root, 'title')
        author = get_text(xml_root, 'author')
        year   = get_text(xml_root, 'year')
        genre  = get_text(xml_root, 'genre')
        isbn   = get_text(xml_root, 'isbn')

        if title:  book.title = title
        if author: book.author = author
        if genre:  book.genre = genre
        if year:
            try:
                book.year = int(year)
            except ValueError:
                return xml_error('<year> must be an integer.', 400)
        if isbn:
            if Book.objects.filter(isbn=isbn).exclude(pk=book_id).exists():
                return xml_error(f'ISBN "{isbn}" already used by another book.', 409)
            book.isbn = isbn

        book.save()
        return xml_response({'status': 'success', 'message': 'Book updated.', **book.to_dict()})

    elif request.method == 'DELETE':
        title = book.title
        book_id_str = str(book.id)
        book.delete()
        return xml_response({
            'status': 'success',
            'message': f'Book "{title}" deleted.',
            'deleted_id': book_id_str
        })

    return xml_error(f'Method {request.method} not allowed.', 405)


# ── ENDPOINT 3: /api/books/search/?q=keyword ─────────────────

@csrf_exempt
def book_search(request):
    if request.method != 'GET':
        return xml_error('Only GET is allowed.', 405)

    query = request.GET.get('q', '').strip()
    if not query:
        return xml_error('Provide ?q=keyword', 400)

    books = Book.objects.filter(title__icontains=query) | \
            Book.objects.filter(author__icontains=query)
    books_data = [b.to_dict() for b in books]
    return xml_response({'status': 'success', 'query': query, 'count': str(len(books_data)), 'books': books_data})