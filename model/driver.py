from dataclasses import dataclass
import datetime

@dataclass
class Driver:
    driverId: int
    forename: str
    surname: str

    def __hash__(self):
        return self.driverId

    def __str__(self):
        return f"{self.forename} ({self.surname})"

    def __eq__(self, other):
        return self.driverId == other.driverId