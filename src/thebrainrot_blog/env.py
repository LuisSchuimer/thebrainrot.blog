from os import getenv
from dotenv import load_dotenv

load_dotenv()

"Number of chars that can be included in a article abstract"
ABSTRACT_LEN: int = int(str(getenv("ABSTRACT_LEN")))

"Password that is used for the admin panel"
ADMIN_PASS: str = str(getenv("ADMIN_PASS"))

"Should be a 32 bit server secret key for jwt token"
SERVER_SECRET: str = str(getenv("SERVER_SECRET"))