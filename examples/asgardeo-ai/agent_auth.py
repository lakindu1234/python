"""
Copyright (c) 2025, WSO2 LLC. (https://www.wso2.com).
WSO2 LLC. licenses this file to you under the Apache License,
Version 2.0 (the "License"); you may not use this file except
in compliance with the License.
You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
KIND, either express or implied. See the License for the
specific language governing permissions and limitations
under the License.
"""

"""
AI Agent authentication example using Asgardeo AI SDK.

This example shows how to authenticate an AI agent and get tokens
for the agent to perform operations.
"""

import asyncio

from asgardeo import AsgardeoConfig
from asgardeo_ai import AgentAuthManager, AgentConfig


async def main():
    """AI Agent authentication example."""
    
    # Asgardeo configuration - Replace with your actual values
    config = AsgardeoConfig(
        base_url="https://api.asgardeo.io/t/<org-name>",
        client_id="<client-id>",
        redirect_uri="<redirect-uri>",
        client_secret="<client-secret>"
    )
    
    # AI Agent configuration - Replace with your actual agent credentials
    agent_config = AgentConfig(
        agent_id="<agent-id>",
        agent_secret="<agent-secret>"
    )
    
    try:
        # Create agent auth manager with context manager for cleanup
        async with AgentAuthManager(config, agent_config) as auth_manager:
            print("Authenticating AI Agent...")
            
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
