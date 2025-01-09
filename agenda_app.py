import tkinter as tk
from tkinter import PhotoImage
from tkinter import ttk, messagebox
from db import verificar_usuario, registrar_usuario, agregar_evento, obtener_eventos, guardar_materias, obtener_materias, guardar_deber, obtener_deberes
import datetime

class AgendaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Agenda App")
        
        # Crear el frame para el inicio de sesión
        login_frame = tk.Frame(self.root, bg="#f0f0f0")
        login_frame.pack(expand=True, fill="both")
        
        # Cargar y mostrar el logotipo
        self.logo = PhotoImage(file="logo.png")
        tk.Label(login_frame, image=self.logo, bg="#f0f0f0").pack(pady=20)
        
        # Etiqueta y campo de entrada para el nombre de usuario
        tk.Label(login_frame, text="Usuario:", font=("Arial", 12), bg="#f0f0f0").pack(pady=5)
        self.entrada_usuario = tk.Entry(login_frame, font=("Arial", 12))
        self.entrada_usuario.pack(pady=5)
        
        # Etiqueta y campo de entrada para la contraseña
        tk.Label(login_frame, text="Contraseña:", font=("Arial", 12), bg="#f0f0f0").pack(pady=5)
        self.entrada_contrasena = tk.Entry(login_frame, font=("Arial", 12), show="*")
        self.entrada_contrasena.pack(pady=5)
        
        # Botón de inicio de sesión
        tk.Button(login_frame, text="Iniciar Sesión", command=self.mostrar_horario, font=("Arial", 12), bg="#4a90e2", fg="white").pack(pady=20)
    
    def mostrar_horario(self):
        # Aquí puedes agregar la lógica para mostrar el horario después de iniciar sesión
        pass

    # --- Ventanas de la Aplicación ---

    def mostrar_menu_eventos(self, usuario):
        self.limpiar_ventana()

        tk.Label(self.root, text=f"Bienvenido, {usuario}", font=("Arial", 18), bg="#F0F8FF").pack(pady=20)

        # Cambiamos los nombres de los botones y sus funciones
        tk.Button(self.root, 
                 text="Gestionar Horario y Deberes", 
                 command=lambda: self.mostrar_horario(usuario), 
                 bg="#ADD8E6",
                 width=25,
                 height=2).pack(pady=5)
        
        tk.Button(self.root, 
                 text="Ver Deberes Pendientes", 
                 command=lambda: self.mostrar_deberes(usuario), 
                 bg="#ADD8E6",
                 width=25,
                 height=2).pack(pady=5)
        
        tk.Button(self.root, 
                 text="Cerrar Sesión", 
                 command=self.mostrar_login, 
                 bg="#FFB6C1",
                 width=25,
                 height=2).pack(pady=10)

    def mostrar_horario(self, usuario):
        self.limpiar_ventana()
        
        # Título principal
        tk.Label(self.root, text="Horario Escolar", 
                font=("Arial", 18, "bold"), 
                bg="#F0F8FF").pack(pady=10)
        
        # Frame para el horario
        horario_frame = tk.Frame(self.root, bg="white")
        horario_frame.pack(expand=True, fill="both", padx=20, pady=10)
        
        # Días de la semana
        dias = ["Hora", "Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
        for i, dia in enumerate(dias):
            tk.Label(horario_frame, 
                    text=dia,
                    font=("Arial", 10, "bold"),
                    bg="#4a90e2",
                    fg="white",
                    relief="raised",
                    width=15,
                    height=2).grid(row=0, column=i, sticky="nsew", padx=1, pady=1)
        
        # Horas y celdas para materias
        self.celdas_materias = {}
        horas = ["7:00", "8:00", "9:00", "10:00", "11:00", "12:00"]
        
        for i, hora in enumerate(horas, 1):
            # Columna de hora
            tk.Label(horario_frame,
                    text=hora,
                    font=("Arial", 10, "bold"),
                    bg="#4a90e2",
                    fg="white",
                    relief="raised",
                    width=15,
                    height=2).grid(row=i, column=0, sticky="nsew", padx=1, pady=1)
            
            # Celdas editables para materias
            for j in range(1, 6):
                entry = tk.Entry(horario_frame,
                               font=("Arial", 10),
                               justify="center",
                               relief="solid")
                entry.grid(row=i, column=j, sticky="nsew", padx=1, pady=1)
                self.celdas_materias[(hora, j)] = entry
        
        # Configurar el grid
        for i in range(6):
            horario_frame.grid_columnconfigure(i, weight=1)
        for i in range(7):
            horario_frame.grid_rowconfigure(i, weight=1)
        
        # Frame para botones
        botones_frame = tk.Frame(self.root, bg="#F0F8FF")
        botones_frame.pack(pady=10)
        
        # Botones
        tk.Button(botones_frame,
                 text="Guardar Horario",
                 command=lambda: self.guardar_horario(usuario),
                 bg="#90EE90",
                 width=15).pack(side=tk.LEFT, padx=5)
        
        tk.Button(botones_frame,
                 text="Agregar Deber",
                 command=lambda: self.agregar_deber(usuario),
                 bg="#ADD8E6",
                 width=15).pack(side=tk.LEFT, padx=5)
        
        tk.Button(botones_frame,
                 text="Volver",
                 command=lambda: self.mostrar_menu_eventos(usuario),
                 bg="#FFB6C1",
                 width=15).pack(side=tk.LEFT, padx=5)
        
        # Cargar horario guardado
        horario_guardado = obtener_materias(usuario)
        for (hora, dia), entry in self.celdas_materias.items():
            dia_texto = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"][dia-1]
            clave = f"{hora}-{dia_texto}"
            if clave in horario_guardado:
                entry.insert(0, horario_guardado[clave])

    def mostrar_deberes(self, usuario):
        self.limpiar_ventana()
        
        # Título
        tk.Label(self.root, text="Deberes Pendientes", 
                font=("Arial", 18, "bold"), 
                bg="#F0F8FF").pack(pady=10)
        
        # Frame para la lista de deberes
        deberes_frame = tk.Frame(self.root, bg="white")
        deberes_frame.pack(expand=True, fill="both", padx=20, pady=10)
        
        # Crear Treeview para mostrar los deberes
        columns = ("Materia", "Descripción", "Fecha de Entrega")
        tree = ttk.Treeview(deberes_frame, columns=columns, show="headings")
        
        # Configurar las columnas
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        
        # Agregar scrollbar
        scrollbar = ttk.Scrollbar(deberes_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        
        # Obtener y mostrar los deberes
        deberes = obtener_deberes(usuario)
        for deber in deberes:
            tree.insert("", "end", values=deber)
        
        tree.pack(expand=True, fill="both")
        
        # Frame para botones
        botones_frame = tk.Frame(self.root, bg="#F0F8FF")
        botones_frame.pack(pady=10)
        
        # Botón para volver
        tk.Button(botones_frame,
                 text="Volver",
                 command=lambda: self.mostrar_menu_eventos(usuario),
                 bg="#FFB6C1",
                 width=15).pack(side=tk.LEFT, padx=5)
        
        # Botón para actualizar
        tk.Button(botones_frame,
                 text="Actualizar",
                 command=lambda: self.actualizar_deberes(usuario, tree),
                 bg="#90EE90",
                 width=15).pack(side=tk.LEFT, padx=5)

    def actualizar_deberes(self, usuario, tree):
        # Limpiar el árbol
        for item in tree.get_children():
            tree.delete(item)
        
        # Recargar los deberes
        deberes = obtener_deberes(usuario)
        for deber in deberes:
            tree.insert("", "end", values=deber)

    def agregar_deber(self, usuario):
        # Crear ventana emergente
        ventana_deber = tk.Toplevel(self.root)
        ventana_deber.title("Agregar Deber")
        ventana_deber.geometry("400x500")
        ventana_deber.configure(bg="#F0F8FF")

        # Frame principal
        frame = tk.Frame(ventana_deber, bg="#F0F8FF")
        frame.pack(padx=20, pady=20, fill="both", expand=True)

        # Título
        tk.Label(frame, 
                text="Agregar Nuevo Deber", 
                font=("Arial", 16, "bold"),
                bg="#F0F8FF").pack(pady=10)

        # Campo Materia
        tk.Label(frame, 
                text="Materia:", 
                font=("Arial", 10, "bold"),
                bg="#F0F8FF").pack(pady=(10,2))
        materia_entry = tk.Entry(frame, width=40)
        materia_entry.pack()

        # Campo Descripción
        tk.Label(frame, 
                text="Descripción:", 
                font=("Arial", 10, "bold"),
                bg="#F0F8FF").pack(pady=(10,2))
        descripcion_text = tk.Text(frame, height=4, width=40)
        descripcion_text.pack()

        # Campo Fecha
        tk.Label(frame, 
                text="Fecha de Entrega (YYYY-MM-DD):", 
                font=("Arial", 10, "bold"),
                bg="#F0F8FF").pack(pady=(10,2))
        fecha_entry = tk.Entry(frame, width=40)
        fecha_entry.insert(0, datetime.date.today().strftime('%Y-%m-%d'))
        fecha_entry.pack()

        def guardar_y_cerrar():
            materia = materia_entry.get().strip()
            descripcion = descripcion_text.get("1.0", tk.END).strip()
            fecha = fecha_entry.get().strip()

            if not all([materia, descripcion, fecha]):
                messagebox.showerror("Error", "Por favor completa todos los campos")
                return

            try:
                # Validar formato de fecha
                datetime.datetime.strptime(fecha, '%Y-%m-%d')
                
                # Intentar guardar el deber
                if guardar_deber(usuario, materia, descripcion, fecha):
                    messagebox.showinfo("Éxito", "Deber guardado correctamente")
                    ventana_deber.destroy()
                else:
                    messagebox.showerror("Error", "No se pudo guardar el deber")
            except ValueError:
                messagebox.showerror("Error", "Formato de fecha incorrecto. Use YYYY-MM-DD")

        # Frame para botones
        botones_frame = tk.Frame(frame, bg="#F0F8FF")
        botones_frame.pack(pady=20)

        # Botón Guardar
        tk.Button(botones_frame,
                 text="Guardar Deber",
                 command=guardar_y_cerrar,
                 bg="#90EE90",
                 width=15,
                 height=2).pack(side=tk.LEFT, padx=5)

        # Botón Cancelar
        tk.Button(botones_frame,
                 text="Cancelar",
                 command=ventana_deber.destroy,
                 bg="#FFB6C1",
                 width=15,
                 height=2).pack(side=tk.LEFT, padx=5)

        # Hacer la ventana modal
        ventana_deber.transient(self.root)
        ventana_deber.grab_set()
        ventana_deber.focus_set()

    def guardar_horario(self, usuario):
        try:
            horario = {}
            print("\n=== INICIO GUARDADO DE HORARIO ===")
            print(f"Usuario actual: {usuario}")
            
            for (hora, dia), entry in self.celdas_materias.items():
                materia = entry.get().strip()
                if materia:
                    dia_texto = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"][dia-1]
                    clave = f"{hora}-{dia_texto}"
                    horario[clave] = materia
                    print(f"Agregando al horario: {clave} = {materia}")
            
            if not horario:
                print("No hay materias para guardar")
                messagebox.showwarning("Advertencia", "No hay materias para guardar en el horario")
                return
            
            print(f"Total de materias a guardar: {len(horario)}")
            resultado = guardar_materias(usuario, horario)
            print(f"Resultado del guardado: {resultado}")
            
            if resultado:
                messagebox.showinfo("Éxito", "Horario guardado correctamente")
            else:
                messagebox.showerror("Error", 
                                   "No se pudo guardar el horario.\n" +
                                   "Por favor, revisa la consola para más detalles y\n" +
                                   "contacta al soporte técnico si el problema persiste.")
        
        except Exception as e:
            print(f"Error inesperado: {type(e).__name__}")
            print(f"Descripción: {str(e)}")
            messagebox.showerror("Error", f"Error inesperado al guardar: {str(e)}")

    # --- Ventana de Inicio de Sesión ---
    def mostrar_login(self):
        self.limpiar_ventana()

        tk.Label(self.root, text="Iniciar Sesión", font=("Arial", 18), bg="#F0F8FF").pack(pady=20)

        tk.Label(self.root, text="Usuario:", bg="#F0F8FF").pack()
        self.usuario_entry = tk.Entry(self.root)
        self.usuario_entry.pack()

        tk.Label(self.root, text="Contraseña:", bg="#F0F8FF").pack()
        self.contrasena_entry = tk.Entry(self.root, show="*")
        self.contrasena_entry.pack()

        tk.Button(self.root, text="Iniciar Sesión", command=self.iniciar_sesion, bg="#ADD8E6").pack(pady=10)
        tk.Button(self.root, text="Registrar Usuario", command=self.mostrar_registro, bg="#90EE90").pack()

    # --- Ventana de Registro ---
    def mostrar_registro(self):
        self.limpiar_ventana()

        tk.Label(self.root, text="Registrar Usuario", font=("Arial", 18), bg="#F0F8FF").pack(pady=20)

        tk.Label(self.root, text="Nuevo Usuario:", bg="#F0F8FF").pack()
        self.nuevo_usuario_entry = tk.Entry(self.root)
        self.nuevo_usuario_entry.pack()

        tk.Label(self.root, text="Contraseña:", bg="#F0F8FF").pack()
        self.nueva_contrasena_entry = tk.Entry(self.root, show="*")
        self.nueva_contrasena_entry.pack()

        tk.Button(self.root, text="Registrar", command=self.registrar_usuario, bg="#90EE90").pack(pady=10)
        tk.Button(self.root, text="Volver", command=self.mostrar_login, bg="#FFB6C1").pack()

    # --- Ventana para Ver Eventos ---
    def mostrar_eventos(self, usuario):
        self.limpiar_ventana()

        tk.Label(self.root, text="Tus Eventos", font=("Arial", 18), bg="#F0F8FF").pack(pady=20)

        eventos = obtener_eventos(usuario)
        if not eventos:
            tk.Label(self.root, text="No hay eventos programados.", bg="#F0F8FF").pack()
        else:
            for evento, dia in eventos:
                tk.Label(self.root, text=f"{dia}: {evento}", bg="#F0F8FF").pack()

        tk.Button(self.root, text="Volver", command=lambda: self.mostrar_menu_eventos(usuario), bg="#FFB6C1").pack(pady=10)

        # Simular notificación
        self.notificar_eventos(eventos)

    # --- Funciones de Manejo ---
    def iniciar_sesion(self):
        usuario = self.usuario_entry.get()
        contrasena = self.contrasena_entry.get()
        if verificar_usuario(usuario, contrasena):
            self.mostrar_menu_eventos(usuario)
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos.")

    def registrar_usuario(self):
        usuario = self.nuevo_usuario_entry.get()
        contrasena = self.nueva_contrasena_entry.get()
        if registrar_usuario(usuario, contrasena):
            messagebox.showinfo("Éxito", "Usuario registrado correctamente.")
            self.mostrar_login()
        else:
            messagebox.showerror("Error", "El usuario ya existe.")

    def guardar_evento(self, usuario):
        evento = self.evento_entry.get()
        fecha = self.calendario.get_date()
        if evento and fecha:
            agregar_evento(usuario, evento, fecha)
            messagebox.showinfo("Éxito", "Evento guardado correctamente.")
            self.mostrar_menu_eventos(usuario)
        else:
            messagebox.showerror("Error", "Completa todos los campos.")

    def notificar_eventos(self, eventos):
        hoy = datetime.date.today().strftime("%Y-%m-%d")
        for evento, fecha in eventos:
            if fecha == hoy:
                messagebox.showinfo("Notificación", f"Tienes un evento hoy: {evento}")

    def limpiar_ventana(self):
        for widget in self.root.winfo_children():
            widget.destroy()


# Ejecutar la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = AgendaApp(root)
    root.mainloop()
