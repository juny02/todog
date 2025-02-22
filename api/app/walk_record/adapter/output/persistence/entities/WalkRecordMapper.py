import datetime

from app.walk_record.adapter.output.persistence.entities.WalkRecordSQLModelEntity import (
    WalkRecordSQLModelEntity,
)
from app.walk_record.domain.WalkRecord import WalkRecord


class WalkRecordMapper:

    @staticmethod
    def map_to_domain(sqlmodel_entity: WalkRecordSQLModelEntity):
        return WalkRecord(
            id=sqlmodel_entity.id,
            dog_id=sqlmodel_entity.dog_id,
            user_id=sqlmodel_entity.user_id,
            start_time=sqlmodel_entity.start_time.replace(tzinfo=datetime.UTC),
            end_time=sqlmodel_entity.end_time.replace(tzinfo=datetime.UTC),
            description=sqlmodel_entity.description,
            photo_url=sqlmodel_entity.photo_url,
        )

    @staticmethod
    def map_to_sqlmodel(domain_entity: WalkRecord):
        return WalkRecordSQLModelEntity(
            id=domain_entity.id,
            dog_id=domain_entity.dog_id,
            user_id=domain_entity.user_id,
            start_time=domain_entity.start_time,
            end_time=domain_entity.end_time,
            description=domain_entity.description,
            photo_url=domain_entity.photo_url,
        )
