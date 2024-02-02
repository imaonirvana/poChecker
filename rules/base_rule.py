from abc import ABC, abstractmethod


class BaseRule(ABC):
    @abstractmethod
    def fix_translation(self, original: str, translated: str) -> str:
        pass

    @abstractmethod
    def is_broken(self, original: str, translated: str) -> bool:
        pass

    @abstractmethod
    def get_error_message(self, original: str, translated: str, file_path, line_num) -> str:
        pass

    pass
