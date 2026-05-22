from dataclasses import dataclass
from uuid import UUID


@dataclass
class Persona:
    id: UUID
    nome: str
    email: str = ""

    def ruolo_atteso(self) -> str:  # pragma: no cover
        raise NotImplementedError
