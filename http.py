import asyncio
import aiohttp
import argparse

# Set up command-line argument parsing
parser = argparse.ArgumentParser(description="Asynchronous Web Server Load Test Tool")
parser.add_argument('url', type=str, help='Target URL')
parser.add_argument('-n', '--num_requests', type=int, default=1000, help='Number of requests to send (default 1000)')
args = parser.parse_args()

async def send_request(session, url):
    try:
        async with session.get(url) as response:
            print(f"Received {response.status} from {url}")
            await response.read()  # Ensure complete response is read
    except Exception as e:
        print(f"Request failed: {e}")

async def main():
    async with aiohttp.ClientSession() as session:
        tasks = []
        for _ in range(args.num_requests):
            task = asyncio.create_task(send_request(session, args.url))
            tasks.append(task)
            # Remove any explicit delay to maximize request speed
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
