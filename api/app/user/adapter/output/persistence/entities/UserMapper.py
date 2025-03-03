from app.user.adapter.output.persistence.entities.UserSQLModelEntity import UserSQLModelEntity
from app.user.domain.User import User


class UserMapper:

    @staticmethod
    def map_to_domain(sqlmodel_entity: UserSQLModelEntity):
        return User(
            id=sqlmodel_entity.id,
            name=sqlmodel_entity.name,
            password=sqlmodel_entity.password,
            provider=sqlmodel_entity.provider,
            email=sqlmodel_entity.email,
            profile=sqlmodel_entity.profile
        )

    @staticmethod
    def map_to_sqlmodel(domain_entity: User):
        return UserSQLModelEntity(
            id=domain_entity.id,
            name=domain_entity.name,
            password=domain_entity.password,
            provider=domain_entity.provider,
            email=domain_entity.email,
            profile=domain_entity.profile
        )