# ─────────────────────────────────────────────────────────────────────────────
# IMPORTACIONES DE LIBRERÍAS
# ─────────────────────────────────────────────────────────────────────────────
import tkinter as tk                   # Librería base de Python para interfaces gráficas
import customtkinter as ctk            # Versión mejorada de tkinter con diseño moderno
import sympy as sp                     # Librería matemática para trabajar con expresiones simbólicas (letras, no solo números)
import matplotlib                      # Librería para crear gráficos y figuras matemáticas

# parse_expr: convierte el texto que escribe el usuario en una expresión matemática real
# standard_transformations: reglas básicas de interpretación matemática
# implicit_multiplication_application: permite escribir "2x" en vez de "2*x"
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application

matplotlib.use('TkAgg')                # Le dice a matplotlib que dibuje dentro de una ventana Tkinter
import matplotlib.pyplot as plt        # Sublibrería de matplotlib para crear y manejar los gráficos
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # Integra el gráfico de matplotlib dentro de la ventana tkinter

# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURACIÓN VISUAL DE LA APLICACIÓN
# ─────────────────────────────────────────────────────────────────────────────
ctk.set_appearance_mode("System")      # La app adopta el modo claro u oscuro según la configuración del sistema operativo
ctk.set_default_color_theme("blue")    # Define el color principal de los botones y elementos interactivos como azul


# ─────────────────────────────────────────────────────────────────────────────
# CLASE PRINCIPAL DE LA APLICACIÓN
# ─────────────────────────────────────────────────────────────────────────────
class AppLimites(ctk.CTk):             # Define la clase que representa toda la ventana de la app, heredando de CTk

    # ── CONSTRUCTOR: se ejecuta al iniciar la aplicación ─────────────────────
    def __init__(self):
        super().__init__()             # Inicializa la ventana base de customtkinter

        # Configuración básica de la ventana
        self.title("Calculadora de Límites - Análisis Paso a Paso")  # Texto que aparece en la barra superior de la ventana
        self.geometry("1100x700")      # Tamaño inicial de la ventana: 1100 píxeles de ancho, 700 de alto

        # Configuración del sistema de cuadrícula (grid) de la ventana
        self.grid_columnconfigure(0, weight=1)   # Columna izquierda: ocupa 1 parte del espacio disponible
        self.grid_columnconfigure(1, weight=2)   # Columna derecha: ocupa 2 partes (más ancha, para la gráfica)
        self.grid_rowconfigure(0, weight=1)      # La única fila se expande para llenar toda la altura

        # ── PANEL IZQUIERDO: controles de entrada ────────────────────────────
        self.frame_izquierdo = ctk.CTkFrame(self, corner_radius=15)                          # Crea un panel con esquinas redondeadas
        self.frame_izquierdo.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")         # Lo ubica en columna 0, con márgenes de 20px y que se expanda en todas direcciones
        self.frame_izquierdo.grid_columnconfigure(0, weight=1)                               # La columna interna del panel se expande horizontalmente

        # Título del panel izquierdo
        self.lbl_titulo = ctk.CTkLabel(self.frame_izquierdo, text="Cálculo de Límites", font=ctk.CTkFont(size=22, weight="bold"))  # Etiqueta grande y en negrita
        self.lbl_titulo.grid(row=0, column=0, padx=20, pady=20)                             # Se ubica en la fila 0 del panel izquierdo

        # Etiqueta explicativa del campo de función
        self.lbl_funcion = ctk.CTkLabel(self.frame_izquierdo, text="Función f(x): Suma(+), resta(-), multiplicación(*), división(/), potencia(**)")  # Texto de instrucción para el usuario
        self.lbl_funcion.grid(row=1, column=0, padx=20, pady=5, sticky="w")                 # Alineado a la izquierda (west)

        # Campo de texto donde el usuario escribe la función matemática
        self.entry_funcion = ctk.CTkEntry(self.frame_izquierdo, placeholder_text="Ej: (x**2 - 9)/(x - 3)")  # Muestra texto de ejemplo cuando está vacío
        self.entry_funcion.grid(row=2, column=0, padx=20, pady=5, sticky="ew")              # Se expande horizontalmente (east-west)

        # Etiqueta explicativa del campo del punto
        self.lbl_punto = ctk.CTkLabel(self.frame_izquierdo, text="Valor h al que tiende x (infinito = oo):")  # Indica al usuario qué ingresar
        self.lbl_punto.grid(row=3, column=0, padx=20, pady=5, sticky="w")                   # Alineado a la izquierda

        # Campo de texto donde el usuario escribe el punto al que tiende x
        self.entry_punto = ctk.CTkEntry(self.frame_izquierdo, placeholder_text="Ej: 3")     # Muestra "Ej: 3" cuando está vacío
        self.entry_punto.grid(row=4, column=0, padx=20, pady=5, sticky="ew")                # Se expande horizontalmente

        # Botón que dispara el cálculo y la graficación al ser presionado
        self.btn_calcular = ctk.CTkButton(self.frame_izquierdo, text="Calcular y Graficar", command=self.calcular_limite)  # Al hacer clic llama a calcular_limite()
        self.btn_calcular.grid(row=5, column=0, padx=20, pady=20, sticky="ew")              # Se expande horizontalmente

        # Etiqueta del cuadro de resultados
        self.lbl_resolucion = ctk.CTkLabel(self.frame_izquierdo, text="Resolución y Resultado:", font=ctk.CTkFont(size=14, weight="bold"))  # Título en negrita
        self.lbl_resolucion.grid(row=6, column=0, padx=20, pady=5, sticky="w")              # Alineado a la izquierda

        # Cuadro de texto donde se muestra el desarrollo paso a paso del límite
        self.txt_resolucion = ctk.CTkTextbox(self.frame_izquierdo, wrap="word", height=230) # wrap="word" hace que las líneas largas corten en palabras, no en medio de una palabra
        self.txt_resolucion.grid(row=7, column=0, padx=20, pady=10, sticky="nsew")          # Se expande en todas las direcciones
        self.frame_izquierdo.grid_rowconfigure(7, weight=1)                                  # Esta fila se estira para ocupar el espacio sobrante del panel

        # ── PANEL DERECHO: área gráfica ───────────────────────────────────────
        self.frame_derecho = ctk.CTkFrame(self, corner_radius=15, fg_color="transparent")   # Panel transparente para que el gráfico se vea directamente
        self.frame_derecho.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")           # Ubicado en columna 1, se expande en todas las direcciones
        self.frame_derecho.grid_columnconfigure(0, weight=1)                                 # Su columna interna se expande
        self.frame_derecho.grid_rowconfigure(0, weight=1)                                    # Su fila interna se expande

        # Crea la figura y los ejes del gráfico con matplotlib
        self.fig, self.ax = plt.subplots(figsize=(6, 5), dpi=100)  # figsize define el tamaño en pulgadas, dpi la resolución
        self.configurar_grafico_vacio()                              # Dibuja los ejes y cuadrícula iniciales sin ninguna función

        # Integra el gráfico de matplotlib dentro del panel derecho de tkinter
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame_derecho)                 # Convierte la figura en un widget de tkinter
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew", padx=10, pady=10)  # Lo ubica en el panel derecho expandido

        # Configura qué hacer cuando el usuario cierra la ventana con la X
        self.protocol("WM_DELETE_WINDOW", self.on_closing)  # Llama a on_closing() para cerrar también matplotlib


    # ── MÉTODO: dibuja el gráfico vacío con ejes y cuadrícula ────────────────
    def configurar_grafico_vacio(self):
        self.ax.clear()                                              # Borra todo lo que haya dibujado antes en los ejes
        self.ax.axhline(0, color='black', linewidth=0.8, linestyle='--')  # Dibuja la línea horizontal del eje X (y=0)
        self.ax.axvline(0, color='black', linewidth=0.8, linestyle='--')  # Dibuja la línea vertical del eje Y (x=0)
        self.ax.set_title("Gráfica de f(x)")                        # Título que aparece arriba del gráfico
        self.ax.grid(True, linestyle=':', alpha=0.6)                 # Activa la cuadrícula con líneas punteadas semitransparentes


    # ─────────────────────────────────────────────────────────────────────────
    # ALGORITMO PRINCIPAL: calcula el límite paso a paso SIN usar sp.limit()
    # Recibe: funcion (expresión simbólica), x (variable), punto (valor límite)
    # Retorna: (resultado, explicacion) donde resultado es el valor del límite
    # ─────────────────────────────────────────────────────────────────────────
    def resolver_limite(self, funcion, x, punto):

        explicacion = ""                            # Texto acumulativo que se mostrará en pantalla con el desarrollo

        # sp.fraction() descompone la función en numerador y denominador
        # Ejemplo: (x²-4)/(x-2) → num = x²-4, den = x-2
        num, den = sp.fraction(funcion)

        # ── PASO 1: Sustitución directa ──────────────────────────────────────
        explicacion += "🔹 PASO 1: Sustitución Directa\n"

        # Verificamos si el punto es infinito (oo o -oo), porque no se puede sustituir directamente
        es_infinito = (punto == sp.oo or punto == -sp.oo)  # True si el punto es ±infinito, False si es un número normal

        if es_infinito:
            # Si x tiende a infinito, omitimos la sustitución directa
            val_num = None                                          # No hay valor numérico para el numerador
            val_den = None                                          # No hay valor numérico para el denominador
            explicacion += "  • x tiende a infinito → sustitución directa no aplica.\n\n"  # Informamos al usuario
        else:
            # Si el punto es un número, sustituimos x por ese valor en num y den
            val_num = num.subs(x, punto)   # Reemplaza x por el punto en el numerador y evalúa el resultado
            val_den = den.subs(x, punto)   # Reemplaza x por el punto en el denominador y evalúa el resultado
            explicacion += f"  • Numerador en x={punto}: {val_num}\n"    # Muestra el resultado del numerador
            explicacion += f"  • Denominador en x={punto}: {val_den}\n\n"  # Muestra el resultado del denominador

        # ─────────────────────────────────────────────────────────────────────
        # A partir de aquí clasificamos el caso y aplicamos la técnica correcta
        # ─────────────────────────────────────────────────────────────────────

        # ── CASO A: Sustitución directa exitosa (denominador ≠ 0) ────────────
        if not es_infinito and val_den != 0:
            # Si el denominador no es cero, el límite es simplemente num/den
            explicacion += "✅ No hay indeterminación → evaluación directa.\n\n"
            resultado = val_num / val_den  # División aritmética directa: nuestra lógica, no SymPy
            return resultado, explicacion  # Retornamos el resultado y terminamos

        # ── CASO B: Indeterminación 0/0 → factorizar y cancelar ──────────────
        if not es_infinito and val_num == 0 and val_den == 0:
            # Cuando ambos son 0, hay un factor común que se puede cancelar
            explicacion += "⚠️ Indeterminación 0/0 detectada.\n\n"
            explicacion += "🔹 PASO 2: Factorización y cancelación algebraica\n"

            # sp.factor() factoriza el numerador y denominador por separado (solo para mostrar al usuario)
            num_fact = sp.factor(num)  # Ejemplo: x²-4 → (x-2)(x+2)
            den_fact = sp.factor(den)  # Ejemplo: x-2 → (x-2)
            explicacion += f"  • Numerador factorizado:   {num_fact}\n"    # Mostramos la factorización del numerador
            explicacion += f"  • Denominador factorizado: {den_fact}\n\n"  # Mostramos la factorización del denominador

            # sp.cancel() cancela los factores comunes entre numerador y denominador
            # Ejemplo: (x-2)(x+2)/(x-2) → (x+2)
            funcion_cancelada = sp.cancel(funcion)
            explicacion += "🔹 PASO 3: Expresión simplificada tras cancelar\n"
            explicacion += f"  • f(x) simplificada = {funcion_cancelada}\n\n"  # Muestra la función sin el factor común

            # Volvemos a extraer num y den de la función ya simplificada
            num_c, den_c = sp.fraction(funcion_cancelada)   # Descompone la función cancelada en num y den nuevamente
            val_num_c = num_c.subs(x, punto)                # Sustituye x por el punto en el numerador simplificado
            val_den_c = den_c.subs(x, punto)                # Sustituye x por el punto en el denominador simplificado
            explicacion += f"  • Sustituyendo x={punto} en la expresión simplificada:\n"
            explicacion += f"    Numerador: {val_num_c}  |  Denominador: {val_den_c}\n\n"

            if val_den_c != 0:
                resultado = val_num_c / val_den_c  # Si el denominador ya no es 0, dividimos directamente
            else:
                # Si sigue siendo 0/0 después de cancelar, no podemos resolverlo con esta técnica
                resultado = sp.nan                 # nan = "Not a Number", indica que no se pudo determinar
                explicacion += "  ⚠️ No se pudo resolver por factorización simple.\n\n"
            return resultado, explicacion  # Retornamos el resultado y terminamos

        # ── CASO C: k/0 → analizar límites laterales con epsilon ─────────────
        if not es_infinito and val_num != 0 and val_den == 0:
            # El numerador tiene valor (k ≠ 0) pero el denominador es 0 → posible asíntota vertical
            explicacion += "⚠️ División por cero (k/0) → posible asíntota vertical.\n\n"
            explicacion += "🔹 PASO 2: Análisis de límites laterales\n"
            explicacion += f"  • El denominador se anula en x = {punto}.\n"
            explicacion += f"  • Evaluamos el signo de la función cerca del punto.\n\n"

            # Epsilon es un número muy pequeño (0.001) para acercarnos al punto sin tocarlo
            # Usamos sp.Rational para que sea una fracción exacta y no un decimal con error de redondeo
            epsilon = sp.Rational(1, 1000)  # Equivale a 0.001, pero representado exactamente como 1/1000

            # Evaluamos la función en punto+epsilon (acercándonos por la derecha)
            val_derecha  = funcion.subs(x, punto + epsilon).evalf()  # .evalf() convierte a número decimal
            # Evaluamos la función en punto-epsilon (acercándonos por la izquierda)
            val_izquierda = funcion.subs(x, punto - epsilon).evalf()

            explicacion += f"  • f({punto} + ε) ≈ {round(float(val_derecha),  4)}  → lado derecho\n"   # Muestra el valor por la derecha
            explicacion += f"  • f({punto} - ε) ≈ {round(float(val_izquierda), 4)}  → lado izquierdo\n\n"  # Muestra el valor por la izquierda

            # Determinamos hacia dónde tiende la función por la derecha según su signo
            if val_derecha > 0:        # Si el valor es positivo, la función sube hacia +infinito
                lim_der  = sp.oo       # Límite por la derecha es +∞
                signo_der = "+∞"
            else:                      # Si el valor es negativo, la función baja hacia -infinito
                lim_der  = -sp.oo      # Límite por la derecha es -∞
                signo_der = "-∞"

            # Mismo análisis para el lado izquierdo
            if val_izquierda > 0:      # Valor positivo → tiende a +∞
                lim_izq  = sp.oo
                signo_izq = "+∞"
            else:                      # Valor negativo → tiende a -∞
                lim_izq  = -sp.oo
                signo_izq = "-∞"

            explicacion += f"  • Límite por la derecha  (x → {punto}⁺) = {signo_der}\n"   # Muestra resultado derecho
            explicacion += f"  • Límite por la izquierda (x → {punto}⁻) = {signo_izq}\n\n"  # Muestra resultado izquierdo

            # Comparamos ambos laterales para decidir si el límite existe
            if lim_der == lim_izq:
                # Si los dos lados van hacia el mismo infinito, el límite existe
                explicacion += "  ✅ Ambos laterales coinciden.\n\n"
                resultado = lim_der    # El límite es ese infinito común
            else:
                # Si van a infinitos distintos (+∞ ≠ -∞), el límite no existe
                explicacion += "  ❌ Los laterales NO coinciden → el límite NO EXISTE.\n\n"
                resultado = "NO_EXISTE"  # Usamos el string "NO_EXISTE" como señal especial
            return resultado, explicacion  # Retornamos el resultado y terminamos

        # ── CASO D: x → ±∞ → comparación de grados del polinomio ────────────
        if es_infinito:
            explicacion += "🔹 PASO 2: Análisis al infinito (comparación de grados)\n"

            try:
                # sp.degree() obtiene el grado del polinomio respecto a x
                # Ejemplo: x³+2x → grado 3
                grado_num = sp.degree(sp.expand(num), x)   # Grado del numerador
                grado_den = sp.degree(sp.expand(den), x)   # Grado del denominador

                # sp.LC() obtiene el coeficiente líder (el número que acompaña al término de mayor grado)
                # Ejemplo: 3x²+x → coeficiente líder = 3
                coef_num = sp.LC(sp.expand(num), x)        # Coeficiente líder del numerador
                coef_den = sp.LC(sp.expand(den), x)        # Coeficiente líder del denominador

                explicacion += f"  • Grado del numerador:   {grado_num}  (coef. líder: {coef_num})\n"   # Muestra grado y coeficiente del numerador
                explicacion += f"  • Grado del denominador: {grado_den}  (coef. líder: {coef_den})\n\n" # Muestra grado y coeficiente del denominador

                # Regla 1: si el numerador tiene menor grado, la fracción tiende a 0
                if grado_num < grado_den:
                    explicacion += "  • Grado num < Grado den → el límite es 0.\n\n"
                    resultado = sp.Integer(0)              # El límite es exactamente 0

                # Regla 2: si tienen el mismo grado, el límite es el cociente de sus coeficientes líderes
                elif grado_num == grado_den:
                    resultado = coef_num / coef_den        # Ejemplo: (3x²+1)/(6x²+2) → 3/6 = 1/2
                    explicacion += f"  • Grado num = Grado den → límite = {coef_num}/{coef_den} = {resultado}.\n\n"

                # Regla 3: si el numerador tiene mayor grado, la función diverge al infinito
                else:
                    explicacion += "  • Grado num > Grado den → diverge al infinito.\n"
                    # Evaluamos con un número muy grande para determinar el signo del infinito
                    val_grande = funcion.subs(x, sp.Integer(10**6)).evalf()  # f(1.000.000) nos dice el signo

                    if punto == sp.oo:
                        # Si x→+∞, usamos el valor positivo grande
                        resultado = sp.oo if val_grande > 0 else -sp.oo    # Positivo → +∞, negativo → -∞
                    else:
                        # Si x→-∞, usamos un valor negativo muy grande
                        val_grande_neg = funcion.subs(x, sp.Integer(-10**6)).evalf()  # f(-1.000.000)
                        resultado = sp.oo if val_grande_neg > 0 else -sp.oo           # Determinamos el signo

                    explicacion += f"  • Signo al alejarse: {'+ ∞' if resultado == sp.oo else '- ∞'}\n\n"

            except Exception:
                # Si la función no es un polinomio simple (ej: raíces, exponenciales), fallback numérico
                explicacion += "  • Función no polinómica → evaluación por aproximación.\n"
                val_grande = funcion.subs(x, sp.Integer(10**9)).evalf()    # Evaluamos en un número muy grande
                resultado = sp.oo if val_grande > 0 else -sp.oo            # El signo determina hacia dónde va
                explicacion += f"  • f(10⁹) ≈ {val_grande}  → resultado: {resultado}\n\n"

            return resultado, explicacion  # Retornamos el resultado del caso infinito

        # ── FALLBACK: caso no contemplado ─────────────────────────────────────
        return sp.nan, explicacion + "  ⚠️ Caso no clasificado.\n\n"  # Nunca debería llegar aquí en casos normales


    # ── MÉTODO: se ejecuta al presionar el botón "Calcular y Graficar" ────────
    def calcular_limite(self):
        self.txt_resolucion.delete("1.0", tk.END)   # Borra el texto anterior del cuadro de resultados ("1.0" = desde línea 1 columna 0)
        self.configurar_grafico_vacio()              # Limpia el gráfico anterior para dibujar uno nuevo

        # Leemos y limpiamos los textos ingresados por el usuario
        str_funcion = self.entry_funcion.get().strip().replace(" ", "")  # .get() lee el campo, .strip() quita espacios extremos, .replace() elimina espacios internos
        str_punto   = self.entry_punto.get().strip().replace(" ", "")    # Lo mismo para el campo del punto

        # Validamos que ambos campos tengan contenido antes de calcular
        if not str_funcion or not str_punto:
            self.txt_resolucion.insert(tk.END, "⚠️ Error: Por favor, rellena ambos campos.")  # Muestra mensaje de error
            return  # Salimos del método sin calcular nada

        x = sp.Symbol('x')  # Definimos 'x' como símbolo matemático para que SymPy pueda operar con él como variable

        try:
            # Configuramos las transformaciones para interpretar la entrada del usuario
            transformaciones = standard_transformations + (implicit_multiplication_application,)  # Añadimos multiplicación implícita (2x = 2*x)

            # Convertimos el texto de la función en una expresión simbólica de SymPy
            funcion = parse_expr(str_funcion, transformations=transformaciones)  # Ejemplo: "(x**2-4)/(x-2)" → objeto matemático

            # Convertimos el texto del punto en un valor simbólico de SymPy
            punto = sp.sympify(str_punto)  # Ejemplo: "3" → 3, "oo" → ∞, "-2" → -2

            # Encabezado informativo que aparecerá en el cuadro de resultados
            encabezado = f"📌 Análisis de f(x) = {funcion}\n   Evaluando cuando x ➔ {punto}\n\n"

            # Llamamos a nuestro algoritmo propio que resuelve el límite paso a paso
            resultado, pasos = self.resolver_limite(funcion, x, punto)  # Retorna el valor y la explicación textual

            # Unimos el encabezado con los pasos del desarrollo
            explicacion = encabezado + pasos

            # Formateamos el resultado final según su tipo
            if resultado == "NO_EXISTE":
                explicacion += "🎯 RESULTADO FINAL: El límite NO EXISTE\n"   # Caso laterales distintos
            elif resultado == sp.oo:
                explicacion += "🎯 RESULTADO FINAL: +∞\n"                    # Caso diverge hacia más infinito
            elif resultado == -sp.oo:
                explicacion += "🎯 RESULTADO FINAL: -∞\n"                    # Caso diverge hacia menos infinito
            elif resultado == sp.nan:
                explicacion += "🎯 RESULTADO FINAL: No determinado\n"        # Caso no pudo resolverse
            else:
                try:
                    val_float = float(resultado.evalf())    # Convertimos el resultado simbólico a decimal
                    if resultado.is_Integer:
                        explicacion += f"🎯 RESULTADO FINAL: {resultado}\n"  # Si es entero, mostramos solo el entero
                    else:
                        explicacion += f"🎯 RESULTADO FINAL: {resultado}  (≈ {round(val_float, 4)})\n"  # Si es fracción, mostramos fracción y decimal
                except Exception:
                    explicacion += f"🎯 RESULTADO FINAL: {resultado}\n"      # Fallback si no se puede convertir

            # Mostramos todo el desarrollo en el cuadro de texto
            self.txt_resolucion.insert(tk.END, explicacion)

            # ── GRAFICAR LA FUNCIÓN ───────────────────────────────────────────
            es_infinito = (punto == sp.oo or punto == -sp.oo)  # Verificamos de nuevo si el punto es infinito

            if not es_infinito:
                # Si el punto es un número, graficamos 5 unidades a cada lado del punto
                inicio = float(punto) - 5   # Valor inicial del eje X
                fin    = float(punto) + 5   # Valor final del eje X
            else:
                # Si el punto es infinito, usamos un rango fijo de -10 a 10
                inicio, fin = -10, 10

            pasos_grafica = 300                              # Número de puntos a calcular: más puntos = curva más suave
            paso_tamano   = (fin - inicio) / pasos_grafica  # Distancia entre cada punto del eje X

            x_vals = []  # Lista que almacenará los valores válidos del eje X
            y_vals = []  # Lista que almacenará los valores válidos del eje Y

            # Recorremos todos los puntos del rango con un ciclo for
            for i in range(pasos_grafica + 1):
                val_x = inicio + (i * paso_tamano)  # Calculamos el valor de x para este punto (avanzamos de a paso_tamano)
                try:
                    res_y = funcion.subs(x, val_x).evalf()           # Evaluamos f(val_x) numéricamente
                    if res_y.is_real and not res_y.is_infinite:       # Solo graficamos si el resultado es real y finito (descartamos asíntotas)
                        x_vals.append(float(val_x))                  # Agregamos x a la lista si es válido
                        y_vals.append(float(res_y))                  # Agregamos y a la lista si es válido
                except Exception:
                    continue  # Si hay error en algún punto (ej: división por 0 exacta), lo saltamos y seguimos

            # Si obtuvimos puntos válidos, graficamos la curva
            if x_vals:
                self.ax.plot(x_vals, y_vals, color="#1f77b4")  # Dibuja la curva con color azul
                self.canvas.draw()                              # Actualiza el canvas para mostrar la nueva gráfica

        except Exception as e:
            # Si ocurre cualquier error inesperado, mostramos un mensaje descriptivo
            self.txt_resolucion.insert(
                tk.END,
                f"❌ Error en el procesamiento:\n{str(e)}\n\nRevisa que la función esté bien escrita."
            )

    # ── MÉTODO: cierre correcto de la aplicación ─────────────────────────────
    def on_closing(self):
        plt.close('all')   # Cierra todas las figuras de matplotlib para liberar memoria
        self.destroy()     # Destruye la ventana de tkinter y termina la aplicación


# ─────────────────────────────────────────────────────────────────────────────
# PUNTO DE ENTRADA DEL PROGRAMA
# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = AppLimites()   # Crea una instancia de la aplicación (construye la ventana)
    app.mainloop()       # Inicia el bucle principal: mantiene la ventana abierta y escucha eventos del usuario
