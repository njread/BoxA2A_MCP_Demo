"""
JWT-based Box Authentication for Agent
Following: https://github.com/box/box-python-sdk?tab=readme-ov-file#authorization
"""

import os
import json
import logging
from typing import Optional, Dict, Any
from dotenv import load_dotenv
from boxsdk import Client, JWTAuth
from boxsdk.exception import BoxAPIException

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class JWTBoxAuth:
    """JWT-based Box authentication using official SDK"""
    
    def __init__(self):
        # Load JWT configuration from environment or file
        self.jwt_config_path = os.getenv("BOX_JWT_CONFIG_PATH", "box_jwt_config.json")
        self.jwt_config = self._load_jwt_config()
        
        if not self.jwt_config:
            raise ValueError("JWT configuration not found. Please provide BOX_JWT_CONFIG_PATH or set config via environment variables")
        
        # Initialize JWT Auth
        try:
            logger.info(f"🔧 JWTAuth class: {JWTAuth}")
            logger.info(f"🔧 JWTAuth type: {type(JWTAuth)}")
            
            # Use the official Box SDK JWT authentication method
            logger.info("🔧 Using official Box SDK JWT method")
            self.auth = JWTAuth(
                client_id=self.jwt_config["boxAppSettings"]["clientID"],
                client_secret=self.jwt_config["boxAppSettings"]["clientSecret"],
                enterprise_id=self.jwt_config["enterpriseID"],
                jwt_key_id=self.jwt_config["boxAppSettings"]["appAuth"]["publicKeyID"],
                rsa_private_key_data=self.jwt_config["boxAppSettings"]["appAuth"]["privateKey"],
                rsa_private_key_passphrase=self.jwt_config["boxAppSettings"]["appAuth"]["passphrase"]
            )
            
            # Authenticate and get access token (required step)
            logger.info("🔧 Authenticating with Box...")
            access_token = self.auth.authenticate_instance()
            logger.info(f"✅ Box authentication successful, access token: {access_token[:20]}...")
            
        except Exception as e:
            logger.error(f"❌ Failed to create JWTAuth: {e}")
            logger.error(f"❌ JWT config: {json.dumps(self.jwt_config, indent=2)}")
            logger.error(f"❌ Exception type: {type(e)}")
            raise
        
        # Initialize client
        self.client = None
        self._authenticate()
    
    def _load_jwt_config(self) -> Optional[Dict[str, Any]]:
        """Load JWT configuration from file or environment variables"""
        
        # Try loading from file first
        if os.path.exists(self.jwt_config_path):
            try:
                with open(self.jwt_config_path, 'r') as f:
                    config = json.load(f)
                    logger.info("✅ JWT config loaded from file")
                    logger.info(f"📁 Config path: {self.jwt_config_path}")
                    logger.info(f"🔑 Config keys: {list(config.keys())}")
                    return config
            except Exception as e:
                logger.warning(f"⚠️  Could not load JWT config from file: {e}")
                logger.warning(f"📁 File path: {self.jwt_config_path}")
        
        # Try loading from environment variables
        try:
            config = {
                "boxAppSettings": {
                    "clientID": os.getenv("BOX_CLIENT_ID"),
                    "clientSecret": os.getenv("BOX_CLIENT_SECRET"),
                    "appAuth": {
                        "publicKeyID": os.getenv("BOX_PUBLIC_KEY_ID"),
                        "privateKey": os.getenv("BOX_PRIVATE_KEY", "").replace('\\n', '\n'),
                        "passphrase": os.getenv("BOX_PASSPHRASE", "")
                    }
                },
                "enterpriseID": os.getenv("BOX_ENTERPRISE_ID")
            }
            
            # Validate required fields
            required_fields = [
                config["boxAppSettings"]["clientID"],
                config["boxAppSettings"]["clientSecret"],
                config["boxAppSettings"]["appAuth"]["publicKeyID"],
                config["boxAppSettings"]["appAuth"]["privateKey"],
                config["enterpriseID"]
            ]
            
            if all(field for field in required_fields):
                logger.info("✅ JWT config loaded from environment variables")
                return config
            else:
                logger.warning("⚠️  Missing required JWT configuration in environment variables")
                
        except Exception as e:
            logger.warning(f"⚠️  Could not load JWT config from environment: {e}")
        
        return None
    
    def _authenticate(self):
        """Authenticate with Box using JWT"""
        try:
            # Create client with service account (enterprise) authentication
            self.client = Client(self.auth)
            
            # Test authentication by getting service account user info
            service_account = self.client.user().get()
            logger.info(f"✅ JWT Authentication successful as service account: {service_account.name}")
            
            return self.client
            
        except BoxAPIException as e:
            logger.error(f"❌ JWT Authentication failed: {e}")
            raise
        except Exception as e:
            logger.error(f"❌ Unexpected error during JWT authentication: {e}")
            raise
    
    def get_client(self) -> Client:
        """Get the authenticated Box client"""
        return self.client
    
    def get_headers(self) -> Dict[str, str]:
        """Get headers for direct API calls"""
        try:
            # Get access token from the client
            access_token = self.client.auth.access_token
            return {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
        except Exception as e:
            logger.error(f"Error getting headers: {e}")
            raise

def get_jwt_auth() -> JWTBoxAuth:
    """Get a JWT Box authentication instance"""
    return JWTBoxAuth()

def ensure_authenticated() -> JWTBoxAuth:
    """Ensure we have an authenticated Box client"""
    return get_jwt_auth()

def get_box_client() -> Client:
    """Get an authenticated Box client"""
    return get_jwt_auth().get_client() 