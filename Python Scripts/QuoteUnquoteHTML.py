from urllib.parse import quote, unquote

# Basic encoding
text = "Hello World!"
encoded = quote(text)
print(encoded)  # "Hello%20World%21"

# Encode with safe characters (won't be encoded)
path = "/api/users/john doe"
encoded_path = quote(path, safe="/")
print(encoded_path)  # "/api/users/john%20doe"

# Encode everything (no safe characters)
encoded_all = quote(text, safe="")
print(encoded_all)  # "Hello%20World%21"

# Decoding with unquote()
encoded = "Hello%20World%21"
decoded = unquote(encoded)
print(decoded)  # "Hello World!"

# Handle plus signs as spaces
from urllib.parse import unquote_plus
encoded_plus = "Hello+World"
decoded = unquote_plus(encoded_plus)
print(decoded)  # "Hello World"

# Use urlencode() for encoding dictionaries as query strings:

params = {
    "name": "John Doe",
    "city": "New York",
    "tags": ["python", "web"]
}

# Basic encoding
query_string = urlencode(params)
print(query_string)
# "name=John+Doe&city=New+York&tags=%5B%27python%27%2C+%27web%27%5D"

# Handle lists properly with doseq=True
params_list = [
    ("name", "John"),
    ("tag", "python"),
    ("tag", "web")
]
query_string = urlencode(params_list)
print(query_string)
# "name=John&tag=python&tag=web"

# Parsing Query Strings
from urllib.parse import parse_qs, parse_qsl

query_string = "name=John&age=30&tag=python&tag=web"

# Parse to dictionary (values are lists)
params = parse_qs(query_string)
print(params)
# {'name': ['John'], 'age': ['30'], 'tag': ['python', 'web']}

# Parse to list of tuples
params_list = parse_qsl(query_string)
print(params_list)
# [('name', 'John'), ('age', '30'), ('tag', 'python'), ('tag', 'web')]
Working with URLs
from urllib.parse import urlparse, urlunparse, urljoin

# Parse a URL
url = "https://example.com/path?query=value#section"
parsed = urlparse(url)
print(parsed.scheme)    # "https"
print(parsed.netloc)    # "example.com"
print(parsed.path)      # "/path"
print(parsed.query)     # "query=value"
print(parsed.fragment)  # "section"

# Build a URL from components
components = ("https", "example.com", "/search", "", "q=hello", "")
url = urlunparse(components)
print(url)  # "https://example.com/search?q=hello"

# Join URLs
base = "https://example.com/api/"
endpoint = "users/123"
full_url = urljoin(base, endpoint)
print(full_url)  # "https://example.com/api/users/123"

quote_plus() for Form Data
Use quote_plus() when encoding form data (spaces become +):
from urllib.parse import quote_plus

text = "Hello World"
encoded = quote_plus(text)
print(encoded)  # "Hello+World"

# vs quote() which uses %20
encoded_percent = quote(text)
print(encoded_percent)  # "Hello%20World"
