from pydantic import BaseModel


class SDirInput(BaseModel):
    dir_names: list[str]
    root_dir: str | None = None
