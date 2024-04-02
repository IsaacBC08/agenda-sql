import flet as ft
from datetime import datetime as dt
import sqlite3 as sql

# GUI content/colors
bgColor = "bluegrey700"
bgColor2 = "#0f0f0f"
bgColor3 = "bluegrey500"
bgColor4 = {"": 'green600'}
bdColor = "white"
bdColor2 = "transparent"
dvColor = "white24"


class DataBase(object):
    def conectar_db():
        try:
            db = sql.connect('tareas.db')
            c = db.cursor()
            c.execute('CREATE TABLE IF NOT EXISTS tareas (id INTEGER PRIMARY KEY, tarea VARCHAR(255) NOT NULL, fecha VARCHAR(255) NOT NULL, limite VARCHAR(255) NOT NULL)')
            return db
        except Exception as e:
            print()

    def leer_datos(db):
        c = db.cursor()
        c.execute('SELECT tarea, fecha, limite FROM tareas')
        datos = c.fetchall()
        return datos
    def agregar_datos(db, values):
        c = db.cursor()
        c.execute('INSERT INTO tareas (tarea, fecha, limite) VALUES (?,?,?)', values)
        db.commit()
    def eliminar_datos(db, value):
        c = db.cursor()
        c.execute('DELETE FROM tareas WHERE tarea = ?', value)
        db.commit()
    def actualizar_datos(db, value):
        c = db.cursor()
        c.execute('UPDATE tareas SET tarea = ?, fecha = ? WHERE tarea = ?', (value))

        db.commit()

class ContenedorForm(ft.UserControl):
    def __init__(self, func):
        self.func = func
        super().__init__()
    
    def build(self):
        return ft.Container(
            width= 1120,
            height=80,
            bgcolor=bgColor3,
            opacity=0,
            border_radius=40,
            margin= ft.margin.only(left=10, right=10),
            animate= ft.animation.Animation(800, "decelerate"),
            animate_opacity= 400, 
            padding= ft.padding.only(top=45, bottom=45),
            content= ft.Column(
                horizontal_alignment= ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.TextField(
                        height= 48,
                        width= 1000,
                        filled= True,
                        border_color=bdColor2,
                        color = "grey100",
                        text_size = 24,
                        hint_text="Descripción de la tarea",
                        hint_style= ft.TextStyle(size= 22, color= "grey100")
                    ),                    
                    ft.TextField(
                        height= 48,
                        width= 1000,
                        filled= True,
                        border_color=bdColor2,
                        color = "grey100",
                        text_size = 24,
                        hint_text="Fecha Limite",
                        hint_style= ft.TextStyle(size= 22, color= "grey100")
                    ),
                    ft.IconButton(
                        content= 
                            ft.Text(value = "Añadir"),
                            width = 550,
                            height= 44,
                            on_click= self.func,
                            style= ft.ButtonStyle(bgcolor= bgColor4, shape= {"": ft.RoundedRectangleBorder(radius=8)})

                    )
                ]
            )
            
            
            )
            
class CrearTarea(ft.UserControl):
    def __init__(self, tarea : str, limite : str,fecha: str, func1, func2):
        super().__init__()
        self.tarea = tarea
        self.fecha = "Agendado: " + fecha
        self.limite = "Fecha limite: " + limite
        self.func1 = func1
        self.func2 = func2

    
    def eliminar_editar_tarea(self, nombre, color, func):
        return ft.IconButton(
            icon= nombre,
            width= 60,
            height=60,
            icon_size= 30,
            icon_color= color, 
            opacity= 0,
            animate_opacity= 300,
            on_click= lambda e: func(self.obtenerInstancia()),
        )
    def obtenerInstancia(self):
        return self  
    def eliminar_tarea(self):
        pass
    def iconos(self, e):
        if e.data == "true":
            e.control.content.controls[1].controls[0].opacity = 1
            e.control.content.controls[1].controls[1].opacity = 1
            e.control.content.update()
        else:
            e.control.content.controls[1].controls[0].opacity = 0
            e.control.content.controls[1].controls[1].opacity = 0
            e.control.content.update()
    
    def build(self):
        return ft.Container(
            width=1120,
            height=90,
            border= ft.border.all(0.85, "white"),
            border_radius=10,
            on_hover= lambda e: self.iconos(e),
            clip_behavior= ft.ClipBehavior.HARD_EDGE,
            padding=10,
            content= ft.Row(
                alignment= ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Column(
                        spacing=1,
                        alignment= ft.MainAxisAlignment.CENTER,
                        controls=[
                            ft.Text(self.fecha, size=12, color="white54"),                       
                            ft.Text(self.tarea, size= 20, weight="bold"),
                            ft.Text(self.limite, size= 18, weight="bold", color= "red400")
                        ]
                    ),
                    ft.Row(
                        spacing= 0, 
                        alignment= ft.MainAxisAlignment.CENTER,
                        controls=[
                            self.eliminar_editar_tarea(ft.icons.DELETE, "red600", self.func1),
                            self.eliminar_editar_tarea(ft.icons.EDIT, "white80", self.func2)
                        ]
                    )
                ]
            )
        )

def main(page: ft.Page):
    page.horizontal_alignment = 'center'
    page.vertical_alignment = 'center'
    page.window_width = 1120
    page.window_height = 660    

    def agregar_tarea(e):
        datetime = dt.now().strftime("%I:%M, %b %d, %Y ")
        db = DataBase.conectar_db()
        DataBase.agregar_datos(db, (formulario.content.controls[0].value, formulario.content.controls[1].value, datetime))
        db.close()

        if formulario.content.controls[0].value:
            _main_column.controls.append(
                CrearTarea(
                    formulario.content.controls[0].value,
                    formulario.content.controls[1].value,
                    datetime,
                    eliminar,
                    actualizar
                )
            )
            _main_column.update()
            crear_tarea(e)
        else:
            db.close()

    def eliminar(e):
        db = DataBase.conectar_db()
        dt = [e.controls[0].content.controls[0].controls[1].value]
        DataBase.eliminar_datos(
            db,  (dt)
            )
        db.close()        
        _main_column.controls.remove(e)
        _main_column.update()

    def actualizar(e):
        formulario.height, formulario.opacity = 250, 1
        tarea = formulario.content.controls[0]
        tarea.value = e.controls[0].content.controls[0].controls[1].value
        fechaLimite =  formulario.content.controls[1]
        fechaLimite.value = None
        btn_actualizar = formulario.content.controls[2]
        btn_actualizar.content.value = "Actualizar"
        btn_actualizar.on_click = lambda _: finalizarActualizar(e)
        formulario.update()
    
    def finalizarActualizar(e):
        db = DataBase.conectar_db()
        DataBase.actualizar_datos(db, (formulario.content.controls[0].value, formulario.content.controls[1].value,tarea[0]))
        e.controls[0].content.controls[0].controls[1].value = formulario.content.controls[0].value
        e.controls[0].content.controls[0].controls[2].value = formulario.content.controls[1].value
        e.controls[0].content.update()
        crear_tarea(e)

    def crear_tarea(e):
        if formulario.height != 250:
            formulario.height = 250
            formulario.opacity = 1
            formulario.update()
        else: 
            formulario.opacity = 0
            formulario.height = 80
            formulario.content.controls[0].value = None
            formulario.content.controls[1].value = None
            formulario.content.controls[2].content.value = "Añadir"
            formulario.content.controls[2].on_click = lambda e : agregar_tarea(e)
            formulario.update()
    
    _main_column = ft.Column(scroll= "hidden",
                             expand= True,
                             alignment= ft.MainAxisAlignment.START,
                             controls=[
                                 ft.Row(alignment= ft.MainAxisAlignment.SPACE_BETWEEN,
                                        controls=[
                                            ft.Text(
                                                value="Agenda", size= 54, weight="bold"),
                                            ft.IconButton(
                                                icon= ft.icons.ADD_CIRCLE_ROUNDED, icon_size= 54,
                                                on_click= lambda e : crear_tarea(e),
                                            )
                                        ]),
                                    ft.Divider(height= 12, color= dvColor)
                             ]
                             )

    sc_column =  ft.Column(alignment= ft.MainAxisAlignment.CENTER,
                    expand= True,
                    controls=[
                        _main_column,
                        ContenedorForm(lambda e : agregar_tarea(e))                        
                        ]
                    )  

    page.add(sc_column)

    page.update()

    formulario = page.controls[0].controls[1].controls[0]
    db = DataBase.conectar_db()

    for tarea in DataBase.leer_datos(db):
        _main_column.controls.append(
         CrearTarea(
                tarea[0],
                tarea[1],
                tarea[2],
                eliminar,
                actualizar
            )
        )
    _main_column.update()

if __name__ == '__main__':
    ft.app(target=main)