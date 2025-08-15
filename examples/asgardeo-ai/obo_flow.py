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
On-Behalf-Of (OBO) token flow example using Asgardeo AI SDK.

This example shows how an AI agent can get authorization from users
and then obtain tokens on behalf of those users.
"""

import asyncio

from asgardeo import AsgardeoConfig
from asgardeo_ai import AgentAuthManager, AgentConfig


async def main():
    """On-Behalf-Of (OBO) token flow example."""
    
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
        async with AgentAuthManager(config, agent_config) as auth_manager:
            print("Starting On-Behalf-Of (OBO) flow...")
            
            # Step 1: Get agent token first
            print("Getting agent token...")
            agent_scopes = ["openid", "profile"]
            agent_token = await auth_manager.get_agent_token(agent_scopes)
            print(f"Agent authenticated: {agent_token.access_token[:20]}...")
            
            # Step 2: Generate authorization URL for user
            print("Generating user authorization URL...")
            user_scopes = ["openid", "profile", "email"]
            auth_url, state = auth_manager.get_authorization_url(
                scopes=user_scopes,
                resource="https://api.example.com"  # Optional resource parameter
            )
            
            print(f"AUTHORIZATION URL:")
            print("=" * 80)
            print(auth_url)
            print("=" * 80)
            print(f"STATE: {state}")
            
            print("NEXT STEPS:")
            print("1. Copy the URL above and open it in your browser")
            print("2. Log in with your Asgardeo credentials")
            print("3. Authorize the AI agent")
            print("4. After authorization, you'll be redirected to the callback URL")
            print("5. Copy the 'code' parameter from the callback URL")
            print("6. Come back here and paste it below")
            
            # Wait for user to complete OAuth flow
            print("Waiting for you to complete the OAuth flow...")
            input("Press ENTER when you've opened the URL and are ready to continue...")
            
            # Get authorization code from user
            print("Please paste the authorization code from the callback URL:")
            print("   (Look for '?code=...' in the URL after authorization)")
            authorization_code = input("Authorization code: ").strip()
            
            if not authorization_code:
                print("No authorization code provided. Exiting...")
                return
            
            # Step 3: Exchange authorization code for user token
            print(f"Exchanging authorization code for user token...")
            print(f"Using code: {authorization_code[:20]}...")
            
            try:
                # Exchange the real authorization code for user tokens
                user_token = await auth_manager.get_obo_token(
                    auth_code=authorization_code,
                    scopes=user_scopes,
                    agent_token=agent_token
                )
                
                print("SUCCESS! User token obtained via OBO flow!")
                print(f"User Access Token: {user_token.access_token[:30]}...")
                if user_token.id_token:
                    print(f"User ID Token: {user_token.id_token[:30]}...")
                if user_token.refresh_token:
                    print(f"User Refresh Token: {user_token.refresh_token[:30]}...")
                print(f"Expires in: {user_token.expires_in} seconds")
                print(f"Scope: {user_token.scope}")

                # Now the agent can act on behalf of the user
                print("\nThe AI agent can now:")
                print("   • Access user's protected resources")
                print("   • Make API calls on behalf of the user")
                print("   • Maintain user context in AI operations")
                print("   • Perform actions with user's permissions")

                # Demonstrate token usage
                print("\nTesting token validity...")
                await asyncio.sleep(1)  # Simulate some work
                print("Token is valid and ready for use!")
                
            except Exception as e:
                print(f"\nToken exchange failed: {e}")
                print("\nTroubleshooting tips:")
                print("   • Make sure you copied the complete authorization code")
                print("   • Check that the code hasn't expired (usually valid for ~10 minutes)")
                print("   • Verify your Asgardeo configuration is correct")
                print("   • Ensure the redirect URI matches your configuration")
                
    except Exception as e:
        print(f"OBO flow failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    print("Asgardeo AI On-Behalf-Of (OBO) Flow Example")
    print("=" * 55)
    asyncio.run(main())
