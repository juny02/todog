from typing import List

from fastapi import Depends
from sqlmodel import Session, col, select

from app.dog.adapter.output.persistence.repository.DogSQLModelRepository import (
    DogSQLModelRepository,
)
from app.dog.application.error.DogNotFoundError import DogNotFoundError
from app.dog.application.port.output.repository.DogRepository import DogRepository
from app.meal_record.adapter.output.persistence.entities.MealRecordMapper import (
    MealRecordMapper,
)
from app.meal_record.adapter.output.persistence.entities.MealRecordSQLModelEntity import (
    MealRecordSQLModelEntity,
)
from app.meal_record.application.error.MealRecordNotFoundError import (
    MealRecordNotFoundError,
)
from app.meal_record.application.error.MealRecordOwnershipError import MealRecordOwnershipError
from app.meal_record.application.port.input.CreateMealRecordCommand import (
    CreateMealRecordCommand,
)
from app.meal_record.application.port.input.GetMealRecordsCommand import GetMealRecordsCommand
from app.meal_record.application.port.input.UpdateMealRecordCommand import (
    UpdateMealRecordCommand,
)
from app.meal_record.application.port.output.repository.MealRecordRepository import (
    MealRecordRepository,
)
from app.meal_record.domain.MealRecord import MealRecord
from app.user.adapter.output.persistence.repository.UserSQLModelRepository import (
    UserSQLModelRepository,
)
from app.user.application.error.UserNotFoundError import UserNotFoundError
from core.db.dependency import get_session
from core.enums import SortOrder


class MealRecordSQLModelRepository(MealRecordRepository):

    def __init__(
        self,
        session: Session = Depends(get_session),
        dog_repo: DogRepository = Depends(DogSQLModelRepository),
        user_repo: DogRepository = Depends(UserSQLModelRepository),
    ):
        self.mapper = MealRecordMapper
        self.session = session
        self.dog_repo = dog_repo
        self.user_repo = user_repo

    async def create(self, cmd: CreateMealRecordCommand) -> MealRecord:

        if await self.dog_repo.get(cmd.dog_id) is None:
            raise DogNotFoundError(f"Dog with id '{cmd.dog_id}' does not exist.")

        if await self.user_repo.get(cmd.user_id) is None:
            raise UserNotFoundError(f"User with id '{cmd.user_id}' does not exist.")

        meal_record = MealRecordSQLModelEntity(
            dog_id=cmd.dog_id,
            user_id=cmd.user_id,
            given_at=cmd.given_at,
            meal_type=cmd.meal_type,
            amount=cmd.amount,
            photo_url=cmd.photo_url,
            description=cmd.description,
        )

        self.session.add(meal_record)
        self.session.commit()
        self.session.refresh(meal_record)

        return self.mapper.map_to_domain(meal_record)

    async def get(self, id: str, dog_id: str) -> MealRecord:
        meal_record = await self._get_by_id_for_dog(id=id, dog_id=dog_id)
        return self.mapper.map_to_domain(meal_record)

    async def get_all(self, cmd: GetMealRecordsCommand) -> List[MealRecord]:

        if await self.dog_repo.get(cmd.dog_id) is None:
            raise DogNotFoundError(f"Dog with id '{cmd.dog_id}' does not exist.")

        statement = select(MealRecordSQLModelEntity)
        statement = statement.where(MealRecordSQLModelEntity.dog_id == cmd.dog_id)
        
        if cmd.start:
            statement = statement.where(col(MealRecordSQLModelEntity.given_at) >= cmd.start)
        if cmd.end:
            statement = statement.where(col(MealRecordSQLModelEntity.given_at) <= cmd.end)
        
        if cmd.user_id:
            statement = statement.where(MealRecordSQLModelEntity.user_id == cmd.user_id)
        if cmd.meal_type:
            statement = statement.where(MealRecordSQLModelEntity.meal_type == cmd.meal_type)
        if cmd.description:
            statement = statement.where(
                col(MealRecordSQLModelEntity.description).contains(cmd.description)
            )
            
        if cmd.order == SortOrder.DESC:
            statement = statement.order_by(col(MealRecordSQLModelEntity.given_at).desc())
        else:
            statement = statement.order_by(col(MealRecordSQLModelEntity.given_at).asc())


        meal_records = self.session.exec(statement).all()

        return [self.mapper.map_to_domain(meal_record) for meal_record in meal_records]

    async def update(self, cmd: UpdateMealRecordCommand) -> MealRecord:
        meal_record = await self._get_by_id_for_dog(id=cmd.id, dog_id=cmd.dog_id)

        if cmd.user_id is not None:
            if await self.user_repo.get(cmd.user_id) is None:
                raise UserNotFoundError(f"User with id '{cmd.user_id}' does not exist.")
            meal_record.user_id = cmd.user_id
        if cmd.given_at is not None:
            meal_record.given_at = cmd.given_at
        if cmd.meal_type is not None:
            meal_record.meal_type = cmd.meal_type
        if cmd.amount is not None:
            meal_record.amount = cmd.amount
        if cmd.description is not None:
            meal_record.description = cmd.description
        if cmd.photo_url is not None:
            meal_record.photo_url = cmd.photo_url

        self.session.commit()
        self.session.refresh(meal_record)

        return self.mapper.map_to_domain(meal_record)

    async def delete(self, id: str, dog_id: str) -> None:
        meal_record = await self._get_by_id_for_dog(id=id, dog_id=dog_id)

        self.session.delete(meal_record)
        self.session.commit()

    async def _get_by_id(self, id: str) -> MealRecordSQLModelEntity:
        meal_record = self.session.get(MealRecordSQLModelEntity, id)
        if not meal_record:
            raise MealRecordNotFoundError(f"MealRecord with ID '{id}' not found")
        return meal_record

    async def _get_by_id_for_dog(
        self, id: str, dog_id: str
    ) -> MealRecordSQLModelEntity:
        meal_record = self.session.get(MealRecordSQLModelEntity, id)
        if not meal_record:
            raise MealRecordNotFoundError(f"MealRecord with ID '{id}' not found")
        if meal_record.dog_id != dog_id:
            raise MealRecordOwnershipError(
                f"MealRecord {id} does not belong to Dog {dog_id}."
            )

        return meal_record
