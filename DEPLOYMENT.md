# 🚀 Despliegue en Streamlit Cloud + GitHub

## ¡En 10 minutos tu dashboard estará en la nube!

### Estructura confirmada del Excel

Tu archivo Excel tendrá la hoja **"DATA"** (a partir de fila 6) con estas columnas:

```
MES, DÍA, MONTADOR, NOMBRE DEL MONTADOR / LÍDER, PRODUCTO, CLIENTE, INY,
MONTAJE (X), DESMONTAJE (X), ID, HORA DE INICIO, HORA DE FINALIZACIÓN,
TIEMPO TOTAL (HORAS), TIEMPO BRUTO (MIN), TIEMPOS PAROS/MUERTOS,
TIEMPO NETO, TIEMPO PROGRAMADO
```

✅ **Confirmado y configurado en la aplicación**

---

## 📋 Paso 1: Crear Repositorio en GitHub (2 minutos)

### 1.1 Ir a GitHub
1. Abre https://github.com/new
2. **Rellena los datos:**
   - **Repository name**: `dashboard-montajes` (o el nombre que prefieras)
   - **Description**: "Dashboard interactivo de montajes - KPIs semanales"
   - **Public** ← Selecciona esto (importante para Streamlit Cloud)
   - ✅ Marca "Add a README file"
3. Haz clic en **"Create repository"**

### 1.2 Copiar la URL
Después de crear, GitHub te muestra tu repositorio.
Copia la URL: `https://github.com/TU-USUARIO/dashboard-montajes.git`

---

## 📤 Paso 2: Subir código a GitHub (3 minutos)

En tu computadora, abre **PowerShell** o **CMD** y ejecuta:

```bash
cd C:\Users\vgutierrez\Desktop\dashboard-montajes-streamlit
```

### 2.1 Configurar Git (primera vez solo)
```bash
git config --global user.name "Tu Nombre"
git config --global user.email "tu@email.com"
```

### 2.2 Inicializar y subir a GitHub
```bash
git init
git add .
git commit -m "Dashboard montajes - Versión inicial"
git branch -M main
git remote add origin https://github.com/TU-USUARIO/dashboard-montajes.git
git push -u origin main
```

⚠️ **Reemplaza:**
- `TU-USUARIO` con tu usuario de GitHub

✅ **Cuando termine sin errores, tu código está en GitHub**

---

## 🌐 Paso 3: Desplegar en Streamlit Cloud (5 minutos)

### 3.1 Crear cuenta Streamlit Cloud

1. Ve a https://streamlit.io/cloud
2. Haz clic en **"Sign up"**
3. Usa tu cuenta de GitHub (click en "Sign up with GitHub")
4. **Autoriza Streamlit Cloud** a acceder a GitHub
   - Haz clic en "Authorize streamlitapp"
   - Selecciona tu repositorio `dashboard-montajes`
   - Haz clic en "Install"

### 3.2 Crear Nueva App

1. Ya en Streamlit Cloud, haz clic en **"New app"**
2. **Rellena los datos:**
   - **Repository**: Selecciona `dashboard-montajes`
   - **Branch**: `main`
   - **Main file path**: `app.py`
3. Haz clic en **"Deploy"**

### 3.3 Esperar el Deploy
- **Primera vez**: Tarda 2-3 minutos
- Verás una URL como: `https://dashboard-montajes-xxxxx.streamlit.app/`

✅ **¡Tu dashboard está en vivo!**

---

## 🎉 ¿Ya está funcionando?

Si ves la aplicación Streamlit sin errores:

### Prueba con el archivo de ejemplo:
1. En el sidebar izquierdo, busca **"Cargar archivo Excel"**
2. Carga el archivo `MARZO_EJEMPLO.xlsx` (está en tu carpeta local)
3. Deberías ver gráficos y KPIs aparecer

### ¿No hay gráficos?
- Verifica que el archivo tenga la hoja "DATA"
- Los datos deben empezar en la fila 6
- Las columnas deben coincidirexactamente con la estructura esperada

---

## 🔄 Flujo de Actualización Semanal (Cada Jueves)

Ahora que tu dashboard está en la nube:

### Opción A: Carga directo en la web (MÁS FÁCIL)

1. Abre tu dashboard: `https://dashboard-montajes-xxxxx.streamlit.app/`
2. En el sidebar: **"Cargar archivo Excel"**
3. Selecciona tu Excel actualizado (MARZO.xlsx o el mes actual)
4. ¡Listo! Los gráficos se actualizan automáticamente

**Ventaja:** No necesitas tocar nada en GitHub, muy simple

### Opción B: Subir a GitHub para guardar histórico

Si quieres guardar copias de los archivos:

```bash
# En la carpeta del proyecto
cp C:\ruta\a\tu\MARZO.xlsx ./datos/MARZO.xlsx

git add datos/
git commit -m "Actualización datos - Semana de [FECHA]"
git push
```

Streamlit Cloud se actualizará automáticamente en 10 segundos.

---

## 📊 Tu Dashboard en línea

**URL de acceso:**
```
https://dashboard-montajes-xxxxx.streamlit.app/
```

(Reemplaza `xxxxx` con lo que te generó Streamlit)

### Puedes compartir esta URL con tu equipo de gerencia
- No necesitan instalar nada
- Funciona en cualquier navegador
- Se actualiza cada jueves cuando cargas el Excel

---

## 🔐 Seguridad & Privacidad

✅ Tu repositorio es **público** (necesario para Streamlit Cloud gratuito)
✅ **Los archivos Excel NO se guardan en GitHub** (.gitignore los ignora)
✅ Solo se guardan los scripts de la aplicación
✅ Cada usuario carga sus propios archivos Excel al cargar

---

## 🆘 Troubleshooting

### Error: "Repository not found"
- Verifica que copiaste bien la URL de GitHub
- Asegúrate que el repositorio es PUBLIC

### Error: "ModuleNotFoundError"
- Streamlit Cloud instala automáticamente `requirements.txt`
- Verifica que el archivo esté en la raíz

### La app tarda mucho en cargar
- Primera carga: 30-60 segundos (normal)
- Luego: 5-10 segundos
- Si tarda más: verifica en el botón "Manage app" > "Advanced settings"

### "No se encontraron datos válidos"
- El Excel no tiene la hoja "DATA"
- Los datos no empiezan en la fila 6
- Columnasno coinciden exactamente

### Ver logs de errores
En Streamlit Cloud, en tu app, haz clic en los 3 puntitos (⋮) > "View logs"

---

## 📞 ¿Necesitas ayuda?

1. **Problemas con Git/GitHub**: Ver "Paso 2" arriba
2. **Problemas con Streamlit**: [Documentación oficial](https://docs.streamlit.io/)
3. **Problemas con el Excel**: Revisa la estructura en "ESTRUCTURA CONFIRMADA DEL EXCEL"

---

## ✅ Checklist Final

- [ ] Creé repositorio en GitHub
- [ ] Subí el código con Git
- [ ] Conecté Streamlit Cloud con GitHub
- [ ] Hice Deploy en Streamlit Cloud
- [ ] Tengo una URL pública (https://dashboard-montajes-xxxxx.streamlit.app/)
- [ ] Probé cargando el archivo MARZO_EJEMPLO.xlsx
- [ ] Vi gráficos y KPIs aparecer
- [ ] Compartí la URL con gerencia

---

## 🎯 Próximas actualizaciones

Cada jueves:

```
Excel actualizado → Carga en Streamlit Cloud → Dashboard actualizado
```

¡Nada más que hacer!

---

**¿Listo? Ve al Paso 1 y comienza!**
