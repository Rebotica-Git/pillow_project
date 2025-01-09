from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Ellipse, Color, Line
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.properties import NumericProperty
from kivy.base import EventLoop

# Основной виджет для игры
class BallAppWidget(Widget):
    ball_radius = NumericProperty(15)  # Радиус мяча
    circle_radius = NumericProperty(200)  # Радиус окружности
    ball_x = NumericProperty(0)  # Горизонтальная позиция мяча
    ball_y = NumericProperty(0)  # Вертикальная позиция мяча
    ball_vx = NumericProperty(0)  # Скорость мяча по X
    ball_vy = NumericProperty(0)  # Скорость мяча по Y
    gravity = NumericProperty(0.2)  # "Гравитация"
    elasticity = NumericProperty(0.9)  # Коэффициент отскока

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Позиция мяча
        self.ball_x = self.width // 2
        self.ball_y = self.height // 2 - 50
        self.bind(size=self.update_canvas)

        # Настройка отрисовки
        with self.canvas:
            self.circle = Line(circle=(self.width // 2, self.height // 2, self.circle_radius), width=3)
            self.ball = Ellipse(pos=(self.ball_x - self.ball_radius, self.ball_y - self.ball_radius), size=(self.ball_radius * 2, self.ball_radius * 2))

        # Подключение акселерометра
        EventLoop.window.bind(on_motion=self.on_motion)

        # Запуск обновлений
        Clock.schedule_interval(self.update, 1 / 60)

    def update_canvas(self, *args):
        self.circle.circle = (self.width // 2, self.height // 2, self.circle_radius)

    def update(self, dt):
        # Обновление позиции мяча
        self.ball_x += self.ball_vx
        self.ball_y += self.ball_vy

        # Центр окружности
        cx, cy = self.width // 2, self.height // 2

        # Проверка столкновения с окружностью
        dx = self.ball_x - cx
        dy = self.ball_y - cy
        distance = (dx ** 2 + dy ** 2) ** 0.5

        if distance + self.ball_radius >= self.circle_radius:
            # Нормаль к окружности
            normal_x, normal_y = dx / distance, dy / distance

            # Отражение скорости
            dot_product = self.ball_vx * normal_x + self.ball_vy * normal_y
            self.ball_vx -= 2 * dot_product * normal_x
            self.ball_vy -= 2 * dot_product * normal_y

            # Применение коэффициента эластичности
            self.ball_vx *= self.elasticity
            self.ball_vy *= self.elasticity

        # Обновление позиции мяча
        self.ball.pos = (self.ball_x - self.ball_radius, self.ball_y - self.ball_radius)

    def on_motion(self, window, etype, motionevent):
        if etype == 'sensor':
            # Управление скоростью мяча на основе акселерометра
            self.ball_vx += motionevent.accel[0] * 0.5
            self.ball_vy -= motionevent.accel[1] * 0.5


# Основной класс приложения
class BallApp(App):
    def build(self):
        return BallAppWidget()


# Запуск приложения
if __name__ == '__main__':
    BallApp().run()
