from dataclasses import dataclass
import datetime
from enum import Enum
from typing import Optional
from sqlalchemy import Column, DateTime, Integer, String, func, Enum as SAEnum

from app.database.base import Base


class FileStatus(str, Enum):
    UPLOADED = "UPLOADED"
    PROCESSED = "PROCESSED"
    FAILED = "FAILED"


class DatasetORM(Base):
    __tablename__ = "datasets"

    id = Column(Integer, primary_key=True, index=True)
    bucket = Column(String, nullable=False)
    object_key = Column(String, nullable=False, unique=True)
    filename = Column(String, nullable=False)
    content_type = Column(String, nullable=True)
    size_bytes = Column(Integer, nullable=True)
    etag = Column(String, nullable=True)
    version_id = Column(String, nullable=True)
    status = Column(SAEnum(FileStatus), nullable=False, default=FileStatus.UPLOADED)
    created_at = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
    deleted_at = Column(DateTime(timezone=True), nullable=True)


@dataclass(kw_only=True)
class DatasetEntity:
    id: Optional[int] = None
    bucket: str
    object_key: str
    filename: str
    content_type: Optional[str] = None
    size_bytes: Optional[int] = None
    etag: Optional[str] = None
    version_id: Optional[str] = None
    status: FileStatus = FileStatus.UPLOADED
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    def mark_uploaded(
        self, etag: str, size: int, version_id: Optional[str] = None
    ) -> None:
        self.etag = etag
        self.size_bytes = size
        self.version_id = version_id
        self.status = FileStatus.UPLOADED


def to_entity(row: DatasetORM) -> DatasetEntity:
    return DatasetEntity(
        id=row.id,
        bucket=row.bucket,
        object_key=row.object_key,
        filename=row.filename,
        content_type=row.content_type,
        size_bytes=row.size_bytes,
        etag=row.etag,
        version_id=row.version_id,
        status=row.status,
        created_at=row.created_at,
        updated_at=row.updated_at,
        deleted_at=row.deleted_at,
    )


def to_orm(entity: DatasetEntity) -> DatasetORM:
    return DatasetORM(
        bucket=entity.bucket,
        object_key=entity.object_key,
        filename=entity.filename,
        content_type=entity.content_type,
        size_bytes=entity.size_bytes,
        etag=entity.etag,
        version_id=entity.version_id,
        status=entity.status,
        deleted_at=entity.deleted_at,
    )
