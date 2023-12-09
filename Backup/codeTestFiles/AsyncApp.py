
import time

import aiohttp
import asyncio
async def getInf(i,t):
    await asyncio.sleep(t)
    print(f'task {i} done')

async def main():

    times = [.5,1,2]
    # times = [1,2,3]

    Tasks = []

    start = time.time()

    for i,t in enumerate(times):
        Tasks.append(asyncio.create_task( getInf(i+1,t) ))

    await asyncio.gather(*Tasks)

    end = time.time()
    print(f'Time taken: {end-start}')


if __name__ == '__main__':
    asyncio.run(main())