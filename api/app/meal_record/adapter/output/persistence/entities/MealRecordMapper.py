import datetime

from app.meal_record.adapter.output.persistence.entities.MealRecordSQLModelEntity import (
    MealRecordSQLModelEntity,
)
from app.meal_record.domain.MealRecord import MealRecord


class MealRecordMapper:

    @staticmethod
    def map_to_domain(sqlmodel_entity: MealRecordSQLModelEntity):
        return MealRecord(
            id=sqlmodel_entity.id,
            dog_id=sqlmodel_entity.dog_id,
            user_id=sqlmodel_entity.user_id,
            given_at=sqlmodel_entity.given_at.replace(tzinfo=datetime.UTC),
            meal_type=sqlmodel_entity.meal_type,
            amount=sqlmodel_entity.amount,
            description=sqlmodel_entity.description,
            photo_url=sqlmodel_entity.photo_url,
        )

    @staticmethod
    def map_to_sqlmodel(domain_entity: MealRecord):
        return MealRecordSQLModelEntity(
            id=domain_entity.id,
            dog_id=domain_entity.dog_id,
            user_id=domain_entity.user_id,
            given_at=domain_entity.given_at,
            meal_type=domain_entity.meal_type,
            amount=domain_entity.amount,
            description=domain_entity.description,
            photo_url=domain_entity.photo_url,
        )
