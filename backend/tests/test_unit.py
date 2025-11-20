import pytest
from app.services.task_service import TaskService
from app.schemas import TaskSchema
from app.models import Task

class TestTaskSchema:
    """Suite de pruebas unitarias para esquemas (5 pruebas)"""
    
    def test_validate_task_valid(self):
        data = {'title': 'Test Task'}
        is_valid, message = TaskSchema.validate_task(data)
        assert is_valid is True
        assert message == 'Valid'
    
    def test_validate_task_missing_title(self):
        data = {'description': 'No title'}
        is_valid, message = TaskSchema.validate_task(data)
        assert is_valid is False
        assert 'Title is required' in message
    
    def test_validate_task_title_too_short(self):
        data = {'title': 'ab'}
        is_valid, message = TaskSchema.validate_task(data)
        assert is_valid is False
        assert '3 characters' in message
    
    def test_validate_task_invalid_status(self):
        data = {'title': 'Valid', 'status': 'invalid_status'}
        is_valid, message = TaskSchema.validate_task(data)
        assert is_valid is False
        assert 'Invalid status' in message
    
    def test_validate_task_invalid_priority(self):
        data = {'title': 'Valid', 'priority': 'super_high'}
        is_valid, message = TaskSchema.validate_task(data)
        assert is_valid is False
        assert 'Invalid priority' in message

class TestTaskModel:
    """Pruebas unitarias para modelo Task (5 pruebas)"""
    
    def test_task_creation(self):
        task = Task(id=1, title='Test', description='Desc', status='pending', priority='high')
        assert task.id == 1
        assert task.title == 'Test'
    
    def test_task_to_dict(self):
        task = Task(id=1, title='Test', description='Desc', status='pending', priority='high')
        task_dict = task.to_dict()
        assert task_dict['id'] == 1
        assert task_dict['title'] == 'Test'
        assert task_dict['status'] == 'pending'
    
    def test_task_optional_fields(self):
        task = Task(id=1, title='Test', description=None, status='pending', priority='low')
        assert task.description is None
    
    def test_task_default_priority(self):
        task = Task(id=1, title='Test', description='Desc', status='pending', priority='medium')
        assert task.priority == 'medium'
    
    def test_task_status_values(self):
        statuses = ['pending', 'in_progress', 'completed', 'cancelled']
        for status in statuses:
            task = Task(id=1, title='Test', description='Desc', status=status, priority='high')
            assert task.status == status