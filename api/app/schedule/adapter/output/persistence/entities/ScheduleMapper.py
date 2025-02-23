
import datetime

from app.schedule.adapter.output.persistence.entities.ScheduleSQLModelEntity import (
    ScheduleSQLModelEntity,
)
from app.schedule.domain.Schedule import Schedule


class ScheduleMapper:

    @staticmethod
    def map_to_domain(sqlmodel_entity: ScheduleSQLModelEntity):
        return Schedule(
            id=sqlmodel_entity.id,
            dog_id=sqlmodel_entity.dog_id,
            title=sqlmodel_entity.title,
            content=sqlmodel_entity.content,
            complete=sqlmodel_entity.complete,
            scheduled_at=sqlmodel_entity.scheduled_at.replace(tzinfo=datetime.UTC),
        )

    @staticmethod
    def map_to_sqlmodel(domain_entity: Schedule):
        return ScheduleSQLModelEntity(
            id=domain_entity.id,
            dog_id=domain_entity.dog_id,
            title=domain_entity.title,
            content=domain_entity.content,
            complete=domain_entity.complete,
            scheduled_at=domain_entity.scheduled_at,
        )