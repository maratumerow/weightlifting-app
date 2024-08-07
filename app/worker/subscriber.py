import redis

print("Starting app", flush=True)

try:
    r = redis.Redis(host="redis", port=6379, db=0)
    p = r.pubsub()
    p.subscribe("second")
    print("Subscribed to channel 'second'", flush=True)
except Exception as e:
    print(f"Error connecting to Redis: {e}", flush=True)
    exit(1)

print("Waiting for message", flush=True)

while True:
    message = p.get_message()
    if message:
        print(f"Received message: {message['data']}", flush=True)
