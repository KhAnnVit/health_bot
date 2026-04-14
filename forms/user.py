from aiogram.fsm.state import State, StatesGroup


class Form(StatesGroup):
    name = State()
    age = State()
    gender = State()


class Sets(StatesGroup):
    set_weight = State()
    set_pressure = State()
