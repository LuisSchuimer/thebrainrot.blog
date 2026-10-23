from os import getenv
from dotenv import load_dotenv

load_dotenv()

ABSTRACT_LEN: int = int(str(getenv("ABSTRACT_LEN")))
ADMIN_PASS: str = str(getenv("ADMIN_PASS"))