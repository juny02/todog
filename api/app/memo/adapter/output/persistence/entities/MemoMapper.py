
import datetime

from app.memo.adapter.output.persistence.entities.MemoSQLModelEntity import (
    MemoSQLModelEntity,
)
from app.memo.domain.Memo import Memo


class MemoMapper:

    @staticmethod
    def map_to_domain(sqlmodel_entity: MemoSQLModelEntity):
        return Memo(
            id=sqlmodel_entity.id,
            dog_id=sqlmodel_entity.dog_id,
            user_id=sqlmodel_entity.user_id,
            content=sqlmodel_entity.content,
            fixed=sqlmodel_entity.fixed,
            created_at=sqlmodel_entity.created_at.replace(tzinfo=datetime.UTC),
        )

    @staticmethod
    def map_to_sqlmodel(domain_entity: Memo):
        return MemoSQLModelEntity(
            id=domain_entity.id,
            dog_id=domain_entity.dog_id,
            user_id=domain_entity.user_id,
            content=domain_entity.content,
            fixed=domain_entity.fixed,
            created_at=domain_entity.created_at,
        )