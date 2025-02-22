from typing import List

from fastapi import Depends
from sqlmodel import Session, select

from app.treat.adapter.output.persistence.entities.TreatMapper import TreatMapper
from app.treat.adapter.output.persistence.entities.TreatSQLModelEntity import (
    TreatSQLModelEntity,
)
from app.treat.application.error.TreatNotFoundError import TreatNotFoundError
from app.treat.application.port.input.CreateTreatCommand import CreateTreatCommand
from app.treat.application.port.input.UpdateTreatCommand import UpdateTreatCommand
from app.treat.application.port.output.repository.TreatRepository import TreatRepository
from app.treat.domain.Treat import Treat
from core.db.dependency import get_session


class TreatSQLModelRepository(TreatRepository):

    def __init__(self, session: Session = Depends(get_session)):
        self.mapper = TreatMapper
        self.session = session

    async def create(self, cmd: CreateTreatCommand) -> Treat:
        treat = TreatSQLModelEntity(
            name=cmd.name, dog_id=cmd.dog_id, description=cmd.description
        )

        self.session.add(treat)
        self.session.commit()
        self.session.refresh(treat)

        return self.mapper.map_to_domain(treat)

    async def get(self, id: str) -> Treat:
        treat = await self._get_by_id(id)
        return self.mapper.map_to_domain(treat)

    async def get_by_dog(self, dog_id: str) -> List[Treat]:

        statement = select(TreatSQLModelEntity)
        statement = statement.where(TreatSQLModelEntity.dog_id == dog_id)

        treats = self.session.exec(statement).all()

        return [self.mapper.map_to_domain(treat) for treat in treats]

    async def update(self, cmd: UpdateTreatCommand) -> Treat:
        treat = await self._get_by_id(cmd.id)

        if cmd.name is not None:
            treat.name = cmd.name
        if cmd.description is not None:
            treat.description = cmd.description

        self.session.commit()
        self.session.refresh(treat)

        return self.mapper.map_to_domain(treat)

    async def delete(self, id: str) -> None:
        treat = await self._get_by_id(id)

        self.session.delete(treat)
        self.session.commit()

    async def _get_by_id(self, id: str) -> TreatSQLModelEntity:
        treat = self.session.get(TreatSQLModelEntity, id)
        if not treat:
            raise TreatNotFoundError(f"Treat with ID '{id}' not found")
        return treat
