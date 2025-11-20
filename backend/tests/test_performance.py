import pytest
from app.services.task_service import TaskService

class TestPerformance:
    """Suite de pruebas de performance (5 pruebas)"""
    
    def test_create_task_performance(self, benchmark):
        def create():
            TaskService.create_task('Performance Test', 'Description', 'high')
        
        benchmark(create)
    
    def test_get_all_tasks_performance(self, benchmark):
        for i in range(20):
            TaskService.create_task(f'Task {i}', 'Desc', 'medium')
        
        def get_all():
            TaskService.get_all_tasks()
        
        benchmark(get_all)
    
    def test_update_task_performance(self, benchmark):
        task = TaskService.create_task('Performance Task', 'Desc', 'high')
        
        def update():
            TaskService.update_task(task.id, title='Updated', status='completed')
        
        benchmark(update)
    
    def test_filter_tasks_performance(self, benchmark):
        for i in range(30):
            priority = 'high' if i % 3 == 0 else 'low'
            TaskService.create_task(f'Task {i}', 'Desc', priority)
        
        def filter_tasks():
            TaskService.get_all_tasks(priority='high')
        
        benchmark(filter_tasks)
    
    def test_statistics_performance(self, benchmark):
        for i in range(50):
            TaskService.create_task(f'Task {i}', 'Desc', 'medium')
        
        def get_stats():
            TaskService.get_statistics()
        
        benchmark(get_stats)