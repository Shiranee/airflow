"""
Django-native Cigam authentication module using Django's cache framework
and requests library for HTTP operations.
"""
import base64
import json
import requests
from datetime import datetime, timezone, timedelta
from typing import Dict, Any
from django.core.cache import cache
from django.conf import settings
from django.core import signing


class CigamClient:
    def __init__(self):
        """Initialize the Cigam API client with Django configuration."""
        self.base_url = "https://api.cigamgestor.com.br"
        self.auth_endpoint = "/autenticacao/autenticar"
        self.data_endpoint = "/api/Consulta/ObterCarga"
        self.auth_cache_key = "cigam_auth_token"
        
        cigam_config = settings.CIGAM_API
        self.cigam_user = cigam_config['user']
        self.cigam_password = cigam_config['password']

    def _get_headers(self) -> Dict[str, str]:
        """Get base headers for API requests."""
        return {
            "Authorization": '',
            "Content-Type": "application/json; charset=utf-8",
            "Acesso": "live!"
        }

    def _encrypt_token(self, token: str) -> str:
        """Encrypt the token for secure storage using Django's signing."""
        return signing.dumps(token)

    def _decrypt_token(self, encrypted_token: str) -> str:
        """Decrypt the token for use using Django's signing."""
        try:
            return signing.loads(encrypted_token)
        except signing.BadSignature:
            raise ValueError("Invalid or corrupted token")

    def _authenticate(self) -> Dict[str, Any]:
        """Authenticate with the Cigam API and store the token in Django cache."""
        if not all([self.cigam_user, self.cigam_password]):
            raise ValueError("CIGAM_API credentials are not configured in settings")

        auth_string = f"{self.cigam_user}:{self.cigam_password}"
        auth_header = "Basic " + base64.b64encode(auth_string.encode()).decode()
        
        headers = self._get_headers()
        headers['Authorization'] = auth_header
        
        payload = {"ParametrosRetorno": [None, None]}
        url = f"{self.base_url}{self.auth_endpoint}"

        try:
            response = requests.post(
                url,
                json=payload,
                headers=headers,
                timeout=30
            )
            response.raise_for_status()
            
            response_data = response.json()
            token = response_data["dados"]["token"]
            expiration = response_data["dados"]["expiraEm"]
            
            expires_at = datetime.fromisoformat(expiration.replace('Z', '+00:00'))
            current_time = datetime.now(timezone.utc)
            
            cache_timeout = max(300, int((expires_at - current_time).total_seconds()) - 300)
            
            encrypted_token = self._encrypt_token(token)
            auth_data = {
                "token": encrypted_token,
                "expires_at": expires_at.isoformat(),
                "name": "Cigam Auth"
            }
            
            cache.set(self.auth_cache_key, auth_data, timeout=cache_timeout)
            
            return {
                "status": "success",
                "message": "Token stored in cache",
                "expires_at": expires_at
            }
            
        except requests.exceptions.RequestException as e:
            return {
                "error": "HTTP request failed", 
                "details": str(e)
            }
        except (KeyError, json.JSONDecodeError) as e:
            return {
                "error": "Invalid response format", 
                "details": str(e)
            }
        except Exception as e:
            return {
                "error": "Authentication failed", 
                "details": str(e)
            }

    def _get_token(self) -> str:
        """Get the current Cigam authentication token, refreshing if necessary."""
        auth_data = cache.get(self.auth_cache_key)
        
        if auth_data:
            try:
                expires_at = datetime.fromisoformat(auth_data["expires_at"])
                current_time = datetime.now(timezone.utc)
                
                if expires_at > current_time + timedelta(minutes=1):
                    return self._decrypt_token(auth_data["token"])
                    
            except Exception as e:
                pass
        
        auth_result = self._authenticate()
        
        if "error" in auth_result:
            raise Exception(f"Failed to authenticate with CIGAM: {auth_result['error']}")
        
        auth_data = cache.get(self.auth_cache_key)
        if not auth_data:
            raise Exception("Failed to retrieve token after authentication")
        
        return self._decrypt_token(auth_data["token"])

    def get_data(self, guid: str, body: Dict[str, Any]) -> Dict[str, Any]:
        """Get data from the Cigam API.
        
        Args:
            guid: The GUID parameter for the API endpoint
            body: The request body/payload
            
        Returns:
            Dict[str, Any]: The response data or error information
        """
        url = f"{self.base_url}{self.data_endpoint}?guid={guid}"
        
        headers = self._get_headers()
        headers['Authorization'] = f"Bearer {self._get_token()}"

        try:
            response = requests.post(
                url,
                json=body,
                headers=headers,
                timeout=30
            )
            response.raise_for_status()
            
            response_data = response.json()
            return response_data.get('dados', response_data)
            
        except requests.exceptions.RequestException as e:
            return {
                "error": "HTTP request failed", 
                "details": str(e),
                "status_code": getattr(e.response, 'status_code', None)
            }
        except json.JSONDecodeError:
            return {"error": "Invalid JSON response"}
        except Exception as e:
            return {
                "error": "Failed to process request", 
                "details": str(e)
            }
