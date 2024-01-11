from sqlalchemy import Table, Column, Integer, String, MetaData

metadata = MetaData()

User = Table(
    "user",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("email", String, nullable=False),
    Column("password", String, nullable=False)
)