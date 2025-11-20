import React from 'react'
import { useSelector, useDispatch } from 'react-redux'
import { updateTask, deleteTask } from '../store/taskSlice'
import TaskItem from './TaskItem'

export default function TaskList() {
  const { tasks, loading, error } = useSelector(state => state.tasks)
  const dispatch = useDispatch()

  if (loading) return <div className="loading">Cargando tareas...</div>

  const handleToggleStatus = (task) => {
    const newStatus = task.status === 'completed' ? 'pending' : 'completed'
    dispatch(updateTask({ id: task.id, data: { status: newStatus } }))
  }

  const handleDelete = (id) => {
    if (window.confirm('¿Estás seguro de eliminar esta tarea?')) {
      dispatch(deleteTask(id))
    }
  }

  const handleUpdateTitle = (id, newTitle) => {
    if (newTitle.trim()) {
      dispatch(updateTask({ id, data: { title: newTitle } }))
    }
  }

  if (tasks.length === 0) {
    return (
      <div className="task-list">
        <div className="empty-state">
          <h3>📭 No hay tareas</h3>
          <p>Crea una nueva tarea para comenzar</p>
        </div>
      </div>
    )
  }

  return (
    <div className="task-list">
      {error && <div className="error">{error}</div>}
      {tasks.map(task => (
        <TaskItem
          key={task.id}
          task={task}
          onToggleStatus={handleToggleStatus}
          onDelete={handleDelete}
          onUpdateTitle={handleUpdateTitle}
        />
      ))}
    </div>
  )
}