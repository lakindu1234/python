# Examples

This directory contains examples for using the Asgardeo Python SDKs.

## Structure

- `asgardeo/` - Examples for the core Asgardeo SDK
- `asgardeo-ai/` - Examples for the Asgardeo AI SDK

## Setup

Before running the examples, make sure to:

1. Install the packages:
```bash
cd asgardeo && poetry install
cd ../asgardeo-ai && poetry install
```

2. Set up your configuration in each example file with your actual Asgardeo credentials.

## Running Examples

Each example is a standalone Python script that can be run directly:

```bash
python examples/asgardeo/basic_auth.py
python examples/asgardeo-ai/agent_auth.py
```