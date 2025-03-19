import os
from dotenv import load_dotenv
load_dotenv()
from sqlalchemy import BigInteger, Integer, String,DateTime, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.types import JSON
from sqlalchemy import select, insert, update, Column, DateTime
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
import datetime

class Base(AsyncAttrs, DeclarativeBase):
    pass
class Orders(Base):
    __tablename__ = 'orders'
    id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    odata = mapped_column(JSON)
    odate = mapped_column(DateTime, default=datetime.datetime.now())
    isaccepted:Mapped[int] = mapped_column(nullable=False)
    iscooking:Mapped[bool] = mapped_column(nullable=False)
    isready:Mapped[bool] = mapped_column(nullable=False)
    ispayed:Mapped[bool] = mapped_column(nullable=False)
    def str(self):
        return f"VkPostsRaw(id={self.id}, oData={self.odata}, isaccepted={self.isaccepted}, iscooking={self.isaccepted}, isready={self.isready}, ispayed={self.ispayed}"
    
engine = create_async_engine(url=os.getenv("DATABASE_URL"))
async_session = async_sessionmaker(engine)

async def async_main():
    async with engine.begin() as conn:
        #await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)