# frontend.py

import aiohttp
import asyncio
import time

async def fetch(session, url):
    """
    Fetches data from the specified URL using the provided session.

    Args:
        session (aiohttp.ClientSession): The session to use for making the request.
        url (str): The URL to fetch data from.

    Returns:
        tuple: A tuple containing the elapsed time (in seconds) and the response data.

    """
    start_time = time.time()  # Captura el tiempo de inicio de la solicitud
    async with session.get(url) as response:
        elapsed_time = time.time() - start_time  # Calcula el tiempo transcurrido
        response_data = await response.json()
        return elapsed_time, response_data

async def main():
    """
    Perform asynchronous HTTP requests in batches and calculate average response time.

    This function sends a specified number of HTTP requests to a given URL in batches using asyncio.
    It calculates the total time taken to complete all the requests and the average time per request.

    Args:
        None

    Returns:
        None
    """
    total_time = 0
    total_requests = 100  # Número total de solicitudes a realizar
    batch_size = 10  # Tamaño del lote de solicitudes
    
    async with aiohttp.ClientSession() as session:
        tasks = []
        for _ in range(total_requests // batch_size):
            batch_tasks = []
            for _ in range(batch_size):
                task = asyncio.create_task(fetch(session, 'http://localhost:8080/'))
                batch_tasks.append(task)
            batch_responses = await asyncio.gather(*batch_tasks)
            for elapsed_time, response_data in batch_responses:
                total_time += elapsed_time
                print(response_data)
        
        # Procesar las solicitudes restantes (si hay menos de batch_size)
        remaining_tasks = total_requests % batch_size
        for _ in range(remaining_tasks):
            task = asyncio.create_task(fetch(session, 'http://localhost:8080/'))
            elapsed_time, response_data = await task
            total_time += elapsed_time
            print(response_data)
    
    average_time_per_request = total_time / total_requests
    print(f"Tiempo total: {total_time} segundos")
    print(f"Número total de peticiones: {total_requests}")
    print(f"tamaño del lote: {batch_size}")
    print(f"Tiempo promedio por petición: {average_time_per_request} segundos")

if __name__ == '__main__':
    asyncio.run(main())
