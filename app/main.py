from fastapi import FastAPI, HTTPException, Request, status
from sqlalchemy import text

from app.api.v1 import dataset_router
from app.containers.main import MainContainer


def create_app() -> FastAPI:
    app = FastAPI(
        title="RAG-PRAC",
        description="API for the application",
        version="1.0.0",
    )

    container = MainContainer()
    app.container = container

    app.add_event_handler("startup", container.init_resources)   # 서버 시작 시 리소스 준비
    app.add_event_handler("shutdown", container.shutdown_resources) # 서버 종료 시 리소스 정리

    app.include_router(dataset_router.router)
    
    @app.get("/health", status_code=status.HTTP_200_OK, summary="Health check")
    async def health_check(request: Request):
        infra = request.app.container.infra()

        db = await infra.db_session()
        try:
            await db.execute(text("SELECT 1"))
            return {"status": "ok", "db": "ok"}
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"status": "fail", "db": "fail", "error": str(e)},
            )
        finally:
            await db.close()

    return app


app = create_app()