from flask import (
    request,
    redirect,
    make_response
)
from werkzeug.wrappers import Response

from jwt import decode, encode # type: ignore
from datetime import datetime, timedelta
from typing import Tuple

from thebrainrot_blog.env import SERVER_SECRET

"returns connecting ip addr over cloudflare (if configured) or normal request ip addr (mostly for non-production)"
def get_remote_ip_addr() -> str:
    return request.headers.get("Cf-Connecting-Ip") or request.remote_addr or ""

"Shifts index to be correct after removal of multpile others"
def index_offset(to_be_offset: Tuple[int,int], indexes_to_be_removed: list[Tuple[int,int]]) -> Tuple[int,int]:
    for removed in indexes_to_be_removed:
        if removed[1] <= to_be_offset[0]:
            offset = removed[1] - removed[0]
            to_be_offset = (to_be_offset[0] - offset, to_be_offset[1] - offset)
    return to_be_offset

"Ensures that the path can only be accessed when jwt-token and its values are expected"
def login_required(path): # type: ignore
    def myinner(*args, **kwargs): # type: ignore
        if not (jwt_token := request.cookies.get("jwt_token")): return make_response("This action is not allowed")

        decoded = decode(jwt_token, SERVER_SECRET, algorithms=["HS256"])
        if decoded["associated_ipaddr"] == get_remote_ip_addr() and datetime.strptime(decoded["valid_till"], r"%Y %m %d %H %M %S") > datetime.now(): 
            return path(*args, **kwargs) # type: ignore

    return myinner # type: ignore

"Sets a new jwt token as a cookie when called and redirects to admin page"
def set_jwt_cookie() -> Response:
    response = redirect("/admin")
    response.set_cookie("jwt_token", encode({
        "associated_ipaddr": get_remote_ip_addr(),
        "valid_till": ((expire_date := datetime.now() + timedelta(minutes=30))).strftime(r"%Y %m %d %H %M %S")
    }, SERVER_SECRET, algorithm="HS256"), expires=expire_date)

    return response