import React from 'react'

export default function TaskItem({ task, onToggleStatus, onDelete, onUpdateTitle }) {
  const [isEditing, setIsEditing] = React.useState(false)
  const [editTitle, setEditTitle] = React.useState(task.title)

  const handleEditSave = () => {
    onUpdateTitle(task.id, editTitle)
    setIsEditing(false)
  }

  const priorityColor = {
    low: '#388e3c',
    medium: '#f57c00',
    high: '#d32f2f'
  }

  const priorityLabel = {
    low: 'Baja',
    medium: 'Media',
    high: 'Alta'
  }

  const statusLabel = {
    pending: 'Pendiente',
    in_progress: 'En Progreso',
    completed: 'Completada',
    cancelled: 'Cancelada'
  }

  return (
    <div className="task-item">
      <div className="task-content">
        {isEditing ? (
          <input
            type="text"
            value={editTitle}
            onChange={(e) => setEditTitle(e.target.value)}
            onBlur={handleEditSave}
            onKeyPress={(e) => e.key === 'Enter' && handleEditSave()}
            autoFocus
            style={{ width: '100%', padding: '8px', marginBottom: '8px' }}
          />
        ) : (
          <div className="task-title" style={{
            textDecoration: task.status === 'completed' ? 'line-through' : 'none',
            opacity: task.status === 'completed' ? 0.6 : 1
          }}>
            {task.title}
          </div>
        )}
        
        {task.description && (
          <div className="task-description">{task.description}</div>
        )}
        
        <div className="task-meta">
          <span className="badge badge-status" style={{
            background: task.status === 'completed' ? '#e8f5e9' : '#e3f2fd',
            color: task.status === 'completed' ? '#388e3c' : '#1976d2'
          }}>
            {statusLabel[task.status]}
          </span>
          <span className="badge badge-priority" style={{
            color: priorityColor[task.priority]
          }}>
            {priorityLabel[task.priority]}
          </span>
        </div>
      </div>

      <div className="task-actions">
        <button
          className="btn-icon btn-complete"
          onClick={() => onToggleStatus(task)}
          title={task.status === 'completed' ? 'Marcar como pendiente' : 'Marcar como completada'}
        >
          {task.status === 'completed' ? '↩️' : '✓'}
        </button>
        <button
          className="btn-icon btn-edit"
          onClick={() => setIsEditing(true)}
          title="Editar tarea"
        >
          ✎
        </button>
        <button
          className="btn-icon btn-delete"
          onClick={() => onDelete(task.id)}
          title="Eliminar tarea"
        >
          🗑
        </button>
      </div>
    </div>
  )
}