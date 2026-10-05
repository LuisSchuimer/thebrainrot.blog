from flask import (
    Flask,
    render_template
)
from flask_socketio import SocketIO
from flask_limiter import Limiter

from thebrainrot_blog.utils import get_remote_ip_addr
from thebrainrot_blog.markdown_handler.parse_markdown import construct_line
from thebrainrot_blog.markdown_handler.piece_types import styling_types, piece_types
#from thebrainrot_blog.logger import logging


app = Flask(__name__)
socketio = SocketIO(app)

limiter = Limiter(
    get_remote_ip_addr,
    app=app
)

@app.route("/")
def main(): return render_template("index.html")

@socketio.on("parser_submit")
def parser_runner(data): 
    out = construct_line(line_content=str(data["content"]))
    socketio.emit("parser_return", {
        "content": out.content,
        "styling_types": [(styling_type.style_type.value, styling_type.index) for styling_type in out.styling[styling_types.SPECIFIC]] + [(styling_type.style_type.value) for styling_type in out.styling[styling_types.GLOBAL]]
    })



if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=8000)