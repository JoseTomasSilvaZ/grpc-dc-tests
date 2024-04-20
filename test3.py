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
        print(f"isFromCache:{response.json()["fromCache"]}")
        return {
            'data': response.json(),
            'time': (end_time - start_time) * 1000,  # Convert seconds to milliseconds
            'hit': is_hit
        }
    except requests.RequestException as e:
        print(f"Failed to retrieve data for ID {id}: {e}")
        return None
    
def generate_random_id():
    return random.randint(1, 1000000)

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
    api_options = ['classic', 'partitioned', 'replicated']
    print_api_options()
    scope = input("Enter API option: ")

    for _ in range(1000):
        id = generate_random_id()
        data = get_data(id, api_options[int(scope) - 1])
        if data:
            responses_by_id[id] = data
            if data['hit']:
                cache_hits_times.append(data['time'])
            else:
                cache_misses_times.append(data['time'])
    
    print(f"Cache hits: {len(cache_hits_times)}")
    print(f"Cache misses: {len(cache_misses_times)}")
    print(f"Cache hit average time: {sum(cache_hits_times) / len(cache_hits_times) if len(cache_hits_times) > 0 else 0:.2f} ms")
    print(f"Cache misses average time: {sum(cache_misses_times) / len(cache_misses_times) if len(cache_misses_times) > 0 else 0:.2f} ms")

    plt.figure(figsize=(14, 7))

    # Scatter plot for cache hits and misses
    plt.subplot(1, 2, 1)
    plt.scatter(range(len(cache_hits_times)), cache_hits_times, color='green', alpha=0.7, label='Cache Hits')
    plt.scatter(range(len(cache_misses_times)), cache_misses_times, color='red', alpha=0.7, label='Cache Misses')
    plt.title('Response Times for Cache Hits and Misses')
    plt.xlabel('Sample Number')
    plt.ylabel('Response Time (ms)')
    plt.legend()

    # Bar chart for comparison of hits and misses
    plt.subplot(1, 2, 2)
    plt.bar(['Cache Hits', 'Cache Misses'], [len(cache_hits_times), len(cache_misses_times)], color=['green', 'red'])
    plt.title('Number of Cache Hits vs Misses')
    plt.ylabel('Count')

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
