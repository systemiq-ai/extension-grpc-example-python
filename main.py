import logging
import runner

def process(request, payload, config):
    """
    Business-logic stub.

    Replace this with your real processing pipeline.
    """
    logging.info(
        "Received action: %s, Payload: %s, Data: %s, Indicators: %s, Config: %s",
        request.action,
        payload,
        list(request.data),
        list(request.indicators),
        config,
    )

if __name__ == "__main__":
    runner.serve(process)