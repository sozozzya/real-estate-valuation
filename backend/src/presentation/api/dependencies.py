# src/presentation/api/dependencies.py


from src.infrastructure.di.container import container


def get_calculate_use_case():
    if not container.use_case:
        raise RuntimeError("Use case not initialized")
    return container.use_case
