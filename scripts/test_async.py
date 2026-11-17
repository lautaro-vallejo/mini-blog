"""Módulo 7: dispara 4 peticiones al mismo tiempo y mide el tiempo total.

Uso (con la API corriendo):
    python scripts/test_async.py                 # contra /async
    python scripts/test_async.py sync            # contra /sync
    python scripts/test_async.py async https://tu-app.onrender.com
"""
import asyncio
import sys
import time

import httpx

MODE = sys.argv[1] if len(sys.argv) > 1 else "async"
BASE = sys.argv[2] if len(sys.argv) > 2 else "http://127.0.0.1:8000"
URL = f"{BASE.rstrip('/')}/api/v1/posts/{MODE}"
SLEEPS = [3.0, 5.5, 7.8, 9.7]


async def timed_get(client: httpx.AsyncClient, t: float):
    start = time.perf_counter()
    response = await client.get(URL, params={"t": t})
    response.raise_for_status()
    print(f"sleep={t:<4} tardó={time.perf_counter() - start:.2f}s")


async def main():
    async with httpx.AsyncClient(timeout=60) as client:
        start = time.perf_counter()

        # Dispara 4 peticiones AL MISMO TIEMPO
        await asyncio.gather(*(timed_get(client, t) for t in SLEEPS))

        total = time.perf_counter() - start
        print(f"Endpoint: {URL}")
        print(f"Suma de esperas: {sum(SLEEPS):.1f}s")
        print(f"Tiempo total de pared: {total:.2f}s")


if __name__ == "__main__":
    asyncio.run(main())
