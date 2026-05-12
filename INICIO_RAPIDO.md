# ⚡ Inicio Rápido - Dashboard Montajes

## En 5 minutos, tu dashboard está funcionando

### Opción A: En tu computadora (Local) - Lo más rápido

```bash
# 1. Abre terminal en la carpeta del proyecto
cd dashboard-montajes-streamlit

# 2. Instala dependencias
pip install -r requirements.txt

# 3. Ejecuta la aplicación
streamlit run app.py

# 4. Se abrirá en http://localhost:8501
```

**¡Listo!** Carga tu Excel y verás el dashboard.

---

### Opción B: En la nube (Streamlit Cloud) - Lo más profesional

1. **Crea cuenta**: https://streamlit.io/cloud
2. **Conecta GitHub**: Autoriza acceso a tus repositorios
3. **Nuevo app**:
   - Repository: `dashboard-montajes`
   - Main file: `app.py`
4. **Deploy**: Haz clic y espera 2 minutos

**¡Listo!** Tu dashboard está en una URL pública que puedes compartir

---

## Primeros pasos después de iniciar

### Carga de datos cada jueves:

1. 📁 **Prepara tu Excel**
   - Asegúrate que tenga una hoja llamada "DATA"
   - Con las columnas: MES, DÍA, MONTADOR, PRODUCTO, CLIENTE, HORA DE INICIO, HORA DE FINALIZACIÓN, TIEMPO NETO, TIEMPO PROGRAMADO

2. 📤 **Sube el archivo**
   - En el sidebar izquierdo: "Cargar archivo Excel"
   - Selecciona tu archivo

3. 📊 **Visualiza los datos**
   - El dashboard se actualiza automáticamente
   - Explora las 3 pestañas: Eficiencia, Productividad, Tendencias

4. 📥 **Descarga reportes** (opcional)
   - Botones para descargar KPIs en CSV

---

## Probar con datos de ejemplo

```bash
# Genera un archivo Excel de ejemplo y lo abre en el dashboard
python test_app.py test
```

---

## Archivos importantes

| Archivo | Propósito |
|---------|-----------|
| `app.py` | **La aplicación principal** - Aquí está toda la lógica |
| `requirements.txt` | Las librerías necesarias (Streamlit, Pandas, Plotly) |
| `README.md` | Documentación completa |
| `GUIA_DESPLIEGUE.md` | Instrucciones detalladas para GitHub y Streamlit Cloud |
| `.streamlit/config.toml` | Configuración de tema y colores |
| `.gitignore` | Qué archivos ignorar al subir a GitHub |

---

## Estructura esperada del Excel

La hoja "DATA" debe tener (a partir de fila 6):

```
MES | DÍA | MONTADOR | NOMBRE DEL MONTADOR | PRODUCTO | CLIENTE | HORA DE INICIO | HORA DE FINALIZACIÓN | TIEMPO NETO | TIEMPO PROGRAMADO
```

**Ejemplo:**
```
MARZO | 2026-03-01 | AAJ | ALONSO | 90503564 | Arthro Care | 04:12:00 | 04:48:00 | 36.0 | 60
```

---

## 🆘 Ayuda rápida

### ❌ Error: "No module named 'streamlit'"
```bash
pip install streamlit
```

### ❌ Error: "No se encontraron datos válidos"
- Verifica que la hoja se llama "DATA"
- Que los datos estén a partir de la fila 6

### ❌ Error: "Columna X no encontrada"
- Tus columnas no coinciden con lo esperado
- Ver "Estructura esperada del Excel" arriba

### ❌ La app tarda mucho en cargar (Streamlit Cloud)
- Primera carga tarda 30-60 segundos
- Las siguientes son más rápidas

---

## 📚 Documentación

- **Inicio Rápido**: Este archivo
- **Guía Completa**: `README.md`
- **Despliegue**: `GUIA_DESPLIEGUE.md`
- **Código**: `app.py` (bien comentado)

---

## Próximo paso

👉 **Abre `GUIA_DESPLIEGUE.md` si quieres publicar en Streamlit Cloud**

O simplemente:
```bash
streamlit run app.py
```

---

**¿Problemas? Revisa README.md o GUIA_DESPLIEGUE.md**
