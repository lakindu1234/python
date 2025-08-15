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
Native authentication example using Asgardeo SDK.

This example shows the detailed authentication flow with manual steps,
useful for understanding the authentication process or handling complex flows.
"""

import asyncio

from asgardeo import AsgardeoConfig, AsgardeoNativeAuthClient, FlowStatus


async def main():
    """Native authentication example."""
    
    # Configuration - Replace with your actual values
    config = AsgardeoConfig(
        base_url="https://api.asgardeo.io/t/<org-name>",
        client_id="<client-id>",
        redirect_uri="<redirect-uri>",
        client_secret="<client-secret>"
    )
    
    try:
        async with AsgardeoNativeAuthClient(config) as client:
            print("Starting authentication flow...")
            
            # Step 1: Initialize authentication
            init_response = await client.authenticate()
            print(f"Flow ID: {client.flow_id}")
            print(f"Flow Status: {client.flow_status}")

            if client.flow_status == FlowStatus.INCOMPLETE:
                print("Authentication requires additional steps")

                # Find the username/password authenticator
                authenticators = client.next_step.get('authenticators', [])
                print(f"Available authenticators: {[auth.get('authenticator') for auth in authenticators]}")

                # Look for BasicAuthenticator
                basic_auth = None
                for auth in authenticators:
                    if auth.get('authenticator') in ['Username & Password']:
                        basic_auth = auth
                        break
                
                if basic_auth:
                    print(f"Using authenticator: {basic_auth['authenticator']}")

                    # Step 2: Authenticate with credentials
                    username = "<username>"  # Replace with actual
                    password = "<password>"      # Replace with actual

                    auth_response = await client.authenticate(
                        authenticator_id=basic_auth['authenticatorId'],
                        params={
                            'username': username,
                            'password': password
                        }
                    )
                    print(f"Updated Flow Status: {client.flow_status}")
                else:
                    print("No username/password authenticator found")
                    return
            
            # Step 3: Get tokens if authentication succeeded
            if client.flow_status == FlowStatus.SUCCESS_COMPLETED:
                print("Authentication completed successfully!")
                
                tokens = await client.get_token()
                print("Retrieved tokens:")
                print(f"  Access Token: {tokens.access_token[:20]}...")
                if tokens.id_token:
                    print(f"  ID Token: {tokens.id_token[:20]}...")
                if tokens.refresh_token:
                    print(f"  Refresh Token: {tokens.refresh_token[:20]}...")
                print(f"  Expires in: {tokens.expires_in} seconds")
                print(f"  Scope: {tokens.scope}")
            else:
                print(f"Authentication failed with status: {client.flow_status}")
                
    except Exception as e:
        print(f"Error during authentication: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        await config.session.aclose()


if __name__ == "__main__":
    print("Asgardeo Native Authentication Example")
    print("=" * 55)
    asyncio.run(main())
