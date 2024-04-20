import requests
import random
import time
import matplotlib.pyplot as plt

def plot_data(ax, data, title, xlabel, ylabel, kind="line", ids=None):
    if kind == "line":
        ax.plot(data)
    elif kind == "bar":
        ax.bar(range(len(data)), data, tick_label=ids)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(True)
    ax.tick_params(axis='x', rotation=90)  # Rotate labels to prevent overlap


# 1. Request time



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
            'time': end_time - start_time,
            'hit': is_hit
        }
    except requests.RequestException as e:
        print(f"Failed to retrieve data for ID {id}: {e}")
        return None

def generate_random():
    return random.randint(1, 1000000)

def print_api_options():
    print("API Options:")
    print("1. Classic Cache")
    print("2. Partitioned Cache")
    print("3. Replicated Cache")
    print("Select an option by entering the corresponding number")

def main():
    results_dict = {}
    requests_by_id = {}
    response_times = []
    cache_hits = []
    cache_misses = []
    api_options = ['classic', 'partitioned', 'replicated']
    print_api_options()
    scope = input("Enter the API option: ")

    for _ in range(100):
        id = generate_random()
        data = get_data(id, api_options[int(scope) - 1])
        if data:
            results_dict[id] = data
            requests_by_id[id] = requests_by_id.get(id, 0) + 1
            response_times.append(data['time'])
            if data['hit']:
                cache_hits.append(data['time'])
            else:
                cache_misses.append(data['time'])

    fig, axs = plt.subplots(4, 1, figsize=(10, 20))
    plot_data(axs[0], response_times, "Response Times for Each Request", "Request Number", "Response Time (s)")
    plot_data(axs[1], cache_hits, "Response Times for Cache Hits", "Hit Number", "Response Time (s)")
    plot_data(axs[2], cache_misses, "Response Times for Cache Misses", "Miss Number", "Response Time (s)")
    plot_data(axs[3], list(requests_by_id.values()), "Number of Requests by ID", "ID", "Number of Requests", "bar", ids=list(requests_by_id.keys()))
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
