import React, { useState } from 'react'
import { useDispatch } from 'react-redux'
import { createTask } from '../store/taskSlice'

export default function TaskForm() {
  const dispatch = useDispatch()
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    priority: 'medium'
  })
  const [error, setError] = useState('')

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: value
    }))
    setError('')
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    
    if (!formData.title.trim()) {
      setError('El título es requerido')
      return
    }

    // Log payload to help debug 400 responses from the API
    console.log('Creating task payload:', formData)

    try {
      await dispatch(createTask(formData)).unwrap()
      setFormData({
        title: '',
        description: '',
        priority: 'medium'
      })
    } catch (err) {
      setError(err.message || 'Error al crear la tarea')
    }
  }

  return (
    <div className="task-form">
      <h2>Nueva Tarea</h2>
      {error && <div className="error">{error}</div>}
      
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="title">Título *</label>
          <input
            id="title"
            type="text"
            name="title"
            value={formData.title}
            onChange={handleChange}
            placeholder="Describe tu tarea..."
            maxLength="200"
          />
        </div>

        <div className="form-group">
          <label htmlFor="description">Descripción</label>
          <textarea
            id="description"
            name="description"
            value={formData.description}
            onChange={handleChange}
            placeholder="Detalles adicionales (opcional)"
            maxLength="1000"
          />
        </div>

        <div className="form-group">
          <label htmlFor="priority">Prioridad</label>
          <select
            id="priority"
            name="priority"
            value={formData.priority}
            onChange={handleChange}
          >
            <option value="low">Baja</option>
            <option value="medium">Media</option>
            <option value="high">Alta</option>
          </select>
        </div>

        <div className="form-actions">
          <button type="submit" className="btn btn-primary">
            Crear Tarea
          </button>
        </div>
      </form>
    </div>
  )
}