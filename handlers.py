from aiogram import Router,html
from aiogram.filters import CommandStart,Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from FMS import FormTrain
from utils.train import Train
from services.database import add_train, get_or_create_exercise,add_set


router = Router()


@router.message(CommandStart())
async def start_handler(message: Message):
    await message.answer(f"Приветствую, {html.code(message.from_user.full_name)}!")


@router.message(Command('train'))
async def train_handler(message: Message,state: FSMContext):
    await message.answer(f'Жду тренировку')
    await state.set_state(FormTrain.get_train)


@router.message(FormTrain.get_train)
async def process_train(message: Message,state: FSMContext):
    train = Train.create(message.text)
    date, train_type, approaches = train.get_data()
    await message.answer(f'{date} - {approaches}\nЕсли есть ошибки - введи команду rewrite, если нет - save')
    await state.update_data(
        date=date,
        train_type=train_type,
        approaches=approaches
    )
    await state.set_state(FormTrain.check_train)


@router.message(FormTrain.check_train)
async def check_train(message: Message,state: FSMContext):
    text = message.text.strip().lower()
    if text=='rewrite':
        await message.answer('Жду тренировку')
        await state.set_state(FormTrain.get_train)
    elif text=='save':
        await save_train(message, state)


async def save_train(message: Message,state: FSMContext):
    data = await state.get_data()
    date, train_type, approaches = data['date'],data['train_type'],data['approaches']
    workout_id = await add_train(date, train_type)
    for exersice in approaches.keys():
        set_index = 1
        weight, reps = approaches[exersice]
        if not isinstance(reps, list):
            reps = [reps]
        for rep in reps:
            await add_set(workout_id,
                          exersice,
                          set_index,
                          weight,
                          rep)
            set_index += 1
    await message.answer('Тренировка сохранена')
    await state.clear()


@router.message()
async def echo_handler(message: Message):
    await message.send_copy(message.chat.id)