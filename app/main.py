from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy import text

from app.api.v1 import dataset_router
from app.database.session import get_db

app = FastAPI(
    title="RAG-PRAC",
    description="API for the application",
    version="1.0.0",
)

app.include_router(dataset_router.router)


@app.get(
    "/health",
    summary="Health check",
    description="데이터베이스 연결 상태를 확인합니다.",
    status_code=status.HTTP_200_OK,
)
async def health_check(db=Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {
            "status": "ok",
            "db": "ok",
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "status": "fail",
                "db": "fail",
                "error": str(e),
            },
        )
