import re

class FixTranslations:
    @staticmethod
    def fixed_translation(original, translated):
        pattern = r'\$\(([^\)]+)\)'

        fixed =