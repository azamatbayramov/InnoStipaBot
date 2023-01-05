import asyncio
import os
import json
import emoji
from aiogram import Bot, Dispatcher, types
from dotenv import load_dotenv
import datetime

load_dotenv()

with open("grades_values.json") as file:
    GRADES_VALUES = json.load(file)

with open("scholarship_emojis.json") as file:
    SCHOLARSHIP_EMOJIS = json.load(file)

with open("gpa_emojis.json") as file:
    GPA_EMOJIS = json.load(file)

with open("settings.json") as file:
    SETTINGS = json.load(file)

with open("message_texts.json") as file:
    MESSAGE_TEXTS = json.load(file)

B_MIN = SETTINGS["B_MIN"]
B_MAX = SETTINGS["B_MAX"]
DATETIME_FORMAT = SETTINGS["DATETIME_FORMAT"]
TOKEN = os.environ.get("TOKEN")

HELP_MESSAGE = "help"
SCHOLARSHIP_MESSAGE = "scholarship_message"
SOMETHING_WENT_WRONG = "something_went_wrong"
STATE_MESSAGE = "state_message"

start_datetime = datetime.datetime.now().strftime(DATETIME_FORMAT)
count_of_calculated_scholarships = 0


async def convert_grade_to_value(grade: str) -> int:
    return GRADES_VALUES[grade]


async def get_emoji_alias_by_gpa(gpa: float) -> str:
    return GPA_EMOJIS[str(round(gpa))]


async def get_emoji_alias_by_scholarship(scholarship: int) -> str:
    return SCHOLARSHIP_EMOJIS[str(scholarship // 1000)]


async def get_message(message_type, incoming_message_text=None):
    message_with_emoji_aliases: str
    message_template = MESSAGE_TEXTS[message_type]

    if message_type == SCHOLARSHIP_MESSAGE:
        incoming_message_text = incoming_message_text.lower()

        grades = await parse_grades(incoming_message_text)

        gpa = await calculate_gpa(grades)
        gpa_emoji_alias = await get_emoji_alias_by_gpa(gpa)

        scholarship = await calculate_scholarship(gpa)
        scholarship_alias = await get_emoji_alias_by_scholarship(scholarship)

        message_with_emoji_aliases = message_template.format(
            round(gpa, 2), gpa_emoji_alias, scholarship, scholarship_alias
        )
    elif message_type == STATE_MESSAGE:
        datetime_now = datetime.datetime.now().strftime(DATETIME_FORMAT)

        message_with_emoji_aliases = message_template.format(
            datetime_now, start_datetime, count_of_calculated_scholarships
        )
    else:
        message_with_emoji_aliases = message_template

    return emoji.emojize(message_with_emoji_aliases, language="alias")


async def parse_grades(grades_str: str) -> list[int]:
    grades = list()

    for grade_str in grades_str:
        if grade_str.isdigit():
            n = int(grade_str) - 1
            grades += [grades[-1]] * n
        else:
            grades.append(await convert_grade_to_value(grade_str))

    return grades


async def calculate_gpa(grades: list[int]) -> float:
    return sum(grades) / len(grades)


async def calculate_scholarship(gpa: float) -> int:
    return round(B_MIN + (B_MAX - B_MIN) * (((gpa - 2) / 3) ** 2.5)) // 100 * 100


bot = Bot(token=TOKEN)

dp = Dispatcher(bot)


@dp.message_handler(commands=["start", "help"])
async def handle_help(message: types.Message):
    answer_message = await get_message(HELP_MESSAGE)
    await message.answer(answer_message)


@dp.message_handler(commands=["ping"])
async def handle_ping(message: types.Message):
    await message.answer("pong")


@dp.message_handler(commands=["state"])
async def handle_state(message: types.Message):
    answer_message = await get_message(STATE_MESSAGE)
    await message.answer(answer_message)


@dp.message_handler()
async def handle_grades(message: types.Message):
    global count_of_calculated_scholarships
    try:
        answer_message = await get_message(SCHOLARSHIP_MESSAGE, message.text)
        await message.answer(answer_message)

        count_of_calculated_scholarships += 1
    except Exception as e:
        answer_message = await get_message(SOMETHING_WENT_WRONG)
        await message.answer(answer_message)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
