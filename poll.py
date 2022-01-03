from telethon.sync import TelegramClient
from telethon import functions

# # # Pool function
from telethon.tl.types import InputMediaPoll, Poll, PollAnswer

def start_a_pool(client, entity, question, answers=[], id_pool=1234):
    # question: str, answers: list (Eg:["yes", "no"])
    # To start a pool, this function need at least 2 answers
    answers_list = []
    for i in range(len(answers)):
        answers_list.append(PollAnswer(str(answers[i]), str(i)))

    result = client.send_message(entity, file=InputMediaPoll(poll=Poll(
        id=id_pool,question=question, answers=answers_list)
        ))
    if result:
        print(question, "Pool created sucessfully!")
        for message in client.iter_messages(entity, limit=1):
            return(message.id, len(answers_list))

def send_a_vote(client, entity, msg_id, answer_option, answers_amount=None):
    # This function can changing a voted answer from an user
    # answer_option must have integer datatype because it is the index of answers
    # Eg: Pool have these answers: ["answer a", "answer b"] -> answers_amount=2 -> answer_option = "0" or = "1"
    result = client(functions.messages.SendVoteRequest(
        peer=entity,
        msg_id=msg_id,
        options=[str(answer_option)]
    ))
    if result:
        print("Voted/Change to a Pool sucessfully!")
# # # End pool function


# # # Quick example:
import random
# client = TelegramClient("session/877984215", 2127902, "b1b3812aadc2f934aff1cfd717acfdea")
client = TelegramClient("HuaHoan", 6911830, "5d923354cdc50f7c5f197ee192ef2abb")
client.connect()
entity = client.get_entity("https://t.me/group_call_test")
msg_id, answers_amount = start_a_pool(client, entity, "Are you gay?", answers=["yes", "no"])
answer_option = random.choice(range(answers_amount))
send_a_vote(client, entity, msg_id, answer_option)
client.disconnect()
