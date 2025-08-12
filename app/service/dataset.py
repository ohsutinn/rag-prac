import uuid
import boto3
from botocore.config import Config
from datetime import datetime, timezone

from app.core.config import settings

s3 = boto3.client(
    "s3",
    endpoint_url=settings.MINIO_ENDPOINT,
    aws_access_key_id=settings.MINIO_ACCESS_KEY,
    aws_secret_access_key=settings.MINIO_SECRET_KEY,
    config=Config(s3={"addressing_style": "path"}),
    region_name=settings.REGION,
)


class dataset_service:

    async def generate_pre_signed_url(file_name: str):

        # key 생성
        date = datetime.now(timezone.utc).strftime("%Y/%m/%d")
        u8 = uuid.uuid4().hex[:8]
        key = f"datasets/{date}/{file_name}/{u8}"

        # pre_signed_url 생성
        try:
            url = s3.generate_presigned_url(
                ClientMethod="put_object",
                Params={
                    "Bucket": settings.BUCKET,
                    "Key": key,
                },
                ExpiresIn=3600,
            )

        except Exception as e:
            return {"message": "presigned URL 생성 실패", "error": str(e)}

        return {"key": key, "upload_url": url}
