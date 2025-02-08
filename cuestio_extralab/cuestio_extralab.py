import reflex as rx
from backend.principal import formulario
import random
import asyncio  # Para manejar demoras en la lógica del backend

class FormState(rx.State):
    """Estado para manejar los datos del formulario."""
    form_data: dict = {}
    resultado_backend: list = []
    show_alert: bool = False
    show_loading: bool = False

    @rx.event
    async def handle_submit(self, form_data: dict):
        """Maneja el envío del formulario."""
        # Mostrar el indicador de carga
        self.show_loading = True
        self.show_alert = False

        # Simular procesamiento en el backend
        await asyncio.sleep(2)  # Simulación del procesamiento, reemplaza con tu lógica real
        self.form_data = form_data
        self.resultado_backend = formulario(form_data)

        # Ocultar el indicador de carga y mostrar el cuadro emergente
        self.show_loading = False
        self.show_alert = True

        # Esperar unos segundos antes de ocultar el alert
        await asyncio.sleep(5)
        self.hide_alert()

    @rx.event
    def hide_alert(self):
        """Oculta el alert después de un tiempo."""
        self.show_alert = False

def generar_formas_animadas(cantidad: int):
    """Genera una lista de formas animadas para el fondo."""
    formas = []
    for _ in range(cantidad):
        top_pos = random.randint(0, 100)
        left_pos = random.randint(0, 100)
        size = random.randint(30, 80)
        duracion = random.uniform(6, 12)

        forma = rx.box(
            style={
                "position": "absolute",
                "width": f"{size}px",
                "height": f"{size}px",
                "backgroundColor": "rgba(255, 255, 255, 0.15)",
                "borderRadius": "50%",
                "top": f"{top_pos}%",
                "left": f"{left_pos}%",
                "animation": f"moverAnim {duracion}s ease-in-out infinite",
                "animationDelay": f"{random.uniform(0, 5)}s",
                "@keyframes moverAnim": {
                    "0%": {"transform": "translate(0, 0)"},
                    "50%": {"transform": "translate(50px, -50px)"},
                    "100%": {"transform": "translate(0, 0)"},
                },
            }
        )
        formas.append(forma)
    return formas

def index() -> rx.Component:
    return rx.center(
        *generar_formas_animadas(30),
        rx.box(
            rx.vstack(
                # Rueda de carga visible mientras se procesa el formulario
                rx.cond(
                    FormState.show_loading,
                    rx.spinner(size="1", color="green"),  # Asegúrate de usar un tamaño válido como "sm"
                ),
                rx.image(
                    src="/favicon.ico",
                    style={
                        "width": "120px",
                        "height": "120px",
                        "marginBottom": "0.1rem",
                        "alignSelf": "center",
                        "filter": "drop-shadow(0 2px 6px rgba(0, 0, 0, 0.3))",
                        "animation": "pulseShadow 3s ease-in-out infinite",
                        "transition": "transform 0.3s ease",
                        "_hover": {"transform": "scale(1.1)"},
                        "@keyframes pulseShadow": {
                            "0%, 100%": {"filter": "drop-shadow(0 2px 6px rgba(0, 0, 0, 0.3))"},
                            "50%": {"filter": "drop-shadow(0 4px 12px rgba(0, 0, 0, 0.5))"},
                        },
                    },
                ),
                rx.heading(
                    "Batería de riesgo psicosocial",
                    size="1",
                    text_align="center",
                    style={
                        "marginTop": "0rem",
                        "marginBottom": "0.6rem",
                        "fontWeight": "extrabold",
                        "fontSize": "2.8rem",
                        "lineHeight": "1.2",
                        "padding": "0.5rem",
                        "textAlign": "center",
                        "backgroundImage": "linear-gradient(90deg, #27ae60, #1abc9c, #2ecc71)",
                        "backgroundSize": "150% auto",
                        "backgroundClip": "text",
                        "textFillColor": "transparent",
                        "animation": "gradientMove 6s ease infinite",
                        "textShadow": "0px 2px 4px rgba(0, 0, 0, 0.2)",
                        "@keyframes gradientMove": {
                            "0%": {"backgroundPosition": "0% 0%"},
                            "100%": {"backgroundPosition": "100% 0%"},
                        },
                    },
                ),
                rx.form(
                    rx.vstack(
                        rx.input(
                            placeholder="Cédula",
                            name="cedula",
                            color_scheme="green",
                            style={
                                "textAlign": "center",
                                "textTransform": "capitalize",
                                "width": "280px",
                                "height": "40px",
                                "borderRadius": "25px",
                                "fontSize": "1.1rem",
                                "_focus": {
                                    "outline": "none",
                                    "border": "2px green",
                                    "boxShadow": "none",
                                },
                            },
                        ),
                        rx.input(
                            placeholder="Nombre de empleado",
                            name="nombre_empleado",
                            color_scheme="green",
                            style={
                                "textAlign": "center",
                                "textTransform": "capitalize",
                                "width": "280px",
                                "height": "40px",
                                "borderRadius": "25px",
                                "fontSize": "1.1rem",
                                "_focus": {
                                    "outline": "none",
                                    "border": "2px solid green",
                                    "boxShadow": "none",
                                },
                            },
                        ),
                        rx.select(
                            items=["A", "B"],
                            placeholder="Seleccione el tipo de empleado",
                            name="tipo_empleado",
                            radius="full",
                            color_scheme="green",
                            size="3",
                            style={
                                "textAlign": "center",
                                "width": "300px",
                                "height": "50px",
                                "borderRadius": "15px",
                                "fontSize": "1.1rem",
                                "padding": "0.5rem",
                                "appearance": "none",
                                "-webkit-appearance": "none",
                                "-moz-appearance": "none",
                                "boxShadow": "0 4px 10px rgba(0,128,0,0.3)",
                                "_hover": {
                                    "boxShadow": "0 4px 10px rgba(0,128,0,0.5)",
                                    "cursor": "pointer",
                                },
                            },
                        ),
                        rx.select(
                            items=["RRHH", "Operaciones", "Mantenimiento", "Financiera", "SGI", "Gerencia"],
                            placeholder="Seleccione el área",
                            name="area",
                            radius="full",
                            color_scheme="green",
                            size="3",
                            style={
                                "textAlign": "center",
                                "width": "300px",
                                "height": "50px",
                                "borderRadius": "15px",
                                "fontSize": "1.1rem",
                                "padding": "0.5rem",
                                "_hover": {
                                    "boxShadow": "0 4px 10px rgba(0,128,0,0.5)",
                                    "cursor": "pointer",
                                },
                            },
                        ),
                        rx.button(
                            "Procesar empleado",
                            type="submit",
                            style={
                                "width": "140px",
                                "height": "40px",
                                "borderRadius": "1em",
                                "fontSize": "0.8rem",
                                "padding": "0.5rem",
                                "marginTop": "0.4rem",
                                "backgroundImage": "linear-gradient(144deg, #4CAF50, #388E3C 50%, #2E7D32)",
                                "boxShadow": "rgba(34, 139, 34, 0.8) 0 15px 30px -10px",
                                "color": "white",
                                "opacity": "1",
                                "transition": "transform 0.3s ease",
                                "_hover": {"transform": "scale(1.1)"},
                            },
                        ),
                        align_items="center",
                        spacing="4",
                    ),
                    on_submit=FormState.handle_submit,
                    reset_on_submit=True,
                ),
                rx.cond(
                    FormState.show_alert,
                    rx.box(
                        rx.text("Resultados", fontWeight="bold", fontSize="1.2rem"),
                        rx.text(FormState.resultado_backend[0], size="4"),
                        rx.text(FormState.resultado_backend[1], size="4"),
                        style={
                            "position": "fixed",
                            "top": "50%",
                            "left": "50%",
                            "transform": "translate(-50%, -50%)",
                            "background": "#f0f4f8",
                            "padding": "1rem",
                            "borderRadius": "12px",
                            "boxShadow": "0 5px 15px rgba(0,0,0,0.3)",
                            "zIndex": "1000",
                            "opacity": "1",
                            "transition": "opacity 1s ease-in-out",
                        },
                    ),
                ),
            ),
            style={
                "background": "white",
                "borderRadius": "30px",
                "boxShadow": "0 5px 15px rgba(0,0,0,0.1)",
                "padding": "1rem",
                "width": "700px",
                "height": "570px",
                "overflow": "auto",
                "display": "flex",
                "flexDirection": "column",
                "alignItems": "center",
                "textAlign": "center",
                "zIndex": "10",
            },
        ),
        style={
            "background": "linear-gradient(to top, #0d4610, #6fbf73, #a4d17d)",
            "height": "100vh",
            "width": "100vw",
            "display": "flex",
            "flexDirection": "column",
            "justifyContent": "center",
            "alignItems": "center",
            "position": "relative",
            "overflow": "hidden",
        },
    )

app = rx.App()
app.add_page(
    index,
    route="/",
    title="Batería de riesgo psicosocial",
)
