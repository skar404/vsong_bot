from sqlalchemy import Column, String, Integer, DateTime, func, ForeignKey, Index

from app.models import Base


class UsersInfoModel(Base):
    __tablename__ = 'users_info'

    id = Column(Integer, primary_key=True, autoincrement=True)

    telegram_id = Column(Integer, nullable=False, unique=True)

    first_name = Column(String(255))
    last_name = Column(String(255))
    user_name = Column(String(255))
    language_code = Column(String(50))

    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())


class MusicModel(Base):
    __tablename__ = 'music'

    id = Column(Integer, primary_key=True, autoincrement=True)

    artist = Column(String(255), index=True)
    title = Column(String(255), index=True)
    duration = Column(String(255))
    v_url = Column(String(255), nullable=False)

    vk_id = Column(Integer(), index=True)
    owner_id = Column(Integer(), index=True)

    s3_url = Column(String())

    time_created = Column(DateTime(timezone=True), server_default=func.now(), index=True)

    __table_args__ = (
        Index('ui_music_model_id_owner_id_duration', vk_id, owner_id, artist, title, duration, unique=True),
    )

    async def create_music(self, vk_id, owner_id, url, artist, title, duration):
        pass


class UsersStatsModel(Base):
    __tablename__ = 'users_stats'

    id = Column(Integer, primary_key=True, autoincrement=True)

    is_user = Column(ForeignKey('users_info.id'))
    is_music = Column(ForeignKey('music.id'))

    time_created = Column(DateTime(timezone=True), server_default=func.now())
