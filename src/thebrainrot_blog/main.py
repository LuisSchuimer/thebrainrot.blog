from flask import (
    Flask,
    render_template,
    request
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
def test():
    return render_template("index.html", test="<h2>Yayyyy</h2> <br> <h3>Test<h3>")

if __name__ == "__main__":
    app.run("0.0.0.0", port=5000, debug=True)