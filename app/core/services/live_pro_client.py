'''
Service for handling live-pro requests
'''
import requests
import os

BASE_URL = os.environ.get('PRO_URL')


def get_credential():
    """
    Logs in a user via Sanctum and accesses a protected endpoint.
    """

    login_payload = {
        "email": os.environ.get('PRO_EMAIL'),
        "password": os.environ.get('PRO_PASS')
    }

    login_resp = requests.post(f"{BASE_URL}/login", json=login_payload)
    
    if login_resp.status_code != 200:
        raise Exception(f"Login failed: {login_resp.json()}")

    data = login_resp.json()
    token = data.get("token")
    if not token:
        raise Exception(f"No token returned: {data}")

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }
    
    return token, headers

def create_pro_user(documents):
    """
    Creates new ProUser(s) with the given document(s).
    
    Args:
        documents (str | list): A single CPF/CNPJ string OR a list of CPF/CNPJs.
        
    Returns:
        dict: Response from the API
    """
    try:
        token, headers = get_credential()

        if isinstance(documents, str):
            payload = {"document": documents}
        elif isinstance(documents, list):
            payload = {"documents": documents}
        else:
            raise ValueError("documents must be a string or a list of strings")

        response = requests.post(
            f"{BASE_URL}/pro-users/create", 
            json=payload, 
            headers=headers
        )

        if response.status_code in (200, 201):
            return {
                "success": True,
                "data": response.json()
            }
        else:
            return {
                "success": False,
                "status_code": response.status_code,
                "error": response.json() if response.content else response.text
            }

    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {str(e)}")
    except Exception as e:
        raise Exception(f"Error creating pro user(s): {str(e)}")

def pro_audiences(payload: dict, method:str = 'post', route:str = '/'):
		"""
		Module for creating live! pro audiences.
		"""
		try:
				token, headers = get_credential()

				content = {
						"url":f"{BASE_URL}/audiences{route}",
						"json":payload,
						"headers":headers
				}

				if method == 'post':
						response = requests.post(**content)
				elif method == 'get':
						response = requests.get(**content)
				elif method == 'delete':
						response = requests.delete(**content)
				else:
						return 'Invalid method'				

				if response.status_code in (200, 201):
						return {
								"success": True,
								"data": response.json()
						}
				else:
						return {
								"success": False,
								"status_code": response.status_code,
								"error": response.json() if response.content else response.text
						}

		except requests.exceptions.RequestException as e:
				raise Exception(f"Request failed: {str(e)}")
		except Exception as e:
				raise Exception(f"Error creating pro user(s): {str(e)}")
