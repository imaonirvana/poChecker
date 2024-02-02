from rules.base_rule import BaseRule


class PercentRule(BaseRule):
    def fix_translation(self, original: str, translated: str) -> str:
        pass

    def is_broken(self, original: str, translated: str) -> bool:
        pass

    def get_error_message(self, original: str, translated: str, file_path, line_num) -> str:
        pass