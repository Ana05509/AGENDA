import tkinter as tk
from tkinter import ttk, messagebox
from db import verificar_usuario, registrar_usuario, agregar_evento, obtener_eventos, guardar_materias, obtener_materias, guardar_deber, obtener_deberes
import datetime

class AgendaApp:
    def _init_(self):
        self.root = tk.Tk()
        self.root.title("Agenda Escolar")
        self.root.geometry("900x700")
        self.root.configure(bg="#F9F9F9")

        self.fuente_titulo = ("Helvetica", 18, "bold")
        self.fuente_texto = ("Helvetica", 12)

        self.mostrar_login()
        self.root.mainloop()

    def mostrar_menu_eventos(self, usuario):
        self.limpiar_ventana()

        tk.Label(self.root, text=f"Bienvenido, {usuario}", font=self.fuente_titulo, bg="#F9F9F9").pack(pady=20)

        botones = [
            ("Gestionar Horario y Deberes", lambda: self.mostrar_horario(usuario)),
            ("Ver Deberes Pendientes", lambda: self.mostrar_deberes(usuario)),
            ("Cerrar Sesión", self.mostrar_login)
        ]

        for texto, comando in botones:
            tk.Button(self.root, text=texto, command=comando, bg="#4A90E2", fg="white",
                      font=self.fuente_texto, width=30, height=2, relief="raised").pack(pady=10)

    def mostrar_horario(self, usuario):
        self.limpiar_ventana()

        tk.Label(self.root, text="Horario Escolar", font=self.fuente_titulo, bg="#F9F9F9").pack(pady=10)

        horario_frame = tk.Frame(self.root, bg="white", relief="solid", bd=2)
        horario_frame.pack(expand=True, fill="both", padx=20, pady=10)

        dias = ["Hora", "Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
        for i, dia in enumerate(dias):
            tk.Label(horario_frame, text=dia, font=self.fuente_texto, bg="#4A90E2", fg="white",
                     relief="raised", width=15, height=2).grid(row=0, column=i, sticky="nsew", padx=1, pady=1)

        self.celdas_materias = {}
        horas = ["7:00", "8:00", "9:00", "10:00", "11:00", "12:00"]

        for i, hora in enumerate(horas, 1):
            tk.Label(horario_frame, text=hora, font=self.fuente_texto, bg="#4A90E2", fg="white",
                     relief="raised", width=15, height=2).grid(row=i, column=0, sticky="nsew", padx=1, pady=1)

            for j in range(1, 6):
                entry = tk.Entry(horario_frame, font=self.fuente_texto, justify="center", relief="solid")
                entry.grid(row=i, column=j, sticky="nsew", padx=1, pady=1)
                self.celdas_materias[(hora, j)] = entry

        for i in range(6):
            horario_frame.grid_columnconfigure(i, weight=1)
        for i in range(7):
            horario_frame.grid_rowconfigure(i, weight=1)

        botones_frame = tk.Frame(self.root, bg="#F9F9F9")
        botones_frame.pack(pady=10)

        botones = [
            ("Guardar Horario", lambda: self.guardar_horario(usuario)),
            ("Agregar Deber", lambda: self.agregar_deber(usuario)),
            ("Volver", lambda: self.mostrar_menu_eventos(usuario))
        ]

        for texto, comando in botones:
            tk.Button(botones_frame, text=texto, command=comando, bg="#4A90E2", fg="white",
                      font=self.fuente_texto, width=20, height=2).pack(side=tk.LEFT, padx=10)

        horario_guardado = obtener_materias(usuario)
        for (hora, dia), entry in self.celdas_materias.items():
            dia_texto = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"][dia-1]
            clave = f"{hora}-{dia_texto}"
            if clave in horario_guardado:
                entry.insert(0, horario_guardado[clave])

    def mostrar_deberes(self, usuario):
        self.limpiar_ventana()

        tk.Label(self.root, text="Deberes Pendientes", font=self.fuente_titulo, bg="#F9F9F9").pack(pady=10)

        frame = tk.Frame(self.root, bg="white", relief="solid", bd=2)
        frame.pack(expand=True, fill="both", padx=20, pady=10)

        columns = ("Materia", "Descripción", "Fecha de Entrega")
        tree = ttk.Treeview(frame, columns=columns, show="headings")

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=200, anchor="center")

        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        tree.pack(expand=True, fill="both")

        deberes = obtener_deberes(usuario)
        for deber in deberes:
            tree.insert("", "end", values=deber)

        botones_frame = tk.Frame(self.root, bg="#F9F9F9")
        botones_frame.pack(pady=10)

        botones = [
            ("Actualizar", lambda: self.actualizar_deberes(usuario, tree)),
            ("Volver", lambda: self.mostrar_menu_eventos(usuario))
        ]

        for texto, comando in botones:
            tk.Button(botones_frame, text=texto, command=comando, bg="#4A90E2", fg="white",
                      font=self.fuente_texto, width=20, height=2).pack(side=tk.LEFT, padx=10)

    def actualizar_deberes(self, usuario, tree):
        for item in tree.get_children():
            tree.delete(item)

        deberes = obtener_deberes(usuario)
        for deber in deberes:
            tree.insert("", "end", values=deber)

    def agregar_deber(self, usuario):
        ventana_deber = tk.Toplevel(self.root)
        ventana_deber.title("Agregar Deber")
        ventana_deber.geometry("400x400")
        ventana_deber.configure(bg="#F9F9F9")

        tk.Label(ventana_deber, text="Agregar Nuevo Deber", font=self.fuente_titulo, bg="#F9F9F9").pack(pady=10)

        tk.Label(ventana_deber, text="Materia:", font=self.fuente_texto, bg="#F9F9F9").pack(pady=(10, 2))
        materia_entry = tk.Entry(ventana_deber, width=40)
        materia_entry.pack()

        tk.Label(ventana_deber, text="Descripción:", font=self.fuente_texto, bg="#F9F9F9").pack(pady=(10, 2))
        descripcion_text = tk.Text(ventana_deber, height=4, width=40)
        descripcion_text.pack()

        tk.Label(ventana_deber, text="Fecha de Entrega (YYYY-MM-DD):", font=self.fuente_texto, bg="#F9F9F9").pack(pady=(10, 2))
        fecha_entry = tk.Entry(ventana_deber, width=40)
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
                datetime.datetime.strptime(fecha, '%Y-%m-%d')

                if guardar_deber(usuario, materia, descripcion, fecha):
                    messagebox.showinfo("Éxito", "Deber guardado correctamente")
                    ventana_deber.destroy()
                else:
                    messagebox.showerror("Error", "No se pudo guardar el deber")
            except ValueError:
                messagebox.showerror("Error", "Formato de fecha incorrecto. Use YYYY-MM-DD")

        botones_frame = tk.Frame(ventana_deber, bg="#F9F9F9")
        botones_frame.pack(pady=20)

        tk.Button(botones_frame, text="Guardar", command=guardar_y_cerrar, bg="#4A90E2", fg="white",
                  font=self.fuente_texto, width=15).pack(side=tk.LEFT, padx=5)
        tk.Button(botones_frame, text="Cancelar", command=ventana_deber.destroy, bg="#FF5C5C", fg="white",
                  font=self.fuente_texto, width=15).pack(side=tk.LEFT, padx=5)

        ventana_deber.transient(self.root)
        ventana_deber.grab_set()
        ventana_deber.focus_set()

    def guardar_horario(self, usuario):
        horario = {}
        for (hora, dia), entry in self.celdas_materias.items():
            materia = entry.get().strip()
            if materia:
                dia_texto = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"][dia-1]
                clave = f"{hora}-{dia_texto}"
                horario[clave] = materia

        if not horario:
            messagebox.showwarning("Advertencia", "No hay materias para guardar en el horario")
            return

        if guardar_materias(usuario, horario):
            messagebox.showinfo("Éxito", "Horario guardado correctamente")
        else:
            messagebox.showerror("Error", "No se pudo guardar el horario")

    def mostrar_login(self):
        self.limpiar_ventana()

        frame_login = tk.Frame(self.root, bg="white", bd=2, relief="solid")
        frame_login.place(relx=0.5, rely=0.5, anchor="center", width=400, height=400)

        tk.Label(frame_login, text="Bienvenido", font=("Helvetica", 20, "bold"), bg="white", fg="#333333").pack(pady=20)

        tk.Label(frame_login, text="Usuario:", font=self.fuente_texto, bg="white", fg="#666666").pack(anchor="w", padx=40, pady=(10, 0))
        self.usuario_entry = ttk.Entry(frame_login, font=self.fuente_texto)
        self.usuario_entry.pack(fill="x", padx=40, pady=5)

        tk.Label(frame_login, text="Contraseña:", font=self.fuente_texto, bg="white", fg="#666666").pack(anchor="w", padx=40, pady=(10, 0))
        self.contrasena_entry = ttk.Entry(frame_login, font=self.fuente_texto, show="*")
        self.contrasena_entry.pack(fill="x", padx=40, pady=5)

        boton_login = tk.Button(frame_login, text="Iniciar Sesión", command=self.iniciar_sesion, font=self.fuente_texto, bg="#4CAF50", fg="white", relief="flat", cursor="hand2")
        boton_login.pack(pady=20, ipadx=10, ipady=5)

        link_registro = tk.Label(frame_login, text="¿No tienes cuenta? Regístrate aquí", font=("Helvetica", 10, "underline"), bg="white", fg="#0066CC", cursor="hand2")
        link_registro.pack(pady=(10, 0))
        link_registro.bind("<Button-1>", lambda e: self.mostrar_registro())

    def mostrar_registro(self):
        self.limpiar_ventana()

        tk.Label(self.root, text="Registrar Usuario", font=self.fuente_titulo, bg="#F9F9F9").pack(pady=20)

        tk.Label(self.root, text="Nuevo Usuario:", font=self.fuente_texto, bg="#F9F9F9").pack()
        self.nuevo_usuario_entry = tk.Entry(self.root, font=self.fuente_texto)
        self.nuevo_usuario_entry.pack(pady=5)

        tk.Label(self.root, text="Contraseña:", font=self.fuente_texto, bg="#F9F9F9").pack()
        self.nueva_contrasena_entry = tk.Entry(self.root, font=self.fuente_texto, show="*")
        self.nueva_contrasena_entry.pack(pady=5)

        tk.Button(self.root, text="Registrar", command=self.registrar_usuario, bg="#4CAF50", fg="white", font=self.fuente_texto, width=20, height=2).pack(pady=10)
        tk.Button(self.root, text="Volver", command=self.mostrar_login, bg="#FF5C5C", fg="white", font=self.fuente_texto, width=20, height=2).pack()

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

    def limpiar_ventana(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    AgendaApp()