# Asgardeo SDK

Simple async Python SDK for Asgardeo authentication.

## Installation

```bash
pip install asgardeo
```



## Usage

### Native Authentication
```python
async with AsgardeoNativeAuthClient(config) as client:
    # Start flow
    init_response = await client.authenticate()
    
    # Complete with credentials
    auth_response = await client.authenticate(
        authenticator_id="BasicAuthenticator",
        params={"username": "user@example.com", "password": "password"}
    )
    
    # Get tokens
    if client.flow_status == FlowStatus.SUCCESS_COMPLETED:
        tokens = await client.get_tokens()
```

## Features

- **Async/await support** - Non-blocking operations
- **Auto resource cleanup** - Context manager support
- **Simple API** - One-line authentication
- **Error handling** - Meaningful exceptions
- **Type hints** - Full type support

## Requirements

- Python >= 3.10
- httpx (async HTTP client)

## Development

```bash
# Install dependencies
poetry install

# Build
poetry build
```

## License

MIT License
