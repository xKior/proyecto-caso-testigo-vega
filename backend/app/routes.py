from flask import Blueprint, request, jsonify
from .services.task_service import TaskService
from .schemas import TaskSchema

bp = Blueprint('api', __name__, url_prefix='/api')

# ENDPOINTS CRUD

@bp.route('/tasks', methods=['GET'])
def get_tasks():
    """GET: Obtiene todas las tareas con filtros opcionales"""
    try:
        status = request.args.get('status')
        priority = request.args.get('priority')
        
        tasks = TaskService.get_all_tasks(status=status, priority=priority)
        return jsonify({
            'success': True,
            'data': [task.to_dict() for task in tasks],
            'count': len(tasks)
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    """GET: Obtiene una tarea específica"""
    try:
        task = TaskService.get_task_by_id(task_id)
        if not task:
            return jsonify({'success': False, 'error': 'Task not found'}), 404
        
        return jsonify({'success': True, 'data': task.to_dict()}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/tasks', methods=['POST'])
def create_task():
    """POST: Crea una nueva tarea"""
    try:
        data = request.get_json()
        
        is_valid, message = TaskSchema.validate_task(data)
        if not is_valid:
            return jsonify({'success': False, 'error': message}), 400
        
        task = TaskService.create_task(
            title=data['title'],
            description=data.get('description'),
            priority=data.get('priority', 'medium')
        )
        
        return jsonify({'success': True, 'data': task.to_dict()}), 201
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """PUT: Actualiza una tarea"""
    try:
        data = request.get_json()
        
        task = TaskService.get_task_by_id(task_id)
        if not task:
            return jsonify({'success': False, 'error': 'Task not found'}), 404
        
        is_valid, message = TaskSchema.validate_task(data)
        if not is_valid:
            return jsonify({'success': False, 'error': message}), 400
        
        updated_task = TaskService.update_task(task_id, **data)
        
        return jsonify({'success': True, 'data': updated_task.to_dict()}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """DELETE: Elimina una tarea"""
    try:
        task = TaskService.get_task_by_id(task_id)
        if not task:
            return jsonify({'success': False, 'error': 'Task not found'}), 404
        
        TaskService.delete_task(task_id)
        
        return jsonify({'success': True, 'message': 'Task deleted'}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/tasks/status/<status>', methods=['GET'])
def get_tasks_by_status(status):
    """GET: Obtiene tareas por estado"""
    try:
        tasks = TaskService.get_all_tasks(status=status)
        return jsonify({'success': True, 'data': [task.to_dict() for task in tasks]}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/statistics', methods=['GET'])
def get_statistics():
    """GET: Obtiene estadísticas"""
    try:
        stats = TaskService.get_statistics()
        return jsonify({'success': True, 'data': stats}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/health', methods=['GET'])
def health():
    """GET: Health check"""
    return jsonify({'status': 'healthy'}), 200