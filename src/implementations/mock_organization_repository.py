from dataclasses import asdict

from domain.entities.organization import Organization
from domain.organization_repository import OrganizationRepository


class MockOrganizationRepository(OrganizationRepository):

    def __init__(self):
        self.mocks: list[Organization] = [
            Organization(
                id="repetitors",
                name="Ваш репетитор",
                links=["https://repetitors.info/"],
                phones=[]
            ),
            Organization(
                id="hands",
                name="Руки",
                links=["https://hands.ru/company/about/"],
                phones=[]
            ),
        ]

    async def get_organizations(self) -> list[Organization]:
        return self.mocks

    async def insert_organization(self, organization: Organization):
        print("Organization insert into storage", asdict(organization))
