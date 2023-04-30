from vk_api.keyboard import VkKeyboard, VkKeyboardColor

from gpt4free import forefront as fr, quora
import gpt4free
import vk_api.bot_longpoll
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id


def write_msg(id, message):
    vk.method('messages.send', {'chat_id': id, 'message': message, "random_id": get_random_id()})


def send_keyboard(id, message, keyboard):
    vk.method('messages.send', {'chat_id': id, 'message': message, "random_id": get_random_id(), "keyboard": keyboard})


def generate_answer(text):
    global u_parent_msg
    req = gpt4free.usesless.Completion.create(prompt=text, parentMessageId=u_parent_msg)
    u_parent_msg = req["id"]
    return req["text"]


with open("APIKEY", "r") as f:
    vk_token = f.read()

vk = vk_api.VkApi(token=vk_token)
longpoll = VkBotLongPoll(vk, 220213931)
print("☑️Бот запущен")

start_prompt = "hello"
u_parent_msg = ""






for event in longpoll.listen():
    # Если пришло новое сообщение
    if event.type == VkBotEventType.MESSAGE_NEW:
        if event.from_chat:
            # Сообщение от пользователя
            request = event.message["text"]

            # Каменная логика ответа
            if request == "скейт":
                write_msg(event.chat_id, "😍😍😍")
            elif request == "к? настройки?":
                k = VkKeyboard(one_time=True)
                k.add_button("Режим скейтер", color=VkKeyboardColor.NEGATIVE)
                k.add_button("Режим терминатор", color=VkKeyboardColor.POSITIVE)
                send_keyboard(event.chat_id, "ну кароче типа вот", k.get_keyboard())
            elif request == "к? скейтер":
                write_msg(event.chat_id, "ненене")
                # smart_mode = False
            elif request == "к? терминатор":
                smart_mode = True
            elif request == "к? старт":
                pass
            #    тут чета будет мне лень
            elif request.startswith("?"):
                write_msg(event.chat_id, generate_answer(request))

