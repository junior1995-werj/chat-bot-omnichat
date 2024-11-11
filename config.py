from prettyconf import config
from collections import defaultdict

class Settings:
    POSTGRESS_DATABASE_URL = config("OPENAI_API_KEY")
    API_URL = config("API_URL")
    API_KEY = config("API_KEY")


settings = Settings()
user_history = defaultdict(list)
