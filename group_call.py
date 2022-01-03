from telethon.sync import TelegramClient
from telethon import functions, types
from telethon import errors
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.messages import ImportChatInviteRequest

from pytgcalls import idle
from pytgcalls import PyTgCalls
from pytgcalls import StreamType
from pytgcalls.types.input_stream import InputAudioStream
from pytgcalls.types.input_stream import InputStream
import os
import time

def check_group_calling(client, input_group_call):
    result = client(functions.phone.GetGroupCallRequest(call=input_group_call))
    if result.participants:
        return True
    else:
        return

def invite_users_to_call(client, input_group_call, list_user):
    try:
        result = client(functions.phone.InviteToGroupCallRequest(call=input_group_call,users=list_user))
        return result
    except Exception as E:      # RPCError 400: USER_ALREADY_INVITED >> Handle???
        print(E)

def create_group_call(client, group, tittle=None, schedule=None): # schedule: Datetime datatypes
    try:
        result = client(functions.phone.CreateGroupCallRequest(peer=group,title=tittle,schedule_date=schedule))
        return result
    except errors.ScheduleDateInvalidError:
        print("There is a problem with scheduler time, please change it an reuse this function.")

def join_call(client, input_group_call, params):
    result = client(functions.phone.JoinGroupCallRequest(
        call=input_group_call,
        join_as='me',
        params=types.DataJSON(data="me")
        ))
    
    print(result.stringify())

def join_clone_to_group(client, link_group):
    access_hash = link_group.split("/")[-1]
    
    try:
        client(ImportChatInviteRequest(access_hash))
    except errors.InviteHashEmptyError:
        print("Provided group link is not valid. Check group link again!")
    except errors.InviteHashExpiredError:
        try:
            client(functions.channels.JoinChannelRequest(link_group))
        except (ValueError, errors.ChannelInvalidError):
            print("Provided group link cant be found. Check group link again!")
        except (errors.ChannelsTooMuchError, errors.ChannelPrivateError):
            print("Cant join group because of you are join too much group, or group is private, or youre banned from it")


def main_invite_group_call(client, link_group, invite_users_list, leave_after_call=False, delay_join_call=0):
    '''
    ATTENTION!!: This function worked only if group is now calling.
    To make sure this function work, create a call with `create_group_call()`, and then use this function.
    You must be the participant of that voice call.
    Return `True` if sucessful, `None` if not sucess.
    '''
    try:
        for message in client.iter_messages(link_group):
            input_call = None
            
            # Find group call
            try:
                input_call = message.action.call
                break
            except AttributeError: # Find messages but it isnt input group call object
                pass
        
        # If found a call, check that call is now calling or not. If check, invite users to call
        if input_call:
            if check_group_calling(client, input_call):
                invite_users_to_call(client, input_call, invite_users_list)
                return True
            
    except Exception as E:      # No user has "link_group" as username >> Handle??
        print(E)


# # Check client die or notin here.
# check_die(client). . .
client = TelegramClient("HuaHoan", 6911830, "5d923354cdc50f7c5f197ee192ef2abb")

client.connect()
link_group = "https://t.me/joinchat/9NSx17sf6BFjZjI1"
entity = client.get_entity(link_group)
client.disconnect()
