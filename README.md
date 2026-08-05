# Frontend en Django - Sistema de Nómina (Ecuador)

Este es el frontend desarrollado en **Django (Server-Side Rendering con Tailwind CSS y Alpine.js)** que consume la API REST del backend en **FastAPI** para la gestión de empleados, novedades de nómina y procesamiento de roles de pago bajo la **normativa laboral ecuatoriana**.

---

## 1. Arquitectura y Tecnologías Replicadas
Siguiendo la arquitectura del proyecto de referencia (`web1proyecto`):
* **Framework**: Django 6.0 (Arquitectura multi-app con SSR).
* **UI/UX**: Dashboard Windmill adaptado con **Tailwind CSS**, **Alpine.js** e íconos SVG vectoriales.
* **Cliente API**: `APIClient` centralizado (`frontend_nomina/api_client.py`) que consume el backend FastAPI (`http://127.0.0.1:8000`) enviando tokens Bearer guardados en sesión (`request.session['access_token']`).
* **Seguridad & Autenticación**: Integración completa con Supabase Auth del backend.

---

## 2. Aplicaciones y Módulos
1. **`dashboard`**: Panel general con indicadores clave (Total Empleados, Novedades, Nóminas Generadas, Estado API y Normativa SBU $460).
2. **`authentication`**: Login y Signup integrado con Supabase Auth vía la API backend (`/auth/login`, `/auth/signup`).
3. **`empleados`**: CRUD completo de Empleados (RF-1) con validación de Salario Básico Unificado ($460.00) y selección de mensualización de beneficios de ley (Décimos y Fondos de Reserva).
4. **`novedades`**: Registro y consulta de novedades mensuales (RF-2) por empleado y período.
5. **`nominas`**: 
   * **Cálculo Masivo de Nómina** (`POST /nominas/calcular/{periodo}`) aplicando fórmulas legales ecuatorianas.
   * **Histórico y Registro de Estado de Pago** (`GET /nominas/historico/` y `POST /nominas/{id}/registrar-pago`) con simulación de alertas.
   * **Rol Individual de Pagos** (`GET /nominas/reporte/{cedula}/{periodo}`) con plantilla de impresión lista para PDF.
   * **Conciliación Bancaria de Anticipos** (`POST /nominas/conciliar-anticipos/{periodo}`) con reporte visual de transacciones conciliadas e inconsistencias.
   * **Descarga de Archivo SAT** (`GET /nominas/archivo-sat/{periodo}`) para pagos bancarios masivos.

---

## 3. Instrucciones de Ejecución

### 1. Iniciar el Backend (FastAPI)
Asegúrese de que la API de FastAPI esté ejecutándose en la consola:
```bash
uvicorn main:app --reload --port 8000
```

### 2. Iniciar el Frontend (Django)
Navegue a la carpeta del frontend Django:
```bash
cd C:\Users\rsama\OneDrive\Documentos\visual\django\web\web_nomina_frontend
```

Ejecute las migraciones de sesión/base de datos local e inicie el servidor de desarrollo en un puerto diferente (ej: `8001`):
```bash
python manage.py migrate
python manage.py runserver 8001
```

Acceda desde su navegador web:
* **Frontend Django**: http://127.0.0.1:8001
* **Backend FastAPI Swagger**: http://127.0.0.1:8000/docs
