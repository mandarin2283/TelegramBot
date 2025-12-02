from aiogram.fsm.state import State,StatesGroup


class FormTrain(StatesGroup):
    get_train = State()
    check_train = State()


class FormFilm(StatesGroup):
    get_film = State()
    choose_movie = State()