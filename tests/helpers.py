import asyncio
import time


async def run_until_success(coro, timeout: float = 15, retry_delay: float = 1.0):
    start_time = time.time()

    error = None
    while time.time() - start_time < timeout:
        try:
            # Try to run the callable and wait for its result
            result = await asyncio.wait_for(coro(), timeout=timeout)
            return result  # Return the result if successful
        except Exception as e:
            error = e
            # Ignore the error and continue attempting
            print(f"Error occurred: {e}. Retrying...")

        # Wait for the specified retry delay before trying again
        await asyncio.sleep(retry_delay)

    print("Timeout reached. No successful result.")
    raise error
