from typing import List

from fastapi import Depends
from sqlmodel import Session, select

from app.dog.adapter.output.persistence.repository.DogSQLModelRepository import (
    DogSQLModelRepository,
)
from app.dog.application.error.DogNotFoundError import DogNotFoundError
from app.dog.application.port.output.repository.DogRepository import DogRepository
from app.treat.adapter.output.persistence.entities.TreatMapper import TreatMapper
from app.treat.adapter.output.persistence.entities.TreatSQLModelEntity import (
    TreatSQLModelEntity,
)
from app.treat.application.error.TreatNotFoundError import TreatNotFoundError
from app.treat.application.error.TreatOwnershipError import TreatOwnershipError
from app.treat.application.port.input.CreateTreatCommand import CreateTreatCommand
from app.treat.application.port.input.UpdateTreatCommand import UpdateTreatCommand
from app.treat.application.port.output.repository.TreatRepository import TreatRepository
from app.treat.domain.Treat import Treat
from core.db.dependency import get_session


class TreatSQLModelRepository(TreatRepository):

    def __init__(
        self,
        session: Session = Depends(get_session),
        dog_repo: DogRepository = Depends(DogSQLModelRepository),
    ):
        self.mapper = TreatMapper
        self.session = session
        self.dog_repo = dog_repo

    async def create(self, cmd: CreateTreatCommand) -> Treat:

        if await self.dog_repo.get(cmd.dog_id) is None:
            raise DogNotFoundError(f"Dog with id '{cmd.dog_id}' does not exist.")

        treat = TreatSQLModelEntity(
            name=cmd.name, dog_id=cmd.dog_id, description=cmd.description
        )

        self.session.add(treat)
        self.session.commit()
        self.session.refresh(treat)

        return self.mapper.map_to_domain(treat)

    async def get(self, id: str, dog_id: str) -> Treat:
        treat = await self._get_by_id_for_dog(id=id, dog_id=dog_id)
        return self.mapper.map_to_domain(treat)

    async def get_all_by_dog(self, dog_id: str) -> List[Treat]:
        
        if await self.dog_repo.get(dog_id) is None:
            raise DogNotFoundError(f"Dog with id '{dog_id}' does not exist.")


        statement = select(TreatSQLModelEntity)
        statement = statement.where(TreatSQLModelEntity.dog_id == dog_id)

        treats = self.session.exec(statement).all()

        return [self.mapper.map_to_domain(treat) for treat in treats]

    async def update(self, cmd: UpdateTreatCommand) -> Treat:
        treat = await self._get_by_id_for_dog(id=cmd.id, dog_id=cmd.dog_id)
        if cmd.name is not None:
            treat.name = cmd.name
        if cmd.description is not None:
            treat.description = cmd.description

        self.session.commit()
        self.session.refresh(treat)

        return self.mapper.map_to_domain(treat)

    async def delete(self, id: str,  dog_id: str) -> None:
        treat = await self._get_by_id_for_dog(id=id, dog_id=dog_id)

        self.session.delete(treat)
        self.session.commit()

    async def _get_by_id(self, id: str) -> TreatSQLModelEntity:
        treat = self.session.get(TreatSQLModelEntity, id)
        if not treat:
            raise TreatNotFoundError(f"Treat with ID '{id}' not found")
        return treat
    
    async def _get_by_id_for_dog(self, id: str, dog_id: str) -> TreatSQLModelEntity:
        treat = self.session.get(TreatSQLModelEntity, id)
        if not treat:
            raise TreatNotFoundError(f"Treat with ID '{id}' not found")
        if treat.dog_id != dog_id:
            raise TreatOwnershipError(f"Treat {id} does not belong to Dog {dog_id}.")
        
        return treat
    

