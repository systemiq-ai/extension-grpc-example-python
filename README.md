# Extension gRPC Service Example

Systemiq Extensions enable developers to add custom logic to process and analyse data. This example implements a Python based gRPC server that handles extension data requests and integrates JWT authentication.

- **Fetch Data**: The server can read data payloads sent by clients and pass them to a business logic function.
- **Configuration Parsing**: The request may include a JSON string called `config_json`, the server turns it into a dictionary for dynamic settings.
- **Action Processing**: The request carries an `action` field, for example `"process"` or `"skip"`. You can extend the `process` function to act on this flag.
- **Authentication**: Every request must carry a valid RS256 JWT in the `token` field. The server validates the signature, client ID and scopes.

## Requirements

- Python 3.13 or newer  
- RS256 public key  
- The environment variables `PUBLIC_KEY` and `CLIENT_IDS`

## Setup

Install the dependencies:

```bash
pip install -r requirements.txt
```

Export the required variables:

```bash
export PUBLIC_KEY="your-RS256-public-key"
export CLIENT_IDS="1,2,3"
```

Optional, increase the maximum message size (default is 4 MB):

```bash
export MAX_MSG_SIZE_MB=8
```

## Usage

Run the server locally:

```bash
python main.py
```

### Development mode with auto reload

```bash
ENVIRONMENT=development python main.py
```

The included Dockerfile uses `watchmedo` to restart the process when a file changes in development mode.

## Docker

Build the image:

```bash
docker build -t extension-grpc .
```

Run the container:

```bash
docker run --rm \
  -e PUBLIC_KEY="your-RS256-public-key" \
  -e CLIENT_IDS="1" \
  -e MAX_MSG_SIZE_MB=8 \
  -p 50051:50051 \
  extension-grpc
```

## Proto Interface

The service exposes one RPC named `ExtensionData` defined in `extension.proto`.

```proto
rpc ExtensionData(ExtensionRequest) returns (ExtensionResponse);
```

`ExtensionRequest` fields:

| Field        | Type            | Description                                         |
|--------------|-----------------|-----------------------------------------------------|
| token        | string          | RS256 JWT used for authentication                   |
| action       | string          | For example `"process"` or `"skip"`                 |
| data         | repeated string | JSON-encoded data strings to process                |
| indicators   | repeated string | Optional indicator names                            |
| config_json  | string          | Optional JSON configuration for dynamic parameters  |

## License

MIT © [systemiq.ai](https://systemiq.ai)