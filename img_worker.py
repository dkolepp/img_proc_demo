import os
import time
import rediswq
import img_lib

host = os.getenv("REDIS_SERVICE_HOST", "redis")

work_queue_name = os.getenv("QUEUE_NAME", "uploads")
queue = rediswq.RedisWQ(name=work_queue_name, host=host)

print("Worker with sessionID: " +  queue.sessionID())
print("Initial queue state: empty=" + str(queue.empty()))

while not queue.empty():

    # Get an item from the queue
    item = queue.lease(lease_secs=10, block=True, timeout=2)

    if item is not None:
        filename_to_process = item.decode("utf-8")
        print("Working on " + filename_to_process)

        # Use a backend image processing library
        # to process the image file.
        img_lib.process_file(filename_to_process)

        # Mark the queue item complete
        queue.complete(item)
else:
    print("Waiting for work")
    print("Queue empty, exiting")
####

