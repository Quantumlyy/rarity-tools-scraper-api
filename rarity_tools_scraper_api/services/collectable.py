from fastapi import APIRouter, Path, Depends
from fastapi_cache.decorator import cache
from sqlalchemy.orm import Session

from rarity_tools_scraper_data import models
from rarity_tools_scraper_data.database import get_db
from rarity_tools_scraper_lib.data import get_collectable_score, get_collectable_rank

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
            models.Collectable.collection_id == collectable_id,
            models.Collectable.collection_name == collection_id,
        )
        .first()
    )

    if collectable is None or collectable.stale is True:
        score_element, score_driver = get_collectable_score(
            collection_id, collectable_id
        )
        score = score_element.text
        score_driver.close()

        rank_element, rank_driver = get_collectable_rank(collection_id, collectable_id)
        rank = rank_element.text.split("#")[1]
        rank_driver.close()

        collectable = models.Collectable(
            collection_id=collectable_id,
            collection_name=collection_id,
            score=score,
            rank=int(rank),
        )

        db.query(models.Collectable).filter(
            models.Collectable.collection_id == collectable_id,
            models.Collectable.collection_name == collection_id,
        ).delete()

        db.add(collectable)
        db.commit()
        db.refresh(collectable)

    return "{rank}-{score}".format(rank=collectable.rank, score=collectable.score)
