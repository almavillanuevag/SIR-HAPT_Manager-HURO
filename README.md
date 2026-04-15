# SIR-HAPT_Manager-HURO
Aplicación para gestionar usuarios y métricas del juego en Unity SIR-HAPT, desarrollada en Python con KivyMD.
 
La aplicación está compuesta principalmente por dos archivos:
 
- **`app.py`**: Contiene toda la lógica del programa: autenticación, conexión a Firebase, manejo de datos y navegación entre pantallas.
- **`app.kv`**: Es el archivo visual. Define cómo se ve la aplicación: botones, colores, formularios y la interfaz en general.
 
El archivo **`app.py`** es el encargado de gestionar la comunicación entre ellos, por lo que es el único que se debe ejecutar. 

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
File → Open Folder → selecciona la carpeta del proyecto
Terminal → New Terminal

### 3. En la terminal ejecutar los siguientes comandos
1. Permitir ejecución de scripts en PowerShell
```bash
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

2. Crear el entorno virtual
```bash
python -m venv venv
```

3. Activar el entorno virtual
```bash
.\venv\Scripts\Activate.ps1
```
> Sabrás que está activo porque verás `(venv)` al inicio de la terminal.

4. Instalar todas las dependencias
```bash
pip install -r requirements.txt
```
> Esto instala automáticamente todas las librerías necesarias. El proceso puede tardar unos minutos.

5. Verificar instalación
```bash
pip list
```
Se debería ver en la lista: `Kivy`, `kivymd`, `pyinstaller`, `firebase-admin`, entre otros.

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

1. Hacer clic en **"Más información"**
2. Hacer clic en **"Ejecutar de todas formas"**

> Esto es seguro. La advertencia aparece porque el archivo no tiene firma digital comercial, no porque sea dañino.

Si tu antivirus elimina el archivo:

1. Abre tu antivirus
2. Ve a **"Historial de amenazas"** o **"Cuarentena"**
3. Busca `SIR-HAPT_Manager.exe` → **"Restaurar"** o **"Permitir"**

---

## 🔵 Ejecutar el proyecto desde VSCode

Otra opción es correr el código directamente desde VSCode sin isntalar el .exe. Para esto debe estar el proyecto configurado como explicado en el apartado de **Configuración del proyecto**.

1. Abrir el programa **``app.py``** y en la terminal ejecutar:

```bash
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1
pip list
```
2. Seleccionar el intérprete correcto:
```
Ctrl + Shift + P → "Select Interpreter" → selecciona el venv
```
3. Después presionar el botón ▶️

> Nota: No cerrar VSCode mientras se ejecuta el programa.

