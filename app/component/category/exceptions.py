from app.exceptions import DomainError


class CategoryCycleError(DomainError):
    pass


class CategoryNotEmptyError(DomainError):
    pass


class CategoryNotFoundError(DomainError):
    pass
