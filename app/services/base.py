from abc import ABC, abstractmethod


class BaseService(ABC):
    """
    Base class for application services.

    All application services should inherit from this class.
    """

    @abstractmethod
    async def health_check(self) -> bool:
        """
        Basic service health check.
        """
        raise NotImplementedError
