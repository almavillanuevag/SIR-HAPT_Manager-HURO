# SIR-HAPT_Manager-HURO
Aplicacion para gestionar usuarios y métricas del juego en Unity SIR-HAPT desarrollado en Python con KivyMD.

---

## 📋 Requisitos previos

- Windows 10 o superior
- Python 3.10 o superior → [Descargar aquí](https://www.python.org/downloads/)
- Git → [Descargar aquí](https://git-scm.com/downloads)

> ⚠️ Al instalar Python, asegúrate de marcar la opción **"Add Python to PATH"**

---

## ⚙️Configuración del proyecto

### 1. Clonar el repositorio

Abre una terminal y ejecuta:

```bash
git clone https://github.com/almavillanuevag/SIR-HAPT-Manager.git
cd SIR-HAPT-Manager
```

O descárgalo como ZIP desde el botón verde **"Code" → "Download ZIP"** y extráelo.


### 2. Abrir el proyecto en VS Code

```
File → Open Folder → selecciona la carpeta del proyecto
Terminal → New Terminal
```

### 3. En la terminal ejecutar los siguientes comandos
Permitir ejecución de scripts en PowerShell
```bash
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```
Crear el entorno virtual
```bash
python -m venv venv
```
Activar el entorno virtual
```bash
.\venv\Scripts\Activate.ps1
```
> Sabrás que está activo porque verás `(venv)` al inicio de la terminal.

Instalar todas las dependencias
```bash
pip install -r requirements.txt
```

> Esto instala automáticamente todas las librerías necesarias. El proceso puede tardar unos minutos.

---

### 4. Verificar instalación

```bash
pip list
```

Deberías ver en la lista: `Kivy`, `kivymd`, `pyinstaller`, `firebase-admin`, entre otros.

---

## 📦 Generar el ejecutable (.exe)

Una vez configurado el entorno, ejecutar:

```bash
pyinstaller SIR-HAPT_Manager.spec
```

El proceso tarda unos minutos. Al finalizar, el ejecutable estará en:

```
dist/SIR-HAPT_Manager.exe
```

Haz **doble clic** en el `.exe` para abrir la aplicación. 

---

## ⚠️ Si Windows bloquea el archivo 

Es normal que Windows muestre una advertencia la primera vez. 

1. Haz clic en **"Más información"**
2. Haz clic en **"Ejecutar de todas formas"**

> Esto es seguro. La advertencia aparece porque el archivo no tiene firma digital comercial, no porque sea dañino.

Si tu antivirus elimina el archivo:

1. Abre tu antivirus
2. Ve a **"Historial de amenazas"** o **"Cuarentena"**
3. Busca `SIR-HAPT_Manager.exe` → **"Restaurar"** o **"Permitir"**

---

## 🔵 Ejecutar el proyecto desde VSCode

Otra opción es correr el código directamente desde VSCode sin isntalar el .exe. Para esto debe estar el proyecto configurado como explicado en el apartado de **Configuración del proyecto**.

Para ejecturarlo, abrir el programa **app.py** y en la terminal ejecutar:

```bash
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1
pip list
```
Seleccionar el intérprete correcto:
```
Ctrl + Shift + P → "Select Interpreter" → selecciona el venv
```
Después presionar el botón ▶️

> Nota: No cerrar VSCode mientras se ejecuta el programa.

