from sqlalchemy import Column, String, Integer, DateTime, func

from app.models import Base


class UsersInfoModel(Base):
    __tablename__ = 'users_info'

    id = Column(Integer, primary_key=True, autoincrement=False)

    telegram_id = Column(Integer, nullable=False, unique=True)

    first_name = Column(String(255))
    last_name = Column(String(255))
    user_name = Column(String(255))
    language_code = Column(String(50))

    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())


class MusicModel(Base):
    __tablename__ = 'music'

    id = Column(Integer, primary_key=True, autoincrement=False)

    artist = Column(String(255))
    title = Column(String(255))
    duration = Column(String(255))
    v_url = Column(String(255), nullable=False)

    s3_url = Column(String(), nullable=False)

    time_created = Column(DateTime(timezone=True), server_default=func.now())


class UsersStatsModel(Base):
    __tablename__ = 'users_stats'

    id = Column(Integer, primary_key=True, autoincrement=False)

    is_user = Column()
    is_music = Column()

    time_created = Column(DateTime(timezone=True), server_default=func.now())
