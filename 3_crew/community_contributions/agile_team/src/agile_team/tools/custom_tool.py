import os
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type

class FileWriteInput(BaseModel):
    """Input schema for FileWriterTool."""
    filename: str = Field(..., description="The name of the file.")
    content: str = Field(..., description="The content to write to the file.")
    directory: str = Field(..., description="The directory path relative to project root.")

class FileWriterTool(BaseTool):
    name: str = "file_writer_tool"
    description: str = "Writes content to a file at a specific directory. Useful for persisting code and reports."
    args_schema: Type[BaseModel] = FileWriteInput

    def _run(self, filename: str, content: str, directory: str) -> str:
        try:
            # Ensure directory exists
            full_dir = os.path.join("output", directory)
            os.makedirs(full_dir, exist_ok=True)

            full_path = os.path.join(full_dir, filename)
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(content)

            return f"Successfully wrote file to {full_path}"
        except Exception as e:
            return f"Error writing file: {str(e)}"
