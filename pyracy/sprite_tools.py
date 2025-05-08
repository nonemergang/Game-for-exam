
import pygame


import time
import sys


class Animation(object):

    def __init__(self, surface, sheet_size=(1, 1), frame_count=1, rect=None,
                 reverse_x=False, reverse_y=False, reverse_animation=False, colorkey=None, scale=1.0, start_frame=0):


        #Входные аргументы
        self.surface = surface
        self.reverse_x = reverse_x
        self.reverse_y = reverse_y
        self.reverse_animation = reverse_animation
        self.frame_count = frame_count
        self.colorkey = colorkey
        self.scale = scale

        #Разделяем на отдельные спрайты
        self.frames = self.split(surface, sheet_size, frame_count, rect, scale)[start_frame:]
        self.frame_count -= start_frame

    @staticmethod
    def from_path(path, *args, **kwargs):

        return Animation(pygame.image.load(path), *args, **kwargs)

    def split(self, surface, sheet_size, frame_count, rect=None, scale=1.0):


        #Определяем размер кадра, в пикселях
        rect = (0, 0, surface.get_width(), surface.get_height()) if rect is None else rect
        rect = pygame.Rect(*rect)
        pixel_width, pixel_height = rect.width, rect.height
        frame_width = pixel_width//sheet_size[0]
        frame_height = pixel_height//sheet_size[1]

        #   Хранилище кадров
        frames = []

        #   Для каждого кадра анимации
        frame_x = 0
        frame_y = 0
        for idx in range(frame_count):

            # Обрезаем номер кадра в pygame subsurface
            x_origin = frame_x * frame_width + rect[0]
            y_origin = frame_y * frame_height + rect[1]
            frame_rect = x_origin, y_origin, frame_width, frame_height
            new_frame = surface.subsurface(frame_rect)

            # Применяем постобработку для кадра
            if self.reverse_x or self.reverse_y:
                new_frame = pygame.transform.flip(new_frame, self.reverse_x, self.reverse_y)
            else:
                new_frame = new_frame.copy()
            if self.colorkey:
                new_frame.set_colorkey(self.colorkey)
            if scale != 1.0:
                width = int(new_frame.get_width() * scale)
                height = int(new_frame.get_height() * scale)
                new_frame = pygame.transform.scale(new_frame, (width, height))

            # Добавляем кадр в список
            frames.append(new_frame)

            # Итерация по строкам и столбцам
            frame_x += 1
            if frame_x > sheet_size[0]:
                frame_x = 0
                frame_y += 1

        #   Применяем постобратотку для анимаций
        if self.reverse_animation:
            frames = frames[::-1]

        return frames

    def reverse(self, x_bool, y_bool):
        """
            Переворачивает кадры анимации на основе того, какие булевы значения
            xbool: если true, зеркально отображает кадры по горизонтали
            ybool: если true, зеркально отображает кадры по вертикали
        """

        #   Переворачиваем каждый кадр
        for idx, frame in enumerate(self.frames):
            self.frames[idx] = pygame.transform.flip(frame, x_bool, y_bool)


class Sprite(pygame.sprite.Sprite):
    """
        Объект для рендеринга игрового спрайта
    """

    def __init__(self, fps=12, position=(0, 0)):
        """ Инициализация метода для спрайтов """
        super().__init__()

        self.animations = {}  # Сохраняет строковый ключ, сопоставленный каждому объекту Animation.
        self.animation_fps_overrides = {}  # Сохраняет строковый ключ, сопоставленный с числом FPS
        self.animation_chain_mapping = {}  # Сопоставляет ключи анимации с анимациями, которые должны следовать за ними по умолчанию
        self.animation_callbacks = {}  # Сопоставляет ключи анимации с функциями, которые будут вызваны после их завершения
        self.animation_temporary_callbacks = {}  # Сопоставляет ключи анимации с функциями, которые будут вызываться при их следующем завершении

        self.image = None
        self.rect = None
        self.x, self.y = position

        self.angle = 0

        #   Начальные флаги и значения
        self.paused = False
        self.paused_at = 0
        self.active_animation_key = None

        #   количество кадров в секунду
        self.fps = fps
        self.now = 0

    def add_animation(self, anim_dict, fps_override=None, loop=False):
        """
        Добавляет одну или несколько анимаций в словарь анимации спрайта.
        """

        for name in anim_dict:
            self.animations[name] = anim_dict[name]
            if fps_override:
                self.animation_fps_overrides[name] = fps_override
            if loop:
                self.chain_animation(name, name)

    def start_animation(self, name, restart_if_active=True, clear_time=True):
        """
        Запускает анимацию выбранного имени.

        name: строковый ключ для анимации, добавленной через add_animation.
        force_restart (по умолчанию True): если True, запустить анимацию с первого кадра, даже если она уже воспроизводится
        """

        self.resume()

        # Если мы уже воспроизводим правильную анимацию и не принуждаем ее перезапускать, прерываем раньше
        if not restart_if_active and name == self.active_animation_key:
            return

        # Запоминаем, когда началась эта анимация. Если clear_time — False, вызывающий должен соответствующим образом настроить self.now.
        if clear_time:
            self.now = 0

        # Меняем активную анимацию
        self.active_animation_key = name

    def get_frame_num(self):
        fps = self.fps
        if self.active_animation_key in self.animation_fps_overrides:
            fps = self.animation_fps_overrides[self.active_animation_key]
        frame_time = 1.0/fps
        frame_number = int(self.now/frame_time)
        return frame_number

    def get_image(self):
        """
        Получаем surface для текущего кадра
        """
        active_animation = self.animations[self.active_animation_key]
        frame_time = 1/self.fps
        frame_number = self.get_frame_num()
        if frame_number >= active_animation.frame_count:
            new_animation_exists = self.on_animation_finished(self.active_animation_key)
            if not new_animation_exists:
                self.pause()
                self.now = frame_time * (len(active_animation.frames) - 0.5)
                return active_animation.frames[-1]
            self.now -= frame_time * active_animation.frame_count
            return self.get_image()

        image = active_animation.frames[frame_number]
        if self.angle != 0:
            image = pygame.transform.rotate(image, self.angle)
        return image

    def update_image(self):
        self.image = self.get_image()

    def set_angle(self, angle):
        self.angle = angle

    def draw(self, surface, offset=(0, 0)):
        """
        Рисует текущий кадр на поверхности.
        """

        #   Если активной анимации нету, то выдаем ошибку
        if self.active_animation_key not in self.animations:
            raise Sprite.InvalidAnimationKeyException(f"Animation key {self.active_animation_key} has not been added.")

        #   Рисуем анимацию на повверхности
        if not self.image:
            self.image = self.get_image()
        x = int(self.x - self.image.get_width()/2 - offset[0])
        y = int(self.y - self.image.get_height()/2 - offset[1])
        surface.blit(self.image, (x, y))

    def pause(self):
        """ Ставим на паузу активниуюю анимацию """
        self.paused = True

    def resume(self):
        """ Возобновляем актиыную анимацию """
        self.paused = False

    def update(self, dt, events):
        """ Обновляет анимацию с шагом dt. """
        if not self.paused:
            self.now += dt

        self.image = self.get_image()
        w = self.image.get_width()
        h = self.image.get_height()
        x = int(self.x - w/2)
        y = int(self.y - h/2)
        self.rect = pygame.Rect(x, y, w, h)

    def set_position(self, pos):
        """ Позиция спрайта на экране. """
        self.x, self.y = pos

    def add_callback(self, animation_key, callback, args=None, kwargs=None, temporary=False):
        """
        Добавляет обратный вызов, который будет вызван после завершения указанной анимации.
        """
        args = args if args else ()
        kwargs = kwargs if kwargs else {}
        if temporary:
            callback_dict = self.animation_temporary_callbacks
        else:
            callback_dict = self.animation_callbacks
        if animation_key not in callback_dict:
            callback_dict[animation_key] = []
        callback_dict[animation_key].append((callback, args, kwargs))

    def chain_animation(self, previous_animation, next_animation):
        """
        Объединяет две анимации вместе, что когда одна заканчивается, по умолчанию запускается следующая.

        previous_animation: строковый ключ первой анимации
        next_animation: строковый ключ анимации для воспроизведения после завершения previous_animation
        """
        self.animation_chain_mapping[previous_animation] = next_animation

    def on_animation_finished(self, animation_key):
        """

Обрабатывает обратные вызовы и цепочки, когда анимация завершается или зацикливается.
        """
        self.run_callbacks(animation_key)
        next_animation = self.get_next_animation(animation_key)
        if next_animation:
            self.start_animation(next_animation, restart_if_active=True, clear_time=False)
            return True
        return False

    def run_callbacks(self, animation_key):
        """
        Обрабатывает обратные вызовы, когда анимация завершается. Также очищает временные обратные вызовы после запуска.
        """

        # Временные обратные вызовы анимации
        if animation_key in self.animation_temporary_callbacks:
            for callback, args, kwargs in self.animation_temporary_callbacks[animation_key]:
                callback(*args, **kwargs)
            del self.animation_temporary_callbacks[animation_key]

        # Повторные обратные вызовы анимации
        if animation_key in self.animation_callbacks:
            for callback, args, kwargs in self.animation_callbacks[animation_key]:
                callback(*args, **kwargs)


    def get_next_animation(self, animation_key):
        """
        Возвращает ключ анимации, которая должна следовать за указанной, или None, если таковой не существует.
        """
        if animation_key in self.animation_chain_mapping:
            return self.animation_chain_mapping[animation_key]
        return None

    class InvalidAnimationKeyException(IndexError):
        pass


if __name__ == '__main__':

    class Counter:
        """
        Считаем каждый раз, когда анимация спрайта зацикливается
        """

        def __init__(self):
            self.value = 0
            self.font = pygame.font.SysFont("sans serif", 16, False)

        def count(self):
            self.value += 1

        def draw(self, surface):
            pygame.font.init()
            text = self.font.render(f"{self.value}", False, (255, 255, 255))
            surface.blit(text,
                         (surface.get_width() - text.get_width() - 2,
                          surface.get_height() - text.get_height() - 2))

    pygame.init()
    screen = pygame.display.set_mode((220, 150))
    pygame.display.set_caption("Sprite Tools Test")

    #  Создаем спрайт и добавляем к нему анимацию бездействия
    a = Animation.from_path("TestSprite.png", sheet_size=(4, 1), frame_count=4, colorkey=(255, 0, 255))
    c = Counter()
    b = Sprite(fps=9, position=(110, 75))
    b.add_animation({"Idle": a}, loop=True)
    b.start_animation("Idle")
    b.add_callback("Idle", c.count)

    then = time.time()
    time.sleep(0.01)
    while True:

        #   Calculate time step
        now = time.time()
        dt = now - then
        then = now

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        #   пустой экран
        screen.fill((50, 50, 50))

        #   отображаем текущий кадр на экране
        b.update(dt, events)
        b.draw(screen)
        c.draw(screen)

        pygame.display.flip()