import { createSlice, createAsyncThunk } from '@reduxjs/toolkit'
import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || '/api'

export const fetchTasks = createAsyncThunk(
  'tasks/fetchTasks',
  async (filters = {}) => {
    const params = new URLSearchParams()
    if (filters.status) params.append('status', filters.status)
    if (filters.priority) params.append('priority', filters.priority)
    
    const response = await axios.get(`${API_URL}/tasks?${params}`)
    return response.data.data
  }
)

export const fetchStatistics = createAsyncThunk(
  'tasks/fetchStatistics',
  async () => {
    const response = await axios.get(`${API_URL}/api/statistics`)
    return response.data.data
  }
)

export const createTask = createAsyncThunk(
  'tasks/createTask',
  async (taskData) => {
    try {
      const response = await axios.post(`${API_URL}/api/tasks`, taskData)
      return response.data.data
    } catch (err) {
      const msg = err?.response?.data?.error || err?.response?.data?.message || err.message || 'Unknown error'
      throw new Error(msg)
    }
  }
)

export const updateTask = createAsyncThunk(
  'tasks/updateTask',
  async ({ id, data }) => {
    const response = await axios.put(`${API_URL}/api/tasks/${id}`, data)
    return response.data.data
  }
)

export const deleteTask = createAsyncThunk(
  'tasks/deleteTask',
  async (id) => {
    await axios.delete(`${API_URL}/api/tasks/${id}`)
    return id
  }
)

const initialState = {
  tasks: [],
  statistics: null,
  loading: false,
  error: null,
  filters: {
    status: '',
    priority: ''
  }
}

const taskSlice = createSlice({
  name: 'tasks',
  initialState,
  reducers: {
    setFilters: (state, action) => {
      state.filters = action.payload
    },
    clearFilters: (state) => {
      state.filters = { status: '', priority: '' }
    },
    clearError: (state) => {
      state.error = null
    }
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchTasks.pending, (state) => {
        state.loading = true
        state.error = null
      })
      .addCase(fetchTasks.fulfilled, (state, action) => {
        state.loading = false
        state.tasks = action.payload
      })
      .addCase(fetchTasks.rejected, (state, action) => {
        state.loading = false
        state.error = action.error.message
      })
      .addCase(fetchStatistics.pending, (state) => {
        state.loading = true
      })
      .addCase(fetchStatistics.fulfilled, (state, action) => {
        state.loading = false
        state.statistics = action.payload
      })
      .addCase(fetchStatistics.rejected, (state) => {
        state.loading = false
      })
      .addCase(createTask.fulfilled, (state, action) => {
        state.tasks.unshift(action.payload)
        state.error = null
      })
      .addCase(createTask.rejected, (state, action) => {
        state.error = action.error.message
      })
      .addCase(updateTask.fulfilled, (state, action) => {
        const index = state.tasks.findIndex(t => t.id === action.payload.id)
        if (index !== -1) {
          state.tasks[index] = action.payload
        }
        state.error = null
      })
      .addCase(updateTask.rejected, (state, action) => {
        state.error = action.error.message
      })
      .addCase(deleteTask.fulfilled, (state, action) => {
        state.tasks = state.tasks.filter(t => t.id !== action.payload)
        state.error = null
      })
      .addCase(deleteTask.rejected, (state, action) => {
        state.error = action.error.message
      })
  }
})

export const { setFilters, clearFilters, clearError } = taskSlice.actions
export default taskSlice.reducer