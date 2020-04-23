Japronto Extra
==============
A bit of sugar for the fastest python framework.

```python
@route("/")
@jsonify
def home(request):
    return "You can pass an url explicitly"


@route
@jsonify
def hello_world(request):
    # if you omit it though, the function name will be used
    return {"I'm served at": "/hello-world"}


@route
@jsonify
def foo__bar(request):
    # double underscores map onto slashes
    return "I'm at /foo/bar"


@route
@jsonify
def basic_validation(request):
    # required integer query argument
    id = get_argument(request.query, "id", int)
    # optional `datetime` json argument with a default fallback
    at = get_argument(
        request.json, "start", datetime.fromisoformat, default=datetime.now()
    )
    return {"id": id, "at": at}
```

The full working example is in [expample.py](./example.py)
