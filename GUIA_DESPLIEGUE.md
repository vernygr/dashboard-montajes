# 🚀 Guía de Despliegue en Streamlit Cloud

## Opción 1: Despliegue RÁPIDO (Recomendado)

### Paso 1: Crear cuenta en Streamlit Cloud
1. Ve a https://streamlit.io/cloud
2. Haz clic en "Sign up"
3. Usa tu cuenta de GitHub (o crea una)

### Paso 2: Conectar GitHub
1. Autoriza Streamlit Cloud a acceder a GitHub
2. Selecciona los repositorios que quieres conectar

### Paso 3: Deploy
1. Haz clic en "New app"
2. Selecciona:
   - **Repository**: `dashboard-montajes`
   - **Branch**: `main`
   - **Main file path**: `app.py`
3. Haz clic en "Deploy"

**¡Listo!** Tu dashboard está en vivo en una URL pública como:
```
https://dashboard-montajes-xxxxx.streamlit.app/
```

---

## Opción 2: Primero en GitHub

### Paso 1: Crear repositorio en GitHub

1. Ve a https://github.com/new
2. **Nombre**: `dashboard-montajes`
3. **Descripción**: Dashboard interactivo de montajes
4. Selecciona "Public" (para acceso público)
5. Haz clic en "Create repository"

### Paso 2: Subir código a GitHub

En tu computadora, en la carpeta del proyecto:

```bash
git init
git add .
git commit -m "Dashboard montajes inicial"
git branch -M main
git remote add origin https://github.com/TU-USUARIO/dashboard-montajes.git
git push -u origin main
```

Reemplaza `TU-USUARIO` con tu nombre de usuario de GitHub.

### Paso 3: Conectar con Streamlit Cloud

Sigue los pasos de "Opción 1" (Paso 1-3)

---

## Cómo Actualizar Cada Jueves

### Método 1: Actualización a través de Streamlit Cloud (Más fácil)

1. **Carga tu Excel** en la interfaz del dashboard
2. ¡El dashboard se actualiza automáticamente!
3. No necesitas hacer nada en GitHub

### Método 2: Actualización a través de GitHub (Si quieres guardar histórico)

Si quieres que el Excel se guarde como histórico:

1. Actualiza tu Excel localmente (Ejemplo: `MARZO.xlsx`)
2. Copia el archivo a la carpeta del proyecto
3. Ejecuta en terminal:
   ```bash
   git add datos/MARZO.xlsx
   git commit -m "Actualización datos - Marzo 2026"
   git push
   ```
4. Streamlit Cloud se actualizará automáticamente en 5-10 segundos

---

## Estructura de carpetas recomendada

```
dashboard-montajes/
├── app.py
├── requirements.txt
├── README.md
├── GUIA_DESPLIEGUE.md
├── .streamlit/
│   └── config.toml
├── .gitignore
├── .github/
│   └── workflows/              (Opcional para automatización)
└── datos/                      (Opcional para guardar Excel)
    └── MARZO.xlsx
```

---

## Verificar que todo funciona

1. Abre la URL de Streamlit Cloud
2. Deberías ver el dashboard vacío
3. Carga un archivo Excel
4. Los gráficos y KPIs deberían aparecer

¿Ves el dashboard? **¡Éxito!** ✅

---

## Problemas comunes

### "ModuleNotFoundError: No module named 'streamlit'"
- Verifica que `requirements.txt` esté en la raíz del proyecto
- Streamlit Cloud instalará automáticamente todas las dependencias

### "FileNotFoundError: No such file or directory: 'data/MARZO.xlsx'"
- No incluyas archivos Excel en el repositorio (.gitignore los ignora)
- Los usuarios cargarán el Excel a través de la interfaz

### La app tarda mucho en cargar
- La primera carga en Streamlit Cloud puede tardar 30-60 segundos
- Las cargas subsecuentes son más rápidas

### "Columna X no encontrada"
- El Excel debe tener exactamente la estructura esperada
- Revisa la sección "Estructura esperada del Excel" en README.md

---

## Soporte de Streamlit Cloud

Si tienes problemas con Streamlit Cloud:
1. [Documentación oficial](https://docs.streamlit.io/streamlit-cloud/get-started)
2. [Comunidad de Streamlit](https://discuss.streamlit.io/)
3. [Status page](https://status.streamlit.io/)

---

## Próximos pasos (Opcional)

### 1. Agregar histórico de datos
Crea una carpeta `datos/` y guarda cada semana:
```
datos/
├── 2026-03-01_MARZO.xlsx
├── 2026-03-08_MARZO.xlsx
└── 2026-03-15_MARZO.xlsx
```

### 2. Automatizar actualizaciones
Crea un GitHub Action que automáticamente:
- Descargue el Excel de OneDrive/Google Drive
- Lo suba al repositorio cada jueves
- Active el redeploy automático

### 3. Agregar más métricas
Modifica `app.py` para agregar:
- Análisis de tendencias temporales
- Predicciones de eficiencia
- Alertas automáticas si cae la eficiencia

---

**¿Preguntas? Abre un issue en GitHub o contacta al equipo de desarrollo.**
