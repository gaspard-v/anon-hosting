from dataclasses import dataclass, fields


@dataclass(init=False)
class FileMetadata:
    original_filename: str
    content_type: str
    readable_size: str
    size: int

    def __init__(self, **kwargs):
        names = set([f.name for f in fields(self)])
        for k, v in kwargs.items():
            if k in names:
                setattr(self, k, v)

    def to_dict(self) -> dict[str, str | int]:
        return {
            "original_filename": self.original_filename,
            "content_type": self.content_type,
            "readable_size": self.readable_size,
            "size": self.size,
        }
