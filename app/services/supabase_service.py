from supabase import create_client, Client
from app.core.config import settings
from typing import Dict, Any, Optional

class SupabaseService:
    def __init__(self):
        # Only initialize if we have valid Supabase credentials
        if (settings.SUPABASE_URL 
            and settings.SUPABASE_KEY 
            and settings.SUPABASE_URL != "your_supabase_url_here"
            and settings.SUPABASE_KEY != "your_supabase_anon_key_here"):
            self.client: Client = create_client(
                settings.SUPABASE_URL, 
                settings.SUPABASE_KEY
            )
            self.admin_client: Client = create_client(
                settings.SUPABASE_URL, 
                settings.SUPABASE_SERVICE_KEY
            ) if settings.SUPABASE_SERVICE_KEY and settings.SUPABASE_SERVICE_KEY != "your_supabase_service_key_here" else None
        else:
            self.client = None
            self.admin_client = None
    
    async def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verify JWT token and return user data"""
        if not self.client:
            return None
        try:
            response = self.client.auth.get_user(token)
            return response.user.model_dump() if response.user else None
        except Exception:
            return None
    
    async def get_user_profile(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user profile from database"""
        if not self.client:
            return None
        try:
            response = self.client.table("profiles").select("*").eq("id", user_id).single().execute()
            return response.data
        except Exception:
            return None

supabase_service = SupabaseService()