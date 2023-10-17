from dataclasses import dataclass, fields


@dataclass(init=False)
class UploadedFileDataStructure:
    key: str
    tweak: str
    original_filename: str
    stored_filename: str
    content_type: str

    def __init__(self, **kwargs):
        names = set([f.name for f in fields(self)])
        for k, v in kwargs.items():
            if k in names:
                setattr(self, k, v)

    def to_dict(self) -> dict[str, str]:
        return {
            "key": self.key,
            "tweak": self.tweak,
            "original_filename": self.original_filename,
            "stored_filename": self.stored_filename,
            "content_type": self.content_type,
        }
