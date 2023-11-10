import asyncio
import json
import platform

import aiohttp
import faker


NUMBER_CONTACTS = 1000


fake_data = faker.Faker("uk_UA")


async def get_fake_contacts():
    for _ in range(NUMBER_CONTACTS):
        yield (lambda x: [x[1], x[2]] if len(x) == 3 else [x[0], x[1]])(
            fake_data.name().split(" ")
        ) + [
            fake_data.email(),
            fake_data.phone_number(),
            fake_data.date(),
            fake_data.address(),
        ]


async def send_data_to_api() -> None:
    headers = {
        "content-type": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbmlzdHJhdG9yQGFwaS5jb20iLCJpYXQiOjE2OTk1ODAyNjMsImV4cCI6MTY5OTU4MTE2Mywic2NvcGUiOiJhY2Nlc3NfdG9rZW4ifQ.ywYta7MR8kiGcO9XaCZBtjCjTlP5Ohzc0ynSJmepleg",
    }
    session = aiohttp.ClientSession()
    async for first_name, last_name, email, phone, birthday, address in get_fake_contacts():
        data = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "phone": phone,
            "birthday": birthday,
            "address": address,
        }
        try:
            await session.post(
                "http://127.0.0.1:8000/api/contacts",
                headers=headers,
                data=json.dumps(data),
            )
        except aiohttp.ClientOSError as err:
            print(f"Connection error: {str(err)}")
    await session.close()
    print("Done")


if __name__ == "__main__":
    if platform.system() == "Windows":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(send_data_to_api())