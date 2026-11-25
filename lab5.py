from datetime import date
from enum import Enum

class MovieType(Enum):
    ACTION = "ACTION"
    COMEDY = "COMEDY"
    DRAMA = "DRAMA"
    FANTASY = "FANTASY"

class Movie:
    def __init__(self, id, title, ranking, release_date, character_number,
                 ticket_price, comment="", movie_type=MovieType.DRAMA):
        self._id = id
        self._title = title
        self.ranking = ranking            
        self._release_date = release_date
        self._character_number = character_number
        self.ticket_price = ticket_price    
        self._comment = comment
        self._type = movie_type
        print(f"[Конструктор] Створено фільм '{title}'")

    def __del__(self):
        print(f"[Деструктор] Фільм '{self._title}' видалено")

    @property
    def id(self):
        return self._id

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if not value:
            raise ValueError("Назва не може бути порожньою")
        self._title = value

    @property
    def ranking(self):
        return self._ranking

    @ranking.setter
    def ranking(self, value):
        if not 0 <= value <= 10:
            raise ValueError("Рейтинг має бути від 0 до 10")
        self._ranking = value

    @property
    def release_date(self):
        return self._release_date

    @release_date.setter
    def release_date(self, value):
        if not isinstance(value, date):
            raise TypeError("Дата випуску має бути об'єктом date")
        self._release_date = value

    @property
    def character_number(self):
        return self._character_number

    @character_number.setter
    def character_number(self, value):
        if value < 0:
            raise ValueError("Кількість персонажів не може бути від'ємною")
        self._character_number = value

    @property
    def ticket_price(self):
        return self._ticket_price

    @ticket_price.setter
    def ticket_price(self, value):
        if value < 0:
            raise ValueError("Ціна квитка не може бути від'ємною")
        self._ticket_price = value

    @property
    def comment(self):
        return self._comment

    @comment.setter
    def comment(self, value):
        self._comment = value

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        if not isinstance(value, MovieType):
            raise TypeError("Тип має бути значенням MovieType")
        self._type = value

    # ---- виведення ----
    def __str__(self):
        return (f"[{self._id}] {self._title} ({self._type.value}) | "
                f"Рейтинг: {self._ranking} | Дата: {self._release_date} | "
                f"Персонажів: {self._character_number} | "
                f"Ціна: {self._ticket_price} грн | Коментар: {self._comment}")


class Cinema:
    def __init__(self, name, location):
        self._name = name
        self._location = location
        self._movies = []      # перелік фільмів, що показуються
        self._sales = {}       # (id фільму, день) -> кількість проданих квитків
        print(f"[Конструктор] Створено кінотеатр '{name}'")

    def __del__(self):
        print(f"[Destruct] Кінотеатр '{self._name}' закрито")

    @property
    def name(self):
        return self._name

    @property
    def location(self):
        return self._location

    @property
    def movies(self):
        return list(self._movies)  

    def add_movie(self, movie):
        self._movies.append(movie)

    def sell_tickets(self, movie, day, count):
        key = (movie.id, day)
        self._sales[key] = self._sales.get(key, 0) + count

    def calculate_profit(self, movie, day):
        """Прибуток від фільму за певний день (проданих квитків * ціна)."""
        tickets = self._sales.get((movie.id, day), 0)
        return tickets * movie.ticket_price

    def select_movie(self, movie_type=None, min_ranking=0, max_price=None):
        """Вибір фільму за параметрами: тип, мінімальний рейтинг, макс. ціна.
        Повертає фільм з найвищим рейтингом серед підходящих або None."""
        candidates = [
            m for m in self._movies
            if (movie_type is None or m.type == movie_type)
            and m.ranking >= min_ranking
            and (max_price is None or m.ticket_price <= max_price)
        ]
        return max(candidates, key=lambda m: m.ranking, default=None)
        
    def sort_by_release_date(self, reverse=False):
        return sorted(
            self._movies,
            key=lambda m: m.release_date,
            reverse=reverse,
        )

    def show_movies(self):
        print(f"\nКінотеатр '{self._name}', {self._location}. Афіша:")
        for movie in self._movies:
            print("  " + str(movie))

    def __str__(self):
        return f"Кінотеатр '{self._name}' ({self._location}), фільмів: {len(self._movies)}"


def main():
    cinema = Cinema("Кіно Зоряне", "Львів")
    m1 = Movie(1, "Місія можлива", 8.5, date(2023, 7, 12), 45, 180,
                "Динамічний бойовик", MovieType.ACTION)
    m2 = Movie(2, "Звичайна історія", 7.2, date(2019, 3, 5), 12, 120,
               "Легка комедія", MovieType.COMEDY)
    m3 = Movie(3, "Хроніки драконів", 9.1, date(2024, 11, 1), 30, 220,
               "Казковий світ", MovieType.FANTASY)

    for m in (m1, m2, m3):
        cinema.add_movie(m)

    cinema.show_movies()

    print("\nСортування за датою випуску (від старих до нових):")
    for m in cinema.sort_by_release_date():
        print(f"  {m.title}: {m.release_date}")

    print("\nВибір фільму (комедія, рейтинг від 5):")
    chosen = cinema.select_movie(movie_type=MovieType.COMEDY, min_ranking=5)
    print("  Обрано:", chosen.title if chosen else "нічого не знайдено")

    print("\nВибір фільму (фентезі, ціна до 300 грн):")
    chosen = cinema.select_movie(movie_type=MovieType.FANTASY, max_price=300)
    print("  Обрано:", chosen.title if chosen else "нічого не знайдено")

    day = date(2026, 11, 9)
    cinema.sell_tickets(m1, day, 50)
    cinema.sell_tickets(m3, day, 30)
    print(
    f"\nПрибуток за {day}:\n"
    f" {m1.title}: {cinema.calculate_profit(m1, day)} грн\n"
    f" {m3.title}: {cinema.calculate_profit(m3, day)} грн"
    )

    m1.ticket_price = 200
    print("\nПісля зміни ціни квитка:", m1)

    print()
    print(cinema)


if __name__ == "__main__":
    main()
