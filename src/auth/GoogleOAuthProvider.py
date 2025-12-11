from typing import Dict, List, Tuple, Optional
import os
from chainlit.user import User
import httpx


class OAuthProvider:
    id: str
    env: List[str]
    client_id: str
    client_secret: str
    authorize_url: str
    authorize_params: Dict[str, str]
    default_prompt: Optional[str] = None

    def is_configured(self):
        return all([os.environ.get(env) for env in self.env])

    async def get_token(self, code: str, url: str) -> str:
        raise NotImplementedError

    async def get_user_info(self, token: str) -> Tuple[Dict[str, str], User]:
        raise NotImplementedError

    def get_env_prefix(self) -> str:
        """Return environment prefix, like AZURE_AD."""

        return self.id.replace("-", "_").upper()

    def get_prompt(self) -> Optional[str]:
        """Return OAuth prompt param."""
        if prompt := os.environ.get(f"OAUTH_{self.get_env_prefix()}_PROMPT"):
            return prompt

        if prompt := os.environ.get("OAUTH_PROMPT"):
            return prompt

        return self.default_prompt


class GoogleOAuthProvider(OAuthProvider):
    id = "google"
    env = ["OAUTH_GOOGLE_CLIENT_ID", "OAUTH_GOOGLE_CLIENT_SECRET"]
    authorize_url = "https://accounts.google.com/o/oauth2/v2/auth"

    def init(self, 
             oauth_google_client_id: str = None,
             oauth_google_client_secret: str = None):
        # self.client_id = os.environ.get("OAUTH_GOOGLE_CLIENT_ID")
        # self.client_secret = os.environ.get("OAUTH_GOOGLE_CLIENT_SECRET")
        self.client_id = oauth_google_client_id
        self.client_secret = oauth_google_client_secret
        self.authorize_params = {
            "scope": "https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/userinfo.email",
            "response_type": "code",
            "access_type": "offline",
        }
        if prompt := self.get_prompt():
            self.authorize_params["prompt"] = prompt

    async def get_token(self, code: str, url: str):
        payload = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": url,
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://oauth2.googleapis.com/token",
                data=payload,
            )
            response.raise_for_status()
            json = response.json()
            token = json.get("access_token")
            if not token:
                raise httpx.HTTPStatusError(
                    "Failed to get the access token",
                    request=response.request,
                    response=response,
                )
            return token

    async def get_user_info(self, token: str):
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://www.googleapis.com/userinfo/v2/me",
                headers={"Authorization": f"Bearer {token}"},
            )
            response.raise_for_status()
            google_user = response.json()
            user = User(
                identifier=google_user["email"],
                metadata={
                    "image": google_user["picture"], "provider": "google"},
            )
            return (google_user, user)
