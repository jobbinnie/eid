import tkinter as tk
import customtkinter as ctk
import sympy as sp
import matplotlib

from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class AppLimites(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Calculadora de Límites - Análisis Paso a Paso")
        self.geometry("1100x700")

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)

        self.frame_izquierdo = ctk.CTkFrame(self, corner_radius=15)
        self.frame_izquierdo.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.frame_izquierdo.grid_columnconfigure(0, weight=1)

        self.lbl_titulo = ctk.CTkLabel(self.frame_izquierdo, text="Cálculo de Límites", font=ctk.CTkFont(size=22, weight="bold"))
        self.lbl_titulo.grid(row=0, column=0, padx=20, pady=20)

        self.lbl_funcion = ctk.CTkLabel(self.frame_izquierdo, text="Función f(x): Suma(+), resta(-), multiplicación(*), división(/), potencia(**)")
        self.lbl_funcion.grid(row=1, column=0, padx=20, pady=5, sticky="w")

        self.entry_funcion = ctk.CTkEntry(self.frame_izquierdo, placeholder_text="Ej: (x**2 - 9)/(x - 3)")
        self.entry_funcion.grid(row=2, column=0, padx=20, pady=5, sticky="ew")

        self.lbl_punto = ctk.CTkLabel(self.frame_izquierdo, text="Valor h al que tiende x (infinito = oo):")
        self.lbl_punto.grid(row=3, column=0, padx=20, pady=5, sticky="w")

        self.entry_punto = ctk.CTkEntry(self.frame_izquierdo, placeholder_text="Ej: 3")
        self.entry_punto.grid(row=4, column=0, padx=20, pady=5, sticky="ew")

        self.btn_calcular = ctk.CTkButton(self.frame_izquierdo, text="Calcular y Graficar", command=self.calcular_limite)
        self.btn_calcular.grid(row=5, column=0, padx=20, pady=20, sticky="ew")

        self.lbl_resolucion = ctk.CTkLabel(self.frame_izquierdo, text="Resolución y Resultado:", font=ctk.CTkFont(size=14, weight="bold"))
        self.lbl_resolucion.grid(row=6, column=0, padx=20, pady=5, sticky="w")

        self.txt_resolucion = ctk.CTkTextbox(self.frame_izquierdo, wrap="word", height=230)
        self.txt_resolucion.grid(row=7, column=0, padx=20, pady=10, sticky="nsew")
        self.frame_izquierdo.grid_rowconfigure(7, weight=1)

        self.frame_derecho = ctk.CTkFrame(self, corner_radius=15, fg_color="transparent")
        self.frame_derecho.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.frame_derecho.grid_columnconfigure(0, weight=1)
        self.frame_derecho.grid_rowconfigure(0, weight=1)

        self.fig, self.ax = plt.subplots(figsize=(6, 5), dpi=100)
        self.configurar_grafico_vacio()

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame_derecho)
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def configurar_grafico_vacio(self):
        self.ax.clear()
        self.ax.axhline(0, color='black', linewidth=0.8, linestyle='--')
        self.ax.axvline(0, color='black', linewidth=0.8, linestyle='--')
        self.ax.set_title("Gráfica de f(x)")
        self.ax.grid(True, linestyle=':', alpha=0.6)

    def resolver_limite(self, funcion, x, punto):

        explicacion = ""

        num, den = sp.fraction(funcion)

        explicacion += "🔹 PASO 1: Sustitución Directa\n"

        es_infinito = (punto == sp.oo or punto == -sp.oo)

        if es_infinito:
            val_num = None
            val_den = None
            explicacion += "  • x tiende a infinito → sustitución directa no aplica.\n\n"
        else:
            val_num = num.subs(x, punto)
            val_den = den.subs(x, punto)
            explicacion += f"  • Numerador en x={punto}: {val_num}\n"
            explicacion += f"  • Denominador en x={punto}: {val_den}\n\n"

        if not es_infinito and val_den != 0:
            explicacion += "✅ No hay indeterminación → evaluación directa.\n\n"
            resultado = val_num / val_den
            return resultado, explicacion

        if not es_infinito and val_num == 0 and val_den == 0:
            explicacion += "⚠️ Indeterminación 0/0 detectada.\n\n"

            explicacion += "🔹 PASO 2: Verificando límites trigonométricos fundamentales\n"

            resultado_trig = None

            if punto == 0:
                funcion_str = str(funcion)

                tiene_trig = any(t in funcion_str for t in ["sin", "cos", "tan"])

                if tiene_trig:
                    if num.func == sp.sin and den.func == sp.sin:
                        arg_num = num.args[0]
                        arg_den = den.args[0]
                        coef_num_x = arg_num.coeff(x)
                        coef_den_x = arg_den.coeff(x)

                        if coef_num_x != 0 and coef_den_x != 0:
                            resultado_trig = coef_num_x / coef_den_x
                            explicacion += f"  • Patrón detectado: sin({arg_num}) / sin({arg_den})\n"
                            explicacion += f"  • Usando límite fundamental: lim sin(ax)/sin(bx) = a/b\n"
                            explicacion += f"  • a = {coef_num_x}, b = {coef_den_x}\n"
                            explicacion += f"  • Resultado = {coef_num_x}/{coef_den_x} = {resultado_trig}\n\n"

                    elif num.func == sp.sin:
                        arg_sin = num.args[0]
                        coef_sin = arg_sin.coeff(x)
                        coef_den_x = den.coeff(x)

                        if coef_sin != 0 and coef_den_x != 0:
                            resultado_trig = coef_sin / coef_den_x
                            explicacion += f"  • Patrón detectado: sin({arg_sin}) / ({den})\n"
                            explicacion += f"  • Usando límite fundamental: lim sin(ax)/bx = a/b\n"
                            explicacion += f"  • a = {coef_sin}, b = {coef_den_x}\n"
                            explicacion += f"  • Resultado = {coef_sin}/{coef_den_x} = {resultado_trig}\n\n"

                    elif num.is_Add and any(a.has(sp.cos) for a in num.args):
                        coef_den_x = den.coeff(x)
                        if coef_den_x != 0:
                            resultado_trig = sp.Integer(0)
                            explicacion += f"  • Patrón detectado: (1 - cos(...)) / ({den})\n"
                            explicacion += f"  • Usando límite fundamental: lim (1-cos(ax))/bx = 0\n"
                            explicacion += f"  • Resultado = 0\n\n"

                    elif num.func == sp.tan:
                        arg_tan = num.args[0]
                        coef_tan = arg_tan.coeff(x)
                        coef_den_x = den.coeff(x)

                        if coef_tan != 0 and coef_den_x != 0:
                            resultado_trig = coef_tan / coef_den_x
                            explicacion += f"  • Patrón detectado: tan({arg_tan}) / ({den})\n"
                            explicacion += f"  • Usando límite fundamental: lim tan(ax)/bx = a/b\n"
                            explicacion += f"  • a = {coef_tan}, b = {coef_den_x}\n"
                            explicacion += f"  • Resultado = {coef_tan}/{coef_den_x} = {resultado_trig}\n\n"

            if resultado_trig is not None:
                return resultado_trig, explicacion

            explicacion += "  • No se detectó patrón trigonométrico fundamental directo.\n\n"

            explicacion += "🔹 PASO 3: Verificando si aplica Racionalización\n"

            tiene_raiz_num = bool(num.atoms(sp.Pow)) and any(
                p.exp == sp.Rational(1, 2) for p in num.atoms(sp.Pow)
            )
            tiene_raiz_den = bool(den.atoms(sp.Pow)) and any(
                p.exp == sp.Rational(1, 2) for p in den.atoms(sp.Pow)
            )

            resultado_racionalizado = None

            if tiene_raiz_num:
                if num.is_Add:
                    terminos = num.args
                    conjugado = sum(
                        -t if t.could_extract_minus_sign() else t
                        for t in terminos
                    )
                    explicacion += f"  • El numerador tiene raíces: {num}\n"
                    explicacion += f"  • Conjugado del numerador: {conjugado}\n"
                    explicacion += f"  • Multiplicamos num y den por el conjugado ({conjugado})\n\n"

                    num_racionalizado = sp.expand(num * conjugado)
                    den_racionalizado = sp.expand(den * conjugado)

                    explicacion += f"  • Nuevo numerador: {num_racionalizado}\n"
                    explicacion += f"  • Nuevo denominador: {den_racionalizado}\n\n"

                    nueva_funcion = sp.cancel(sp.simplify(num_racionalizado / den_racionalizado))
                    explicacion += f"  • Expresión simplificada: {nueva_funcion}\n\n"

                    nuevo_num, nuevo_den = sp.fraction(nueva_funcion)
                    val_nuevo_num = nuevo_num.subs(x, punto)
                    val_nuevo_den = nuevo_den.subs(x, punto)
                    explicacion += f"  • Sustituyendo x={punto}: {val_nuevo_num} / {val_nuevo_den}\n\n"

                    if val_nuevo_den != 0:
                        resultado_racionalizado = val_nuevo_num / val_nuevo_den
                        explicacion += f"  ✅ Racionalización exitosa → resultado = {resultado_racionalizado}\n\n"

            if resultado_racionalizado is not None:
                return resultado_racionalizado, explicacion

            if tiene_raiz_num or tiene_raiz_den:
                explicacion += "  • La racionalización no eliminó la indeterminación.\n\n"
            else:
                explicacion += "  • No hay raíces → racionalización no aplica.\n\n"

            explicacion += "🔹 PASO 4: Factorización y cancelación algebraica\n"

            num_fact = sp.factor(num)
            den_fact = sp.factor(den)
            explicacion += f"  • Numerador factorizado:   {num_fact}\n"
            explicacion += f"  • Denominador factorizado: {den_fact}\n\n"

            funcion_cancelada = sp.cancel(funcion)
            explicacion += f"  • Expresión simplificada: {funcion_cancelada}\n\n"

            num_c, den_c = sp.fraction(funcion_cancelada)
            val_num_c = num_c.subs(x, punto)
            val_den_c = den_c.subs(x, punto)
            explicacion += f"  • Sustituyendo x={punto}: {val_num_c} / {val_den_c}\n\n"

            if val_den_c != 0:
                resultado = val_num_c / val_den_c
                return resultado, explicacion

            resultado = sp.nan
            explicacion += "  ⚠️ Ninguna técnica resolvió la indeterminación.\n\n"
            return resultado, explicacion

        if not es_infinito and val_num != 0 and val_den == 0:
            explicacion += "⚠️ División por cero (k/0) → posible asíntota vertical.\n\n"
            explicacion += "🔹 PASO 2: Análisis de límites laterales\n"
            explicacion += f"  • El denominador se anula en x = {punto}.\n"
            explicacion += f"  • Evaluamos el signo de la función cerca del punto.\n\n"

            epsilon = sp.Rational(1, 1000)

            val_derecha  = funcion.subs(x, punto + epsilon).evalf()
            val_izquierda = funcion.subs(x, punto - epsilon).evalf()

            explicacion += f"  • f({punto} + ε) ≈ {round(float(val_derecha),  4)}  → lado derecho\n"
            explicacion += f"  • f({punto} - ε) ≈ {round(float(val_izquierda), 4)}  → lado izquierdo\n\n"

            if val_derecha > 0:
                lim_der  = sp.oo
                signo_der = "+∞"
            else:
                lim_der  = -sp.oo
                signo_der = "-∞"

            if val_izquierda > 0:
                lim_izq  = sp.oo
                signo_izq = "+∞"
            else:
                lim_izq  = -sp.oo
                signo_izq = "-∞"

            explicacion += f"  • Límite por la derecha  (x → {punto}⁺) = {signo_der}\n"
            explicacion += f"  • Límite por la izquierda (x → {punto}⁻) = {signo_izq}\n\n"

            if lim_der == lim_izq:
                explicacion += "  ✅ Ambos laterales coinciden.\n\n"
                resultado = lim_der
            else:
                explicacion += "  ❌ Los laterales NO coinciden → el límite NO EXISTE.\n\n"
                resultado = "NO_EXISTE"
            return resultado, explicacion

        if es_infinito:
            explicacion += "🔹 PASO 2: Análisis al infinito (comparación de grados)\n"

            try:
                grado_num = sp.degree(sp.expand(num), x)
                grado_den = sp.degree(sp.expand(den), x)

                coef_num = sp.LC(sp.expand(num), x)
                coef_den = sp.LC(sp.expand(den), x)

                explicacion += f"  • Grado del numerador:   {grado_num}  (coef. líder: {coef_num})\n"
                explicacion += f"  • Grado del denominador: {grado_den}  (coef. líder: {coef_den})\n\n"

                if grado_num < grado_den:
                    explicacion += "  • Grado num < Grado den → el límite es 0.\n\n"
                    resultado = sp.Integer(0)

                elif grado_num == grado_den:
                    resultado = coef_num / coef_den
                    explicacion += f"  • Grado num = Grado den → límite = {coef_num}/{coef_den} = {resultado}.\n\n"

                else:
                    explicacion += "  • Grado num > Grado den → diverge al infinito.\n"
                    val_grande = funcion.subs(x, sp.Integer(10**6)).evalf()

                    if punto == sp.oo:
                        resultado = sp.oo if val_grande > 0 else -sp.oo
                    else:
                        val_grande_neg = funcion.subs(x, sp.Integer(-10**6)).evalf()
                        resultado = sp.oo if val_grande_neg > 0 else -sp.oo

                    explicacion += f"  • Signo al alejarse: {'+ ∞' if resultado == sp.oo else '- ∞'}\n\n"

            except Exception:
                explicacion += "  • Función no polinómica → evaluación por aproximación.\n"
                val_grande = funcion.subs(x, sp.Integer(10**9)).evalf()
                resultado = sp.oo if val_grande > 0 else -sp.oo
                explicacion += f"  • f(10⁹) ≈ {val_grande}  → resultado: {resultado}\n\n"

            return resultado, explicacion

        return sp.nan, explicacion + "  ⚠️ Caso no clasificado.\n\n"

    def calcular_limite(self):
        self.txt_resolucion.delete("1.0", tk.END)
        self.configurar_grafico_vacio()

        str_funcion = self.entry_funcion.get().strip().replace(" ", "").replace("R(", "sqrt(")
        str_punto   = self.entry_punto.get().strip().replace(" ", "")

        if not str_funcion or not str_punto:
            self.txt_resolucion.insert(tk.END, "⚠️ Error: Por favor, rellena ambos campos.")
            return

        x = sp.Symbol('x')

        try:
            transformaciones = standard_transformations + (implicit_multiplication_application,)

            funcion = parse_expr(str_funcion, transformations=transformaciones)

            punto = sp.sympify(str_punto)

            encabezado = f"📌 Análisis de f(x) = {funcion}\n   Evaluando cuando x ➔ {punto}\n\n"

            resultado, pasos = self.resolver_limite(funcion, x, punto)

            explicacion = encabezado + pasos

            if resultado == "NO_EXISTE":
                explicacion += "🎯 RESULTADO FINAL: El límite NO EXISTE\n"
            elif resultado == sp.oo:
                explicacion += "🎯 RESULTADO FINAL: +∞\n"
            elif resultado == -sp.oo:
                explicacion += "🎯 RESULTADO FINAL: -∞\n"
            elif resultado == sp.nan:
                explicacion += "🎯 RESULTADO FINAL: No determinado\n"
            else:
                try:
                    val_float = float(resultado.evalf())
                    if resultado.is_Integer:
                        explicacion += f"🎯 RESULTADO FINAL: {resultado}\n"
                    else:
                        explicacion += f"🎯 RESULTADO FINAL: {resultado}  (≈ {round(val_float, 4)})\n"
                except Exception:
                    explicacion += f"🎯 RESULTADO FINAL: {resultado}\n"

            self.txt_resolucion.insert(tk.END, explicacion)

            es_infinito = (punto == sp.oo or punto == -sp.oo)

            if not es_infinito:
                inicio = float(punto) - 5
                fin    = float(punto) + 5
            else:
                inicio, fin = -10, 10

            pasos_grafica = 300
            paso_tamano   = (fin - inicio) / pasos_grafica

            x_vals = []
            y_vals = []

            for i in range(pasos_grafica + 1):
                val_x = inicio + (i * paso_tamano)
                try:
                    res_y = funcion.subs(x, val_x).evalf()
                    if res_y.is_real and not res_y.is_infinite:
                        x_vals.append(float(val_x))
                        y_vals.append(float(res_y))
                except Exception:
                    continue

            if x_vals:
                self.ax.plot(x_vals, y_vals, color="#1f77b4")
                self.canvas.draw()

        except Exception as e:
            self.txt_resolucion.insert(
                tk.END,
                f"❌ Error en el procesamiento:\n{str(e)}\n\nRevisa que la función esté bien escrita."
            )

    def on_closing(self):
        plt.close('all')
        self.destroy()

if __name__ == "__main__":
    app = AppLimites()
    app.mainloop()