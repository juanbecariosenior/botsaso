from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import pyodbc
import asyncio
from dotenv import load_dotenv
import os 
load_dotenv()

# Configuración de la conexión SQL Server
server = os.getenv('server')
bd = os.getenv('bd')
usuario = os.getenv('usuario')
contrsena = os.getenv('contrsena')

def obtener_platillos(precio_minimo):
    """Realiza la consulta SQL con un parámetro y devuelve los resultados."""
    try:
        conexion = pyodbc.connect(
            f'DRIVER={{ODBC Driver 17 for SQL server}};SERVER={server};DATABASE={bd};UID={usuario};PWD={contrsena}'
        )
        cursor = conexion.cursor()
        consulta = "Select Cod,Descripcion,Precio from RE_Platillos where Descripcion LIKE '%'+?+'%'"
        cursor.execute(consulta, (precio_minimo,))
        platillos = cursor.fetchall()
        cursor.close()
        conexion.close()
        return platillos
    except Exception as e:
        print(f"Error al consultar la base de datos: {e}")
        return None

# Manejadores de comandos
async def say_hello(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello World!")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(update.message.text)

async def quien_soy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Soy becario Senior")

"""async def mostrar_platillos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    #Manejador del comando /platillos con un parámetro dinámico.
    try:
        # Obtener el parámetro del mensaje del usuario
        args = context.args
        if not args or not args[0].isalpha():
            await update.message.reply_text("Por favor, especifica una breve descripcion del platillo. Ejemplo: /platillos hamburguesa")
            return
        
        desc_platillo = args[0]
        await update.message.reply_text(f"Consultando platillos con una descripcion similar a {desc_platillo}, por favor espera...")
        
        # Ejecutar la consulta SQL en un hilo separado
        loop = asyncio.get_event_loop()
        platillos = await loop.run_in_executor(None, obtener_platillos, desc_platillo)
        
        # Formatear y enviar los resultados
        if platillos:
            respuesta = "Platillos disponibles:\n"
            respuesta += "\n".join([f"{cod}: {desc} - ${precio:.2f} " for cod, desc,precio in platillos])
        else:
            respuesta = f"No se encontraron platillos con una descripcion similar a {desc_platillo}."
        
        await update.message.reply_text(respuesta)
    except Exception as e:
        await update.message.reply_text(f"Ocurrió un error: {e}")"""

def dividir_mensaje(mensaje, max_longitud=4096):
    """Divide un mensaje en fragmentos más pequeños para cumplir con el límite de Telegram."""
    return [mensaje[i:i+max_longitud] for i in range(0, len(mensaje), max_longitud)]

async def mostrar_platillos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Manejador del comando /platillos con un parámetro dinámico."""
    try:
        # Obtener el parámetro del mensaje del usuario
        args = context.args
        if not args or not args[0].isalpha():
            await update.message.reply_text("Por favor, especifica una breve descripción del platillo. Ejemplo: /platillos hamburguesa")
            return
        
        desc_platillo = args[0]
        await update.message.reply_text(f"Consultando platillos con una descripción similar a '{desc_platillo}', por favor espera...")
        
        # Ejecutar la consulta SQL en un hilo separado
        loop = asyncio.get_event_loop()
        platillos = await loop.run_in_executor(None, obtener_platillos, desc_platillo)
        
        # Formatear los resultados
        if platillos:
            respuesta = "Platillos disponibles:\n"
            respuesta += "\n".join([f"{cod}: {desc} - ${precio:.2f}" for cod, desc, precio in platillos])
        else:
            respuesta = f"No se encontraron platillos con una descripción similar a '{desc_platillo}'."
        
        # Dividir el mensaje si es muy largo
        fragmentos = dividir_mensaje(respuesta)
        for fragmento in fragmentos:
            await update.message.reply_text(fragmento)
    except Exception as e:
        await update.message.reply_text(f"Ocurrió un error: {e}")



# Configuración del bot
application = ApplicationBuilder().token(os.getenv("token")).build()

# Registrar manejadores
application.add_handler(CommandHandler("start", say_hello))
application.add_handler(CommandHandler("echo", echo))
application.add_handler(CommandHandler("juanisimo", quien_soy))
application.add_handler(CommandHandler("platillos", mostrar_platillos))

# Iniciar el bot
print("El bot está corriendo...")
application.run_polling(allowed_updates=Update.ALL_TYPES)







