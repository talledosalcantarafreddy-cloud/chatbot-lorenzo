import streamlit as st
import sqlite3

# Configuración de la pestaña en Chrome
st.set_page_config(page_title="ChatBot Lorenzo 🤖", page_icon="🤖", layout="centered")

st.title("ChatBot Lorenzo 🤖")
st.write("---")

def conectar_db():
    conn = sqlite3.connect("chatbot.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS historial (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            emisor TEXT,
            texto TEXT
        )
    """)
    conn.commit()
    return conn

def guardar_mensaje(emisor, texto):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO historial (emisor, texto) VALUES (?, ?)", (emisor, texto))
    conn.commit()
    conn.close()

def cargar_historial():
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT emisor, texto FROM historial")
    filas = cursor.fetchall()
    conn.close()
    
    historial = []
    for fila in filas:
        historial.append({"emisor": fila[0], "texto": fila[1]})
    return historial

def borrar_historial_db():
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM historial")
    conn.commit()
    conn.close()

if "historial" not in st.session_state:
    st.session_state.historial = cargar_historial()
    
    # Si la base de datos estaba vacía, ponemos el saludo inicial
    if len(st.session_state.historial) == 0:
        saludo_inicial = "hola me llamo lorenzo en que puedo yiyiarte"
        guardar_mensaje("Lorenzo", saludo_inicial)
        st.session_state.historial = [{"emisor": "Lorenzo", "texto": saludo_inicial}]

if "esperando_numeros" not in st.session_state:
    st.session_state.esperando_numeros = False
    st.session_state.paso_suma = 0
    st.session_state.n1 = 0.0

for mensaje in st.session_state.historial:
    with st.chat_message("assistant" if mensaje["emisor"] == "Lorenzo" else "user"):
        st.write(f"**{mensaje['emisor']}:** {mensaje['texto']}")

usuario = st.chat_input("Escribe un mensaje...")

if usuario:
    usuario_limpio = usuario.strip()
    usuario_lower = usuario_limpio.lower()

    with st.chat_message("user"):
        st.write(f"**Tú:** {usuario_limpio}")
    guardar_mensaje("Tú", usuario_limpio)
    st.session_state.historial.append({"emisor": "Tú", "texto": usuario_limpio})
    
    respuesta_lorenzo = ""

    if st.session_state.esperando_numeros:
        try:
            if st.session_state.paso_suma == 1:
                st.session_state.n1 = float(usuario_lower)
                st.session_state.paso_suma = 2
                respuesta_lorenzo = "dime el segundo número:"
                
            elif st.session_state.paso_suma == 2:
                n2 = float(usuario_lower)
                
                
                if st.session_state.operacion == "suma":
                    resultado = st.session_state.n1 + n2
                elif st.session_state.operacion == "resta":
                    resultado = st.session_state.n1 - n2
                elif st.session_state.operacion == "multiplicacion":
                    resultado = st.session_state.n1 * n2
                elif st.session_state.operacion == "division":
                    resultado = st.session_state.n1 / n2
                
                if resultado.is_integer():
                    resultado = int(resultado)
                    
                respuesta_lorenzo = f"el resultado es {resultado} (ya no me molestes)"
                st.session_state.esperando_numeros = False
                st.session_state.paso_suma = 0
                st.session_state.operacion = "" 

        except ValueError:
            respuesta_lorenzo = "eso ni siquiera es un número, no inventes. Vuelve a intentar:"

            
    
    else:
        if usuario_lower == "hola":
            respuesta_lorenzo = "hola como estas"
        elif usuario_lower == "como estas" or usuario_lower == "que onda furrito de leche":
            respuesta_lorenzo = "mal porque existe lorenzo"
        elif usuario_lower == "tem puedom premgumtam algom":
            respuesta_lorenzo = "hoy no mañana si"
        elif usuario_lower == "muchas garcias" or usuario_lower == "tenkiu":
            respuesta_lorenzo = "de nada no vuelvas"
        elif usuario_lower == "salir":
            respuesta_lorenzo = "lorenzo dice adios :p"
            
        elif usuario_lower in ["suma", "sumar"]:
            st.session_state.esperando_numeros = True
            st.session_state.paso_suma = 1
            st.session_state.operacion = "suma" 
            respuesta_lorenzo = "dime el primer número para sumarlo:"

        elif usuario_lower in ["resta", "restar"]:
            st.session_state.esperando_numeros = True
            st.session_state.paso_suma = 1
            st.session_state.operacion = "resta" 
            respuesta_lorenzo = "dime el primer número para restarlo:"

        elif usuario_lower in ["multiplica", "multiplicar", "multiplicacion"]:
            st.session_state.esperando_numeros = True
            st.session_state.paso_suma = 1
            st.session_state.operacion = "multiplicacion" 
            respuesta_lorenzo = "dime el primer número para multiplicarlo:"

        elif usuario_lower in ["divide", "dividir", "division"]:
            st.session_state.esperando_numeros = True
            st.session_state.paso_suma = 1
            st.session_state.operacion = "division" 
            respuesta_lorenzo = "dime el primer número para dividirlo:"

    

        elif "de que color es el agua" in usuario_lower or "de que color es el awa" in usuario_lower:
            respuesta_lorenzo = "Azul"
        elif usuario_lower == "awa" or usuario_lower == "agua":
            respuesta_lorenzo = "Moja"
        elif usuario_lower == "a que sabe la nutella":
            respuesta_lorenzo = "Nose"
        elif usuario_lower == "te gusta la leche?":
            respuesta_lorenzo = "Ci"
        elif usuario_lower == "franco":
            respuesta_lorenzo = "Mi mejor amigo"
        elif usuario_lower == "noar jb":
            respuesta_lorenzo = "Reportar cuenta"
        elif usuario_lower == "de que color es el papel":
            respuesta_lorenzo = "Blanco"
        elif usuario_lower == "de que te gusta el jugo":
            respuesta_lorenzo = "De naranja"
        elif usuario_lower == "mejor actor":
            respuesta_lorenzo = "Adam Sandler"
        elif usuario_lower == "que haces en una silla":
            respuesta_lorenzo = "Te sientas"
        elif usuario_lower == "como te llamas":
            respuesta_lorenzo = "Lorenzo"
        elif usuario_lower == "gugugaga" or usuario_lower == "wawa":
            respuesta_lorenzo = "Bebe"
        elif usuario_lower == "tele" or usuario_lower == "tv":
            respuesta_lorenzo = "Cine"
        elif usuario_lower == "cual es la identidad secreta de noar jb":
            respuesta_lorenzo = "Cesar :0"
        elif usuario_lower == "cual es el sentido de la vida":
            respuesta_lorenzo = "Papitas"
        else:
            respuesta_lorenzo = "yo no entender"

    # Mostrar y guardar la respuesta de Lorenzo en la Base de Datos
    with st.chat_message("assistant"):
        st.write(f"**Lorenzo:** {respuesta_lorenzo}")
    guardar_mensaje("Lorenzo", respuesta_lorenzo)
    st.session_state.historial.append({"emisor": "Lorenzo", "texto": respuesta_lorenzo})

st.sidebar.markdown("### Opciones del Sistema")
if st.sidebar.button("Borrar historial de la BD"):
    borrar_historial_db()
    st.session_state.historial = []
    st.rerun()
