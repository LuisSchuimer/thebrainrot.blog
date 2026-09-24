from flask import request
from typing import Tuple

def get_remote_ip_addr() -> str | None:
    # returns connecting ip addr over cloudflare (if configured) or normal request ip addr (mostly for non-production)
    return request.headers.get("Cf-Connecting-Ip") or request.remote_addr

def index_offset(to_be_offset: Tuple[int,int], indexes_to_be_removed: list[Tuple[int,int]]) -> Tuple[int,int]:
    for removed in indexes_to_be_removed:
        if removed[1] < to_be_offset[0]:
            offset = removed[1] - removed[0]
            to_be_offset = (to_be_offset[0] - offset, to_be_offset[1] - offset)
    return to_be_offset