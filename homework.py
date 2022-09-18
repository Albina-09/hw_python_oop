from codecs import replace_errors


class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self, training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float) -> None:
        self.training_type = training_type  # имя класса
        self.duration = duration  # длительность тренировки в часах
        self.distance = distance  # дистанция в километрах
        self.speed = speed  # средняя скорость движения пользователя;
        self.calories = calories  # количество килокалорий,
        # которое израсходовал пользователь за время тренировки.

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    M_IN_KM: int = 1000  # константа для перевода метров в километры
    LEN_STEP: float = 0.65   # константа переводит расстояние из шагов в метры
    """Базовый класс тренировки."""

    def __init__(self,
                 action: int,  # количество совершённых действий
                               # (число шагов при ходьбе и беге
                               # либо гребков — при плавании)
                 duration: float,  # длительность тренировки
                 weight: float,  # вес спортсмена.
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self. M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(training_type=type(self).__name__,
                           duration=self.duration,
                           distance=self.get_distance(),
                           speed=self.get_mean_speed(),
                           calories=self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    coeff_calorie_1: int = 18  # базовый коэффициент для бега
    coeff_calorie_2: int = 20  # базовый коэффициент для бега
    coeff_calorie_3: int = 60  # константа для перевода часов в минуты

    def get_spent_calories(self) -> float:
        return ((18 * self.get_mean_speed() - 20) * self.weight / self.M_IN_KM
                * (self.duration * 60))


class SportsWalking(Training):
    coeff_calorie_1: float = 0.035  # базовый коэффициент для спортивной ходьбы
    coeff_calorie_2: float = 0.029  # базовый коэффициент для спортивной ходьбы
    coeff_calorie_3: int = 60  # константа для перевода часов в минуты
    """Тренировка: спортивная ходьба."""
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height  # рост спортсмена

    def get_spent_calories(self) -> float:
        return ((0.035 * self.weight + self.get_mean_speed()**2
                 // self.height
                * 0.029 * self.weight) * (self.duration * 60))


class Swimming(Training):
    LEN_STEP: float = 1.38  # константа переводит гребки спортсмена в метры
    coeff_calorie_1: float = 1.1  # базовый коэффициент для плавания
    coeff_calorie_2: int = 2      # базовый коэффициент для плавания
    coeff_calorie_3: int = 60     # константа для перевода часов в минуты

    """Тренировка: плавание."""
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,  # длина бассейна в метрах
                 count_pool: float  # сколько раз пользователь переплыл бассейн
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        return (self.length_pool * self.count_pool / self.M_IN_KM
                / self.duration)

    def get_spent_calories(self) -> float:
        return (self.get_mean_speed() + 1.1) * 2 * self.weight


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    a = {'SWM': Swimming,
         'RUN': Running,
         'WLK': SportsWalking
         }
    return a[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
