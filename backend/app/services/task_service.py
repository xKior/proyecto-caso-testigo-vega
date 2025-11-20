from ..database import get_db_context
from ..models import Task
from datetime import datetime
from typing import List, Optional, Tuple

class TaskService:
    """Servicio de tareas - Implementa patrones SOLID"""
    
    @staticmethod
    def create_task(title: str, description: str = None, 
                   priority: str = 'medium') -> Task:
        """Crea una nueva tarea (SRP)"""
        with get_db_context() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO tasks (title, description, status, priority, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (title, description, 'pending', priority, datetime.now(), datetime.now()))
            conn.commit()
            task_id = cursor.lastrowid
            return TaskService.get_task_by_id(task_id)
    
    @staticmethod
    def get_task_by_id(task_id: int) -> Optional[Task]:
        """Obtiene una tarea por ID"""
        with get_db_context() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
            row = cursor.fetchone()
            
            if not row:
                return None
            
            return Task(
                id=row['id'],
                title=row['title'],
                description=row['description'],
                status=row['status'],
                priority=row['priority'],
                created_at=row['created_at'],
                updated_at=row['updated_at']
            )
    
    @staticmethod
    def get_all_tasks(status: Optional[str] = None, 
                     priority: Optional[str] = None) -> List[Task]:
        """Obtiene todas las tareas con filtros opcionales"""
        with get_db_context() as conn:
            cursor = conn.cursor()
            query = 'SELECT * FROM tasks WHERE 1=1'
            params = []
            
            if status:
                query += ' AND status = ?'
                params.append(status)
            
            if priority:
                query += ' AND priority = ?'
                params.append(priority)
            
            query += ' ORDER BY created_at DESC'
            cursor.execute(query, params)
            rows = cursor.fetchall()
            
            return [Task(
                id=row['id'],
                title=row['title'],
                description=row['description'],
                status=row['status'],
                priority=row['priority'],
                created_at=row['created_at'],
                updated_at=row['updated_at']
            ) for row in rows]
    
    @staticmethod
    def update_task(task_id: int, **kwargs) -> Optional[Task]:
        """Actualiza una tarea (Liskov Substitution)"""
        task = TaskService.get_task_by_id(task_id)
        if not task:
            return None
        
        with get_db_context() as conn:
            cursor = conn.cursor()
            updates = []
            params = []
            
            for key, value in kwargs.items():
                if key in ['title', 'description', 'status', 'priority']:
                    updates.append(f'{key} = ?')
                    params.append(value)
            
            if updates:
                updates.append('updated_at = ?')
                params.append(datetime.now())
                params.append(task_id)
                
                query = f"UPDATE tasks SET {', '.join(updates)} WHERE id = ?"
                cursor.execute(query, params)
                conn.commit()
        
        return TaskService.get_task_by_id(task_id)
    
    @staticmethod
    def delete_task(task_id: int) -> bool:
        """Elimina una tarea"""
        with get_db_context() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
            conn.commit()
            return cursor.rowcount > 0
    
    @staticmethod
    def get_statistics() -> dict:
        """Obtiene estadísticas de tareas"""
        with get_db_context() as conn:
            cursor = conn.cursor()
            
            cursor.execute('SELECT COUNT(*) as total FROM tasks')
            total = cursor.fetchone()['total']
            
            cursor.execute("SELECT COUNT(*) as completed FROM tasks WHERE status = 'completed'")
            completed = cursor.fetchone()['completed']
            
            cursor.execute("SELECT COUNT(*) as pending FROM tasks WHERE status = 'pending'")
            pending = cursor.fetchone()['pending']
            
            cursor.execute("SELECT COUNT(*) as high_priority FROM tasks WHERE priority = 'high'")
            high_priority = cursor.fetchone()['high_priority']
            
            return {
                'total': total,
                'completed': completed,
                'pending': pending,
                'high_priority': high_priority,
                'completion_rate': round((completed / total * 100) if total > 0 else 0, 2)
            }