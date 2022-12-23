import asyncio

import emoji
from aiogram import Bot, Dispatcher, types

GRADES = {
    "a": 5,
    "b": 4,
    "c": 3,
    "d": 2,
    "p": 5,
    "f": 2
}

SCHOLARSHIP_EMOJI = {
    3: ":dizzy_face:",
    4: ":astonished:",
    5: ":confounded:",
    6: ":sob:",
    7: ":cold_sweat:",
    8: ":fearful:",
    9: ":cry:",
    10: ":pensive:",
    11: ":unamused:",
    12: ":grimacing:",
    13: ":confused:",
    14: ":sweat_smile:",
    15: ":relieved:",
    16: ":relaxed:",
    17: ":grinning:",
    18: ":smirk:",
    19: ":blush:",
    20: ":heart_eyes:"
}
B_min = 3000
B_max = 20000
TOKEN = open("token.txt").readline().strip()


async def parse_grades(grades_str: str) -> list[int]:
    grades = list()

    for grade_str in grades_str:
        if grade_str.isdigit():
            n = int(grade_str) - 1
            grades += [grades[-1]] * n
        else:
            grades.append(GRADES[grade_str])

    return grades


async def get_gpa(grades: list[int]) -> float:
    return sum(grades) / len(grades)


async def calculate_scholarship(gpa: float) -> int:
    return round(B_min + (B_max - B_min) * (((gpa - 2) / 3) ** 2.5)) // 100 * 100


bot = Bot(token=TOKEN)

dp = Dispatcher(bot)


@dp.message_handler(commands=["start", "help"])
async def handle_help(message: types.Message):
    await message.answer(emoji.emojize(
        f"Hello:wave: I will help you to calculate your scholarship:moneybag:\n"
        "Just send me your grades in a row. Example: AABBCP or A2B2CP\n"
        "\n"
        "Programmer: @azamatbayramov", language="alias"))


async def get_emoji(scholarship: int) -> str:
    return emoji.emojize(SCHOLARSHIP_EMOJI[scholarship // 1000], language="alias")


@dp.message_handler(commands=["ping"])
async def handle_help(message: types.Message):
    await message.answer("pong")


@dp.message_handler()
async def handle_grades(message: types.Message):
    try:
        grades = await parse_grades(message.text.lower())
        gpa = await get_gpa(grades)
        scholarship = await calculate_scholarship(gpa)
        emoji_str = await get_emoji(scholarship)
        await message.answer(f"{emoji_str} Your scholarship will be {scholarship} rubles {emoji_str}")
    except Exception:
        await message.answer(emoji.emojize("Something went wrong, try again :cry:\n\n"
                                           "If you need help, write me /help :wink:", language="alias"))


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
