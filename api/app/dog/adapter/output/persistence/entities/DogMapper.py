from app.dog.adapter.output.persistence.entities.DogSQLModelEntity import (
    DogSQLModelEntity,
)
from app.dog.domain.Dog import Dog


class DogMapper:

    @staticmethod
    def map_to_domain(sqlmodel_entity: DogSQLModelEntity):
        return Dog(
            id=sqlmodel_entity.id,
            name=sqlmodel_entity.name,
            age=sqlmodel_entity.age,
            photo=sqlmodel_entity.photo,
            species=sqlmodel_entity.species,
            daily_walk_goal=sqlmodel_entity.daily_walk_goal,
            meal_pattern=sqlmodel_entity.meal_pattern,
        )

    @staticmethod
    def map_to_sqlmodel(domain_entity: Dog):
        return DogSQLModelEntity(
            id=domain_entity.id,
            name=domain_entity.name,
            age=domain_entity.age,
            photo=domain_entity.photo,
            species=domain_entity.species,
            meal_pattern=domain_entity.meal_pattern,
            daily_walk_goal=domain_entity.daily_walk_goal,
        )
