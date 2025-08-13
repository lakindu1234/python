"""
On-Behalf-Of (OBO) token flow example using Asgardeo AI SDK.

This example shows how an AI agent can get authorization from users
and then obtain tokens on behalf of those users.
"""

import asyncio

import httpx
from asgardeo import AsgardeoConfig
from asgardeo_ai import AgentAuthManager, AgentConfig


async def main():
    """On-Behalf-Of (OBO) token flow example."""
    
    # AI Agent configuration - Replace with your actual agent credentials
    agent_config = AgentConfig(
        agent_id="<agent-id>",
        agent_secret="<agent-secret>"
    )
    
    # Create separate HTTP sessions to avoid sharing and closure issues
    session1 = httpx.AsyncClient()
    session2 = httpx.AsyncClient()
    
    try:
        # Create first config for agent authentication
        config1 = AsgardeoConfig(
            base_url="https://api.asgardeo.io/t/<org-name>",
            client_id="<client-id>",
            redirect_uri="<redirect-uri>",
            client_secret="<client-secret>",
            session=session1
        )
        
        # Create auth manager for initial operations
        auth_manager = AgentAuthManager(config1, agent_config)
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
            # Create fresh config and auth manager for OBO token exchange
            config2 = AsgardeoConfig(
                base_url="https://api.asgardeo.io/t/<org-name>",
                client_id="<client-id>",
                redirect_uri="<redirect-uri>",
                client_secret="<client-secret>",
                session=session2
            )
            
            # Create new auth manager with fresh session for OBO operation
            obo_auth_manager = AgentAuthManager(config2, agent_config)
            
            # Exchange the real authorization code for user tokens
            user_token = await obo_auth_manager.get_obo_token(
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
            print("The AI agent can now:")
            print("   • Access user's protected resources")
            print("   • Make API calls on behalf of the user")
            print("   • Maintain user context in AI operations")
            print("   • Perform actions with user's permissions")

            # Demonstrate token usage
            print("Testing token validity...")
            await asyncio.sleep(1)  # Simulate some work
            print("Token is valid and ready for use!")

        except Exception as e:
            print(f"Token exchange failed: {e}")
            print("Troubleshooting tips:")
            print("   • Make sure you copied the complete authorization code")
            print("   • Check that the code hasn't expired (usually valid for ~10 minutes)")
            print("   • Verify your Asgardeo configuration is correct")
            print("   • Ensure the redirect URI matches your configuration")
                
    except Exception as e:
        print(f"OBO flow failed: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Ensure proper cleanup of both sessions
        if 'session1' in locals():
            await session1.aclose()
        if 'session2' in locals():
            await session2.aclose()

if __name__ == "__main__":
    print("🚀 Asgardeo AI On-Behalf-Of (OBO) Flow Example")
    print("=" * 55)
    asyncio.run(main())
