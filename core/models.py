
from dataclasses import dataclass


@dataclass
class BinaryVariant:
    name: str
    sample_size: int
    success_count: int

    @property
    def failure_count(self) -> int:
        return self.sample_size - self.success_count

    @property
    def success_rate(self) -> float:
        if self.sample_size == 0:
            return 0.0

        return self.success_count / self.sample_size
