from typing import List

from app.user.adapter.output.persistence.entities.UserSQLModelEntity import UserSQLModelEntity
from app.user.application.error.UserNotFoundError import UserNotFoundError
from app.user.application.port.input.CreateUserCommand import CreateUserCommand
from app.user.application.port.input.GetUsersCommand import GetUsersCommand
from app.user.application.port.input.UpdateUserCommand import UpdateUserCommand
from app.user.domain.User import User
from fastapi import Depends
from sqlmodel import Session, select

from app.user.adapter.output.persistence.entities.UserMapper import UserMapper
from app.user.application.port.output.repository.UserRepository import UserRepository
from core.db.dependency import get_session


class UserSQLModelRepository(UserRepository):

    def __init__(self, session: Session = Depends(get_session)):
        self.mapper = UserMapper
        self.session = session

    async def create(self, cmd: CreateUserCommand) -> User:
        user = UserSQLModelEntity(
            name=cmd.name, provider=cmd.provider, email=cmd.email, profile=cmd.profile
        )
        print(user)

        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)

        return self.mapper.map_to_domain(user)

    async def get(self, id: str) -> User:
        user = await self._get_by_id(id)
        return self.mapper.map_to_domain(user)

    async def get_all(self, cmd: GetUsersCommand) -> List[User]:

        statement = select(UserSQLModelEntity)
        if cmd.name:
            statement = statement.where(UserSQLModelEntity.name == cmd.name)
        if cmd.provider:
            statement = statement.where(UserSQLModelEntity.provider == cmd.provider)
        if cmd.email:
            statement = statement.where(UserSQLModelEntity.email == cmd.email)
        if cmd.profile:
            statement = statement.where(UserSQLModelEntity.profile == cmd.profile)

        users = self.session.exec(statement).all()

        return [self.mapper.map_to_domain(user) for user in users]

    async def update(self, cmd: UpdateUserCommand) -> User:
        user = await self._get_by_id(cmd.id)

        if cmd.name is not None:
            user.name = cmd.name
        if cmd.email is not None:
            user.email = cmd.email
        if cmd.profile is not None:
            user.profile = cmd.profile
        if cmd.provider is not None:
            user.provider = cmd.provider

        self.session.commit()
        self.session.refresh(user)

        return self.mapper.map_to_domain(user)

    async def delete(self, id: str) -> None:
        user = await self._get_by_id(id)

        self.session.delete(user)
        self.session.commit()

    async def _get_by_id(self, id: str) -> UserSQLModelEntity:
        user = self.session.get(UserSQLModelEntity, id)
        if not user:
            raise UserNotFoundError(f"User with ID '{id}' not found")
        return user
