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

with open("APIKEY", "r") as f:
    vk_token = f.read()

vk = vk_api.VkApi(token=vk_token)
longpoll = VkBotLongPoll(vk, 220213931)
print("☑️Бот запущен")

# f_token = "eyJhbGciOiJSUzI1NiIsImtpZCI6Imluc18yTzZ3UTFYd3dxVFdXUWUyQ1VYZHZ2bnNaY2UiLCJ0eXAiOiJKV1QifQ.eyJhenAiOiJodHRwczovL2FjY291bnRzLmZvcmVmcm9udC5haSIsImV4cCI6MTY4Mjg1MDAyNSwiaWF0IjoxNjgyODQ5OTY1LCJpc3MiOiJodHRwczovL2NsZXJrLmZvcmVmcm9udC5haSIsIm5iZiI6MTY4Mjg0OTk1NSwic2lkIjoic2Vzc18yUDhzSWhUOXM0UGd1N2JIMU8yaFpFbnh2dkkiLCJzdWIiOiJ1c2VyXzJQOHNJZE5WR01qYjFyRnZsR1BVNnVwNlJMSCJ9.Mr99GCZbEmm8FHYREV079-6BlQY09FndpcsBnJQrm7BjAUYCgJtYVeQx-3cJEsTAEBuCMBAzFabh4zyV_05xLmNekrhFT9hbvFzhi9w7phIf7cSHFiD43NpMYyczDV-MIIptI4ZTtbCui9pRQ4_Qf1NXPVRqLZUVMptydSgZgycQLnDg3cvLZjfP_R_c7K4zUKTknaDWhX8bNnYxSNXrr_zH8a3d2E6CD75bZTHKI5mh-KzxqZJMhUsiaw2lT8YgjWK8fGXYhoaVx15G55lnLmGki7gB0Lc12hnZRb3N1c8LxcvSP-jlyrd54qrl9KgVetK70KVQBSmWgwNKX55UTA"
f_token = fr.Account.create(logging=True)
print("☑️Токен Forefront получен: " + f_token)

start_prompt = "hello"
smart_mode = True
chat_id = ""

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
                answer = ""
                if smart_mode:
                    for response in fr.StreamingCompletion.create(token=f_token,
                                                                  prompt=start_prompt, model='gpt-4'):
                        answer += response.choices[0].text
                        chat_id = response.id

                print("response: " + answer)
                if answer == "":
                    answer = "чето проблемы какие то с апи"
                write_msg(event.chat_id, answer)
            elif request.startswith("?") and chat_id != "":
                print("Получено сообщение:", request)
                answer = ""
                if smart_mode:
                    for response in fr.StreamingCompletion.create(token=f_token,
                                                                         prompt=request, model='gpt-4', chat_id=chat_id, action_type="continue"):
                        print(response)
                        answer += response.choices[0].text
                        chat_id = response.id
                    print("")

                print("response: "+answer)
                if answer == "":
                    answer = "че"
                write_msg(event.chat_id, answer)

# # get a response
# for response in fr.StreamingCompletion.create(token=token,
#                                                      prompt='hello world', model='gpt-4'):
#     print(response.choices[0].text, end='')
# print("")

