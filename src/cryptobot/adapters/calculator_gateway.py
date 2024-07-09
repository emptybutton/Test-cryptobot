from typing import Optional

import aiohttp

from src.periphery.envs import Env


async def calculate(a: int, b: int) -> Optional[int]:
    data = {'a': a, 'b': b}
    url = f"{Env.calculator_url.value}/api/0.1v/calculate/sum"

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data) as response:
            response_data = await response.json()
            sum_ = response_data.get("sum")

            return sum_ if isinstance(sum_, int) else None
