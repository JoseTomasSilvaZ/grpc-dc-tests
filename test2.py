import requests
import random
import time
import pandas as pd
import matplotlib.pyplot as plt

def plot_data(data, title, xlabel, ylabel, kind="line", ids=None):
    plt.figure(figsize=(10, 5))
    if kind == "line":
        plt.plot(data)
    elif kind == "bar":
        plt.bar(range(len(data)), data, tick_label=ids)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True)
    plt.xticks(rotation=90)
    plt.show()

def get_data(id):
    """Fetch data from the server and measure the request time."""
    try:
        start_time = time.time()
        response = requests.get(f"http://localhost:3000/posts/classic-cache/{id}")
        response.raise_for_status()
        end_time = time.time()
        is_hit = response.json().get('fromCache', False)
        return {
            'id': id,
            'time': end_time - start_time,
            'hit': is_hit,
            'data': response.json()
        }
    except requests.RequestException as e:
        print(f"Failed to retrieve data for ID {id}: {e}")
        return None

def generate_random():
    """Generate a random integer within a specified range."""
    return random.randint(1, 700000)

def main():
    results = []
    for _ in range(100):
        id = generate_random()
        data = get_data(id)
        if data:
            results.append(data)

    df = pd.DataFrame(results)
    df['hit_flag'] = df['hit'].apply(lambda x: 'Hit' if x else 'Miss')

    # Plot response times
    plot_data(df['time'], "Response Times for Each Request", "Request Number", "Response Time (s)")

    # Hits and Misses response times
    hits = df[df['hit'] == True]['time']
    misses = df[df['hit'] == False]['time']
    plot_data(hits, "Response Times for Cache Hits", "Hit Number", "Response Time (s)", "bar")
    plot_data(misses, "Response Times for Cache Misses", "Miss Number", "Response Time (s)", "bar")

    # Hit Rate and Miss Rate
    hit_rate = len(hits) / len(df)
    miss_rate = len(misses) / len(df)
    print(f"Cache Hit Rate: {hit_rate:.2f}, Cache Miss Rate: {miss_rate:.2f}")

    # Histogram of Response Times
    plt.figure(figsize=(10, 5))
    plt.hist(df['time'], bins=20, alpha=0.7, label='Total')
    plt.hist(hits, bins=20, alpha=0.7, label='Hits')
    plt.hist(misses, bins=20, alpha=0.7, label='Misses')
    plt.title("Histogram of Response Times")
    plt.xlabel("Response Time (s)")
    plt.ylabel("Frequency")
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main()

