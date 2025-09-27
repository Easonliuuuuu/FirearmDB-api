from slowapi import Limiter
from app.auth import dynamic_key_func

# Define the limiter instance here
limiter = Limiter(
    key_func=dynamic_key_func,
    storage_uri="memory://"  # Add storage configuration
)