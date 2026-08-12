# 🛰️ API REST de Superresolución para Imágenes Satelitales

![CI/CD Pipeline](https://img.shields.io/github/actions/workflow/status/Jomao03/api_superresolucion/pruebas.yml?branch=main&label=CI%2FCD%20Pipeline&style=flat-square)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat-square&logo=fastapi)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white)
![ONNX Runtime](https://img.shields.io/badge/ONNX_Runtime-005C84?style=flat-square&logo=onnx&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=flat-square&logo=postgresql&logoColor=white)

Servicio web en la nube para la mejora de resolución espacial en imágenes satelitales mediante Deep Learning. La arquitectura está diseñada para ofrecer inferencias ultrarrápidas (~40ms en CPU) utilizando un modelo **SwinIR** optimizado a formato ONNX, con persistencia de datos en PostgreSQL y despliegue automatizado.

---

## 🚀 Demo e Interfaz Interactiva (Swagger)

Puedes probar la API en producción a través de la documentación interactiva:
👉 **[Ver Documentación en Vivo (Swagger UI)](https://api-superresolucion.onrender.com/docs)**

---

## 🛠️ Arquitectura y Tecnologías

* **Backend Framework:** FastAPI (Python 3.10)
* **Inferencia de IA:** ONNX Runtime (Modelo SwinIR optimizado)
* **Base de Datos:** PostgreSQL + SQLAlchemy (Trazabilidad e historial de peticiones)
* **Contenerización:** Docker & Docker Compose
* **Despliegue PaaS:** Render
* **CI/CD Pipeline:** GitHub Actions (Validación de calidad con `pytest` y despliegue continuo automático)

---

## 🔄 Flujo de Trabajo CI/CD

El repositorio cuenta con una canalización automatizada mediante GitHub Actions:
1. **Integración Continua (CI):** Ante cada `push` a la rama principal, se instancia un contenedor de PostgreSQL en el servidor de integración y se ejecutan las pruebas unitarias con `pytest`.
2. **Despliegue Continuo (CD):** Si el control de calidad pasa exitosamente, se dispara un *Deploy Hook* seguro que actualiza automáticamente la instancia en Render.

---

## 💻 Ejecución Local con Docker

Si deseas clonar y ejecutar este proyecto de forma local:

### Requisitos previos
* Git
* Docker Desktop instalados

### Pasos
1. Clonar el repositorio:
   ```bash
   git clone [https://github.com/Jomao03/api_superresolucion.git](https://github.com/Jomao03/api_superresolucion.git)
   cd api_superresolucion