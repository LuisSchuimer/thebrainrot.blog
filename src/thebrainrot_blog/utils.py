from flask import (
    request,
    redirect
)
from werkzeug.wrappers import Response

from jwt import decode, encode # type: ignore
from datetime import datetime, timedelta
from typing import Tuple

from thebrainrot_blog.env import SERVER_SECRET, IS_PRODUCTION

"""
returns connecting ip addr over cloudflare (if server setup configured as 'production') 
or normal request ip addr (configured as 'non-production')"
"""
def get_remote_ip_addr() -> str:
    return request.headers.get("Cf-Connecting-Ip") or "" if IS_PRODUCTION else request.remote_addr or ""

"Shifts index to be correct after removal of multpile others"
def index_offset(to_be_offset: Tuple[int,int], indexes_to_be_removed: list[Tuple[int,int]]) -> Tuple[int,int]:
    for removed in indexes_to_be_removed:
        if removed[1] <= to_be_offset[0]:
            offset = removed[1] - removed[0]
            to_be_offset = (to_be_offset[0] - offset, to_be_offset[1] - offset)
    return to_be_offset

"Checks if user is logged in and returns the login state"
def logged_in() -> bool | None:
    if not (jwt_token := request.cookies.get("jwt_token")): return False
    decoded = decode(jwt_token, SERVER_SECRET, algorithms=["HS256"])
    if decoded["associated_ipaddr"] == get_remote_ip_addr() and datetime.strptime(decoded["valid_till"], r"%Y %m %d %H %M %S") > datetime.now(): 
        return True
    return None

"Ensures that the path can only be accessed when jwt-token and its values are expected"
def login_required(path): # type: ignore
    def myinner(*args, **kwargs): # type: ignore
        match logged_in():
            case True: return path(*args, **kwargs) # type: ignore
            case False: return redirect("/login")
            case None: return del_jwt_cookie()
    return myinner # type: ignore

"Sets a new jwt token as a cookie when called and redirects to admin page"
def set_jwt_cookie() -> Response:
    response = redirect("/admin")
    expire_date = datetime.now() + timedelta(minutes=30)
    response.set_cookie("jwt_token", encode({
        "associated_ipaddr": get_remote_ip_addr(),
        "valid_till": expire_date.strftime(r"%Y %m %d %H %M %S")
    }, SERVER_SECRET, algorithm="HS256"), expires=expire_date, secure=True, httponly=True, samesite="strict")

    return response

"Delete jwt token cookie when called and redirects to the login form"
def del_jwt_cookie() -> Response:
    resp = redirect("/login")
    resp.delete_cookie("jwt_token")

    return resp
