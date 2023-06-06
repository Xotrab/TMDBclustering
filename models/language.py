from models.base import Base
from sqlalchemy.orm import Mapped, mapped_column

class Language(Base):
    __tablename__ = 'languages'

    iso_639_1: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)

    def __repr__(self) -> str:
        return f'<Language iso_639_1={self.iso_639_1}, name={self.name}>'
