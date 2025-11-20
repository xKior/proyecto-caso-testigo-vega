import React from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { setFilters, clearFilters, fetchTasks } from '../store/taskSlice'

export default function FilterPanel() {
  const dispatch = useDispatch()
  const { filters } = useSelector(state => state.tasks)

  const handleFilterChange = (filterType, value) => {
    const newFilters = { ...filters, [filterType]: value }
    dispatch(setFilters(newFilters))
    dispatch(fetchTasks(newFilters))
  }

  const handleClearFilters = () => {
    dispatch(clearFilters())
    dispatch(fetchTasks())
  }

  return (
    <div className="sidebar">
      <h2>Filtros</h2>
      
      <div className="filter-group">
        <label htmlFor="status-filter">Estado</label>
        <select
          id="status-filter"
          value={filters.status}
          onChange={(e) => handleFilterChange('status', e.target.value)}
        >
          <option value="">Todos los estados</option>
          <option value="pending">Pendiente</option>
          <option value="in_progress">En Progreso</option>
          <option value="completed">Completada</option>
          <option value="cancelled">Cancelada</option>
        </select>
      </div>

      <div className="filter-group">
        <label htmlFor="priority-filter">Prioridad</label>
        <select
          id="priority-filter"
          value={filters.priority}
          onChange={(e) => handleFilterChange('priority', e.target.value)}
        >
          <option value="">Todas las prioridades</option>
          <option value="low">Baja</option>
          <option value="medium">Media</option>
          <option value="high">Alta</option>
        </select>
      </div>

      <button className="btn-clear" onClick={handleClearFilters}>
        Limpiar Filtros
      </button>
    </div>
  )
}