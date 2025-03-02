import datetime

from app.medicine_schedule.adapter.output.persistence.entities.MedScheduleSQLModelEntity import (
    MedScheduleSQLModelEntity,
)
from app.medicine_schedule.domain.MedSchedule import MedSchedule


class MedScheduleMapper:

    @staticmethod
    def map_to_domain(sqlmodel_entity: MedScheduleSQLModelEntity):
        return MedSchedule(
            id=sqlmodel_entity.id,
            dog_id=sqlmodel_entity.dog_id,
            medicine_name=sqlmodel_entity.medicine_name,
            dosage=sqlmodel_entity.dosage,
            daily_doses=sqlmodel_entity.daily_doses,
            dose_times=sqlmodel_entity.dose_times,
            type=sqlmodel_entity.type,
            interval_days=sqlmodel_entity.interval_days,
            start=sqlmodel_entity.start.replace(tzinfo=datetime.UTC),
            end=(
                sqlmodel_entity.end.replace(tzinfo=datetime.UTC)
                if sqlmodel_entity.end
                else None
            ),
            notes=sqlmodel_entity.notes,
        )

    @staticmethod
    def map_to_sqlmodel(domain_entity: MedSchedule):
        return MedScheduleSQLModelEntity(
            id=domain_entity.id,
            dog_id=domain_entity.dog_id,
            medicine_name=domain_entity.medicine_name,
            dosage=domain_entity.dosage,
            daily_doses=domain_entity.daily_doses,
            dose_times=domain_entity.dose_times,
            type=domain_entity.type,
            interval_days=domain_entity.interval_days,
            start=domain_entity.start,
            end=domain_entity.end,
            notes=domain_entity.notes,
        )
