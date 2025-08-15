# Asgardeo Python SDKs

Official Python SDKs for [Asgardeo](https://wso2.com/asgardeo/) - WSO2's Identity and Access Management platform.

## Packages

This repository contains two complementary Python packages:

### [asgardeo](./packages/asgardeo/)
Core Python SDK for Asgardeo authentication flows.

```bash
pip install asgardeo
```

**Features:**
- ✅ Native authentication flows (no browser redirects)
- ✅ Token management (exchange, refresh)
- ✅ Full async/await support
- ✅ Automatic resource cleanup
- ✅ Type hints and error handling

### [asgardeo-ai](./packages/asgardeo-ai/)
AI agent authentication and on-behalf-of (OBO) token flows.

> ⚠️ WARNING: Asgardeo AI SDK is currently under development, is not intended for production use, and therefore has no official support.

```bash  
pip install asgardeo-ai
```

**Features:**
- ✅ AI agent authentication
- ✅ On-behalf-of (OBO) token flows
- ✅ User authorization URL generation
- ✅ Built on top of core asgardeo SDK

## Quick Start

### Core Authentication
```python
from asgardeo import AsgardeoConfig, AsgardeoNativeAuthClient

config = AsgardeoConfig(
    base_url="https://api.asgardeo.io/t/your-org",
    client_id="your_client_id",
    redirect_uri="your_redirect_uri",
    client_secret="your_client_secret"
)

async with AsgardeoNativeAuthClient(config) as client:
    # Authenticate user
    await client.authenticate()
    await client.authenticate(
        authenticator_id="BasicAuthenticator",
        params={"username": "user@example.com", "password": "password"}
    )
    
    # Get tokens
    if client.flow_status == "SUCCESS_COMPLETED":
        tokens = await client.get_tokens()
        print(f"Access Token: {tokens.access_token}")
```

### AI Agent Authentication
```python
from asgardeo import AsgardeoConfig
from asgardeo_ai import AgentAuthManager, AgentConfig

config = AsgardeoConfig(
    base_url="https://api.asgardeo.io/t/your-org",
    client_id="your_client_id",
    redirect_uri="https://your-app.com/callback",
    client_secret="your_client_secret"
)

agent_config = AgentConfig(
    agent_id="your_agent_id",
    agent_secret="your_agent_secret"
)

async with AgentAuthManager(config, agent_config) as auth_manager:
    # Get agent token
    agent_token = await auth_manager.get_agent_token(["openid", "profile"])
    
    # Generate user authorization URL
    auth_url, state = auth_manager.get_authorization_url(["openid", "email"])
    
    # Exchange auth code for user token (OBO flow)
    user_token = await auth_manager.get_obo_token(auth_code, agent_token=agent_token)
```

## Documentation

- **[Core SDK Guide](./packages/asgardeo/README.md)** - Native authentication flows
- **[AI SDK Guide](./packages/asgardeo-ai/README.md)** - Agent authentication and OBO flows  
- **[Examples](./examples/)** - Complete working examples
- **[Publishing Guide](./PUBLISHING.md)** - Release and deployment process

## Examples

The [`examples/`](./examples/) directory contains practical examples:

### Core SDK Examples
- **[native_auth.py](./examples/asgardeo/native_auth.py)** - Step-by-step authentication flow

### AI SDK Examples  
- **[agent_auth.py](./examples/asgardeo-ai/agent_auth.py)** - Basic AI agent authentication
- **[obo_flow.py](./examples/asgardeo-ai/obo_flow.py)** - Interactive OBO token flow

## Development

### Prerequisites
- Python 3.10+
- [Poetry](https://python-poetry.org/) for dependency management

### Setup
```bash
# Clone repository
git clone https://github.com/asgardeo/python.git
cd python

# Install core SDK
cd packages/asgardeo
poetry install

# Install AI SDK
cd ../asgardeo-ai  
poetry install
```

### Building
```bash
# Build core SDK
cd packages/asgardeo
poetry build

# Build AI SDK
cd ../asgardeo-ai
poetry build
```

### Testing Examples
```bash
# Test core SDK example
python examples/asgardeo/native_auth.py

# Test AI SDK examples
python examples/asgardeo-ai/agent_auth.py
python examples/asgardeo-ai/obo_flow.py
```

## 📋 Requirements

- **Python 3.10+** - Modern async/await features
- **Asgardeo Account** - Sign up at [asgardeo.io](https://asgardeo.io)
