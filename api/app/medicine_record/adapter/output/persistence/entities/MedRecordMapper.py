import datetime

from app.medicine_record.adapter.output.persistence.entities.MedRecordSQLModelEntity import (
    MedRecordSQLModelEntity,
)
from app.medicine_record.domain.MedRecord import MedRecord


class MedRecordMapper:

    @staticmethod
    def map_to_domain(sqlmodel_entity: MedRecordSQLModelEntity):
        return MedRecord(
            id=sqlmodel_entity.id,
            dog_id=sqlmodel_entity.dog_id,
            user_id=sqlmodel_entity.user_id,
            given_at=sqlmodel_entity.given_at.replace(tzinfo=datetime.UTC),
            schedule_id=sqlmodel_entity.schedule_id,
            dose_given=sqlmodel_entity.dose_given,
            description=sqlmodel_entity.description,
            photo_url=sqlmodel_entity.photo_url,
        )

    @staticmethod
    def map_to_sqlmodel(domain_entity: MedRecord):
        return MedRecordSQLModelEntity(
            id=domain_entity.id,
            dog_id=domain_entity.dog_id,
            user_id=domain_entity.user_id,
            given_at=domain_entity.given_at,
            schedule_id=domain_entity.schedule_id,
            dose_given=domain_entity.dose_given,
            description=domain_entity.description,
            photo_url=domain_entity.photo_url,
        )
