from os import getenv
from dotenv import load_dotenv

load_dotenv()

"If running in production or not (when production, the server expects a cloudflare setup)"
IS_PRODUCTION: bool = bool(str(getenv("IS_PRODUCTION")))

"Number of chars that can be included in a article abstract"
ABSTRACT_LEN: int = int(str(getenv("ABSTRACT_LEN")))

"Password that is used for the admin panel"
ADMIN_PASS: str = str(getenv("ADMIN_PASS"))

"Should be a 32 bit server secret key for jwt token"
SERVER_SECRET: str = str(getenv("SERVER_SECRET"))

"Path where uploaded raw posts (.md) are stored"
RAW_POST_PATH: str = str(getenv("RAW_POST_PATH"))