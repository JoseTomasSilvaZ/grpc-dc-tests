import requests
import random
import time
import matplotlib.pyplot as plt


def get_data(id, scope):
    """Fetch data from the server and measure the request time."""
    try:
        start_time = time.time()
        response = requests.get(f"http://localhost:3000/posts/{scope}-cache/{id}")
        response.raise_for_status()
        end_time = time.time()
        is_hit = response.json().get('fromCache', False)
        return {
            'data': response.json(),
            'time': (end_time - start_time) * 1000,
            'hit': is_hit
        }
    except requests.RequestException as e:
        print(f"Failed to retrieve data for ID {id}: {e}")
        return None
    
def generate_random_id():
    return random.randint(1, 80_000)

def print_api_options():
    print("API Options:")
    print("1. Classic Cache")
    print("2. Partitioned Cache")
    print("3. Replicated Cache")
    print("Select an option by entering the corresponding number")

def main():
    cache_hits_times = []
    cache_misses_times = []
    responses_by_id = {}
    response_source = {}
    api_options = ['classic', 'partitioned', 'replicated']
    amount_of_requests = input("Enter the amount of requests: ")
    image_name = input("Enter the image name: ")
    print_api_options()
    scope = input("Enter API option: ")

    for x in range(int(amount_of_requests)):
        id = generate_random_id()
        data = get_data(id, api_options[int(scope) - 1])
        if data:
            source = data['data']['source']
            response_source[source] = response_source.get(source, 0) + 1
            responses_by_id[id] = data
            print(f"ID: {id}, Request: {x}, Cache: {'Hit' if data['hit'] else 'Miss'}")
            if data['hit']:
                cache_hits_times.append(data['time'])
            else:
                cache_misses_times.append(data['time'])
    
    print(f"Cache hits: {len(cache_hits_times)}")
    print(f"Cache misses: {len(cache_misses_times)}")
    print(f"Cache hit average time: {sum(cache_hits_times) / len(cache_hits_times) if len(cache_hits_times) > 0 else 0:.2f} ms")
    print(f"Cache misses average time: {sum(cache_misses_times) / len(cache_misses_times) if len(cache_misses_times) > 0 else 0:.2f} ms")
    print(f"Response sources: {response_source}")
    plt.figure(figsize=(14, 7))

    plt.subplot(4, 1, 1)
    plt.scatter(range(len(cache_hits_times)), cache_hits_times, color='green', alpha=0.7, label='Cache Hits')
    plt.scatter(range(len(cache_misses_times)), cache_misses_times, color='gray', alpha=0.7, label='Cache Misses')
    plt.title('Response Times for Cache Hits and Misses')
    plt.xlabel('Sample Number')
    plt.ylabel('Response Time (ms)')
    plt.legend()

    plt.subplot(4, 1, 3)
    plt.bar(range(len(cache_hits_times)), cache_hits_times, color='green', alpha=0.7, label='Cache Hits')
    plt.bar(range(len(cache_misses_times)), cache_misses_times, color='gray', alpha=0.7, label='Cache Misses')
    plt.title('Response Times for Cache Hits and Misses')
    plt.xlabel('Sample Number')
    plt.ylabel('Response Time (ms)')
    plt.legend()


    plt.subplot(4, 1, 2)
    plt.bar(['Cache Hits', 'Cache Misses'], [len(cache_hits_times), len(cache_misses_times)], color=['green', 'gray'])
    plt.title('Number of Cache Hits vs Misses')
    plt.ylabel('Count')

    plt.subplot(4, 1, 4)
    plt.bar(response_source.keys(), response_source.values(), color=['green', 'gray', 'red', 'blue', 'aqua'], alpha=0.7, label=response_source.keys())
    plt.title('Number of Responses by Source')
    plt.xlabel('Source')
    plt.ylabel('Responses')
    plt.legend()
    plt.tight_layout()

    plt.savefig(f"./{image_name}.png")
    plt.show()

if __name__ == "__main__":
    main()
