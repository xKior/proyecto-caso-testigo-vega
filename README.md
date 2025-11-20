# Sistema de Gestión de Tareas Empresarial con CI/CD

Proyecto completo que integra backend en Flask, frontend en React, suite de testing completa y despliegue en Vercel con CI/CD.

## 🎯 Características

### Backend (Flask)
- ✅ 5 endpoints CRUD completos
- ✅ Principios SOLID implementados
- ✅ Validaciones robustas
- ✅ Manejo de errores centralizado
- ✅ Servicio de tareas con métodos reutilizables

### Frontend (React + Redux)
- ✅ 5 componentes funcionales
- ✅ Gestión de estado con Redux Toolkit
- ✅ Responsive design (mobile-first)
- ✅ Integración total con API backend
- ✅ Interfaz moderna y atractiva

### Testing
- ✅ 10 pruebas unitarias (pytest)
- ✅ 20 pruebas de integración
- ✅ 5 pruebas de performance
- ✅ Cobertura de código 80%+
- ✅ CI/CD automatizado con GitHub Actions

## 📋 Requisitos Previos

- Python 3.11+
- Node.js 18+
- Git
- Cuenta en GitHub y Vercel

## 🚀 Instalación Local

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
python app/main.py
```

El backend estará disponible en `http://localhost:5000`

### Frontend
```bash
cd frontend
npm install
npm run dev
```

El frontend estará disponible en `http://localhost:3000`

## 🧪 Ejecutar Tests

### Todas las pruebas
```bash
cd backend
pytest -v
```

### Pruebas específicas
```bash
# Solo unitarias
pytest tests/test_unit.py -v

# Solo integración
pytest tests/test_integration.py -v

# Solo performance
pytest tests/test_performance.py -v

# Con cobertura
pytest --cov=app --cov-report=html
```

## 📊 Endpoints API

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/tasks` | Obtiene todas las tareas |
| GET | `/api/tasks/<id>` | Obtiene una tarea específica |
| POST | `/api/tasks` | Crea una nueva tarea |
| PUT | `/api/tasks/<id>` | Actualiza una tarea |
| DELETE | `/api/tasks/<id>` | Elimina una tarea |
| GET | `/api/tasks/status/<status>` | Filtra por estado |
| GET | `/api/statistics` | Obtiene estadísticas |
| GET | `/api/health` | Health check |

## 🔧 Estructura de Proyectos