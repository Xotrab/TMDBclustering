from models.base import Base
from sqlalchemy.orm import Mapped, mapped_column

class Company(Base):
    __tablename__ = 'companies'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    origin_country: Mapped[str] = mapped_column(nullable=False)

    def __repr__(self) -> str:
        return f'<Company id={self.id}, name={self.name}, origin_country={self.origin_country}>'