from sqlalchemy import Column, Integer, String, UniqueConstraint, Float, Boolean

from rarity_tools_scraper_data.database import Base


class Collectable(Base):
    __tablename__: str = "collectables"

    id = Column(Integer, primary_key=True, index=True)

    collection_name = Column(String, index=True)
    collection_id = Column(Integer, index=True)

    score = Column(Float)
    rank = Column(Integer)

    stale = Column(Boolean, default=False)

    __table_args__ = (
        UniqueConstraint(
            "collection_name", "collection_id", name="_collection_name_id_uc"
        ),
    )


class Collection(Base):
    __tablename__: str = "collections"

    id = Column(String, primary_key=True, index=True)

    # collectables = https://docs.sqlalchemy.org/en/14/orm/basic_relationships.html#many-to-one

    progress_count = Column(Integer, default=0)
    collectables_count = Column(Integer)
