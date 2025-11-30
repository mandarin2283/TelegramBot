from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State,StatesGroup


class FormTrain(StatesGroup):
    get_train = State()
    check_train = State()
