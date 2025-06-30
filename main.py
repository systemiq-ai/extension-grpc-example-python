import json
import logging
import grpc
from concurrent import futures
import os

import extension_pb2
import extension_pb2_grpc
from auth import verify_token
from data_processor import process


class DataExtensionService(extension_pb2_grpc.DataExtensionServicer):
    """Implements the ExtensionData RPC."""

    def ExtensionData(self, request, context):
        # 1. Verify JWT to obtain payload
        try:
            payload = verify_token(request.token)
        except ValueError as err:
            context.abort(grpc.StatusCode.UNAUTHENTICATED, str(err))

        # 2. Read request.config (try to JSON-decode, but accept raw string)
        config_raw = request.config_json  # field in your .proto
        try:
            config_dict = json.loads(config_raw) if config_raw else None
        except json.JSONDecodeError as exc:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, f"Invalid config_json: {exc}")

        # 3. Call business logic
        process(request, payload, config_dict)

        return extension_pb2.ExtensionResponse()


def serve(address="[::]:50051", max_workers=10):
    logging.basicConfig(level=logging.INFO)
    max_msg_size_mb = int(os.getenv("MAX_MSG_SIZE_MB", "4"))  # Default to 4 MB
    max_msg_size_bytes = max_msg_size_mb * 1024 * 1024
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=max_workers),
        options=[
            ("grpc.max_receive_message_length", max_msg_size_bytes),
        ],
    )
    extension_pb2_grpc.add_DataExtensionServicer_to_server(
        DataExtensionService(), server
    )
    server.add_insecure_port(address)
    logging.info("Server started on %s", address)
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()