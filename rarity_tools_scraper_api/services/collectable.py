from fastapi import APIRouter, Path, Depends
from fastapi_cache.decorator import cache
from sqlalchemy.orm import Session

from rarity_tools_scraper_data import models
from rarity_tools_scraper_data.database import get_db
from rarity_tools_scraper_lib.data import (
    handle_collectable_data,
    generate_collection_string,
)

router = APIRouter(prefix="/collectable")


@router.get("/score/{collection_id}/{collectable_id}")
@cache(expire=60 * 60 * 24)
async def collectable_score(
    collection_id: str = Path(default="", description="ID of the desired collection"),
    collectable_id: str = Path(default="", description="ID of the desired collectable"),
    db: Session = Depends(get_db),
) -> str:
    collectable = (
        db.query(models.Collectable)
        .filter(
            models.Collectable.id
            == generate_collection_string(collection_id, collectable_id)
        )
        .first()
    )

    if collectable is None or collectable.stale is True:
        score, rank = handle_collectable_data(collection_id, collectable_id)

        collectable = models.Collectable(
            id=generate_collection_string(collection_id, collectable_id),
            collection_id=collectable_id,
            collection_name=collection_id,
            score=score,
            rank=int(rank),
        )

        db.query(models.Collectable).filter(
            models.Collectable.id
            == generate_collection_string(collection_id, collectable_id)
        ).delete()

        db.add(collectable)
        db.commit()
        db.refresh(collectable)

    return "{rank}-{score}".format(rank=collectable.rank, score=collectable.score)
