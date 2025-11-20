import pytest
import json
from app.services.task_service import TaskService

class TestTaskIntegration:
    """Suite de pruebas de integración (20 pruebas)"""
    
    def test_create_and_retrieve_task(self, client):
        response = client.post('/api/tasks', 
            json={'title': 'Integration Test', 'description': 'Test', 'priority': 'high'})
        assert response.status_code == 201
        data = json.loads(response.data)
        task_id = data['data']['id']
        
        response = client.get(f'/api/tasks/{task_id}')
        assert response.status_code == 200
        assert json.loads(response.data)['data']['title'] == 'Integration Test'
    
    def test_create_task_endpoint(self, client):
        response = client.post('/api/tasks', 
            json={'title': 'New Task', 'priority': 'medium'})
        assert response.status_code == 201
        assert json.loads(response.data)['success'] is True
    
    def test_create_task_invalid_data(self, client):
        response = client.post('/api/tasks', json={'title': 'ab'})
        assert response.status_code == 400
        assert 'error' in json.loads(response.data)
    
    def test_get_all_tasks(self, client):
        client.post('/api/tasks', json={'title': 'Task 1'})
        client.post('/api/tasks', json={'title': 'Task 2'})
        
        response = client.get('/api/tasks')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['count'] == 2
    
    def test_get_task_not_found(self, client):
        response = client.get('/api/tasks/9999')
        assert response.status_code == 404
    
    def test_update_task(self, client):
        resp = client.post('/api/tasks', json={'title': 'Original'})
        task_id = json.loads(resp.data)['data']['id']
        
        response = client.put(f'/api/tasks/{task_id}', 
            json={'title': 'Updated', 'status': 'completed'})
        assert response.status_code == 200
        assert json.loads(response.data)['data']['status'] == 'completed'
    
    def test_update_task_not_found(self, client):
        response = client.put('/api/tasks/9999', json={'title': 'Updated'})
        assert response.status_code == 404
    
    def test_delete_task(self, client):
        resp = client.post('/api/tasks', json={'title': 'To Delete'})
        task_id = json.loads(resp.data)['data']['id']
        
        response = client.delete(f'/api/tasks/{task_id}')
        assert response.status_code == 200
        
        response = client.get(f'/api/tasks/{task_id}')
        assert response.status_code == 404
    
    def test_filter_tasks_by_status(self, client):
        client.post('/api/tasks', json={'title': 'Task 1'})
        resp = client.post('/api/tasks', json={'title': 'Task 2', 'status': 'pending'})
        task_id = json.loads(resp.data)['data']['id']
        client.put(f'/api/tasks/{task_id}', json={'status': 'completed'})
        
        response = client.get('/api/tasks?status=completed')
        data = json.loads(response.data)
        assert len([t for t in data['data'] if t['status'] == 'completed']) > 0
    
    def test_filter_tasks_by_priority(self, client):
        client.post('/api/tasks', json={'title': 'Task 1', 'priority': 'low'})
        client.post('/api/tasks', json={'title': 'Task 2', 'priority': 'high'})
        
        response = client.get('/api/tasks?priority=high')
        data = json.loads(response.data)
        assert all(t['priority'] == 'high' for t in data['data'])
    
    def test_task_timestamps(self, client):
        resp = client.post('/api/tasks', json={'title': 'Task with timestamps'})
        data = json.loads(resp.data)
        assert 'created_at' in data['data']
        assert 'updated_at' in data['data']
    
    def test_statistics_endpoint(self, client):
        client.post('/api/tasks', json={'title': 'Task 1'})
        client.post('/api/tasks', json={'title': 'Task 2'})
        
        response = client.get('/api/statistics')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'data' in data
        assert data['data']['total'] >= 2
    
    def test_health_check(self, client):
        response = client.get('/api/health')
        assert response.status_code == 200
        assert json.loads(response.data)['status'] == 'healthy'
    
    def test_update_task_priority(self, client):
        resp = client.post('/api/tasks', json={'title': 'Task', 'priority': 'low'})
        task_id = json.loads(resp.data)['data']['id']
        
        response = client.put(f'/api/tasks/{task_id}', json={'priority': 'high'})
        assert json.loads(response.data)['data']['priority'] == 'high'
    
    def test_update_task_description(self, client):
        resp = client.post('/api/tasks', json={'title': 'Task'})
        task_id = json.loads(resp.data)['data']['id']
        
        response = client.put(f'/api/tasks/{task_id}', json={'description': 'New description'})
        assert json.loads(response.data)['data']['description'] == 'New description'
    
    def test_create_multiple_tasks(self, client):
        for i in range(5):
            response = client.post('/api/tasks', json={'title': f'Task {i}'})
            assert response.status_code == 201
        
        response = client.get('/api/tasks')
        data = json.loads(response.data)
        assert data['count'] == 5
    
    def test_tasks_ordered_by_creation(self, client):
        client.post('/api/tasks', json={'title': 'First'})
        client.post('/api/tasks', json={'title': 'Second'})
        
        response = client.get('/api/tasks')
        data = json.loads(response.data)
        assert data['data'][0]['title'] == 'Second'
    
    def test_get_tasks_by_status_endpoint(self, client):
        resp = client.post('/api/tasks', json={'title': 'Task'})
        task_id = json.loads(resp.data)['data']['id']
        client.put(f'/api/tasks/{task_id}', json={'status': 'in_progress'})
        
        response = client.get('/api/tasks/status/in_progress')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data['data']) > 0
    
    def test_response_structure(self, client):
        response = client.get('/api/tasks')
        data = json.loads(response.data)
        assert 'success' in data
        assert 'data' in data
        assert 'count' in data
    
    def test_error_handling(self, client):
        response = client.post('/api/tasks', json={})
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['success'] is False
        assert 'error' in data