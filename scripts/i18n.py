#!/usr/bin/env python3
import json
import re
from pathlib import Path


DEFAULT_LANGUAGE = "es"
LANGUAGE_LABELS = {
    "es": "Spanish (es)",
    "en": "English (en)",
}


def load_translations(repo_root):
    path = Path(repo_root) / "config" / "i18n.json"
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def detect_language(repo_root, fallback=DEFAULT_LANGUAGE):
    master_path = Path(repo_root) / ".context" / "MASTER.md"
    if not master_path.exists():
        return fallback
    content = master_path.read_text(encoding="utf-8")
    match = re.search(r"Primary Language\*\*:.*\((\w+)\)", content)
    if match:
        code = match.group(1).lower()
        if code in LANGUAGE_LABELS:
            return code
    if "English" in content:
        return "en"
    if "Spanish" in content:
        return "es"
    return fallback


def set_language_in_master(repo_root, lang_code):
    master_path = Path(repo_root) / ".context" / "MASTER.md"
    if not master_path.exists():
        return False
    primary_label = "Spanish (es)" if lang_code == "es" else "English (en)"
    secondary_label = "English (en)" if lang_code == "es" else "Spanish (es)"
    content = master_path.read_text(encoding="utf-8")
    content = re.sub(
        r"- \*\*Primary Language\*\*: .*",
        f"- **Primary Language**: {primary_label}",
        content,
    )
    content = re.sub(
        r"- \*\*Secondary Language\*\*: .*",
        f"- **Secondary Language**: {secondary_label}",
        content,
    )
    master_path.write_text(content.rstrip() + "\n", encoding="utf-8")
    return True


def select_language(translations, default=DEFAULT_LANGUAGE):
    es = translations.get("es", {})
    title = es.get("language.select.title", "Selecciona tu idioma / Select your language")
    prompt = es.get("language.select.prompt", "Elige [1-2]: ")
    option_es = es.get("language.option.es", "1. Espanol (es)")
    option_en = es.get("language.option.en", "2. English (en)")
    print(title)
    print(option_es)
    print(option_en)
    choice = input(prompt).strip()
    if choice == "2":
        return "en"
    if choice == "1":
        return "es"
    return default


class Translator:
    def __init__(self, translations, language=DEFAULT_LANGUAGE):
        self.translations = translations or {}
        self.language = language or DEFAULT_LANGUAGE

    def t(self, key, default=None, **kwargs):
        lang_table = self.translations.get(self.language, {})
        text = lang_table.get(key, default if default is not None else key)
        if kwargs:
            return text.format(**kwargs)
        return text


def get_translator(repo_root, language=None):
    translations = load_translations(repo_root)
    lang = language or detect_language(repo_root)
    return Translator(translations, lang)
