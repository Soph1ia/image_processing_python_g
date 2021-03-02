"""
About Project to resize the image and measure the throughput for the task
"""
# imports
from PIL import Image
import time
import statistics
import logging
import google.cloud.logging


def setup_logging():
    """
    This method connects to google logging client to set up automatically the logging for functions
    :return: None
    """
    client = google.cloud.logging.Client()

    client.get_default_handler()
    client.setup_logging()


def hello_world(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
    request_json = request.get_json()
    if request.args and 'message' in request.args:
        benchmark()
        return "Benchmark Completed"
    elif request_json and 'message' in request_json:
        benchmark()
        return "Benchmark Completed"
    else:
        return f'Hello, failed to run the image processing '


def image_processing():
    """
    This method resizes the image.
    :return: image
    """
    image_to_process = Image.open("image.jpg")

    # Resize the image
    resized_image = image_to_process.resize((1024, 1000))

    return resized_image


def benchmark():
    """
    This is the main benchmarking method that runs the function and calculates the throughput and the average time
    :return: None
    """
    throughput_time = {"Image": []}
    average_duration_time = {"Image": []}

    for i in range(40):  # adjust accordingly so whole thing takes a few sec
        logging.info('Image Processing execution beginning')
        t0 = time.time()
        image_processing()
        t1 = time.time()
        logging.info('Image Processing function ended, calculating metrics')
        if i >= 20:  # We let it warmup for first 20 rounds, then consider the last 20 metrics
            throughput_time["Image"].append(1 / ((t1 - t0) * 1000))
            average_duration_time["Image"].append(((t1 - t0) * 1000) / 1)

           # Printing out results for throughput
    for name, numbers in throughput_time.items():
        logging.info("The throughput time")
        length = str(len(numbers))
        median = str(statistics.median(numbers))
        mean = str(statistics.mean(numbers))
        stdev = str(statistics.stdev(numbers))
        output = "FUNCTION {} used {} times. > MEDIAN {} ops/s > MEAN {} ops/s  > STDEV {} ops/s".format(name,
                                                                                                            length,
                                                                                                            median,
                                                                                                            mean,
                                                                                                            stdev)
        logging.info(output)

    # printing out results for average duration
    for name, numbers in average_duration_time.items():
        logging.info("The average Duration details")
        length = str(len(numbers))
        median = str(statistics.median(numbers))
        mean = str(statistics.mean(numbers))
        stdev = str(statistics.stdev(numbers))
        output = "FUNCTION {} used {} times. > MEDIAN {} s/ops > MEAN {} s/ops  > STDEV {} s/ops".format(name,
                                                                                                            length,
                                                                                                            median,
                                                                                                            mean,
                                                                                                            stdev)
        logging.info(output)

    logging.critical("The benchmark is finished properly")
