import dataclasses


@dataclasses.dataclass
class User:
    id: int
    name: str
    score: int
    answers_id: int
    answers_id_prev: int
    answers_list: list
    date: int

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


usersList = []


questions = [
        Question(1, "Имитирующий алмаз кристалл, выращенный лабораторным способом? ", [
            Answer(1, "Фианит", False),
            Answer(2, "Муассанит", False),
            Answer(3, "Циркон", True),
            Answer(4, "Цирконий", True),
        ],
        False),
        Question(2, "Значение показателя преломления фианита?", [
            Answer(1, "2,15—2,25", False),
            Answer(2, "2,20-2,15", False),
            Answer(3, "2,24 -2,28", False),
            Answer(4, "2,25-2,28", True),
        ],
        False),
        Question(3, "Твёрдость фианита?", [
            Answer(1, "7,5—8,56", False),
            Answer(2, "7,8-7,89", False),
            Answer(3, "8,56 -9,11", False),
            Answer(4, "6,78-7,56", True),
        ],  
        False),
        Question(4, "Как и где могут использоваться фианиты, кроме ювелирных украшений ? (несколько вариантов)", [
            Answer(1, "Cтоматология", True),
            Answer(2, "Химическая промышленность ", True),
            Answer(3, "Керамика", True),
            Answer(4, "Приборостроение", False),
        ],  
        False),
        
]




