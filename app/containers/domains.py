from dependency_injector import containers, providers
from app.crud.dataset import DatasetCRUD
from app.service.dataset import DatasetService

class DomainsContainer(containers.DeclarativeContainer):
    infra = providers.DependenciesContainer()

    # Repositories 
    dataset_crud = providers.Factory(
        DatasetCRUD,
        session=infra.session,
    )

    # Services
    dataset_service = providers.Factory(
        DatasetService,
        s3=infra.s3,
        crud=dataset_crud
    )