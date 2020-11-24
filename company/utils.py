from company.models import CompanyRoles, Role


def create_company_roles(company, roles):
    CompanyRoles.objects.filter(company_id=company.id).delete()
    for role in roles:
        role = Role.objects.create(**role)
        CompanyRoles.objects.create(company=company, role=role)
