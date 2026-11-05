set shell := ["powershell", "-Command"]

server: 
    uv run python -m thebrainrot_blog.main
parser: 
    uv run python -m thebrainrot_blog.backend.markdown_handler.parse_markdown
renderer: 
    uv run python -m thebrainrot_blog.backend.markdown_handler.render_article
db: 
    uv run python -m thebrainrot_blog.backend.database.crud

parser-test: 
    uv run python -m unittest thebrainrot_blog.tests.parser_test -v
renderer-test: 
    uv run python -m unittest thebrainrot_blog.tests.renderer_test -v

css-watch:
    uv run tailwindcss -i src/thebrainrot_blog/static/css/input.css -o src/thebrainrot_blog/static/css/output.css --watch