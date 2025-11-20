import React, { useEffect } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { fetchStatistics } from '../store/taskSlice'

export default function Statistics() {
  const dispatch = useDispatch()
  const { statistics } = useSelector(state => state.tasks)

  useEffect(() => {
    dispatch(fetchStatistics())
  }, [dispatch])

  if (!statistics) return null

  return (
    <div className="stats">
      <div className="stat-card">
        <h3>{statistics.total}</h3>
        <p>Tareas Totales</p>
      </div>
      <div className="stat-card">
        <h3>{statistics.completed}</h3>
        <p>Completadas</p>
      </div>
      <div className="stat-card">
        <h3>{statistics.pending}</h3>
        <p>Pendientes</p>
      </div>
      <div className="stat-card">
        <h3>{statistics.high_priority}</h3>
        <p>Alta Prioridad</p>
      </div>
      <div className="stat-card">
        <h3>{statistics.completion_rate}%</h3>
        <p>Tasa Completación</p>
      </div>
    </div>
  )
}