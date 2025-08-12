from fastapi import APIRouter, File, UploadFile, status

from app.schemas.dataset import PresignedUrlResponse
from app.service.dataset import dataset_service


router = APIRouter(prefix="/v1/datasets", tags=["datasets"])


@router.post(
    "/upload",
    summary="MinIO presigned URL 발급",
    description="클라이언트가 직접 MinIO 에 파일을 업로드하기 전에, presigned URL을 발급받습니다.",
    response_model=PresignedUrlResponse,
    status_code=status.HTTP_201_CREATED,
)
async def generate_pre_signed_url(file: UploadFile = File(...)):

    file_name = file.filename
    result = await dataset_service.generate_pre_signed_url(file_name)

    return PresignedUrlResponse(**result)