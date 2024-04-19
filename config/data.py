import dataclasses

@dataclasses.dataclass
class Question:
    id: int
    name: str
    answers: list
    multiple: bool


@dataclasses.dataclass
class Answer:
    id: int
    url: str
    right: bool


questions = [
    Question(31, "❓ Имитирующий алмаз кристалл, выращенный лабораторным способом?", [
        Answer(1, "Фианит", True),
        Answer(2, "Муассанит", False),
        Answer(3, "Циркон", False),
        Answer(4, "Цирконий", False),
    ],
    True),
    Question(2, "❓ Значение показателя преломления фианита?", [
        Answer(1, "2,15-2,25", True),
        Answer(2, "2,20-2,15", False),
        Answer(3, "2,24-2,28", False),
        Answer(4, "2,25-2,28", False),
    ],
    True),
    Question(3, "❓ Твёрдость фианита?", [
        Answer(1, "7,5-8,56", True),
        Answer(2, "7,8-7,89", False),
        Answer(3, "8,56-9,11", False),
        Answer(4, "6,78-7,56", False),
    ],
    True),
    Question(4, "❓ Как и где могут использоваться фианиты, кроме ювелирных украшений? Возможно выбрать больше одного варианта ответа.", [
        Answer(1, "Cтоматология", True),
        Answer(2, "Химическая промышленность", False),
        Answer(3, "Керамика", True),
        Answer(4, "Приборостроение", False),
    ],
    False),
    Question(5, "❓ Каким был один из первых неювелирных залогов?", [
        Answer(1, "Холодильник", False),
        Answer(2, "Телефон", False),
        Answer(3, "Утюг", True),
        Answer(4, "Чайник", False),
    ],
    True),
    Question(6, "❓ Какой самый дорогой из неювелирных залогов был принят за период работы?", [
        Answer(1, "Телевизор Sony", False),
        Answer(2, "Фотоаппарат цифровой Phase One", True),
        Answer(3, "Телефон сотовый Vertu", False),
        Answer(4, "Macbook Apple", False),
    ],
    True),
    Question(7, "❓ В каком году стали принимать в залог все виды меха?", [
        Answer(1, "2016", False),
        Answer(2, "2017", False),
        Answer(3, "2018", True),
        Answer(4, "2019", False),
    ],
    True),
    Question(8, "❓ Сколько на данный момент составляет ссудный портфель Управления НЮЗ в рублях?", [
        Answer(1, "285 890 499 ₽", False),
        Answer(2, "144 947 345 ₽", False),
        Answer(3, "143 984 888 ₽", True),
        Answer(4, "100 389 000 ₽", False),
    ],
    True),
    Question(9, "❓ Что такое ОФМ?", [
        Answer(1, "Отдел финансового мониторинга", True),
        Answer(2, "Отдел финансов и материалов", False),
        Answer(3, "Отделение физического маркетинга", False),
        Answer(4, "Отдел фактических миграций ", False),
    ],
             True),
    Question(10, "❓ В каком году в Компании появился Учебный центр?", [
        Answer(1, "2017", False),
        Answer(2, "2018", False),
        Answer(3, "2010", True),
        Answer(4, "2013", False),
    ],
    True),
    Question(11, "❓ Выберите верный порядок открытия ломбардов.", [
        Answer(1, "Детский мир, Яшма, Торговый центр", False),
        Answer(2, "Торговый центр, Яшма, Детский мир", False),
        Answer(3, "Яшма, Торговый центр, Детский мир", True),
        Answer(4, "Яшма, Детский мир, Торговый центр", False),
    ],
    True),
    Question(12, "❓ Как назывался первый ломбард Компании?", [
        Answer(1, "Фианит-Ломбард", False),
        Answer(2, "Ломбард ФЛ", False),
        Answer(3, "Фианит", True),
        Answer(4, "Скупка", False),
    ],
    True),
    Question(13, "❓ До какого времени (год) товароведы использовали деревянные счеты?", [
        Answer(1, "Не использовались", False),
        Answer(2, "До 1994 г.", False),
        Answer(3, "До 1996 г.", True),
        Answer(4, "До 1995 г.", False),
    ],
    True),
    Question(14, "❓ Как взвешивали залоги в 1994 году?", [
        Answer(1, "Электронные весы Adventurer OHAUS", False),
        Answer(2, "Электронные весы ARAK GL-602", False),
        Answer(3, "Механические весы", True),
        Answer(4, "Вес определялся «на глаз»", False),
    ],
    True),
    Question(15, "❓ Какие приборы до сих используются в работе товароведа? Возможно выбрать больше одного варианта ответа.", [
        Answer(1, "Лупа", True),
        Answer(2, "Лупа геммологическая", True),
        Answer(3, "Детектор для бриллиантов", True),
        Answer(4, "Полярископ", False),
    ],
    False),
    Question(16, "❓ Что подарили товароведы г. Тюмени на 25-летие Компании?", [
        Answer(1, "Газ", False),
        Answer(2, "Изделие из натурального камня", False),
        Answer(3, "Нефть", True),
        Answer(4, "Общее фото на память", False),
    ],
    True),
    Question(17, "❓ Какая была форма рабочей одежды у товароведов была в Компании в 2008 году?", [
        Answer(1, "Любая одежда", False),
        Answer(2, "Белый верх и темный низ", False),
        Answer(3, "Красно-бордовый шарф, белая блузка и темный низ", True),
        Answer(4, "Белый верх, темный низ и джинсы по пятницам", False),
    ],
    True),
    Question(18, "❓ Самая большая сумма займа в 2023 году?", [
        Answer(1, "6 390 500 руб.", False),
        Answer(2, "1 879 600 руб.", False),
        Answer(3, "2 910 000 руб.", True),
        Answer(4, "1 000 000 руб.", False),
    ],
    True),
    Question(19, "❓ Самый большой чистый вес залога в граммах в 2023 году составил...", [
        Answer(1, "1 294,99 грамм", False),
        Answer(2, "780,65 грамм", False),
        Answer(3, "536,55 грамм", True),
        Answer(4, "454,35 грамм", False),
    ],
    True),
    Question(20, "❓ Самый крупный залог в граммах в 2023 году весил?", [
        Answer(1, "1 809,90 грамм", False),
        Answer(2, "760,50 грамм", False),
        Answer(3, "2 062 грамм", True),
        Answer(4, "3 400 грамм", False),
    ],
    True),
    Question(21, "❓ В каком году появился красный шарф с логотипом Компании?", [
        Answer(1, "2021", False),
        Answer(2, "2023", False),
        Answer(3, "2022", True),
        Answer(4, "2024", False),
    ],
    True),
    Question(22, "❓ В каком году в состав «Фианит-Ломбард» вошел «Донской ломбард»?", [
        Answer(1, "2021", False),
        Answer(2, "2022", False),
        Answer(3, "2023", True),
        Answer(4, "2024", False),
    ],
    True),
    Question(23, "❓ В каком году открылся первый ломбард в г. Санкт-Петербург?", [
        Answer(1, "2010", False),
        Answer(2, "2011", False),
        Answer(3, "2009", True),
        Answer(4, "2012", False),
    ],
    True),
    Question(24, "❓ В каком году «Фианит-Ломбард» открыл первое подразделение в г. Сочи?", [
        Answer(1, "2017", False),
        Answer(2, "2018", False),
        Answer(3, "2021", True),
        Answer(4, "2020", False),
    ],
    True),
    Question(25, "❓ В каком году были выданы первые знаки отличия за выслугу лет?", [
        Answer(1, "2018", False),
        Answer(2, "2017", False),
        Answer(3, "2019", True),
        Answer(4, "2010", False),
    ],
    True),
    Question(26, "❓ За какой стаж работы сотрудник получает золотой знак отличия «Золотое колье»?", [
        Answer(1, "10 лет ", False),
        Answer(2, "15 лет", False),
        Answer(3, "20 лет", True),
        Answer(4, "25 лет", False),
    ],
    True),
    Question(27, "❓ Сколько ломбардов насчитывает наша Компания сегодня?", [
        Answer(1, "487", False),
        Answer(2, "489", False),
        Answer(3, "478 ", True),
        Answer(4, "486", False),
    ], True),
    Question(28, "❓ В какие года открылось больше всего городов ?", [
        Answer(1, "2009", True),
        Answer(2, "2012", False),
        Answer(3, "2010", True),
        Answer(4, "2011", True),
    ], False),
    Question(29, "❓ Сколько отделений на день рождения Компании наcчитывает Санкт-Петербург?", [
        Answer(1, "35", False),
        Answer(2, "50", True),
        Answer(3, "30", False),
        Answer(4, "45", False),
    ], True),
    Question(30, "❓ В каком году открыт самый молодой ломбард в г. Магнитогорск?", [
        Answer(1, "2023", False),
        Answer(2, "2021", False),
        Answer(3, "2020", True),
        Answer(4, "2024", False),
    ], True),
]
