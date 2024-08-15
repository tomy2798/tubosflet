import flet as ft
from Inicio import inicio
from data_manager import DataManager
import re


class espesores(ft.UserControl):
    def __init__(self,page):
        super().__init__()
        self.page= page
        self.dm= DataManager()
        self.busqueda= False
        self.resultado = []
        self.selected_row=[]
        
        
        
       
        
        
        #Seccion agregar espesor
        self.add_espesor= ft.TextField(label="Espesor",autofocus=True,on_submit=lambda _: self.add_valor.focus(),on_change=self.validate_espesor)
        self.add_valor= ft.TextField(label="Valor",on_submit=lambda _: self.add_chapa.focus(),on_change=self.validate_valor)
        self.add_chapa= ft.TextField(label="Chapa")
        self.add_button= ft.ElevatedButton(
                        content=ft.Text("Crear"),
                        width=120,
                        height=40,
                        bgcolor=ft.colors.GREY_400,
                        color=ft.colors.GREY_600,
                        on_click=self.crear_espesor
        )
        
        
        self.add_alert = ft.AlertDialog(
            title=ft.Text("Crear"),
            content = ft.Container(
                padding=10,
                width=350,
                height=350,
                border_radius=10,
                content=ft.Column(
                    controls=[
                        self.add_espesor,
                        self.add_valor,
                        self.add_chapa,
                        self.add_button
                    ]
                )
            )
        )
        
        
        
        
        self.espesor_busqueda= ft.TextField(label="Buscar espesor",on_change=self.show_busqueda_espesor,autofocus=True)
        
        
        
        self.data_espesor = ft.DataTable( 
            border=ft.border.all(2, ft.colors.GREY_300),
            data_row_color=ft.colors.GREY_300,
            horizontal_lines=ft.BorderSide(.5, ft.colors.GREY_300),
            columns=[
                ft.DataColumn(ft.Text("Valor")),
                ft.DataColumn(ft.Text("Espesor")),
                ft.DataColumn(ft.Text("Chapa")),
                ft.DataColumn(ft.Text("Eliminar"))
            ]
        )
        
        
        
        self.buscador = ft.Container(
            padding=10,
            col=2,
            border_radius=10,
            content= ft.Column(
                expand=True,
                controls= [
                    ft.Text("Buscador de espesores",size=20),
                    ft.Row(
                        alignment= ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[ 
                            ft.Container(
                                expand= True,
                                content=(
                                    ft.Row(
                                        controls=[
                                            self.espesor_busqueda,
                                        ]
                                    )
                                )
                                
                                ),
                            ft.Container( 
                                width=100,
                                height=60,
                                content=ft.IconButton(ft.icons.ADD,on_click=self.open_alert,bgcolor=ft.colors.GREY_300)
                                
                            )
                        ]
                        ),
                    ]
            )
        )
        
        
        #CONTENEDOR DE DATATABLE
        self.data_table_esp = ft.Container(
            padding=10,
            expand=True,
            col=10,
            border_radius=10,
            content= ft.ResponsiveRow(
                controls=[
                    self.data_espesor,
                ]
            )
        )
        self.show_espesores()
        
        #CONTENEDOR PRINCIPAL
        self.buscador_esp = ft.Container(
            border_radius=10,
            expand=True,
            content= ft.Column(
                expand=True,
                controls=[
                    self.buscador,
                    self.data_table_esp
                    
                ]
            )
        )
        
    
    def show_espesores(self):
        self.data_espesor.rows=[]
        for x in self.dm.get_espesores():
            self.data_espesor.rows.append(
                ft.DataRow(
                    on_select_changed=self.get_idex,
                    cells=[
                    ft.DataCell(ft.Text (str(x[1]),weight="bold")),
                    ft.DataCell(ft.Text(str(x[0]))),
                    ft.DataCell(ft.Text(x[2])),
                    ft.DataCell(ft.Row(
                        controls=[
                            ft.IconButton(
                                icon=ft.icons.DELETE,
                                on_click=lambda e, x=x: self.delete_espesor(e, x),
                            ),
                        ]
                    )
                ),
            ]))
        self.data_espesor.visible = True
        self.data_table_esp.content = ft.Column(
            scroll="auto",
            controls=[
                ft.ResponsiveRow(controls=[self.data_espesor,])
            ]
        )

        self.update()
        
    def show_busqueda_espesor(self, e):
        self.busqueda = True

        # Inicializamos los parámetros de búsqueda
        busqueda_params = {}

        if self.espesor_busqueda.value:
            busqueda_params['espesor'] = self.espesor_busqueda.value

        
        self.resultado = self.dm.buscador_espesores(**busqueda_params)
        print("impreso desde show_data:", self.resultado)
        # Actualizamos la tabla de resultados
        self.data_espesor.rows = []
        for row in self.resultado:
            self.data_espesor.rows.append(ft.DataRow(
                on_select_changed=self.get_idex,
                cells=[
                    ft.DataCell(ft.Text(row[1],weight="bold")),
                    ft.DataCell(ft.Text(str(row[0]))),
                    ft.DataCell(ft.Text(str(row[2]))),
                    ft.DataCell(ft.Row(
                        controls=[
                            ft.IconButton(
                                icon=ft.icons.DELETE,
                                on_click=lambda e, row=row: self.delete_espesor(e, row),
                            ),
                        ]
                    ))
                    
                ]
            ))


        if not self.data_espesor.rows:
            self.data_espesor.visible = False
            self.data_table_esp.content = ft.Text("Sin resultados", size=20, color="red")
        else:
            self.data_espesor.visible = True
            self.data_table_esp.content = ft.Column(
            scroll="auto",
            controls=[
                ft.ResponsiveRow(controls=[self.data_espesor,])
            ]
        )

        self.update()
    
    
    def open_alert(self,e):
        self.page.dialog = self.add_alert
        self.add_alert.open = True
        self.page.update()
                    
    def crear_espesor(self,e):
        espesor= self.add_espesor.value
        valor= self.add_valor.value
        chapa= self.add_chapa.value
        
        if not espesor or not valor or not chapa:
            self.page.show_snack_bar(
                ft.SnackBar(
                    content=ft.Text("Todos los campos son obligatorios"),
                    bgcolor=ft.colors.RED,
                )
            )
            return
        
    # Validar formato de espesor
        if not self.validate_espesor(None):
            self.page.show_snack_bar(
                ft.SnackBar(
                    content=ft.Text("Formato de espesor inválido"),
                    bgcolor=ft.colors.RED,
                )
            )
            return

        if not self.validate_valor(None):
            self.page.show_snack_bar(
                ft.SnackBar(
                    content=ft.Text("El valor debe ser un número entero"),
                    bgcolor=ft.colors.RED,
                )
            )
            return
    
        try:
            espesor = str(espesor)
            valor = int(valor)
            chapa = str(chapa)
        except ValueError:
            
            return ft.SnackBar(
                duration=ft.snack_bar.SnackBarDismissAnimationDuration.FAST,
                bgcolor=ft.colors.RED,
                content=ft.Text("Hello, world!"))
            
            
        self.dm.add_espesor(espesor, valor, chapa)
        
        # Limpiar los campos después de crear el tubo
        self.add_espesor.value = ""
        self.add_valor.value = ""
        self.add_chapa.value = ""
        self.show_espesores()
        self.add_alert.open = False
        self.page.update()     
        self.page.show_snack_bar(
        ft.SnackBar(
            content=ft.Text("Espesor agregado correctamente"),
            bgcolor=ft.colors.GREEN,
        )
    )            
                    
    def get_idex(self, e):
    # Toggleamos la selección de la fila
        e.control.selected = not e.control.selected
        
        if e.control.selected:
            # Si la fila está seleccionada, guardamos sus datos
            self.selected_row = [cell.content for cell in e.control.cells]
            print("Espesor seleccionado:", self.selected_row)
        else:
            # Si la fila se deselecciona, limpiamos los datos seleccionados
            self.selected_row = None
            print("Selección de espesor eliminada")
        
        self.update()            
    
    def delete_espesor(self,e,row):
        valor = row[1]
        def handle_action_click(e):
            if e.control.text == "Eliminar":
                print(f"Eliminando tubo con valor: {valor}")
                self.dm.delete_espesor(valor)
                self.show_espesores()
            self.page.close(e.control.parent)
            self.update()

        cupertino_actions = [
                ft.CupertinoDialogAction(
                    "Cancelar",
                    is_destructive_action=False,
                    on_click=handle_action_click,
                ),
                ft.CupertinoDialogAction(
                    "Eliminar",
                    is_destructive_action=True,
                    on_click=handle_action_click,
                ),
            ]
        
        self.page.open(
            ft.CupertinoAlertDialog(
                title=ft.Text("Eliminar"),
                content=ft.Text(f"¿Estás seguro de que quieres eliminar el espesor con valor {valor}?"),
                actions=cupertino_actions,
            )
        )        
    
    
    def validate_espesor(self, e):
        text = self.add_espesor.value
        cleaned_text = re.sub(r'[^0-9,]', '', text)
        
        if text != cleaned_text:
            self.add_espesor.error_text = "Solo se permiten números y comas"
            self.add_espesor.update()
            return False
        
        if ',' in cleaned_text and not re.match(r'^\d+,\d+$', cleaned_text):
            self.add_espesor.error_text = "Formato inválido. Use 'X,XX'"
            self.add_espesor.update()
            return False
        
        self.add_espesor.error_text = None
        self.add_espesor.update()
        return True
            
    def validate_valor(self, e):
        valor = self.add_valor.value.strip()  # Eliminamos espacios al inicio y final

        if not valor:
            self.add_valor.error_text = "El campo no puede estar vacío"
            self.add_valor.update()
            return False

        if not valor.isdigit():
            self.add_valor.error_text = "Solo se permiten números enteros positivos"
            self.add_valor.update()
            return False

        # Si llegamos aquí, el valor es válido
        self.add_valor.error_text = None
        self.add_valor.update()
        return True

    
    def validar_button(self):
        if self.add_espesor and self.add_valor and self.add_chapa == "":
            self.add_button.disabled
        else:
            self.crear_espesor
                 
    def build(self):
        return self.buscador_esp
    
    
