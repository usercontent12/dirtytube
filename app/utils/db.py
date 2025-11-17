import requests
from app.config import Config
from functools import lru_cache

class D1Database:
    def __init__(self):
        self.account_id = Config.D1_ACCOUNT_ID
        self.database_id = Config.D1_DATABASE_ID
        self.read_api_key = Config.D1_READ_API_KEY
        self.write_api_key = Config.D1_WRITE_API_KEY
        self.base_url = f"https://api.cloudflare.com/client/v4/accounts/{self.account_id}/d1/database/{self.database_id}/query"
    


    def execute_query(self, sql, params=None, operation_type='read'):
        """
        Execute a SQL query against D1 database
        
        Args:
            sql: SQL query string
            params: Query parameters (optional)
            operation_type: 'read' or 'write' to determine which API key to use
        """
        # Select the appropriate API key based on operation type
        api_key = self.write_api_key if operation_type == 'write' else self.read_api_key
        
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            'sql': sql
        }
        
        if params:
            payload['params'] = params
        
        try:
            response = requests.post(self.base_url, json=payload, headers=headers)
            response.raise_for_status()
            result = response.json()
            
            if result.get('success'):
                return result.get('result', [{}])[0]
            else:
                print(f"D1 Query Error: {result.get('errors')}")
                return None
        except Exception as e:
            print(f"Database error: {str(e)}")
            return None
    
    def get_all_videos(self):
        """Get all videos sorted by favorite, display_order, and upload_date"""
        sql = """
            SELECT * FROM videos 
            ORDER BY favorite DESC, display_order ASC, upload_date DESC
        """
        result = self.execute_query(sql, operation_type='read')
        
        if result and 'results' in result:
            return result['results']
        return []
    
    def get_video_by_uuid(self, uuid):
        """Get a single video by UUID"""
        sql = "SELECT * FROM videos WHERE uuid = ?"
        result = self.execute_query(sql, [uuid], operation_type='read')
        
        if result and 'results' in result and len(result['results']) > 0:
            return result['results'][0]
        return None
    
    def increment_views(self, uuid):
        """Increment view count for a video (WRITE operation)"""
        sql = "UPDATE videos SET views = views + 1 WHERE uuid = ?"
        return self.execute_query(sql, [uuid], operation_type='write')
    
    def increment_likes(self, uuid):
        """Increment like count for a video (WRITE operation)"""
        sql = "UPDATE videos SET likes = likes + 1 WHERE uuid = ?"
        result = self.execute_query(sql, [uuid], operation_type='write')
        
        # Get updated like count using READ key
        video = self.get_video_by_uuid(uuid)
        if video:
            return video.get('likes', 0)
        return 0
    
    def get_video_count(self):
        """Get total video count"""
        sql = "SELECT COUNT(*) as count FROM videos"
        result = self.execute_query(sql, operation_type='read')
        
        if result and 'results' in result and len(result['results']) > 0:
            return result['results'][0].get('count', 0)
        return 0
    
    def get_popular_videos(self, limit=10):
        """Get most popular videos by views (READ operation)"""
        sql = """
            SELECT * FROM videos 
            ORDER BY views DESC, likes DESC 
            LIMIT ?
        """
        result = self.execute_query(sql, [limit], operation_type='read')
        
        if result and 'results' in result:
            return result['results']
        return []
    
    def get_favorite_videos(self):
        """Get all favorite videos (READ operation)"""
        sql = """
            SELECT * FROM videos 
            WHERE favorite = 1
            ORDER BY display_order ASC, upload_date DESC
        """
        result = self.execute_query(sql, operation_type='read')
        
        if result and 'results' in result:
            return result['results']
        return []
    
    def search_videos(self, search_term):
        """Search videos by title (READ operation)"""
        sql = """
            SELECT * FROM videos 
            WHERE title LIKE ? 
            ORDER BY favorite DESC, display_order ASC, upload_date DESC
        """
        result = self.execute_query(sql, [f'%{search_term}%'], operation_type='read')
        
        if result and 'results' in result:
            return result['results']
        return []
    
    def get_random_videos(self, exclude_uuid, limit=12, offset=0):
        """
        Get random videos except the current one, supports pagination via offset.
        """
        sql = """
            SELECT * FROM videos
            WHERE uuid != ?
            ORDER BY RANDOM()
            LIMIT ? OFFSET ?
        """
        result = self.execute_query(sql, [exclude_uuid, limit, offset], operation_type='read')
        
        if result and 'results' in result:
            return result['results']
        return []


    @lru_cache(maxsize=1)
    def get_cached_videos(self):
        return self.get_all_videos()
    
    



# Singleton instance
db = D1Database()