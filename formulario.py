import flet as ft
from data_manager import DataManager
from Inicio import inicio




class formulario(ft.UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.inicio = inicio(page)
        self.data_manager = DataManager()
        self.longitud1 = ft.TextField(label="Introduce la primera longitud",shift_enter=True,on_submit=lambda _: self.longitud2.focus())
        self.longitud2 = ft.TextField(label="Introduce la segunda longitud",shift_enter=True,on_submit=lambda _: self.espesor.focus())
        self.espesor = ft.TextField(label="Introduce el espesor",shift_enter=True,on_submit=lambda _: self.valor.focus())
        self.valor = ft.TextField(label="Introduce el valor",shift_enter=True,on_submit=lambda _: self.tipo.focus())
        self.tipo = ft.Dropdown(
            options=[
                ft.dropdown.Option("Redondo"),
                ft.dropdown.Option("Cuadrado"),
                ft.dropdown.Option("Rectangular"),
            ],
            label="Selecciona una opcion",
            border_color=ft.colors.GREY_400,
        )
        
        self.buscador = ft.Container(
            border_radius=10,
            expand=True,
            content = ft.Column(
                controls=[
                    ft.Text("Crear Tubo", size=20),
                    self.longitud1,
                    self.longitud2,
                    self.espesor,
                    self.valor,
                    self.tipo,
                    
                    ft.ElevatedButton(
                        content=ft.Text("Crear"),
                        width=120,
                        height=40,
                        bgcolor=ft.colors.GREEN_700,
                        color=ft.colors.WHITE,
                        on_click=self.crear_tubo
                    )
                ]
            )
        )
    
    def crear_tubo(self, e):
        
        longitud1 = self.longitud1.value
        longitud2 = self.longitud2.value
        espesor = self.espesor.value
        valor = self.valor.value
        tipo = self.tipo.value
        
        if not longitud1 or not longitud2 or not tipo or not espesor:
            
            return ft.SnackBar(
                bgcolor=ft.colors.RED,
                content=ft.Text("error"))
        
        try:
            tipo = str(tipo)
            longitud1 = str(longitud1)
            longitud2 = str(longitud2)
            valor = int(valor)
            espesor = str(espesor)
        except ValueError:
            
            return ft.SnackBar(
                duration=ft.snack_bar.SnackBarDismissAnimationDuration.FAST,
                bgcolor=ft.colors.RED,
                content=ft.Text("Hello, world!"))
        
        # Aquí puedes agregar lógica para calcular el valor y el espesor si es necesario
          # Placeholder
          # Placeholder
        
        self.data_manager.add_tubo(tipo, valor, longitud1, longitud2, espesor)
        
        # Limpiar los campos después de crear el tubo
        self.longitud1.value = ""
        self.longitud2.value = ""
        self.espesor.value = ""
        self.valor.value = ""
        self.tipo.value = None
        self.inicio.update()
        self.update()
    
   
    
    def build(self):
        return self.buscador