"""add_helloflag_theme

Revision ID: c7a2e91f4d38
Revises: b3f1c0d7ae21
Create Date: 2026-09-06 00:00:00.000000

"""
from uuid import uuid4

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "c7a2e91f4d38"
down_revision = "b3f1c0d7ae21"
branch_labels = None
depends_on = None

THEME_NAME = "HelloFlag"
THEME_FILE = "helloflag.min.css"

theme = sa.table(
    "theme",
    sa.column("id", sa.Integer),
    sa.column("uuid", sa.String),
    sa.column("_name", sa.Unicode),
)
theme_file = sa.table(
    "theme_file",
    sa.column("theme_id", sa.Integer),
    sa.column("_file_name", sa.Unicode),
)


def upgrade():
    """Register the HelloFlag theme on installs bootstrapped before it existed"""
    conn = op.get_bind()
    existing = conn.execute(
        sa.select(theme.c.id).where(theme.c._name == THEME_NAME)
    ).first()
    if existing:
        return
    conn.execute(theme.insert().values(uuid=str(uuid4()), _name=THEME_NAME))
    theme_id = conn.execute(
        sa.select(theme.c.id).where(theme.c._name == THEME_NAME)
    ).first()[0]
    conn.execute(theme_file.insert().values(theme_id=theme_id, _file_name=THEME_FILE))


def downgrade():
    conn = op.get_bind()
    row = conn.execute(sa.select(theme.c.id).where(theme.c._name == THEME_NAME)).first()
    if not row:
        return
    conn.execute(theme_file.delete().where(theme_file.c.theme_id == row[0]))
    conn.execute(theme.delete().where(theme.c.id == row[0]))
