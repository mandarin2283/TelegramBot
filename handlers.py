from aiogram import Router,html
from aiogram.filters import CommandStart,Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from FSM import FormTrain, FormFilm
from utils.train import Train
from utils.movie import Movie
from services.database import add_train, get_or_create_exercise,add_set,save_movie


router = Router()


@router.message(CommandStart())
async def start_handler(message: Message):
    await message.answer(f"Приветствую, {html.code(message.from_user.full_name)}!")


@router.message(Command('train'))
async def train_handler(message: Message,state: FSMContext):
    await message.answer(f'Жду тренировку')
    await state.set_state(FormTrain.get_train)


@router.message(Command('film'))
async def film_handler(message: Message,state: FSMContext):
    await message.answer('Жду фильм (название, оценка)')
    await state.set_state(FormFilm.get_film)


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
    for exercise in approaches.keys():
        set_index = 1
        weight, reps = approaches[exercise]
        if not isinstance(reps, list):
            reps = [reps]
        for rep in reps:
            await add_set(workout_id,
                          exercise,
                          set_index,
                          weight,
                          rep)
            set_index += 1
    await message.answer('Тренировка сохранена')
    await state.clear()


@router.message(FormFilm.get_film)
async def check_film(message: Message,state: FSMContext):
    title,grade = message.text.split(',')
    movie = Movie(title,grade)
    imdb_data = movie.find_movie()
    if imdb_data:
        await save_movie(imdb_data,grade)
        await message.answer('Фильм сохранен')
    else:
        await message.answer('Фильм не найден')
