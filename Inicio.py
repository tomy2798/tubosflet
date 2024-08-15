import flet as ft
from data_manager import DataManager
from flet import AppBar, ElevatedButton, Page, Text, View, colors



class inicio(ft.UserControl):
    def __init__(self,page):
        super().__init__(expand=True)
        self.page = page
        self.dm = DataManager()
        self.selected_row = []
        self.busqueda = False
        self.resultado = []
        #Seccion Busqueda
        
        
        self.longitud1_busqueda = ft.TextField(
            label="Longitud 1",
            border_color=ft.colors.GREY_400,
            autofocus=True,
            cursor_color=ft.colors.GREY_600,
            focused_border_color=ft.colors.GREY_600,
            on_submit=lambda _: self.longitud2_busqueda.focus()
        )
        self.longitud2_busqueda = ft.TextField(
            label="Longitud 2",
            border_color=ft.colors.GREY_400,
            autofocus=True,
            cursor_color=ft.colors.GREY_600,
            focused_border_color=ft.colors.GREY_600,
            on_submit=lambda _: self.espesor_busqueda.focus()
        )
        self.tipo_busqueda = ft.Dropdown(
            options=[
                ft.dropdown.Option("Todos"),
                ft.dropdown.Option("Redondo"),
                ft.dropdown.Option("Cuadrado"),
                ft.dropdown.Option("Rectangular"),
            ],
            label="Selecciona una opcion",
            value= "Todos",
            border_color=ft.colors.GREY_400,
            
                
        )
        self.button_busqueda = ft.ElevatedButton(
            width=40,
            height=40,
            bgcolor=ft.colors.GREY_400,
            color=ft.colors.WHITE,
            on_click=self.show_data_busqueda,
            content= ft.Icon(ft.icons.SEARCH),
                    
        )
        self.espesor_busqueda = ft.TextField(
            label="Espesor",
            border_color=ft.colors.GREY_400,
            autofocus=True,
            cursor_color=ft.colors.GREY_600,
            focused_border_color=ft.colors.GREY_600,
        )
        
        
        #Seccion edicion de tubos
        self.longitud1= ft.TextField(label="Longitud 1")
        self.longitud2= ft.TextField(label="Longitud 2")
        self.espesor= ft.TextField(label="Espesor")
        self.valor= ft.TextField(label="Valor")
        self.tipo = ft.Dropdown(
            options=[
                ft.dropdown.Option("Redondo"),
                ft.dropdown.Option("Cuadrado"),
                ft.dropdown.Option("Rectangular"),
            ],
            label="Selecciona una opcion",
            border_color=ft.colors.GREY_400,
        )
        self.button_edit = ElevatedButton(
            content=ft.Text("Editar"),
            width=120,
            height=40,
            bgcolor=ft.colors.GREEN_700,
            color=ft.colors.WHITE,
            on_click=self.update_tubo_click
        )
       
        
        
        self.dlg = ft.AlertDialog(
            title=ft.Text("Editar"),
            content = ft.Container(
                width=350,
                height=400,
                border_radius=10,
            )
        )
        
        #Datatable Principal
        self.data_table_select = ft.DataTable(
            border=ft.border.all(2, ft.colors.GREY_300),
            data_row_color=ft.colors.GREY_300,
            horizontal_lines=ft.BorderSide(.5, ft.colors.GREY_300),
            columns=[
                ft.DataColumn(ft.Text("Valor")),
                ft.DataColumn(ft.Text("Tipo")),
                ft.DataColumn(ft.Text("Longitud 1")),
                ft.DataColumn(ft.Text("Longitud 2")),
                ft.DataColumn(ft.Text("Espesor")),
                ft.DataColumn(ft.Text("Acciones")),
            ],
            
        )
        
        
        #Mostramos la consulta de la base de datos al iniciar
        
        
       
        #Contenedor con los widgets de busqueda
        self.search = ft.Container(
            bgcolor=ft.colors.GREY_100,
            border_radius=10,
            height=100,
            content=ft.ResponsiveRow(
                alignment=ft.MainAxisAlignment.START,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Container(
                        content=self.longitud1_busqueda,
                        col={"sm": 8, "md": 3},
                        padding=5,
                    ),
                    ft.Container(
                        content=self.longitud2_busqueda,
                        col={"sm": 6, "md": 3},
                        padding=5,
                    ),
                    ft.Container(
                        content=self.espesor_busqueda,
                        col={"sm": 6, "md": 3},
                        padding=5,
                    ),
                    ft.Container(
                        content=self.tipo_busqueda,
                        col={"sm": 6, "md": 2},
                        padding=5,
                    ),
                    ft.Container(
                        content=self.button_busqueda,
                        col={"sm": 12, "md": 1},
                        padding=5,
                    ),
                ],
            ),
        )
        #Seccion de la informacion, Datatables
        self.data= ft.Container(
            expand=True,

        )
        
        self.show_data()
        #Contenedor principal, une la seccion busqueda y la seccion Data
        self.buscador = ft.Container(
            expand=True,
            border_radius=10,
            bgcolor=ft.colors.WHITE,
            content=ft.Column(
                expand=True,
                controls=[
                    ft.Text("Busqueda de Tubos", size=20, weight="bold"),
                    ft.Divider(),
                    self.search,
                    ft.Divider(),
                    ft.Column(
                        expand=True,
                        scroll="auto",
                        controls=[ft.ResponsiveRow(
                            controls=[self.data]
                        )]
                    )
                 
                    
                ]
            )
        )
    def show_data(self):
        self.data_table_select.rows=[]
        for x in self.dm.get_tubos():
            self.data_table_select.rows.append(
                ft.DataRow(
                    on_select_changed=self.get_idex,
                    cells=[
                    ft.DataCell(ft.Text (str(x[1]),weight="bold")),
                    ft.DataCell(ft.Text(str(x[0]))),
                    ft.DataCell(ft.Text(x[2])),
                    ft.DataCell(ft.Text(x[3])),
                    ft.DataCell(ft.Text(str(x[4]))),
                    ft.DataCell(ft.Row(
                        controls=[
                            ft.IconButton(
                                icon=ft.icons.EDIT,
                                on_click=lambda e, row=x :self.show_row_info(e, row),
                            ),
                            ft.IconButton(
                                icon=ft.icons.DELETE,
                                on_click=lambda e, row=x:  self.delete_row(e, row),
                            ),
                        ]
                    )
                ),
            ]))
        self.data_table_select.visible = True                   
        self.data.content= self.data_table_select
        self.update()
    
    def show_data_busqueda(self, e):
        self.busqueda = True

        # Inicializamos los parámetros de búsqueda
        busqueda_params = {}
        if self.tipo_busqueda.value=="Todos":
            self.longitud1_busqueda.value = ""
            self.longitud2_busqueda.value = ""
            self.espesor_busqueda.value = ""
        else:
            busqueda_params['tipo'] = self.tipo_busqueda.value
        # Añadimos los parámetros solo si tienen un valor
        

        if self.longitud1_busqueda.value:
            busqueda_params['longitud1'] = self.longitud1_busqueda.value

        if self.longitud2_busqueda.value:
            busqueda_params['longitud2'] = self.longitud2_busqueda.value

        if self.espesor_busqueda.value:
            busqueda_params['espesor'] = self.espesor_busqueda.value

        # Realizamos la búsqueda con los parámetros que tengan valor
        self.resultado = self.dm.buscador(**busqueda_params)
        print("impreso desde show_data:", self.resultado)

        # Actualizamos la tabla de resultados
        self.data_table_select.rows = []
        for row in self.resultado:
            self.data_table_select.rows.append(ft.DataRow(
                on_select_changed=self.get_idex,
                cells=[
                    ft.DataCell(ft.Text(row[1],weight="bold")),
                    ft.DataCell(ft.Text(str(row[0]))),
                    ft.DataCell(ft.Text(str(row[2]))),
                    ft.DataCell(ft.Text(str(row[3]))),
                    ft.DataCell(ft.Text(row[4])),
                    ft.DataCell(ft.Row(
                        controls=[
                            ft.IconButton(
                                icon=ft.icons.EDIT,
                                on_click=lambda e, row=row: self.show_row_info(e, row),
                            ),
                            ft.IconButton(
                                icon=ft.icons.DELETE,
                                on_click=lambda e, row=row: self.delete_row(e, row),
                            ),
                        ]
                    ))
                    
                ]
            ))

        if not self.data_table_select.rows:
            self.data_table_select.visible = False
            self.data.content = ft.Text("Sin resultados", size=20, color="red")
        else:
            self.data_table_select.visible = True
            self.data.content = self.data_table_select

        self.update()
    
    
        
        
    
    def show_row_info(self, e, row):
        self.original_valor = row[1]
        self.longitud1.value = str(row[2])
        self.longitud2.value = row[3]
        self.espesor.value = str(row[4])
        self.valor.value = str(row[1])
        self.tipo.value = row[0]
        
        
        self.dlg.content = ft.Container(
            width=400,
            height=600,
            content= ft.Column([
                self.longitud1,
                self.longitud2,
                self.espesor,
                self.valor,
                self.tipo,
                self.button_edit
            ])
        )
        self.page.open(self.dlg)
        
        self.update()
        
        print(f"Información de la fila: {row}")  
        
   
    def delete_row(self, e, row):
        valor = row[1]  # Obtiene solo el valor

        def handle_action_click(e):
            if e.control.text == "Eliminar":
                print(f"Eliminando tubo con valor: {valor}")
                self.dm.delete_tubo(valor)
                self.show_data()
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
                content=ft.Text(f"¿Estás seguro de que quieres eliminar el tubo con valor {valor}?"),
                actions=cupertino_actions,
            )
        )        
        
        
    
    def get_idex(self,e):
        if e.control.selected:
           e.control.selected = False
        else:
            e.control.selected = True
            
        valor = e.control.cells[1].content.value
        for row in self.dm.get_tubos():
            if row[1] == valor:
                self.selected_row = row
                break
        print(self.selected_row)
        self.update()
    
    def update_tubo_click(self, e):  # Guardamos el valor original antes de la actualización
        self.dm.update_tubo(
            self.tipo.value,
            self.valor.value,
            self.longitud1.value,
            self.longitud2.value,
            self.espesor.value,
            self.original_valor
        )
        self.tipo_busqueda.value="Todos"
        self.longitud1_busqueda.value=""
        self.longitud2_busqueda.value=""
        self.espesor_busqueda.value=""
        self.show_data()  # Actualiza la tabla después de la edición
        self.dlg.open = False 
        self.page.open(False)# Cierra el diálogo
        self.update()
        self.page.update()

    def build(self):
        return self.buscador
    
    
