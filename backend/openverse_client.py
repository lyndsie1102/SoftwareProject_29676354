import requests
import time
from typing import Dict, Any, Optional, List

class OpenverseClient:
    """
    A client for the OpenVerse API (https://api.openverse.org/v1/)
    that handles authentication and image search functionality.
    """

    BASE_URL = "https://api.openverse.org/v1"

    def __init__(self):
        self.access_token = None
        self.token_expiry = 0
        # You should replace these with your actual client credentials
        self.client_id = ""
        self.client_secret = ""

    def _get_auth_token(self) -> str:
        """
        Get an OAuth access token from the OpenVerse API.
        Caches the token until it expires.
        
        Returns:
            str: The access token
        """
        current_time = time.time()

        # Return cached token if it's still valid
        if self.access_token and current_time < self.token_expiry:
            return self.access_token

        # Request a new token
        auth_url = f"{self.BASE_URL}/auth_tokens/token/"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
        }
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "client_credentials"
        }
        try:
            # Send data as form data, not JSON
            response = requests.post(auth_url, headers=headers, data=data)
            response.raise_for_status()

            token_data = response.json()
            self.access_token = token_data.get("access_token")
            # Set expiry time (usually expires in 1 hour)
            expires_in = token_data.get("expires_in", 3600)
            self.token_expiry = current_time + expires_in

            return self.access_token

        except requests.exceptions.RequestException as e:
            print(f"Error getting auth token: {e} {response.text}")
            return None

    def search_images(self, 
                    query: str, 
                    page: int = 1, 
                    page_size: int = 20, 
                    license_type: Optional[str] = None,
                    creator: Optional[str] = None,
                    tags: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Search for images on OpenVerse
        
        Args:
            query (str): The search query
            page (int, optional): Page number for pagination. Defaults to 1.
            page_size (int, optional): Number of results per page. Defaults to 20.
            license_type (str, optional): Filter by license type.
            creator (str, optional): Filter by creator.
            tags (List[str], optional): List of tags to filter by.
            
        Returns:
            Dict[str, Any]: The search results
        """
        token = self._get_auth_token()
        if not token:
            return {"error": "Failed to authenticate with OpenVerse API"}

        search_url = f"{self.BASE_URL}/images/"
        headers = {
            "Authorization": f"Bearer {token}"
        }

        params = {
            "q": query,
            "page": page,
            "page_size": page_size,
        }

        # Add optional filters if provided
        if license_type:
            params["license"] = license_type
        if creator:
            params["creator"] = creator
        if tags:
            params["tags"] = ",".join(tags)

        try:
            response = requests.get(search_url, headers=headers, params=params)
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            return {"error": f"Error searching images: {str(e)}"}

# Usage example:
# client = OpenVerseClient()
# results = client.search_images("nature", page=1, page_size=10)