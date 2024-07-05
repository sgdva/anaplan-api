from dataclasses import dataclass


@dataclass(frozen=True)
class DimensionDetails:
    _id: str
    _name: str

    @property
    def id(self) -> str:
        return self._id

    @property
    def name(self) -> str:
        return self._name
