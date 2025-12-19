from dataclasses import dataclass
from environs import Env


@dataclass
class DatabaseConnection:
    host: str
    port: int
    dbname: str
    user: str
    password: str

    @classmethod
    def from_env(cls) -> 'DatabaseConnection':
        env = Env()
        env.read_env()
        return cls(
            host=env('DATABASE_HOST'),
            port=env('DATABASE_PORT'),
            dbname=env('DATABASE_NAME'),
            user=env('DATABASE_USER'),
            password=env('DATABASE_PASSWORD'),
        )
