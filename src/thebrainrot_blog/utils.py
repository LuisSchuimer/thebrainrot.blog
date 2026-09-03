from flask import request

def get_remote_ip_addr() -> str | None:
    # returns connecting ip addr over cloudflare (if configured) or normal request ip addr (mostly for non-production)
    return request.headers.get("Cf-Connecting-Ip") or request.remote_addr

