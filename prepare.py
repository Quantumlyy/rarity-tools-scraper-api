#!/usr/bin/env python3
import click
from sqlalchemy.orm import scoped_session

from rarity_tools_scraper_data import models, database
from rarity_tools_scraper_lib import data


@click.command()
@click.option(
    "--collection", prompt="Target collection", help="The collection to scrape."
)
@click.option("--size", prompt="Size of the collection")
def prepare(collection, size):
    db = scoped_session(database.SessionLocal)
    collection_entry = database.get_or_create(
        db, models.Collection, id=collection, collectables_count=size
    )

    db.refresh(collection_entry)

    for i in range(
        collection_entry.progress_count, collection_entry.collectables_count + 1
    ):
        i += 1

        score, rank = data.handle_collectable_data(collection, i)

        collectable = models.Collectable(
            collection_id=i,
            collection_name=collection,
            score=score,
            rank=int(rank),
        )
        collection_entry.progress_count = i

        db.query(models.Collectable).filter(
            models.Collectable.collection_id == i,
            models.Collectable.collection_name == collection,
        ).delete()

        db.add(collectable)
        db.commit()
        db.refresh(collectable)

        print(
            "[{collection}] Completed {id}/{size} - {percentage}%".format(
                id=i,
                size=size,
                collection=collection,
                percentage=(100 * float(i) / float(size)),
            )
        )

    print("[{collection}] Complete".format(collection=collection))
    db.remove()


if __name__ == "__main__":
    prepare()
