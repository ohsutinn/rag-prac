from dependency_injector import containers, providers
from app.core.config import settings
from app.database.session import AsyncSessionFactory
import boto3
from botocore.config import Config as BotoConfig

class InfraContainer(containers.DeclarativeContainer):
    config = providers.Object(settings)

    # 세션 팩토리 provider
    session_factory = providers.Object(AsyncSessionFactory)

    # 요청 범위 세션 리소스
    async def _session_resource(factory):
        async with factory() as session:
            yield session

    db_session = providers.Resource(_session_resource, session_factory)
    
    # S3 client
    s3 = providers.Singleton(
        boto3.client,
        "s3",
        endpoint_url=config.provided.MINIO_ENDPOINT,
        aws_access_key_id=config.provided.MINIO_ACCESS_KEY,
        aws_secret_access_key=config.provided.MINIO_SECRET_KEY,
        config=BotoConfig(s3={"addressing_style": "path"}),
        region_name=config.provided.REGION,
    )