import tkinter as tk # Importar Tkinter para interfaces gráficas
import customtkinter as ctk # Importar CustomTkinter para customizar la apariencia de la interfaz
import sympy as sp # Importar SymPy para cálculos simbólicos y matemáticos avanzados(quien entiende y resuelve los limites)
import matplotlib # Importar Matplotlib para graficar funciones y límites

# Configurar Matplotlib para que sea altamente compatible con Tkinter
matplotlib.use('TkAgg') #es lo que permite intengrar las graficas
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg #Permite mostrar la figura del gráfico como un widget dentro de la aplicación.

ctk.set_appearance_mode("System")  #Ajusta el diseño de la app según el modo de color de tu sistema operativo 
ctk.set_default_color_theme("blue")  
class AppLimites(ctk.CTk):  #Define la estructura principal de la aplicación.
    def __init__(self):  
        super().__init__() #Inicializa la ventana principal.
        self.title("límites") #Título de la ventana
        self.geometry("1100x700") #Tamaño de la ventana
        self.grid_columnconfigure(0, weight=1)    #Define que la ventana tendrá columnas y filas 
        self.grid_columnconfigure(1, weight=2)  
        self.grid_rowconfigure(0, weight=1)   



        # los self.frame crean los paneles para organizar los controles de entrada y la visualización gráfica.
        self.frame_izquierdo = ctk.CTkFrame(self, corner_radius=15) #crea un marco con bordes redondeados
        self.frame_izquierdo.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")  #Ubica el marco en la cuadrícula de la ventana principal
        self.frame_izquierdo.grid_columnconfigure(0, weight=1)  
        self.lbl_titulo = ctk.CTkLabel(self.frame_izquierdo, text="Cálculo de Límites", font=ctk.CTkFont(size=22, weight="bold")) #Etiqueta para el título del panel izquierdo, con un tamaño de fuente grande y negrita.
        self.lbl_titulo.grid(row=0, column=0, padx=20, pady=20) #Ubica la etiqueta del titulo en la cuadrícula del marco izquierdo.


        # Campos de Entrada
        self.lbl_funcion = ctk.CTkLabel(self.frame_izquierdo, text="Función f(x): Suma(+), resta(-), multiplicación(*), división(/), potencia(**)") #Etiqueta para el campo de entrada de la función, con instrucciones sobre cómo ingresar la función.
        self.lbl_funcion.grid(row=1, column=0, padx=20, pady=5, sticky="w") #ubica la zona donde esta la etiqueta
        self.entry_funcion = ctk.CTkEntry(self.frame_izquierdo, placeholder_text="Ej: (x**2 - 9)/(x - 3)") #Campo de entrada para la función
        self.entry_funcion.grid(row=2, column=0, padx=20, pady=5, sticky="ew") #ubica la zona donde podremos escribir la función

        # Entrada del punto 
        self.lbl_punto = ctk.CTkLabel(self.frame_izquierdo, text="Valor h al que tiende x (infinito = oo):") #Etiqueta para el campo de entrada del punto al que tiende x
        self.lbl_punto.grid(row=3, column=0, padx=20, pady=5, sticky="w") #ubica la zona donde esta la etiqueta
        self.entry_punto = ctk.CTkEntry(self.frame_izquierdo, placeholder_text="Ej: 3") #Campo de entrada para el punto al que tiende x
        self.entry_punto.grid(row=4, column=0, padx=20, pady=5, sticky="ew") #ubica la zona donde podremos escribir el punto al que tiende x


        # Botón de Acción
        self.btn_calcular = ctk.CTkButton(self.frame_izquierdo, text="Calcular y Graficar", command=self.calcular_limite) #boton que ejecuta la función calcular_limite cuando se hace clic en él
        self.btn_calcular.grid(row=5, column=0, padx=20, pady=20, sticky="ew") #ubica el botón


        # Cuadro de texto para la resolución
        self.lbl_resolucion = ctk.CTkLabel(self.frame_izquierdo, text="Resolución y Resultado:", font=ctk.CTkFont(size=14, weight="bold")) #Etiqueta para el cuadro de texto de la resolución
        self.lbl_resolucion.grid(row=6, column=0, padx=20, pady=5, sticky="w")  #ubica la zona donde esta la etiqueta
        self.txt_resolucion = ctk.CTkTextbox(self.frame_izquierdo, wrap="word", height=150) #Cuadro de texto para mostrar la resolución y el resultado del cálculo del límite
        self.txt_resolucion.grid(row=7, column=0, padx=20, pady=10, sticky="nsew") #ubica el cuadro de texto 
        self.frame_izquierdo.grid_rowconfigure(7, weight=1) #Permite que el cuadro de texto se expanda verticalmente 


        # --- PANEL DERECHO: Visualización Gráfica ---
        self.frame_derecho = ctk.CTkFrame(self, corner_radius=15, fg_color="transparent") #Crea un marco para la visualización gráfica con bordes redondeados y fondo transparente
        self.frame_derecho.grid(row=0, column=1, padx=20, pady=20, sticky="nsew") #Ubica el marco en la cuadrícula de la ventana principal
        self.frame_derecho.grid_columnconfigure(0, weight=1) #Permite que el marco se expanda horizontalmente
        self.frame_derecho.grid_rowconfigure(0, weight=1) #Permite que el marco se expanda verticalmente
        self.fig, self.ax = plt.subplots(figsize=(6, 5), dpi=100) #Crea una figura y un eje para la gráfica utilizando Matplotlib
        self.configurar_grafico_vacio() #Configura el gráfico para que esté vacío inicialmente, con líneas de referencia en los ejes y una cuadrícula.
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame_derecho) #Crea un lienzo para mostrar la figura de Matplotlib dentro del marco derecho de la aplicación
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew", padx=10, pady=10) #Ubica el lienzo dentro del marco derecho, permitiendo que se expanda para llenar el espacio disponible.



        self.protocol("WM_DELETE_WINDOW", self.on_closing) #Configura el protocolo de cierre de la ventana para asegurarse de que se cierren todas las figuras de Matplotlib cuando se cierre la aplicación.



    def configurar_grafico_vacio(self): #Configura el gráfico para que esté vacío inicialmente, con líneas de referencia en los ejes y una cuadrícula.
        self.ax.clear() #Limpia cualquier contenido previo del gráfico
        self.ax.axhline(0, color='black', linewidth=0.8, linestyle='--') #Dibuja una línea horizontal en y=0 para representar el eje x
        self.ax.axvline(0, color='black', linewidth=0.8, linestyle='--') #Dibuja una línea vertical en x=0 para representar el eje y
        self.ax.set_title("Gráfica de f(x)") #Establece el título del gráfico
        self.ax.grid(True, linestyle=':', alpha=0.6) #Agrega una cuadrícula al gráfico para facilitar la visualización de los puntos y las tendencias de la función



    def calcular_limite(self): #Función que se ejecuta al hacer clic en el botón "Calcular y Graficar". Esta función calcula el límite de la función ingresada en el punto especificado y actualiza la resolución y la gráfica.
        self.txt_resolucion.delete("1.0", tk.END) #Limpia el cuadro de texto de resolución para mostrar la nueva resolución del límite calculado.
        self.configurar_grafico_vacio() #Reconfigura el gráfico para que esté vacío antes de graficar la nueva función.
        str_funcion = self.entry_funcion.get().strip() #Obtiene la función ingresada por el usuario en el campo de entrada, eliminando cualquier espacio en blanco al principio o al final.
        str_punto = self.entry_punto.get().strip() #Obtiene el punto al que tiende x ingresado por el usuario en el campo de entrada, eliminando cualquier espacio en blanco al principio o al final.
        if not str_funcion or not str_punto: #Verifica si alguno de los campos de entrada está vacío
            self.txt_resolucion.insert(tk.END, " Error: Por favor, rellena ambos campos.") #Si alguno de los campos está vacío, muestra un mensaje de error en el cuadro de texto de resolución 
            return #Si los campos están completos, continúa con el cálculo del límite.


        x = sp.Symbol('x') #Define 'x' como una variable simbólica para que SymPy pueda realizar cálculos simbólicos con ella


        try: #Intenta convertir la función y el punto ingresados por el usuario en objetos simbólicos de SymPy para poder calcular el límite de manera analítica.
            funcion = sp.sympify(str_funcion) #Convierte la cadena de texto ingresada por el usuario para la función en una expresión simbólica que SymPy pueda entender y manipular.
            punto = sp.sympify(str_punto) #Convierte la cadena de texto ingresada por el usuario para el punto al que tiende x en una expresión simbólica que SymPy pueda entender y manipular.
            limite_analitico = sp.limit(funcion, x, punto) #Calcula el límite de la función con respecto a 'x' cuando 'x' tiende al punto especificado utilizando la función 'limit' de SymPy.
            explicacion = f" Función: {funcion}\n Evaluando x ➔ {punto}\n\n" #Prepara una explicación que muestra la función ingresada, el punto al que tiende x, y el resultado del límite calculado.
            explicacion += f" RESULTADO: {limite_analitico}\n" #Agrega el resultado del límite calculado a la explicación.
            self.txt_resolucion.insert(tk.END, explicacion) #Muestra la explicación y el resultado del límite calculado en el cuadro de texto de resolución.



            # Generación de gráfica manual 
            if punto.is_real:  #Si el punto al que tiende x es un número real, se establece un rango de x alrededor de ese punto para graficar la función. Si el punto es infinito, se establece un rango fijo de -10 a 10.
                inicio, fin = float(punto) - 5, float(punto) + 5   #si es un numero real
            else:
                inicio, fin = -10, 10 #si es infinito

            pasos = 200 #Número de puntos a calcular para graficar la función, lo que determina la suavidad de la curva en la gráfica.
            paso_tamano = (fin - inicio) / pasos #Calcula el tamaño del paso entre cada punto en el rango de x para graficar la función
            x_vals = []  #Listas para almacenar los valores de x e y que se calcularán para graficar la función.
            y_vals = []  #las listas para almacenar los valores de x e y que se calcularán para graficar la función.


           #Calcula el límite de la función para cada valor de x en el rango definido
            for i in range(pasos + 1): 
                
                val_x = inicio + (i * paso_tamano) #Calcula el valor de x para cada punto en el rango definido, comenzando desde 'inicio' y avanzando en incrementos de 'paso_tamano' hasta llegar a 'fin'.
                try:
                    res_y = funcion.subs(x, val_x).evalf() #Calcula el valor de y para cada valor de x sustituyendo 'x' por 'val_x' en la función y evaluando el resultado numéricamente con 'evalf()'.
                    if res_y.is_real and not res_y.is_infinite:   #Verifica si el resultado de y es un número real y no es infinito antes de agregarlo a las listas de valores para graficar
                        x_vals.append(float(val_x))  #Agrega el valor de x a la lista de valores de x para graficar.
                        y_vals.append(float(res_y))  #Agrega el valor de y a la lista de valores de y para graficar.
                except: continue  #Si ocurre un error al calcular el valor de y para un valor específico de x, se ignora ese punto y se continúa con el siguiente valor de x.

            if x_vals:  #Si se han calculado valores válidos de x e y para graficar, se procede a graficar la función utilizando Matplotlib.
                self.ax.plot(x_vals, y_vals, color="#1f77b4")  #Grafica la función utilizando los valores de x e y calculados, con un color específico para la línea de la gráfica.
                self.canvas.draw()  #Actualiza el lienzo de Matplotlib para mostrar la nueva gráfica de la función después de haberla dibujado.

        except Exception as e:  #Si ocurre cualquier error durante el proceso de conversión de la función o el punto, o durante el cálculo del límite, se captura la excepción y se muestra un mensaje de error en el cuadro de texto de resolución.
            self.txt_resolucion.insert(tk.END, f"❌ Error: {str(e)}")  #Muestra el mensaje de error en el cuadro de texto de resolución, indicando que hubo un problema con la entrada del usuario o con el cálculo del límite.



    def on_closing(self):  #Función que se ejecuta cuando se cierra la ventana de la aplicación. 
        plt.close('all')   #Cierra todas las figuras de Matplotlib 
        self.destroy()     #Destruye la ventana de la aplicación para asegurarse de que se cierre correctamente 
if __name__ == "__main__": #Punto de entrada del programa, que crea una instancia de la aplicación y la ejecuta.
    app = AppLimites()     #Crea una instancia de la clase AppLimites, que representa la aplicación de cálculo de límites.
    app.mainloop()         #Inicia el bucle principal de la aplicación, lo que permite que la ventana se muestre y responda a las interacciones del usuario.