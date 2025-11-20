from typing import Optional

class TaskSchema:
    VALID_STATUSES = ['pending', 'in_progress', 'completed', 'cancelled']
    VALID_PRIORITIES = ['low', 'medium', 'high']
    
    @staticmethod
    def validate_task(data: dict) -> tuple[bool, str]:
        if not data.get('title'):
            return False, 'Title is required'
        
        if len(data['title']) < 3:
            return False, 'Title must be at least 3 characters'
        
        if len(data['title']) > 200:
            return False, 'Title must be less than 200 characters'
        
        if 'status' in data and data['status'] not in TaskSchema.VALID_STATUSES:
            return False, f'Invalid status. Must be one of {TaskSchema.VALID_STATUSES}'
        
        if 'priority' in data and data['priority'] not in TaskSchema.VALID_PRIORITIES:
            return False, f'Invalid priority. Must be one of {TaskSchema.VALID_PRIORITIES}'
        
        if data.get('description') and len(data['description']) > 1000:
            return False, 'Description must be less than 1000 characters'
        
        return True, 'Valid'