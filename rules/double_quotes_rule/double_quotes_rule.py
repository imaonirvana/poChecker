from rules.base_rule import BaseRule


class DoubleQuotesRule(BaseRule):
    def fix_translation(self, original: str, translated: str) -> str:
        return translated.replace('"', "'")

    def is_broken(self, original: str, translated: str) -> bool:
        if '"' in translated:
            return True

    def get_error_message(self, pipeline_input) -> str:
        return self.generate_base_error_message("Double quote", pipeline_input)
