# app/dependencies.py
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_db
from app.service.dataset import DatasetService
import boto3
from botocore.config import Config
from app.core.config import settings

def get_s3():
    return boto3.client(
        "s3",
        endpoint_url=settings.MINIO_ENDPOINT,
        aws_access_key_id=settings.MINIO_ACCESS_KEY,
        aws_secret_access_key=settings.MINIO_SECRET_KEY,
        config=Config(s3={"addressing_style": "path"}),
        region_name=settings.REGION,
    )

def get_dataset_service(
    db: AsyncSession = Depends(get_db),
    s3 = Depends(get_s3),
) -> DatasetService:
    return DatasetService(db=db, s3=s3)