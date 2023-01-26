from abc import ABC, abstractmethod

from domain.entities.organization import Organization


class OrganizationRepository(ABC):

    @abstractmethod
    async def get_organizations(self) -> list[Organization]:
        ...

    @abstractmethod
    async def insert_organization(self, organization: Organization):
        ...
