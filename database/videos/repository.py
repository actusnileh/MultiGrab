from sqlalchemy import desc, select

from database.database import async_session_maker
from database.repository import BaseRepository
from database.videos.models import Videos


class VideoRepository(BaseRepository):
    model = Videos

    @classmethod
    async def find_by_filter_with_pagination(cls, offset=0, limit=None, reverse=True, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            if reverse:
                query = query.order_by(
                    desc(cls.model.id)
                )

            if limit is not None:
                query = query.limit(limit)

            if offset is not None:
                query = query.offset(offset)

            result = await session.execute(query)
            return result.scalars().all()
