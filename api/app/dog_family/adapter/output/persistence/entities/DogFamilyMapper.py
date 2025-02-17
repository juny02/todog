
from app.dog_family.adapter.output.persistence.entities.DogFamilySQLModelEntity import (
    DogFamilySQLModelEntity,
)
from app.dog_family.domain.DogFamily import DogFamily


class DogFamilyMapper:

    @staticmethod
    def map_to_domain(sqlmodel_entity: DogFamilySQLModelEntity):
        return DogFamily(
            id=sqlmodel_entity.id,
            dog_id=sqlmodel_entity.dog_id,
            user_id=sqlmodel_entity.user_id,
            user_nickname=sqlmodel_entity.user_nickname,
            dog_nickname=sqlmodel_entity.dog_nickname
        )

    @staticmethod
    def map_to_sqlmodel(domain_entity: DogFamily):
        return DogFamilySQLModelEntity(
            id=domain_entity.id,
            dog_id=domain_entity.dog_id,
            user_id=domain_entity.user_id,
            user_nickname=domain_entity.user_nickname,
            dog_nickname=domain_entity.dog_nickname
        )