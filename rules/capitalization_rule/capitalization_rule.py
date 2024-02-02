from rules.base_rule import BaseRule


class CapitalizationRule(BaseRule):

    def fix_translation(self, original: str, translated: str) -> str:
        return translated

    def is_broken(self, original: str, translated: str) -> bool:
        if (original and original[0].isalpha() and translated and translated[0].isalpha() and
                ((original[0].isupper() and translated[0].islower()) or
                 (original[0].islower() and translated[0].isupper()))):
            return True

    def get_error_message(self, original: str, translated: str) -> str:
        return "Capitalization mismatch"
