from dataclasses import dataclass

@dataclass 
class User:
    user_name: str
    user_password: str
    id: int = None
