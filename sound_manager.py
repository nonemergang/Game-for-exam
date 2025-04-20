import pygame



class SoundManager:

    """
    Статический класс для загрузки поверхностей, для оптимизации
    """

    initialized = False
    sounds = None


    @staticmethod
    def init():
        SoundManager.initialized = True
        SoundManager.sounds = {}


    @staticmethod
    def check_initialized():
        if not SoundManager.initialized:
            raise Exception("Необходимо вызвать ImageHandler.init() перед любыми другими методами")


    @staticmethod
    def clear(path):
        """
        Удаляет один звук из кеша
        """
        SoundManager.check_initialized()
        if path in SoundManager.sounds:
            del SoundManager.sounds[path]


    @staticmethod
    def clear_all():
        """
        УДАЛЯЕТ ВСЕ ЗВУКИ ИЗ КЕША
        """
        SoundManager.check_initialized()
        SoundManager.sounds = {}


    @staticmethod
    def load(path):
        """
        КЛЮЧЕВОЙ МЕТОД
        ЕСЛИ ЗВУКА НЕТУ В КЕШЕ, ТО ЗАГРУЖАЕТ ЗВУК В КЕШ
        ЕСЛИ ЗВУК ЕСТЬ В КЕШЕ, ТО ОН ВОЗВРАЩАЕТ СУЩЕСТВУЮЩИЙ ОБЪЕКТ
        """

        SoundManager.check_initialized()
        if path in SoundManager.sounds:
            return SoundManager.sounds[path]

        sound = pygame.mixer.Sound(path)
        SoundManager.sounds[path] = sound
        return sound



