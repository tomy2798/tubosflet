import flet as ft
from Inicio import inicio
from formulario import formulario
from espesores import espesores




class UI(ft.UserControl):
    def __init__(self, page: ft.Page):
        self.page = page
        super().__init__(expand=True)
        self.inicio = inicio(page)
        self.formulario = formulario(page)
        self.espesores = espesores(page)
        self.inicio.visible = True 
        self.formulario.visible = False
        self.espesores.visible = False
        def show_inicio(e):
            self.inicio.show_data()
            self.inicio.visible = True
            self.formulario.visible = False
            self.espesores.visible = False
            self.update()
        
        
        def show_formulario(e):
            self.inicio.visible = False
            self.formulario.visible = True
            self.espesores.visible = False
            self.update()
        
        def show_espesores(e):
            self.inicio.visible = False
            self.formulario.visible = False
            self.espesores.visible = True
            self.update()

        
        self.navegacion = ft.Container(
            col=2,
            border_radius=10,
            bgcolor=ft.colors.GREY_300,
            content=ft.Column(
                expand=True,
                controls=[ft.Container(
                    padding=10,
                    height=160,
                    content= ft.Column(
                        controls=[
                            ft.Container(
                                padding=5,
                                expand=True,
                                bgcolor=ft.colors.GREY_200,
                                alignment=ft.alignment.center,
                                border_radius=10,
                                ink=True,
                                shadow=ft.BoxShadow(
                                        spread_radius=1,
                                        blur_radius=2,
                                        color=ft.colors.GREY_400
                                    ),
                                on_click=lambda e: show_inicio(e),
                                content=ft.Row(
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    controls=[
                                        
                                        ft.Icon(ft.icons.HOME, color=ft.colors.BLACK,expand=1),
                                        ft.Text("Inicio", color=ft.colors.BLACK,expand=2),
                                    ]
                                ),
                            ),
                            ft.Container(
                                padding=5,
                                expand=True,
                                bgcolor=ft.colors.GREY_200,
                                alignment=ft.alignment.center,
                                border_radius=10,
                                ink=True,
                                shadow=ft.BoxShadow(
                                        spread_radius=1,
                                        blur_radius=2,
                                        color=ft.colors.GREY_400
                                    ),
                                on_click=lambda e: show_espesores(e),
                                content=ft.Row(
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    controls=[
                                        
                                        ft.Icon(ft.icons.SEARCH, color=ft.colors.BLACK,expand=1),
                                        ft.Text("Espesores", color=ft.colors.BLACK,expand=2),
                                    ]
                                ),
                            ),
                            ft.Container(
                                expand=True,
                                padding=5,
                                alignment=ft.alignment.center,
                                border_radius=10,
                                bgcolor=ft.colors.GREY_200,
                                ink=True,
                                shadow=ft.BoxShadow(
                                        spread_radius=1,
                                        blur_radius=2,
                                        color=ft.colors.GREY_400
                                    ),
                                on_click=lambda e: show_formulario(e),
                                content=ft.Row(
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    controls=[
                                        
                                        ft.Icon(ft.icons.ADD, color=ft.colors.BLACK,expand=1),
                                        ft.Text("Crear Tubo", color=ft.colors.BLACK,expand=2),
                                    ]
                                ),
                            ),
                            
                        ]
                    )
                    
                )
             ]
         )
     )

        self.contenido = ft.Container(
            expand=True,
            col=10,
            content=ft.ResponsiveRow(
                controls=[self.inicio,
                          self.formulario,
                          self.espesores]
            )
            
        )
        
        
        self.principal = ft.ResponsiveRow(
            controls=[self.navegacion,
                      self.contenido]
        )
        
    
        
    def build(self):
        return self.principal

    
def main(page: ft.Page):
    page.window_min_width = 500
    page.window_min_height = 800
    page.add(UI(page))
    
ft.app(main, view=ft.AppView.WEB_BROWSER)