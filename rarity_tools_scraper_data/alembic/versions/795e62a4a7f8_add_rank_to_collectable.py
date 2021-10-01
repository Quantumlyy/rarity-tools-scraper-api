"""add rank to collectable

Revision ID: 795e62a4a7f8
Revises: 411e982acb3a
Create Date: 2021-10-01 21:39:06.805661

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "795e62a4a7f8"
down_revision = "411e982acb3a"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("collectables", sa.Column("rank", sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("collectables", "rank")
    # ### end Alembic commands ###
