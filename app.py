from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.clock import Clock
from kivymd.uix.screen import MDScreen
from datetime import datetime
from kivymd.uix.list import TwoLineListItem
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.core.window import Window
import os
import sys

# Firebase Auth y Firestore
import firebase_admin
from firebase_admin import credentials, firestore

def resource_path(relative_path):
    # Obtiene la ruta absoluta tanto en desarrollo como en ejecutable
    try:
        base_path = sys._MEIPASS  # Cuando corre como .exe
    except Exception:
        base_path = os.path.abspath(".")  # Cuando corre como script

    return os.path.join(base_path, relative_path)


# Ruta dinámica al JSON
cred_path = resource_path("sir-hapt-huro-firebase-adminsdk.json")

# Inicializar credenciales
cred = credentials.Certificate(cred_path)
firebase_admin.initialize_app(cred)
db = firestore.client()


import os
import sys
import csv
import random
from datetime import datetime

import firebase_admin
from firebase_admin import credentials, firestore

from kivy.clock import Clock
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.metrics import dp

from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.menu import MDDropdownMenu

# --- Firebase init -------------------------------------------------------------
def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def init_firebase():
    if not firebase_admin._apps:
        try:
            cred = credentials.Certificate(resource_path("serviceAccountKey.json"))
            firebase_admin.initialize_app(cred)
        except Exception as e:
            print(f"[Firebase] Error: {e}")

init_firebase()
db = firestore.client()

# --- Variables internas ----------------------------------------------------------------
logo_path = resource_path("logo.png")

GRUPOS = [
    "NoFeedback",
    "VisualFeedback",
    "HapticFeedback",
    "MultimodalFeedback",
    "HapticWithoutTube",
]

GRUPO_LABELS = {
    "NoFeedback":         "Sin retroalimentación",
    "VisualFeedback":     "Con retroalimentación visual",
    "HapticFeedback":     "Con retroalimentación háptica",
    "MultimodalFeedback": "Con retroalimentación visual y háptica",
    "HapticWithoutTube":  "Únicamente retroalimentación háptica sin ver el tubo",
}

GRUPO_COLORS = {
    "NoFeedback":         (0.55, 0.55, 0.55, 1),
    "VisualFeedback":     (0.85, 0.18, 0.18, 1),
    "HapticFeedback":     (0.13, 0.47, 0.71, 1),
    "MultimodalFeedback": (0.47, 0.18, 0.68, 1),
    "HapticWithoutTube":  (0.95, 0.60, 0.07, 1),
}

TRAYECTORIAS         = ["T1", "T2", "T3", "T4", "T5"]


# --- Funciones -------------------------------------------------------------------
def session_status(current_rep, total):
    if current_rep <= 0:      return "pending"
    if current_rep >= total:  return "completed"
    return "in_progress"

def status_color(status):
    return {
        "completed":   (0.18, 0.65, 0.33, 1),
        "in_progress": (0.95, 0.65, 0.07, 1),
        "pending":     (0.85, 0.18, 0.18, 1),
    }.get(status, (0.5, 0.5, 0.5, 1))

def status_label(status):
    return {
        "completed":   "Completado",
        "in_progress": "En curso",
        "pending":     "Sin iniciar",
    }.get(status, "—")

# ==========================================================================================
# Funciones para guardar CSV 
import pathlib

def get_export_path(*subcarpetas):
    """
    Construye y crea la ruta:
    Documents/SIR-HAPT-Exports/<subcarpeta1>/<subcarpeta2>/...
    Funciona en Windows en español e inglés, y sobrevive a yInstaller.
    """
    documents = pathlib.Path.home() 
    
    ruta = documents / "SIR-HAPT-Exports"
    for sub in subcarpetas:
        # Sanear el nombre para que sea válido como nombre de carpeta
        sub_seguro = str(sub).replace("/", "-").replace("\\", "-").replace(":", "-")
        ruta = ruta / sub_seguro

    ruta.mkdir(parents=True, exist_ok=True)
    return ruta


def guardar_csv(filas, nombre_archivo, *subcarpetas):
    """
    Guarda el CSV en Documents/SIR-HAPT-Exports/<subcarpetas>/nombre_archivo
    Si el archivo ya existe, agrega un sufijo numérico para no sobreescribir.
    """
    if not filas:
        print("[CSV] Sin datos para exportar")
        return None

    carpeta = get_export_path(*subcarpetas)
    
    # Evitar sobreescritura: si existe, agregar _1, _2, etc.
    base    = pathlib.Path(nombre_archivo).stem
    ext     = pathlib.Path(nombre_archivo).suffix or ".csv"
    archivo = carpeta / nombre_archivo

    contador = 1
    while archivo.exists():
        archivo = carpeta / f"{base}_{contador}{ext}"
        contador += 1

    try:
        with open(archivo, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=list(filas[0].keys()))
            writer.writeheader()
            writer.writerows(filas)
        print(f"[CSV] Guardado: {archivo}")
        return str(archivo)
    except Exception as e:
        print(f"[CSV] Error: {e}")
        return None


# ==========================================================================================
# DASHBOARD  — sólo envuelve el Navigation Rail + inner ScreenManager
# ==========================================================================================
class Dashboard(MDScreen):
    def ir_todos(self):
        app = MDApp.get_running_app()
        app.filtro_grupo = None
        sm = self.ids.screen_manager2
        scr_user = sm.get_screen("users")
        scr_user.cargar_usuarios()
        sm.transition.direction = "right"
        sm.current = "users" 

# ==========================================================================================
# HOME
# ==========================================================================================
class Home(MDScreen):

    def on_enter(self):
        try:
            self.ids.img_logo.source = resource_path("logo.png")
        except Exception:
            pass
        Clock.schedule_once(self.cargar_resumen, 0.2)

    def cargar_resumen(self, dt=None):
        try:
            docs = db.collection("Users").stream()
            conteos = {g: 0 for g in GRUPOS}
            for doc in docs:
                g = doc.to_dict().get("experimentalGroup", "")
                if g in conteos:
                    conteos[g] += 1
            self._actualizar_tabla(conteos)
        except Exception as e:
            print(f"[Home] Error: {e}")

    def _actualizar_tabla(self, conteos):
        mapa = {
            "NoFeedback":         "cnt_nofb",
            "VisualFeedback":     "cnt_vis",
            "HapticFeedback":     "cnt_hap",
            "MultimodalFeedback": "cnt_mm",
            "HapticWithoutTube":  "cnt_hwt",
        }
        for grupo, wid in mapa.items():
            try:
                self.ids[wid].text = str(conteos.get(grupo, 0))
            except Exception:
                pass

    def ir_grupo(self, grupo):
        app = MDApp.get_running_app()
        app.filtro_grupo = grupo
        self.manager.current = "users"
        self.manager.transition.direction = "left"

    def ir_todos(self):
        app = MDApp.get_running_app()
        app.filtro_grupo = None
        self.manager.current = "users"
        self.manager.transition.direction = "left"

    def abrir_nuevo_usuario(self):
        self.manager.current = "newuser"
        self.manager.transition.direction = "left"

# ==========================================================================================
# USERS  — listado de participantes
# ==========================================================================================
class Users(MDScreen):
    _todos = []

    def on_enter(self):
        Clock.schedule_once(self.cargar_usuarios, 0.15)

    def cargar_usuarios(self, dt=None):
        app = MDApp.get_running_app()
        filtro = getattr(app, "filtro_grupo", None)

        # Título y visibilidad del botón de descarga
        try:
            if filtro:
                self.ids.titulo_lista.text = GRUPO_LABELS.get(filtro, filtro)
                self.ids.btn_descargar_grupo.disabled = False
                self.ids.btn_descargar_grupo.opacity  = 1
            else:
                self.ids.titulo_lista.text = "Listado de todos los participantes"
                self.ids.btn_descargar_grupo.disabled = True
                self.ids.btn_descargar_grupo.opacity  = 0
        except Exception:
            pass

        try:
            ref = db.collection("Users")
            if filtro:
                ref = ref.where("experimentalGroup", "==", filtro)
            docs = ref.stream()

            self._todos = []
            for doc in docs:
                d = doc.to_dict()
                d["_id"] = doc.id
                self._todos.append(d)

            self._renderizar(self._todos)
        except Exception as e:
            print(f"[Users] Error: {e}")

    def _renderizar(self, lista):
        from kivy.graphics import Color, Ellipse
        from kivy.uix.widget import Widget as KW
        from kivymd.uix.button import MDIconButton

        contenedor = self.ids.users_list
        contenedor.clear_widgets()

        if not lista:
            contenedor.add_widget(MDLabel(
                text="No hay participantes registrados",
                halign="center", theme_text_color="Hint",
                size_hint_y=None, height=dp(50)
            ))
            return

        for d in lista:
            uid    = d.get("IDux", d["_id"])
            grupo  = d.get("experimentalGroup", "")
            gc     = GRUPO_COLORS.get(grupo, (0.5, 0.5, 0.5, 1))
            glabel = GRUPO_LABELS.get(grupo, grupo)
            
            docConf = db.collection("UnityConfig").document(d["_id"]).get()
            if docConf.exists:
                conf = docConf.to_dict()
                current_rep = conf.get("CurrentRepetition", 1)-1
            else:
                current_rep = 0
            
            total = d.get("totalReps", 0)
            status = session_status(current_rep, total)
            sc     = status_color(status)

            comp = max(0, current_rep)
            row = MDBoxLayout(
                orientation="horizontal",
                size_hint_y=None, height=dp(48),
                padding=[dp(12), 0], spacing=dp(8),
                md_bg_color=(1, 1, 1, 1),
            )


            lbl_id = MDLabel(text=uid, font_style="Subtitle1", bold=True,
                              size_hint_x=0.22, halign="left", valign="center")
            lbl_id.bind(size=lbl_id.setter("text_size"))

            lbl_g = MDLabel(text=glabel, font_style="Body2",
                             size_hint_x=0.38, halign="left", valign="center",
                             theme_text_color="Custom", text_color=gc)
            lbl_g.bind(size=lbl_g.setter("text_size"))

            lbl_p = MDLabel(text=f"{comp}/{total}", font_style="Body2",
                             size_hint_x=0.14, halign="center", valign="center")
            lbl_p.bind(size=lbl_p.setter("text_size"))


            lbl_s = MDLabel(text=status_label(status), font_style="Caption",
                             size_hint_x=0.12, halign="center", valign="center",
                             theme_text_color="Custom", text_color=sc)
            lbl_s.bind(size=lbl_s.setter("text_size"))

            btn = MDIconButton(icon="chevron-right", size_hint_x=None,
                               width=dp(40), theme_icon_color="Custom",
                               icon_color=(0.4, 0.4, 0.4, 1))
            _pid = d["_id"]
            btn.bind(on_release=lambda x, pid=_pid: self.abrir_perfil(pid))

            row.add_widget(lbl_id)
            row.add_widget(lbl_g)
            row.add_widget(lbl_p)
            row.add_widget(lbl_s)
            row.add_widget(btn)

            sep = MDBoxLayout(size_hint_y=None, height=dp(1),
                               md_bg_color=(0.9, 0.9, 0.9, 1))
            contenedor.add_widget(row)
            contenedor.add_widget(sep)

    # Llamado por on_text del MDTextField de búsqueda en el KV
    def buscar(self, texto):
        t = texto.lower().strip()
        if not t:
            self._renderizar(self._todos)
            return
        filtrados = [d for d in self._todos
                     if t in d.get("IDux", "").lower()
                     or t in d.get("_id", "").lower()]
        self._renderizar(filtrados)

    def abrir_perfil(self, uid):
        app = MDApp.get_running_app()
        app.usuario_actual = uid
        self.manager.current = "profile"
        self.manager.transition.direction = "left"

    # Llamado desde el botón "+" del KV
    def abrir_nuevo_usuario(self):
        self.manager.current = "newuser"
        self.manager.transition.direction = "left"

    def descargar_grupo(self):
        app = MDApp.get_running_app()
        filtro = getattr(app, "filtro_grupo", None)
        if not filtro:
            return
        try:
            docs = db.collection("Users").where("experimentalGroup", "==", filtro).stream()
            filas = []
            for doc in docs:
                uid = doc.id
                for s in db.collection("Users").document(uid).collection("Sesiones").stream():
                    sd = s.to_dict()
                    filas.append({
                        "UserID":               uid,
                        "ExperimentalGroup":    filtro,
                        "SessionID":            s.id,
                        "TrajectoryID":         sd.get("TrajectoryID", ""),
                        "SessionIndex":         sd.get("SessionIndex", ""),
                        "TotalTime":            sd.get("TotalTime", ""),
                        "TotalErrors":          sd.get("TotalErrors", ""),
                        "InsideTimePercentage": sd.get("InsideTimePercentage", ""),
                        "Stars":                sd.get("stars", "")
                    })
            guardar_csv(filas, f"{filtro}_metrics.csv", "Descargas por grupo")
        except Exception as e:
            print(f"[Descargar grupo] Error: {e}")

# ==========================================================================================
# NEW_USER  — pantalla de registro (no diálogo)
# ==========================================================================================
class New_User(MDScreen):
    grupo_seleccionado = None
    modo_edicion       = False   # True cuando viene desde Profile
    uid_editando       = None    # ID del usuario que se está editando

    # Trayectorias seleccionadas como set
    _trajs_sel = {"T1", "T2", "T3", "T4", "T5"}

    def on_enter(self):
        self.grupo_seleccionado = None
        self._trajs_sel = {"T1", "T2", "T3", "T4", "T5"}

        if self.modo_edicion and self.uid_editando:
            self._cargar_datos_para_edicion()
        else:
            # Modo creación: autogenerar ID y reset checkboxes
            try:
                self.ids.user_id.disabled = False
                self.ids.titulo_form.text = "Registrar nuevo usuario"
                self.ids.btn_guardar.text = "Guardar usuario"
                self.ids.reps_field.text  = ""
            except Exception:
                pass

    def _cargar_datos_para_edicion(self):
        # Rellena el formulario con los datos existentes del usuario
        try:
            doc = db.collection("Users").document(self.uid_editando).get()
            if not doc.exists:
                return

            d  = doc.to_dict()

            self.ids.user_id.text     = self.uid_editando
            self.ids.user_id.disabled = True   # No se puede cambiar el ID
            self.ids.titulo_form.text = "Editar usuario"
            self.ids.btn_guardar.text = "Guardar cambios"

            # Grupo
            self.grupo_seleccionado = d.get("experimentalGroup", "")
            self.ids.reps_field.text = str(d.get("repsPerTrajectory"))
            self._trajs_sel = set(d.get("trajectoriesIncluded", TRAYECTORIAS))

        except Exception as e:
            print(f"[New_User] Error cargando edición: {e}")

    def sel_grupo(self, grupo):
        self.grupo_seleccionado = grupo

    def toggle_trayectoria(self, traj, activo):
        if activo:
            self._trajs_sel.add(traj)
        else:
            self._trajs_sel.discard(traj)

    def guardar_paciente(self):
        IDux = self.ids.user_id.text.strip()

        if not IDux:
            self.ids.user_id.error = True
            return

        if not self.grupo_seleccionado:
            self.ids.lbl_error.text = "Selecciona una modalidad de juego"
            return

        if not self._trajs_sel:
            self.ids.lbl_error.text = "Selecciona al menos una trayectoria"
            return

        try:
            reps = int(self.ids.reps_field.text.strip())
            if reps < 1 or reps > 20:
                self.ids.lbl_error.text = "Las repeticiones deben estar entre 1 y 20"
                return
        except ValueError:
            self.ids.lbl_error.text = "Número de repeticiones inválido"
            return

        trajs_lista = sorted(self._trajs_sel)   # orden fijo para consistencia
        TOTAL_REPS  = len(trajs_lista) * reps
        orden       = trajs_lista * reps
        random.shuffle(orden)

        try:
            if self.modo_edicion:
                # -- Actualizar usuario existente --------------------------
                db.collection("Users").document(self.uid_editando).update({
                    "experimentalGroup": self.grupo_seleccionado,
                    "totalReps":            TOTAL_REPS,
                    "trajectoriesIncluded": trajs_lista,
                    "repsPerTrajectory":    reps,
                })
                db.collection("UnityConfig").document(self.uid_editando).update({
                    "experimentalGroup":    self.grupo_seleccionado,
                    "trajectoryOrder":      orden,
                    "trajectoriesIncluded": trajs_lista,
                    "repsPerTrajectory":    reps,
                })
                print(f"[New_User] Actualizado: {self.uid_editando}")

            else:
                # -- Crear usuario nuevo -----------------------------------
                if db.collection("Users").document(IDux).get().exists:
                    self.ids.lbl_error.text = f"Ya existe un usuario con ID: {IDux}"
                    return

                datos = {
                    "experimentalGroup": self.grupo_seleccionado,
                    "createdAt": firestore.SERVER_TIMESTAMP,
                    "totalReps": TOTAL_REPS,
                    "trajectoriesIncluded": trajs_lista,
                    "repsPerTrajectory": reps,
                    "status": "pending",
                }
                config = {
                    "experimentalGroup": self.grupo_seleccionado,
                    "trajectoryOrder": orden,
                    "CurrentRepetition": 1,
                    "trajectoriesIncluded": trajs_lista,
                    "repsPerTrajectory": reps,
                }
                db.collection("Users").document(IDux).set(datos)
                db.collection("UnityConfig").document(IDux).set(config)
                print(f"[New_User] Creado: {IDux} → {self.grupo_seleccionado}")

            self.cancelar()

        except Exception as e:
            self.ids.lbl_error.text = f"Error al guardar: {e}"
            print(f"[New_User] Error: {e}")

    def cancelar(self):
        try:
            self.ids.user_id.text      = ""
            self.ids.user_id.disabled  = False
            self.ids.user_id.error     = False
            self.ids.lbl_error.text    = ""
            self.ids.reps_field.text   = ""
            self.grupo_seleccionado    = None
            self._trajs_sel            = {"T1", "T2", "T3", "T4", "T5"}
        except Exception:
            pass
        self.modo_edicion  = False
        self.uid_editando  = None
        self.manager.current = "users"
        self.manager.transition.direction = "right"

# ==========================================================================================
# PROFILE  — perfil del participante
# ==========================================================================================
class Profile(MDScreen):
    from kivymd.uix.label import MDIcon

    _uid = None
    _sesiones = []

    def on_enter(self):
        Clock.schedule_once(self.cargar, 0.15)

    def cargar(self, dt=None):
        app = MDApp.get_running_app()
        self._uid = getattr(app, "usuario_actual", None)
        if not self._uid:
            return
        
        try:
            doc = db.collection("Users").document(self._uid).get()
            if doc.exists:
                d = doc.to_dict()
                self._mostrar_info(d)
                self._cargar_sesiones()
        except Exception as e:
            print(f"[Profile] Error: {e}")

    def _mostrar_info(self, d_user):
        grupo = d_user.get("experimentalGroup", "")
        gc = GRUPO_COLORS.get(grupo, (0.5, 0.5, 0.5, 1))
        total = d_user.get("totalReps", 0)
        trayectorias_str = ", ".join(d_user.get("trajectoriesIncluded", []))

        try:
            sesiones_docs = (db.collection("Users").document(self._uid)
                            .collection("Sesiones").stream())
            comp = sum(1 for _ in sesiones_docs)
        except Exception:
                comp = 0

        self._total_reps = total
        status = session_status(comp, total)
        sc = status_color(status)

        text_info = (
            f"Modalidad de juego {GRUPO_LABELS.get(grupo, grupo)}, "
            f"realizando las trayectorias {trayectorias_str} "
            f"con {d_user.get('repsPerTrajectory', 0)} repeticiones cada una."
        )
        self.ids.lbl_uid.text = self._uid
        self.ids.lbl_grupo.text = text_info
        self.ids.lbl_grupo.text_color = gc
        self.ids.lbl_progreso.text = f"{comp} / {total} repeticiones"
        self.ids.lbl_status.text = status_label(status)
        self.ids.lbl_status.text_color = sc

        puede = comp > 0
        self.ids.btn_dl_metricas.disabled = not puede
        self.ids.btn_dl_metricas.opacity = 1.0 if puede else 0.4

    def _cargar_sesiones(self):
        try:
            sdocs = (db.collection("Users").document(self._uid)
                     .collection("Sesiones")
                     .order_by("SessionIndex")
                     .stream())
            self._sesiones = []
            for s in sdocs:
                sd = s.to_dict()
                sd["_id"] = s.id
                self._sesiones.append(sd)
            self._renderizar_tabla()
        except Exception as e:
            print(f"[Profile] Error sesiones: {e}")

    def _renderizar_tabla(self):
        from kivymd.uix.button import MDIconButton
        from kivymd.uix.label import MDIcon

        tbody = self.ids.tabla_body
        tbody.clear_widgets()

        if not self._sesiones:
            tbody.add_widget(MDLabel(
                text="Sin repeticiones registradas",
                halign="center", theme_text_color="Hint",
                size_hint_y=None, height=dp(40)
            ))
            return
            

        # Anchos deben coincidir exactamente con la cabecera del KV
        COL_W = [0.1, 0.1, 0.1, 0.1, 0.2, 0.1, 0.1, 0.2]
        #
        for s in self._sesiones:
            row = MDBoxLayout(
                orientation="horizontal",
                size_hint_y=None,
                height=dp(36),
                padding=[dp(4), 0]
            )

            # Columnas antes de stars
            vals = [
                str(s.get("SessionIndex", "")),           # #
                s.get("TrajectoryID", ""),                # Trayectoria
                str(s.get("SessionIndex", "")),           # Rep.
                str(s.get("TotalErrors", "")),            # Errores
            ]

            for val, w in zip(vals, COL_W[:4]):
                lbl = MDLabel(
                    text=val,
                    font_style="Body2",
                    halign="center",
                    valign="center",
                    pos_hint={"center_y": 0.5,"center_x":0.5},
                    size_hint_x=w
                )
                lbl.bind(size=lbl.setter("text_size"))
                row.add_widget(lbl)

            # Estrellas
            stars_layout = MDBoxLayout(
                orientation="horizontal",
                spacing=dp(2),
                size_hint_x=COL_W[4],
                pos_hint={"center_y": 0.5,"center_x":0.5}
            )

            num_stars = int(s.get("Stars", 0))

            for i in range(5):
                icon = "star" if i < num_stars else "star-outline"
                star = MDIcon(
                    icon=icon,
                    theme_text_color="Custom",
                    pos_hint={"center_y": 0.5,"center_x":0.5},
                    text_color=(1, 0.75, 0, 1), # Un color ámbar/dorado para que parezcan estrellas reales
                    )
                stars_layout.add_widget(star)

            row.add_widget(stars_layout)

            # % Dentro
            lbl_pct = MDLabel(
                text=f"{s.get('InsideTimePercentage', 0):.1f}%",
                font_style="Body2",
                halign="center",
                valign="center",
                size_hint_x=COL_W[5]
            )
            lbl_pct.bind(size=lbl_pct.setter("text_size"))
            row.add_widget(lbl_pct)

            # Tiempo
            lbl_time = MDLabel(
                text=f"{s.get('TotalTime', 0):.2f} s",
                font_style="Body2",
                halign="center",
                valign="center",
                size_hint_x=COL_W[6]
            )
            lbl_time.bind(size=lbl_time.setter("text_size"))
            row.add_widget(lbl_time)

            # Botón descargar
            btn = MDIconButton(
                icon="download",
                size_hint_x=COL_W[7],
                theme_icon_color="Custom",
                icon_color=(0.13, 0.47, 0.71, 1)
            )
            btn.bind(on_release=lambda x, ses=s: self._descargar_vector(ses))
            row.add_widget(btn)

            sep = MDBoxLayout(
                size_hint_y=None,
                height=dp(1),
                md_bg_color=(0.92, 0.92, 0.92, 1)
            )

            tbody.add_widget(row)
            tbody.add_widget(sep)

    # -- Descargas -------------------------------------------------------------
    def descargar_metricas(self):
        filas = []
        for s in self._sesiones:
            filas.append({
                "UserID":               self._uid,
                "SessionID":            s["_id"],
                "TrajectoryID":         s.get("TrajectoryID", ""),
                "SessionIndex":         s.get("SessionIndex", ""),
                "TotalTime":            s.get("TotalTime", ""),
                "TotalErrors":          s.get("TotalErrors", ""),
                "InsideTimePercentage": s.get("InsideTimePercentage", ""),
                "Stars":                s.get("Stars", ""),
            })
        IDux = self.ids.lbl_uid.text
        guardar_csv(filas, f"{IDux}_session_metrics.csv", "Descargas por usuario", IDux)

    def _descargar_vector(self, sesion):
        puntos = sesion.get("trajectoryPoints", [])
        if not puntos:
            print("[Profile] Sin puntos en esta sesión")
            return
        filas = []
        for i, p in enumerate(puntos):
            filas.append({
                "t":  i,
                "x": p.get("x", "") if isinstance(p, dict) else "",
                "y": p.get("y", "") if isinstance(p, dict) else "",
                "z": p.get("z", "") if isinstance(p, dict) else "",
            })
        IDux = self.ids.lbl_uid.text
        IDses = sesion.get("_id")
        guardar_csv(filas, f"{IDux}_{IDses}_points.csv", "Descargas por usuario", self._uid, "Vectores de trayectorias")

    def descargar_todos_vectores(self):
        filas = []
        for s in self._sesiones:
            for i, p in enumerate(s.get("trajectoryPoints", [])):
                filas.append({
                    "UserID":         self._uid,
                    "SessionID":      s["_id"],
                    "TrajectoryID":   s.get("TrajectoryID", ""),
                    "t":  i,
                    "x": p.get("x", "") if isinstance(p, dict) else "",
                    "y": p.get("y", "") if isinstance(p, dict) else "",
                    "z": p.get("z", "") if isinstance(p, dict) else "",
                })
        IDux = self.ids.lbl_uid.text
        guardar_csv(filas, f"{IDux}_all_points.csv", "Descargas por usuario", IDux)

    def abrir_edicion(self):
        # Botón editar: solo si status es pending.
        doc = db.collection("Users").document(self._uid).get()
        if not doc.exists:
            return
        
        docConf = db.collection("UnityConfig").document(self._uid).get()
        if docConf.exists:
            conf = docConf.to_dict()
            current_rep = conf.get("CurrentRepetition", 1)-1
        else:
            current_rep = 0

        total = doc.to_dict().get("totalReps", 0)
        status = session_status(current_rep, total)

        if status == "pending":
            # Ir a New_User en modo edición
            app = MDApp.get_running_app()
            app.usuario_actual = self._uid
            nu = self.manager.get_screen("newuser")
            nu.modo_edicion  = True
            nu.uid_editando  = self._uid
            self.manager.current = "newuser"
            self.manager.transition.direction = "left"
        else:
            # Mostrar diálogo de advertencia
            self._dialog_edicion = MDDialog(
                title="No se puede editar",
                text="Error: no se puede modificar los datos y configuración del usuario cuando ha comenzado la sesión. ¿Quieres borrar la sesión actual y volver a comenzar?",
                buttons=[
                    MDFlatButton(
                        text="Cancelar",
                        on_release=lambda x: self._dialog_edicion.dismiss()
                    ),
                    MDRaisedButton(
                        text="Borrar sesión actual",
                        md_bg_color=(0.85, 0.18, 0.18, 1),
                        on_release=lambda x: self._borrar_sesion_y_editar()
                    ),
                ]
            )
            self._dialog_edicion.open()

    def _borrar_sesion_y_editar(self):
        # Borra todas las Sesiones del usuario y resetea su estado
        self._dialog_edicion.dismiss()
        try:
            # Borrar subcolección Sesiones
            sesiones = (db.collection("Users").document(self._uid)
                        .collection("Sesiones").stream())
            for s in sesiones:
                s.reference.delete()

            # Resetear contadores en Users
            db.collection("Users").document(self._uid).update({
                "status": "pending",
            })
            # Resetear status en UnityConfig
            db.collection("UnityConfig").document(self._uid).update({
                "CurrentRepetition": 1
            })
            print(f"[Profile] Sesión borrada para: {self._uid}")

            # Ahora sí abrir edición
            nu = self.manager.get_screen("newuser")
            nu.modo_edicion = True
            nu.uid_editando = self._uid
            self.manager.current = "newuser"
            self.manager.transition.direction = "left"

        except Exception as e:
            print(f"[Profile] Error borrando sesión: {e}")

    def confirmar_eliminar_usuario(self):
        """Botón rojo: pide confirmación antes de eliminar."""
        self._dialog_eliminar = MDDialog(
            title="Eliminar usuario",
            text="¿Eliminar este perfil de usuario y toda su información?",
            buttons=[
                MDFlatButton(
                    text="Cancelar",
                    on_release=lambda x: self._dialog_eliminar.dismiss()
                ),
                MDRaisedButton(
                    text="Eliminar perfil",
                    md_bg_color=(0.85, 0.18, 0.18, 1),
                    on_release=lambda x: self._eliminar_usuario()
                ),
            ]
        )
        self._dialog_eliminar.open()

    def _eliminar_usuario(self):
        # Elimina Sesiones, Users y UnityConfig del usuario
        self._dialog_eliminar.dismiss()
        try:
            uid = self._uid
            # Borrar subcolección Sesiones
            for s in db.collection("Users").document(uid).collection("Sesiones").stream():
                s.reference.delete()
            # Borrar documento Users
            db.collection("Users").document(uid).delete()
            # Borrar documento UnityConfig
            db.collection("UnityConfig").document(uid).delete()

            print(f"[Profile] Usuario eliminado: {uid}")
            self.volver()

        except Exception as e:
            print(f"[Profile] Error eliminando: {e}")

    def volver(self):
        self.manager.current = "users"
        self.manager.transition.direction = "right"

    def refresh(self):
        self.cargar()

# ==========================================================================================
# INFORMATION
# ==========================================================================================
class Information(MDScreen):
    def on_enter(self):
        try:
            self.ids.img_logo.source = resource_path("logo.png")
        except Exception:
            pass

    def copiar_repo(self):
        from kivy.core.clipboard import Clipboard
        try:
            url = self.ids.lbl_repo.text
            Clipboard.copy(url)
            print("[Info] URL copiada al portapapeles")
        except Exception as e:
            print(f"[Info] Error copiando: {e}")

# ==========================================================================================
# APP
# ==========================================================================================
class MainApp(MDApp):
    title        = "SIR-HAPT Manager"
    filtro_grupo  = None
    usuario_actual = None

    def build(self):
        Window.size = (1200, 850)
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Indigo"
        self.theme_cls.secondary_palette = "BlueGray"
        Window.set_icon(resource_path('logo.ico'))
        return Builder.load_file(resource_path('app.kv'))

if __name__ == "__main__":
    MainApp().run()