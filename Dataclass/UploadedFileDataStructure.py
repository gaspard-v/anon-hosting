from dataclasses import dataclass


@dataclass
class UploadedFileDataStructure:
    key: str
    tweak: str
    original_filename: str
    stored_filename: str
    content_type: str

    def to_dict(self) -> dict[str, str]:
        return {
            "key": self.key,
            "tweak": self.tweak,
            "original_filename": self.original_filename,
            "stored_filename": self.stored_filename,
            "content_type": self.content_type,
        }
