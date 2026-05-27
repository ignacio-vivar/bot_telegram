import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from dotenv import load_dotenv
from services.add_food import post_food
from services.get_today_food import get_today_food
load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
MI_ID = int(os.getenv("TELEGRAM_ID"))

DES = "Breakfast"
ALM = "Lunch"
OT = "Other"
DI = "Dinner"


async def procesar_comida(update: Update, context: ContextTypes.DEFAULT_TYPE, meal_tag: str) -> None:
    
    if update.effective_user.id != MI_ID:
        await update.message.reply_text("Andá a laburar, crack. No tenés permisos.")
        return
    
    if not context.args:
        await update.message.reply_text("Error!")
        return
    
    texto_completo = " ".join(context.args)
    alimentos = [alimento.strip() for alimento in texto_completo.split(",")]

    mensaje_final = []

    for ind_alim in alimentos:
        fields_ind_alim = ind_alim.split(None, 1)
        
        # Pequeña red de seguridad por si te olvidás de poner el número (ej: "/des manzana")
        if len(fields_ind_alim) < 2:
            mensaje_final.append(f"Formato inválido: {ind_alim}")
            continue
            
        quantity = fields_ind_alim[0]
        content = " ".join(fields_ind_alim[1:])
        
        estado, unidad = await post_food(meal_tag, quantity, content)
        
        if estado == "ok":
            mensaje_final.append(f"Agregado {quantity} {unidad} de {content} ")
        elif estado == "not_found":
            mensaje_final.append(f"No existe {content}")
        elif estado in ("not_post", "failed"):
            mensaje_final.append(f"Agregar {content} falló")
    
    await update.message.reply_text("\n".join(mensaje_final))

async def registrar_desayuno(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await procesar_comida(update, context, DES)

async def registrar_almuerzo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
   await procesar_comida(update, context, ALM)

async def registrar_cena(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
   await procesar_comida(update, context, DI)

async def registrar_merienda(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
   await procesar_comida(update, context, OT)


async def ver_resumen_hoy(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    
    if update.effective_user.id != MI_ID:
        await update.message.reply_text("Andá a laburar, crack. No tenés permisos.")
        return
    
    await update.message.reply_text("Consultando tu diario en FatSecret... ⏳")
    
    # Llamamos a nuestro servicio limpio
    comidas = await get_today_food()
    
    if not comidas:
        await update.message.reply_text("No hay datos cargados para hoy o hubo un error.")
        return

    # Estructuramos la información de salida de forma legible para Telegram
    texto_respuesta = "📊 **Resumen de hoy**\n\n"
    total_cal = 0
    total_prot = 0
    total_carb = 0
    total_fat = 0
    texto_desayuno = "Desayuno: \n"
    texto_almuerzo = "Almuerzo: \n"
    texto_other = "Tentempies: \n"
    texto_dinner = "Cena: \n"
    

    for item in comidas:
        if item.meal == "Breakfast":
            texto_desayuno += f"🐣 {item.food_entry_name} : {item.calories} kcal | P: {item.protein}g\n"
        if item.meal == "Lunch":
            texto_almuerzo+= f"🐥 {item.food_entry_name} : {item.calories} kcal | P: {item.protein}g\n"
        if item.meal == "Other":
            texto_other+= f"🐤 {item.food_entry_name} : {item.calories} kcal | P: {item.protein}g\n"
        if item.meal == "Dinner":
            texto_dinner+= f"🦇 {item.food_entry_name} : {item.calories} kcal | P: {item.protein}g\n"
      
        total_cal += item.calories
        total_prot += item.protein
        total_carb += item.carbohydrate
        total_fat += item.fat
    
    texto_respuesta += texto_desayuno
    texto_respuesta += texto_almuerzo
    texto_respuesta += texto_other
    texto_respuesta += texto_dinner

    texto_respuesta += "\n📈 **Totales:**\n"
    texto_respuesta += f"Calorías: {total_cal:.1f} kcal\n"
    texto_respuesta += f"Proteínas: {total_prot:.1f}g\n"
    texto_respuesta += f"Carbos: {total_carb:.1f}g\n"
    texto_respuesta += f"Grasas: {total_fat:.1f}g"

    await update.message.reply_text(texto_respuesta)


def main() -> None:
    """Configuración y arranque del bot por Polling."""
    print("Iniciando el bot por Polling...")
    
    telegram_app = Application.builder().token(TOKEN).build()

    # Registrás tus comandos
    telegram_app.add_handler(CommandHandler("des", registrar_desayuno))
    telegram_app.add_handler(CommandHandler("alm", registrar_almuerzo))
    telegram_app.add_handler(CommandHandler("cen", registrar_cena))
    telegram_app.add_handler(CommandHandler("me", registrar_merienda))
    telegram_app.add_handler(CommandHandler("ftoday", ver_resumen_hoy))

    # Arranca a escuchar mensajes de forma directa
    telegram_app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()