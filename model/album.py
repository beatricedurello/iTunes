from dataclasses import dataclass
@dataclass
class Album:
    AlbumId: int
    Title: str
    ArtistId: int
    Durata: float

    def __hash__(self):
        return hash(self.AlbumId)

    def __str__(self):
        return f"{self.Title} -- durata: {self.Durata}"

    def __eq__(self, other):
         return self.AlbumId == other.AlbumId
