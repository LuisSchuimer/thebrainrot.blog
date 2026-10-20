from thebrainrot_blog.backend.database.struct import (
    build,
    Posts,
)
from uuid import uuid4

db = build()

#! Later in config file
ABSTRACT_LEN: int = 50

def db_create_post(
    title: str,
    author: str,
    content: str,
    rendered_content: str,
    markdown_file: str,
):
    Posts.create( # type: ignore
        id=str(uuid4()),
        title=title,
        author=author,
        content=content,
        rendered_content=rendered_content,
        markdown_file=markdown_file
    )

def db_get_post_feed() -> list[dict[str, str]]:
    return [{
        "id": post.id,
        "author": post.author,
        "title": post.title,
        "abstract": f"{post.content[:ABSTRACT_LEN]}..."
    } for post in Posts.select()] # type: ignore

print(db_get_post_feed())