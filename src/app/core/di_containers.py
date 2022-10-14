from dependency_injector import containers, providers

from src.app.core.repositories.users import UsersRepository
from src.app.core.services.auth import AuthService
from src.app.core.services.jwt import JWTService
from src.app.core.services.users import UsersService


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "src.app.api.v1.auth.endpoints.auth",
            "src.app.api.v1.users.endpoints.users",
        ]
    )

    # repositories
    users_repository = providers.Singleton(UsersRepository)

    # services
    jwt_service = providers.Singleton(JWTService)
    auth_service = providers.Singleton(AuthService)
    users_service = providers.Singleton(
        UsersService, users_repository=users_repository, auth_service=auth_service
    )
