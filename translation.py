import i18n
from i18n import config

class Language:
    @staticmethod
    def setup_i18n(lang: str = "en"):
        config.set("file_format", "json")
        config.set("filename_format", "{locale}.{format}")
        config.set("load_path", ["locales"])
        i18n.set("locale", lang)
        i18n.set("fallback", "en")
        Language.reload_translations()

    @staticmethod
    def reload_translations():
        """Перезагружает переводы и очищает кэш."""
        i18n.load_path.clear()
        i18n.load_path.append("locales")
        i18n.translations.container.clear()
# Инициализация
Language.setup_i18n(lang="ru")