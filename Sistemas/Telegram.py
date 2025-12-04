import requests
import os
import time
from dotenv import load_dotenv


load_dotenv("C:/Users/thiago_duarte/Desktop/Sistemas/.env")
TOKEN = os.getenv('TELEGRAM_TOKEN')
URL = f"https://api.telegram.org/bot{TOKEN}/"

print("TOKEN carregado:", TOKEN)

# Armazena quem já recebeu o menu inicial
usuarios_iniciados = {}

# Lista de saudações
saudacoes = ["oi", "olá", "ola", "boa tarde", "bom dia", "boa noite", "ei", "eae", "opa"]


def get_updates(offset=None):
    """Recebe mensagens do Telegram."""
    url = URL + "getUpdates"
    if offset:
        url += f"?offset={offset}"
    return requests.get(url).json()


def send_message(chat_id, text):
    """Envia mensagem para o usuário."""
    requests.post(
        url=URL + "sendMessage",
        data={"chat_id": chat_id, "text": text}
    )


def enviar_menu(chat_id):
    """Envia o MENU completo."""
    send_message(chat_id,
        "👋 *Bem-vindo ao Banco Infinity!*\n\n"
        "Selecione uma opção:\n"
        "1️⃣ Saldo\n"
        "2️⃣ Ajuda\n"
        "3️⃣ Falar com o gerente\n"
        "4️⃣ Promoções\n\n"
        "Digite o número da opção."
    )


def process_message(update):
    message = update.get("message", {})
    chat_id = message["chat"]["id"]
    text = message.get("text", "").lower().strip()

    # 1️⃣ PRIMEIRO CONTATO — sempre mostra o menu
    if chat_id not in usuarios_iniciados:
        usuarios_iniciados[chat_id] = True
        enviar_menu(chat_id)
        return

    # 2️⃣ SAUDAÇÕES — sempre mostra o menu
    if any(s in text for s in saudacoes):
        enviar_menu(chat_id)
        return

    # 3️⃣ MENU manual
    if text in ["/start", "menu"]:
        enviar_menu(chat_id)
        return

    # 4️⃣ OPÇÕES DO BANCO
    if text == "1":
        send_message(chat_id, "💰 Seu saldo atual é: *R$ 3.298,45*")
        return

    if text == "2":
        send_message(chat_id,
            "📞 *Central de Ajuda*\n"
            "Envie sua dúvida.\n"
            "- Como transferir dinheiro\n"
            "- Problemas no cartão\n"
            "- Abrir conta"
        )
        return

    if text == "3":
        send_message(chat_id,
            "👨‍💼 Seu gerente foi acionado!\nAguarde um instante..."
        )
        return

    if text == "4":
        send_message(chat_id,
            "🎉 *Promoções do Banco Infinity*\n"
            "- Cashback\n"
            "- Pontos em dobro\n"
            "- Descontos exclusivos"
        )
        return

    # 5️⃣ NÃO ENTENDI — somente se não for saudação e nem opção
    send_message(chat_id,
        "❓ Não entendi.\nDigite *menu* para ver as opções."
    )


def main():
    offset = None
    print("🤖 Banco Infinity Bot iniciado...")

    while True:
        updates = get_updates(offset)

        results = updates.get("result", [])

        if results:
            for update in results:
                process_message(update)
                offset = update["update_id"] + 1

        time.sleep(1)


main()
