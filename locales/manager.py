# locales/manager.py
import os
import json
from . import ja, en

class TranslationManager:
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(TranslationManager, cls).__new__(cls, *args, **kwargs)
            cls._instance._initialized = False
        return cls._instance
        
    def __init__(self, default_lang="ja"):
        if self._initialized:
            return
        self._initialized = True
        self.current_lang = default_lang
        self.locales = {
            "ja": ja.STRINGS,
            "en": en.STRINGS
        }
        self.callbacks = []
        
    def get(self, key, default=None, **kwargs):
        strings = self.locales.get(self.current_lang, ja.STRINGS)
        text = strings.get(key)
        if text is None:
            # Fallback to English, then Japanese, then default or key
            text = self.locales["en"].get(key, ja.STRINGS.get(key, default or key))
        
        if kwargs:
            try:
                return text.format(**kwargs)
            except Exception:
                return text
        return text
        
    def set_language(self, lang):
        if lang in self.locales and lang != self.current_lang:
            self.current_lang = lang
            self.notify_listeners()
            
    def register_listener(self, callback):
        """Register a callback to be run when the language changes."""
        if callback not in self.callbacks:
            self.callbacks.append(callback)
            
    def unregister_listener(self, callback):
        """Unregister a callback."""
        if callback in self.callbacks:
            self.callbacks.remove(callback)
            
    def notify_listeners(self):
        """Call all registered callbacks to update their strings."""
        for callback in self.callbacks:
            try:
                callback()
            except Exception as e:
                print(f"Error notifying translation listener: {e}")

# Global singleton instance
language_manager = TranslationManager()
