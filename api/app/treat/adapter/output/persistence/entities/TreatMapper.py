from app.treat.adapter.output.persistence.entities.TreatSQLModelEntity import TreatSQLModelEntity
from app.treat.domain.Treat import Treat


class TreatMapper:

    @staticmethod
    def map_to_domain(sqlmodel_entity: TreatSQLModelEntity):
        return Treat(
            id=sqlmodel_entity.id,
            name=sqlmodel_entity.name,
            dog_id=sqlmodel_entity.dog_id,
            description=sqlmodel_entity.description,
        )

    @staticmethod
    def map_to_sqlmodel(domain_entity: Treat):
        return TreatSQLModelEntity(
            id=domain_entity.id,
            name=domain_entity.name,
            dog_id=domain_entity.dog_id,
            description=domain_entity.description
        )