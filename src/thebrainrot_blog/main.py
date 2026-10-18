from flask import (
    Flask,
    render_template
)
from flask_limiter import Limiter

from thebrainrot_blog.utils import get_remote_ip_addr
#from thebrainrot_blog.logger import logging


app = Flask(__name__)

limiter = Limiter(
    get_remote_ip_addr,
    app=app,
    storage_uri="memory://",
)

@app.route("/")
def main(): 
    return render_template("index.html", posts=[
        {
            "title": "Test article",
            "id": 1,
            "author": "Jazz",
            "abstract": "This is a test for future development"
        }
    ])

@limiter.limit("1/minute")
@app.route("/article/<id>")
def show_post(id: str): 
    return render_template("article.html", post_meta_data={
        "title": "How I made this blog page",
        "author": "Luis Schuimer"
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)