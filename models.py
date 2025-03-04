import atexit
import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Integer, String, DateTime, func
from sqlalchemy.orm import mapped_column, Mapped
import os



POSTGRES_USER = os.getenv("POSTGRES_USER", "user")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "123456")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "127.0.0.1")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5431")
POSTGRES_DB = os.getenv("POSTGRES_DB", "netology")

PG_DSN = (
    f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@"
    f"{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)

engine = create_engine(PG_DSN)
Session = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    
    @property
    def id_dict(self):
        return {"id": self.id}


class Advertisment(Base):
    __tablename__ = "app_user"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    Title: Mapped[str] = mapped_column(String, nullable=False)
    Body: Mapped[str] = mapped_column(String, nullable=False)
    Create_time: Mapped[datetime.datetime] = mapped_column(
        DateTime,
        server_default=func.now()
    )
    Owner: Mapped[str] = mapped_column(String, nullable=False)
    

    @property
    def dict(self):
        return {
            "id": self.id,
            "Title": self.Title,
            "Body": self.Body,
            "Create_time": self.Create_time.isoformat(),
            "Owner": self.Owner
        }


Base.metadata.create_all(bind=engine)


atexit.register(engine.dispose)