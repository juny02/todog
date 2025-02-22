from typing import List

from fastapi import Depends
from sqlmodel import Session, select

from app.dog.adapter.output.persistence.entities.DogMapper import DogMapper
from app.dog.adapter.output.persistence.entities.DogSQLModelEntity import (
    DogSQLModelEntity,
)
from app.dog.application.error.DogNotFoundError import DogNotFoundError
from app.dog.application.port.input.CreateDogCommand import CreateDogCommand
from app.dog.application.port.input.GetDogsCommand import GetDogsCommand
from app.dog.application.port.input.UpdateDogCommand import UpdateDogCommand
from app.dog.application.port.output.repository.DogRepository import DogRepository
from app.dog.domain.Dog import Dog
from core.db.dependency import get_session


class DogSQLModelRepository(DogRepository):

    def __init__(self, session: Session = Depends(get_session)):
        self.mapper = DogMapper
        self.session = session

    async def create(self, cmd: CreateDogCommand) -> Dog:
        dog = DogSQLModelEntity(
            name=cmd.name,
            age=cmd.age,
            photo=cmd.photo,
            species=cmd.species,
            daily_walk_goal=cmd.daily_walk_goal,
            meal_pattern=cmd.meal_pattern,
        )
        print(dog)

        self.session.add(dog)
        self.session.commit()
        self.session.refresh(dog)
        print(dog)

        return self.mapper.map_to_domain(dog)

    async def get(self, id: str) -> Dog:
        dog = await self._get_by_id(id)
        return self.mapper.map_to_domain(dog)

    async def get_all(self, cmd: GetDogsCommand) -> List[Dog]:

        statement = select(DogSQLModelEntity)
        if cmd.name:
            statement = statement.where(DogSQLModelEntity.name == cmd.name)
        if cmd.age:
            statement = statement.where(DogSQLModelEntity.age == cmd.age)
        if cmd.photo:
            statement = statement.where(DogSQLModelEntity.photo == cmd.photo)
        if cmd.species:
            statement = statement.where(DogSQLModelEntity.species == cmd.species)

        dogs = self.session.exec(statement).all()

        return [self.mapper.map_to_domain(dog) for dog in dogs]

    async def update(self, cmd: UpdateDogCommand) -> Dog:
        dog = await self._get_by_id(cmd.id)

        if cmd.name is not None:
            dog.name = cmd.name
        if cmd.age is not None:
            dog.age = cmd.age
        if cmd.photo is not None:
            dog.photo = cmd.photo
        if cmd.species is not None:
            dog.species = cmd.species
        if cmd.daily_walk_goal is not None:
            dog.daily_walk_goal = cmd.daily_walk_goal
        if cmd.meal_pattern is not None:
            dog.meal_pattern = cmd.meal_pattern

        self.session.commit()
        self.session.refresh(dog)

        return self.mapper.map_to_domain(dog)

    async def delete(self, id: str) -> None:
        dog = await self._get_by_id(id)

        self.session.delete(dog)
        self.session.commit()

    async def _get_by_id(self, id: str) -> DogSQLModelEntity:
        dog = self.session.get(DogSQLModelEntity, id)
        if not dog:
            raise DogNotFoundError(f"Dog with ID '{id}' not found")
        return dog
