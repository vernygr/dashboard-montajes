# 🚀 INSTRUCCIONES PASO A PASO: GitHub + Streamlit Cloud

## Tu Dashboard en la Nube en 15 Minutos

### ✅ Lo que ya hemos hecho:
- ✅ Aplicación Streamlit completa
- ✅ Estructura confirmada del Excel
- ✅ Git inicializado localmente
- ✅ Todos los archivos listos

### 👉 Lo que TÚ debes hacer:
1. Crear cuenta GitHub (si no tienes)
2. Crear repositorio
3. Hacer push del código
4. Conectar Streamlit Cloud
5. ¡Listo! Dashboard en vivo

---

## PASO 1: Crear Cuenta GitHub (1 minuto)

### Si ya tienes GitHub, salta a PASO 2

1. Abre https://github.com/signup
2. **Email**: Tu email
3. **Password**: Crea una contraseña fuerte
4. **Username**: Algo como `vgutierrez-manufactura` (sin espacios)
5. Haz clic en **"Create account"**
6. Verifica tu email con el código que recibas

✅ **Tienes cuenta GitHub**

---

## PASO 2: Crear Repositorio en GitHub (2 minutos)

1. Abre https://github.com/new
2. **Rellena exactamente esto:**
   - Repository name: `dashboard-montajes`
   - Description: `Dashboard interactivo para análisis de KPIs de montajes - Actualización semanal`
   - Selecciona: **PUBLIC** (muy importante)
   - ✅ Marca "Add a README file"

3. Haz clic en **"Create repository"**

4. **Importante**: Copia la URL que ves:
   ```
   https://github.com/TU-USERNAME/dashboard-montajes.git
   ```
   Reemplaza `TU-USERNAME` con tu usuario de GitHub

✅ **Tienes repositorio en GitHub**

---

## PASO 3: Subir Código a GitHub (5 minutos)

### 3.1 Abre PowerShell o CMD
En Windows, busca "PowerShell" en el menú de inicio y abre

### 3.2 Ve a la carpeta del proyecto
Copia y pega esto en PowerShell:

```bash
cd C:\Users\vgutierrez\Desktop\dashboard-montajes-streamlit
```

### 3.3 Configura tu usuario Git (solo la primera vez)
```bash
git config --global user.name "Tu Nombre Completo"
git config --global user.email "tu.email@ejemplo.com"
```

Ejemplo:
```bash
git config --global user.name "Victor Gutierrez"
git config --global user.email "victor@manufactura.com"
```

### 3.4 Agrega repositorio remoto
Copia esto **pero reemplaza TU-USERNAME**:

```bash
git remote add origin https://github.com/TU-USERNAME/dashboard-montajes.git
```

Ejemplo completo:
```bash
git remote add origin https://github.com/vgutierrez/dashboard-montajes.git
```

### 3.5 Hace push (sube el código)
```bash
git branch -M main
git push -u origin main
```

**Te pedirá credenciales:**
- Username: Tu usuario de GitHub
- Password: Tu token (o contraseña)

Si no tienes token, GitHub te dará un link. Sigue las instrucciones.

### ✅ Cuando termine sin errores, tu código está en GitHub

Verifica: https://github.com/TU-USERNAME/dashboard-montajes

Deberías ver todos tus archivos ahí.

---

## PASO 4: Conectar Streamlit Cloud (5 minutos)

### 4.1 Abre Streamlit Cloud
https://streamlit.io/cloud

### 4.2 Haz clic en "Sign up"

### 4.3 Selecciona "Continue with GitHub"

### 4.4 Autoriza Streamlit
- GitHub te pide confirmar
- Haz clic en "Authorize streamlitapp"
- Selecciona tu repositorio `dashboard-montajes`
- Haz clic en "Install"

### 4.5 Regresa a Streamlit Cloud y crea nueva app

1. Haz clic en **"New app"**
2. **Rellena:**
   - Repository: `TU-USERNAME/dashboard-montajes`
   - Branch: `main`
   - Main file path: `app.py`

3. Haz clic en **"Deploy"**

### 4.6 Espera el deploy (2-3 minutos)

Verás una pantalla azul que dice "Please wait..."

**Cuando termine**, tendrás una URL como:
```
https://dashboard-montajes-xxxxxxxxxxxxx.streamlit.app/
```

### ✅ ¡TU DASHBOARD ESTÁ EN VIVO!

---

## 🧪 PRUEBA TU DASHBOARD

### 1. Abre la URL en tu navegador

Ejemplo: `https://dashboard-montajes-xxxx.streamlit.app/`

### 2. En el sidebar izquierdo, haz clic en "Cargar archivo Excel"

### 3. Carga el archivo: `MARZO_EJEMPLO.xlsx`
   (Está en: `C:\Users\vgutierrez\Desktop\dashboard-montajes-streamlit\`)

### 4. Deberías ver:
   - 4 tarjetas con KPIs
   - 3 pestañas de gráficos
   - Tabla de montadores

Si ves todo esto, **¡ÉXITO!** ✅

### Si NO ves datos:
- Verifica que el archivo Excel tenga hoja "DATA"
- Los datos deben empezar en fila 6
- Usa el archivo MARZO_EJEMPLO.xlsx (está correcto)

---

## 🔄 AHORA: FLUJO SEMANAL (CADA JUEVES)

### Actualizar el dashboard cada semana:

1. **Actualiza tu Excel** con datos nuevos
2. **Abre tu dashboard**: `https://dashboard-montajes-xxxx.streamlit.app/`
3. **En el sidebar**: "Cargar archivo Excel"
4. **Selecciona** tu Excel nuevo
5. **¡Listo!** Gráficos actualizados automáticamente

**Eso es todo. No necesitas tocar GitHub ni nada más.**

---

## 📊 COMPARTIR CON TU EQUIPO

Tu URL del dashboard es pública y puedes compartirla:

```
https://dashboard-montajes-xxxx.streamlit.app/
```

Tu equipo de gerencia puede:
- Abrir en cualquier navegador
- Ver gráficos interactivos
- Descargar reportes en CSV
- No necesitan instalar nada

---

## 🆘 ERRORES COMUNES

### Error: "Repository not found"
**Solución:**
- Copia bien la URL de GitHub
- El repositorio debe ser PUBLIC (no Private)
- Verifica que el nombre sea `dashboard-montajes`

### Error: "ModuleNotFoundError: No module named 'streamlit'"
**Solución:**
- Streamlit Cloud instala automáticamente las dependencias
- Espera 2-3 minutos en "Deploying..."
- Si persiste, ve a "Manage app" y reinicia

### La app tarda mucho en cargar
**Normal:**
- Primera carga: 30-60 segundos
- Cargas después: 5-10 segundos
- Si está más lenta: recarga la página

### "No se encontraron datos válidos"
**Solución:**
- El Excel debe tener hoja "DATA"
- Datos empiezan en fila 6
- Estructura exacta de columnas
- Usa MARZO_EJEMPLO.xlsx para probar primero

### Ver errores detallados
En Streamlit Cloud:
- En tu app, haz clic en "⋮" (3 puntitos)
- Selecciona "View logs"
- Verás qué está fallando

---

## 📝 CHECKLISY FINAL

Marca estos cuando completes cada paso:

```
[ ] 1. Creé cuenta GitHub
[ ] 2. Creé repositorio "dashboard-montajes" (PUBLIC)
[ ] 3. Ejecuté "git push" sin errores
[ ] 4. Vi mis archivos en GitHub (https://github.com/TU-USERNAME/dashboard-montajes)
[ ] 5. Conecté Streamlit Cloud con GitHub
[ ] 6. Hice Deploy en Streamlit Cloud
[ ] 7. Tengo una URL pública que empieza con "https://dashboard-montajes-"
[ ] 8. Cargué MARZO_EJEMPLO.xlsx
[ ] 9. Vi gráficos y KPIs aparecer
[ ] 10. Compartí URL con gerencia
```

---

## 🎯 RESUMEN DE URLS

**GitHub:**
```
https://github.com/TU-USERNAME/dashboard-montajes
```

**Streamlit Cloud (TU DASHBOARD):**
```
https://dashboard-montajes-xxxx.streamlit.app/
```

**Tu equipo accede a:**
```
https://dashboard-montajes-xxxx.streamlit.app/
```

---

## 💬 NOTAS IMPORTANTES

✅ El dashboard se actualiza cuando cargas un Excel nuevo (no necesitas hacer nada más)
✅ Streamlit Cloud es GRATIS para repositorios públicos
✅ La URL es pública - puedes compartirla sin problema
✅ Los archivos Excel NO se guardan en GitHub (se ignoran automáticamente)
✅ Cada usuario carga sus propios Excel al usar el dashboard

---

## 🚀 RESUMEN: QUÉ HACER AHORA

1. Abre PowerShell
2. Ejecuta:
   ```bash
   cd C:\Users\vgutierrez\Desktop\dashboard-montajes-streamlit
   git push -u origin main
   ```
   (Si da error de "remote", ve a PASO 3.4)

3. Entra en Streamlit Cloud
4. Crea nueva app con tu repositorio
5. ¡Listo!

---

**¿Necesitas ayuda con algún paso? Revisa la sección "ERRORES COMUNES" arriba**

**¿Listo? Comienza por PASO 1 ↑**
