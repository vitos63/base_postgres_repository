import asyncpg
from abc import ABC
from dataclasses import asdict, is_dataclass
from typing import TypeVar, Generic, Type, List, Optional

from postgresql_repository.models.database_connection import DatabaseConnection


T = TypeVar('T')


class BasePostgreSQLRepository(Generic[T], ABC):
    def __init__(self, db_connection: DatabaseConnection, table_name: str, model_cls: Type[T]):
        self._pool = None
        self._db_connection = db_connection
        self._table_name = table_name
        self._model_cls = model_cls

    async def setup(self):
        self._pool = await asyncpg.create_pool(
            user=self._db_connection.user,
            password=self._db_connection.password,
            host=self._db_connection.host,
            port=self._db_connection.port,
            database=self._db_connection.dbname,
        )

    def _map_to_model(self, record: asyncpg.Record, model: Type[T]=None) -> T:
        if not record:
            return

        if model:
            return model(**dict(record))
        else:
            return self._model_cls(**dict(record))

    def _map_to_db(self, model: T) -> dict:
        if is_dataclass(model):
            return asdict(model)
        else:
            data =  model.__dict__
            return {k: v for k, v in data.items() if not k.startswith('_')}

    async def get_all(self, order_by: str = 'id') -> List[T]:
        async with self._pool.acquire() as conn:
            query = f'SELECT * FROM {self._table_name} ORDER BY {order_by};'
            records = await conn.fetch(query)
            return [self._map_to_model(record) for record in records]

    async def get_by_id(self, id: int) -> Optional[T]:
        async with self._pool.acquire() as conn:
            query = f'SELECT * FROM {self._table_name} WHERE id = $1;'
            record = await conn.fetchrow(query, id)
            return self._map_to_model(record) if record else None

    async def create(self, model: T) -> T:
        data = {k: v for k, v in self._map_to_db(model).items() if v is not None}

        columns = ', '.join(data.keys())
        placeholders = ', '.join([f'${i+1}' for i in range(len(data))])

        async with self._pool.acquire() as conn:
            query = f'''
                INSERT INTO {self._table_name} ({columns})
                VALUES ({placeholders})
                RETURNING *;
            '''
            record = await conn.fetchrow(query, *data.values())
            return self._map_to_model(record)

    async def update(self, id: int, model: T) -> Optional[T]:

        data = self._map_to_db(model)

        set_clause = ', '.join([f'{key} = ${i+2}' for i, key in enumerate(data.keys())])
        async with self._pool.acquire() as conn:
            query = f'''
                UPDATE {self._table_name}
                SET {set_clause}
                WHERE id = $1
                RETURNING *;
            '''
            record = await conn.fetchrow(query, id, *data.values())
            return self._map_to_model(record) if record else None

    async def delete(self, id: int) -> bool:
        async with self._pool.acquire() as conn:
            query = f'DELETE FROM {self._table_name} WHERE id = $1;'
            result = await conn.execute(query, id)
            return 'DELETE 1' in result

    async def close(self):
        if self._pool:
            await self._pool.close()
