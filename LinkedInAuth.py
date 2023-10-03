import requests
from urllib.parse import urlparse, parse_qs

class LinkedInAuth:

    AUTH_ENDPOINT = "https://www.linkedin.com/oauth/v2/authorization"
    TOKEN_ENDPOINT = "https://www.linkedin.com/oauth/v2/accessToken"
    REDIRECT_URI = "https://www.linkedin.com/developers/tools/oauth/redirect"  # or the other redirect URI you want to use
    SCOPES = ["openid", "profile", "w_member_social", "email"]  # Add or remove scopes as needed
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = None
        self.refresh_token = None  # Note: LinkedIn doesn't use refresh tokens in its standard OAuth2 flow
        self.BASE_URL = "https://api.linkedin.com/v2"

    def get_headers(self):
        if not self.is_authenticated():
            raise Exception("Not authenticated. Please obtain an access token first.")
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
            "X-Restli-Protocol-Version": "2.0.0"
        }

    def get_auth_url(self, state="random_string"):
        params = {
            "response_type": "code",
            "client_id": self.client_id,
            "redirect_uri": self.REDIRECT_URI,
            "state": state,
            "scope": " ".join(self.SCOPES)
        }
        response = requests.get(self.AUTH_ENDPOINT, params=params)
        return response.url

    def exchange_code_for_token(self, callback_url):
        parsed_url = urlparse(callback_url)
        params = parse_qs(parsed_url.query)
        auth_code = params.get("code")[0]

        payload = {
            "grant_type": "authorization_code",
            "code": auth_code,
            "redirect_uri": self.REDIRECT_URI,
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }

        response = requests.post(self.TOKEN_ENDPOINT, data=payload)
        tokens = response.json()

        self.access_token = tokens.get("access_token")
        return self.access_token

    def is_authenticated(self):
        return bool(self.access_token)

    def get_headers(self):
        if not self.is_authenticated():
            raise Exception("Not authenticated. Please obtain an access token first.")
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
            "X-Restli-Protocol-Version": "2.0.0"
        }


    def user_info(self):
        # Example endpoint; real endpoint might differ
        ENDPOINT = "https://api.linkedin.com/v2/userinfo"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        response = requests.get(ENDPOINT, headers=headers)
        return response.json()

    def get_asset(self, assetId):
        endpoint = f"{self.BASE_URL}/v2/assets/{assetId}"
        response = requests.get(endpoint, headers=self.get_headers())
        return response.json()

    def get_group_definition(self, id):
        endpoint = f"{self.BASE_URL}/v2/groupDefinitions/{id}"
        response = requests.get(endpoint, headers=self.get_headers())
        return response.json()

    def batch_get_images(self):
        endpoint = f"{self.BASE_URL}/v2/images"
        response = requests.get(endpoint, headers=self.get_headers())  # Assuming BATCH_GET is analogous to a GET request.
        return response.json()

    def get_image(self, imageId):
        endpoint = f"{self.BASE_URL}/v2/images/{imageId}"
        response = requests.get(endpoint, headers=self.get_headers())
        return response.json()

    def batch_get_videos(self):
        endpoint = f"{self.BASE_URL}/v2/videos"
        response = requests.get(endpoint, headers=self.get_headers())  # Assuming BATCH_GET is analogous to a GET request.
        return response.json()

    def get_video(self, videoId):
        endpoint = f"{self.BASE_URL}/v2/videos/{videoId}"
        response = requests.get(endpoint, headers=self.get_headers())
        return response.json()

# Usage:
linkedin_auth = LinkedInAuth("*****", "****")
auth_url = linkedin_auth.get_auth_url()
print(f"Go to this URL to authorize the app: {auth_url}")

# After user authorizes and gets redirected, you'd do something like:
callback_url_received_from_linkedin =  "https://www.linkedin.com/developers/tools/oauth/redirect?code=*****&state=random_string"
token = linkedin_auth.exchange_code_for_token(callback_url_received_from_linkedin)


posts = linkedin_auth.user_info()
print(posts)


headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json",
    "x-li-format": "json"
}

response = requests.get("https://api.linkedin.com/v2/w_member_social", headers=headers)
data = response.json()
data