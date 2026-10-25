from flask import (
    Flask,
    render_template,
    redirect,
    request
)
from flask_limiter import Limiter

from thebrainrot_blog.backend.database.crud import *
from thebrainrot_blog.env import SERVER_SECRET, ADMIN_PASS
from thebrainrot_blog.utils import (
    get_remote_ip_addr,
    set_jwt_cookie,
    logged_in,
    login_required # type: ignore
)

app = Flask(__name__)

app.secret_key = SERVER_SECRET

limiter = Limiter(
    get_remote_ip_addr,
    app=app,
    storage_uri="memory://",
)

@app.route("/")
def main(): 
    return render_template("index.html", posts=db_get_post_feed())

@app.route("/article/<id>")
@limiter.limit("10/second")
def show_post_mask(id: str): 
    if (post := db_get_post(id=id)) is None: return redirect("/")
    return render_template("article.html", post_meta_data={
        "id": post.id,
        "author": post.author,
        "title": post.title
    })

@app.route("/content/<id>")
@limiter.limit("10/second")
def load_post_content(id: str):
    if (post := db_get_post(id=id)) is None: return render_template("/posts/test.html")
    return render_template(f"/posts/{post.render_file}")

@app.route("/admin")
@limiter.limit("5/second")
@login_required
def admin():
    return render_template("admin.html", admin_page = True)

@app.route("/login", methods=["POST", "GET"])
@limiter.limit("1/second")
def login():
    if logged_in(): return redirect("/admin")
    if not (password := request.form.get("password")): return render_template("login.html")
    if password == ADMIN_PASS: return set_jwt_cookie()

    return render_template("login.html", login_fail=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)