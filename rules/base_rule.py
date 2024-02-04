import os
from abc import ABC, abstractmethod

from PipelineInput import PipelineInput


class BaseRule(ABC):
    @abstractmethod
    def fix_translation(self, original: str, translated: str) -> str:
        pass

    @abstractmethod
    def is_broken(self, original: str, translated: str) -> bool:
        pass

    @abstractmethod
    def get_error_message(self, pipeline_input: PipelineInput) -> str:
        pass

    def generate_base_error_message(self, description: str, pipeline_input: PipelineInput):
        result = ""
        result += "===========================================================================\n"
        result += f"Error in {os.path.basename(pipeline_input.get_file_path())}, line {str(pipeline_input.get_line_num())}:\n"
        result += f"Description: {description}\n"
        result += f"Original: '{pipeline_input.get_original()}'\n"
        if pipeline_input.get_translated() is not None:
            result += f"Translated: '{pipeline_input.get_translated()}'\n"
        result += "===========================================================================\n\n"

        return result
    pass
