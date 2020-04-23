from __future__ import annotations

from asyncio import iscoroutinefunction
from functools import wraps
from typing import Any, Callable, Dict, List, Optional, Union

from japronto import Application
from japronto.request import HttpRequest
from japronto.response.cresponse import Response

try:
    from orjson import dumps as json_dumpb
except ImportError:
    import json

    def json_dumpb(*a, **kw):  # type:ignore
        return json.dumps(*a, *kw).encode("utf-8")


__version__ = "0.1.1"
NONE = object()


class ValidationError(Exception):
    pass


def json_response(request: HttpRequest, data: Any) -> Response:
    if isinstance(data, Response):
        return data
    return request.Response(
        body=json_dumpb(data),
        headers={"Content-Type": "application/json; charset=utf8"},
    )


def jsonify(f: Callable) -> Callable:
    if iscoroutinefunction(f):

        @wraps(f)
        async def wrapper(request: HttpRequest):
            return json_response(request, await f(request))

    else:

        @wraps(f)
        def wrapper(request: HttpRequest):
            return json_response(request, f(request))

    return wrapper


def router(app: Application) -> Callable:
    def route(
        url_or_func: Union[str, Callable],
        method: Optional[str] = None,
        methods: Optional[List[str]] = None,
    ) -> Callable:
        def wrapper(f: Callable):
            url = url_or_func
            if callable(url):
                url = "/" + f.__name__.replace("__", "/").replace("_", "-")
            app.router.add_route(url, f, method, methods)
            return f

        if callable(url_or_func):
            return wrapper(url_or_func)

        return wrapper

    return route


def get_argument(
    container: Dict[str, Any],
    name: str,
    decoder: Optional[Callable] = None,
    *,
    default=NONE,
) -> Any:
    try:
        raw = container[name]
    except KeyError:
        if default is not NONE:
            return default
        raise ValidationError(f"Argument `{name}` is required")
    if not decoder:
        return raw
    try:
        return decoder(raw)
    except Exception:
        raise ValidationError(f"Argument `{name}` has an incorrect format")


def validation_error_handler(
    request: HttpRequest, exception: ValidationError
) -> Response:
    return request.Response(text=exception.args[0], code=400)


def handle_validation_errors(app: Application) -> Callable:
    app.add_error_handler(ValidationError, validation_error_handler)
    return router(app)
