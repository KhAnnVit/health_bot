from aiogram.fsm.state import State, StatesGroup

class Sets(StatesGroup):
    set_weight = State()
    set_pressure = State()


class ProfileStates(StatesGroup):
    waiting_for_name = State()
    waiting_for_gender = State()
    waiting_for_age = State()
    waiting_for_height = State()
    waiting_for_target = State()

class BMICalcStates(StatesGroup):
    waiting_for_weight = State()
    waiting_for_height = State()