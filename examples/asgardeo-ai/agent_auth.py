"""
AI Agent authentication example using Asgardeo AI SDK.

This example shows how to authenticate an AI agent and get tokens
for the agent to perform operations.
"""

import asyncio

import httpx
from asgardeo import AsgardeoConfig
from asgardeo_ai import AgentAuthManager, AgentConfig


async def main():
    """AI Agent authentication example."""
    
    # Asgardeo configuration - Replace with your actual values
    config = AsgardeoConfig(
        base_url="https://api.asgardeo.io/t/<org-name>",
        client_id="<client-id>",
        redirect_uri="<redirect-uri>",
        client_secret="<client-secret>",
        session=httpx.AsyncClient()
    )
    
    # AI Agent configuration - Replace with your actual agent credentials
    agent_config = AgentConfig(
        agent_id="<agent-id>",
        agent_secret="<agent-secret>"
    )
    
    try:
        # Create agent auth manager with context manager for cleanup
        async with AgentAuthManager(config, agent_config) as auth_manager:
            print("🤖 Authenticating AI Agent...")
            
            # Define scopes the agent needs
            scopes = ["openid", "profile", "email"]
            
            # Get token for the agent
            agent_token = await auth_manager.get_agent_token(scopes)
            
            print("Agent authentication successful!")
            print(f"Agent Access Token: {agent_token.access_token[:20]}...")
            if agent_token.id_token:
                print(f"Agent ID Token: {agent_token.id_token[:20]}...")
            if agent_token.refresh_token:
                print(f"Agent Refresh Token: {agent_token.refresh_token[:20]}...")
            print(f"Expires in: {agent_token.expires_in} seconds")
            print(f"Scope: {agent_token.scope}")

            # Example: Use the agent token for API calls
            print("\n🔧 Agent token can now be used for API operations...")
            print("   - Making requests on behalf of the agent")
            print("   - Accessing agent-specific resources")
            print("   - Initiating user authorization flows")
            
    except Exception as e:
        print(f"Agent authentication failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    print("Asgardeo AI Agent Authentication Example")
    print("=" * 50)
    asyncio.run(main())
