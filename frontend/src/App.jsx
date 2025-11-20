import React, { useEffect } from 'react'
import { useDispatch } from 'react-redux'
import { fetchTasks } from './store/taskSlice'
import TaskForm from './components/TaskForm'
import TaskList from './components/TaskList'
import FilterPanel from './components/FilterPanel'
import Statistics from './components/Statistics'

export default function App() {
  const dispatch = useDispatch()

  useEffect(() => {
    dispatch(fetchTasks())
  }, [dispatch])

  return (
    <div>
      <div className="container">
        <header>
          <h1>📋 Gestor de Tareas Empresarial</h1>
          <p>Sistema completo de gestión de tareas con CI/CD integrado</p>
          <Statistics />
        </header>

        <div className="main-content">
          <div>
            <TaskForm />
          </div>
          
          <div>
            <FilterPanel />
          </div>
        </div>

        <TaskList />
      </div>
    </div>
  )
}