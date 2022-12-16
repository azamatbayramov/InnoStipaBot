import asyncio
from aiogram import Bot, Dispatcher, types

GRADES = {
    "A": 5,
    "B": 4,
    "C": 3,
    "D": 2,
    "P": 5,
    "F": 2
}

B_min = 3000
B_max = 20000
TOKEN = open("token.txt").readline().strip()


async def parse_grades(grades_str: str) -> list[int]:
    grades = list()

    for grade_str in grades_str:
        grades.append(GRADES[grade_str])

    return grades


async def get_gpa(grades: list[int]) -> float:
    return sum(grades) / len(grades)


async def calculate_scholarship(gpa: float) -> float:
    return B_min + (B_max - B_min) * (((gpa - 2) / 3) ** 2.5)


bot = Bot(token=TOKEN)

dp = Dispatcher(bot)


@dp.message_handler(commands=["start", "help"])
async def handle_help(message: types.Message):
    await message.answer(
        "Hello! I will help you to calculate your scholarship.\nJust send me your grades in a row. Example: AABBCP\n\nProgrammer: @azamatbayramov")


@dp.message_handler()
async def handle_grades(message: types.Message):
    try:
        grades = await parse_grades(message.text)
        gpa = await get_gpa(grades)
        scholarship = await calculate_scholarship(gpa)
        rounded_scholarship = round(scholarship) // 100 * 100
        await message.answer(f"Your scholarship is {rounded_scholarship} rubles.")
    except Exception:
        await message.answer("Something went wrong. Try again.")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
