Japronto Extra
==============
A bit of sugar for the [fastest python framework][japronto]

    pip install orjson japronto-extra

Api
---

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


@route("/validation", "POST")
@jsonify
def basic_validation(request):
    # required integer query argument
    id = get_argument(request.query, "id", int)
    # optional `datetime` json argument with a default fallback
    at = get_argument(
        request.json, "at", datetime.fromisoformat, default=datetime.now()
    )
    return {"id": id, "at": at}
```

Look at the working example in [expample.py](./example.py)

[japronto]: https://github.com/squeaky-pl/japronto/
