import datetime

from app.treat_record.adapter.output.persistence.entities.TreatRecordSQLModelEntity import (
    TreatRecordSQLModelEntity,
)
from app.treat_record.domain.TreatRecord import TreatRecord


class TreatRecordMapper:

    @staticmethod
    def map_to_domain(sqlmodel_entity: TreatRecordSQLModelEntity):
        return TreatRecord(
            id=sqlmodel_entity.id,
            dog_id=sqlmodel_entity.dog_id,
            user_id=sqlmodel_entity.user_id,
            treat_id=sqlmodel_entity.treat_id,
            quantity=sqlmodel_entity.quantity,
            given_at=sqlmodel_entity.given_at.replace(tzinfo=datetime.UTC),
            description=sqlmodel_entity.description,
            photo_url=sqlmodel_entity.photo_url
        )

    @staticmethod
    def map_to_sqlmodel(domain_entity: TreatRecord):
        return TreatRecordSQLModelEntity(
            id=domain_entity.id,
            dog_id=domain_entity.dog_id,
            user_id=domain_entity.user_id,
            treat_id=domain_entity.treat_id,
            quantity=domain_entity.quantity,
            given_at=domain_entity.given_at,
            description=domain_entity.description,
            photo_url=domain_entity.photo_url
        )