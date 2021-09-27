from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from rarity_tools_scraper_lib import env

engine = create_engine(
    # postgresql+psycopg2://user:password@host:port/dbname[?key=value&key=value...]
    env.env("DATABASE_URL", default=None),
    isolation_level="SERIALIZABLE",
    connect_args={"check_same_thread": False},
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
