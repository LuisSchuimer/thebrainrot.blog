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
    app=app
)

@app.route("/")
def main(): return render_template("index.html")

@app.route("/article")
def article(): return render_template("article.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)