# 📊 Dashboard Montajes - Streamlit

Dashboard interactivo para análisis de KPIs de producción y montajes. Carga tu archivo Excel semanalmente y visualiza en tiempo real:
- **Eficiencia Operativa** (Tiempo neto vs programado)
- **Productividad** (Operaciones completadas)
- **Tendencias** (Clientes y Productos que más se repiten)

## ✨ Características

- 📁 **Carga de archivos Excel** - Sube tu archivo cada jueves
- 📊 **Gráficos interactivos** - Visualizaciones en tiempo real con Plotly
- 📈 **3 KPIs principales** - Eficiencia, Productividad y Tendencias
- 👥 **Análisis detallado** - Por montador, cliente y producto
- 📥 **Descarga de datos** - Exporta KPIs y datos procesados a CSV
- 🌐 **Despliegue en la nube** - Ejecuta en Streamlit Cloud gratuitamente

## 🚀 Instalación Local

### Requisitos previos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Pasos de instalación

1. **Clona el repositorio:**
```bash
git clone https://github.com/tu-usuario/dashboard-montajes.git
cd dashboard-montajes-streamlit
```

2. **Crea un entorno virtual:**
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. **Instala las dependencias:**
```bash
pip install -r requirements.txt
```

4. **Ejecuta la aplicación:**
```bash
streamlit run app.py
```

5. **Abre tu navegador:**
   - La app se abrirá automáticamente en `http://localhost:8501`

## 📁 Estructura de archivos

```
dashboard-montajes-streamlit/
├── app.py                      # Aplicación principal
├── requirements.txt            # Dependencias de Python
├── README.md                   # Este archivo
├── .gitignore                  # Archivos a ignorar en Git
└── .streamlit/
    └── config.toml            # Configuración de Streamlit
```

## 📝 Estructura esperada del Excel

Tu archivo Excel debe tener una hoja llamada **"DATA"** con estas columnas (a partir de la fila 6):

| Columna | Descripción | Ejemplo |
|---------|-------------|---------|
| MES | Mes del registro | MARZO |
| DÍA | Fecha | 2026-03-01 |
| MONTADOR | Código del montador | AAJ, SAE, DBJ |
| NOMBRE DEL MONTADOR | Nombre completo | ALONSO, JOHNNY |
| PRODUCTO | Código del producto | 90503564, 55855-001-R1 |
| CLIENTE | Nombre del cliente | Arthro Care, Moog Medical |
| INY | Número de inyección | 49, 36 |
| MONTAJE (X) | Indicador de montaje | X, (vacío) |
| DESMONTAJE (X) | Indicador de desmontaje | X, (vacío) |
| ID | ID único | 13539, 13540 |
| HORA DE INICIO | Hora inicio | 04:12:00 |
| HORA DE FINALIZACIÓN | Hora final | 04:48:00 |
| TIEMPO TOTAL (HORAS) | Duración total | 00:36:00 |
| TIEMPO BRUTO (MIN) | Minutos sin descontar paros | 36.0 |
| TIEMPOS PAROS/MUERTOS | Tiempo de paros | (opcional) |
| TIEMPO NETO | Tiempo productivo | 36.0 |
| TIEMPO PROGRAMADO | Tiempo estándar | 60 |

## 🌐 Despliegue en Streamlit Cloud (Recomendado)

### Paso 1: Sube tu código a GitHub

1. Crea un repositorio en [GitHub](https://github.com/new)
2. Sube tu código:
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/tu-usuario/dashboard-montajes.git
git push -u origin main
```

### Paso 2: Conecta con Streamlit Cloud

1. Ve a [Streamlit Cloud](https://streamlit.io/cloud)
2. Haz clic en "New app"
3. Selecciona tu repositorio GitHub y la rama `main`
4. Selecciona `app.py` como el archivo principal
5. Haz clic en "Deploy"

**¡Listo!** Tu dashboard estará disponible en una URL pública.

## 📊 Cómo usar

### Cada jueves (o semanalmente):

1. **Actualiza tu Excel** con los datos nuevos de la semana
   - Asegúrate que haya una hoja llamada "DATA"
   - Mantén la estructura de columnas igual

2. **Abre el dashboard**
   - Si está en Streamlit Cloud: ve a tu URL pública
   - Si es local: ejecuta `streamlit run app.py`

3. **Carga el archivo**
   - Haz clic en "Cargar archivo Excel" en la barra lateral
   - Selecciona tu archivo Excel actualizado

4. **Visualiza los datos**
   - El dashboard se actualizará automáticamente
   - Explora las 3 pestañas: Eficiencia, Productividad y Tendencias

5. **Descarga reportes**
   - Exporta los KPIs a CSV para tus reportes
   - Descarga los datos procesados completos

## 📈 Interpretación de KPIs

### Eficiencia Operativa
- **Verde (≥70%)**: Excelente desempeño
- **Ámbar (50-69%)**: Aceptable, pero puede mejorar
- **Rojo (<50%)**: Necesita mejora inmediata

### Operaciones
- Número total de montajes/desmontajes completados en el período

### Horas Productivas
- Tiempo total en el que se realizó trabajo productivo (sin paros)

## 🔧 Troubleshooting

### Error: "No se encontraron datos válidos"
- Verifica que la hoja se llama exactamente "DATA"
- Asegúrate que los datos comienzan en la fila 6

### Error: "Columna no encontrada"
- Verifica que todas las columnas requeridas estén presentes
- Los nombres de columnas deben ser idénticos

### La app es lenta al cargar
- Streamlit Cloud puede ser lento la primera carga
- Para desarrollo local, usa `streamlit run app.py`

## 📧 Soporte y contacto

Si encuentras problemas o tienes sugerencias:
1. Abre un issue en GitHub
2. Contacta al equipo de desarrollo

## 📄 Licencia

Este proyecto está bajo licencia MIT. Ver LICENSE para más detalles.

---

**Creado con ❤️ para optimizar la producción y análisis de datos**
