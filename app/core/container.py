from functools import lru_cache


class Container:
    """
    Application dependency container.
    """

    def __init__(self) -> None:
        self._services = {}

    def register(
        self,
        name: str,
        service: object,
    ) -> None:
        """
        Register a dependency.
        """

        self._services[name] = service

    def resolve(
        self,
        name: str,
    ) -> object:
        """
        Resolve a dependency.
        """

        return self._services[name]


@lru_cache
def get_container() -> Container:
    """
    Return singleton application container.
    """

    return Container()
