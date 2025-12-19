from postgresql_repository.base_postgresql_repository import BasePostgreSQLRepository
from postgresql_repository.models.database_connection import DatabaseConnection
from datetime import datetime, timedelta

from .models.lead import Lead
from .models.statistic import Statistic


class LeadRepository(BasePostgreSQLRepository):
    def __init__(self, db_connection: DatabaseConnection):
        self._db_connection = db_connection
        super().__init__(db_connection, "Lead", Lead)

    async def get_registration_stats(self) -> Statistic:
        async with self._pool.acquire() as conn:
            now = datetime.now()

            start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
            start_of_week = start_of_day - timedelta(days=now.weekday())
            start_of_month = now.replace(
                day=1, hour=0, minute=0, second=0, microsecond=0
            )

            query = """
            SELECT 
                -- Общая статистика
                COUNT(*) as total,
                COUNT(*) FILTER (WHERE created_at >= $1) as monthly,
                COUNT(*) FILTER (WHERE created_at >= $2) as weekly,
                COUNT(*) FILTER (WHERE created_at >= $3) as daily,

                -- Статистика по consultation = True
                COUNT(*) FILTER (WHERE consultation = TRUE) as total_consultation,
                COUNT(*) FILTER (WHERE consultation = TRUE AND created_at >= $1) as monthly_consultation,
                COUNT(*) FILTER (WHERE consultation = TRUE AND created_at >= $2) as weekly_consultation,
                COUNT(*) FILTER (WHERE consultation = TRUE AND created_at >= $3) as daily_consultation
            FROM Lead
            """

            record = await conn.fetchrow(
                query, start_of_month, start_of_week, start_of_day
            )
            return Statistic(
                total=record['total'] or 0,
                monthly=record['monthly'] or 0,
                weekly=record['weekly'] or 0,
                daily=record['daily'] or 0,
                total_consultation=record['total_consultation'] or 0,
                monthly_consultation=record['monthly_consultation'] or 0,
                weekly_consultation=record['weekly_consultation'] or 0,
                daily_consultation=record['daily_consultation'] or 0
            )
