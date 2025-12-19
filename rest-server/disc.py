import websockets;
import asyncio;
import threading;
import time;
import json;
import os;
import logging;
import fb;
import re;
import inspect;
import logger;
import util;
import requests as sync_requests;
import asyncRequests as requests;
from urllib.parse import urlencode;
from websockets.sync.client import connect;
from requests_toolbelt.multipart.encoder import MultipartEncoder;
from os import environ;

config = util.getConfig();

discKey = config["Discord"]["token"];
prefix = config["Discord"]["prefix"];
tokenType = config["Discord"]["token_prefix"];
fullEndpoint = config["Discord"]["api_endpoint"];
securityServers = config["Discord"]["security_server_ids"];
securityRoles = config["Discord"]["security_role_ids"];

logging.basicConfig(level = logging.ERROR, filename='error.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s');

global user;
user = None;

def getSelf() : return user;
def getKey()  : return discKey;

def checkRoles(uid) :
    
    headers = { "Authorization" : f"Bot {discKey}" };
    
    out = False;
    
    for guild in securityServers :
        
        r = sync_requests.get(f"{fullEndpoint}/guilds/{guild}/members/{uid}", headers = headers);
        data = r.json();
        
        if (not r.status_code in [404, 403, 400, 401]) : 
        
            out = any((int) (roleId) in securityRoles for roleId in data['roles']);
            if (out) : break;
        
    return out;

#-- gets discord messages --
async def getMessages(channelID) :
    while True:
        headers = {
            'Authorization' : tokenType + discKey
        }
        r = await requests.get(fullEndpoint + f'/channels/{channelID}/messages', headers = headers);
        if (type(r) == list) : return r;
        elif ('code' in r and int(r['code']) == 31008) : time.sleep(int(r['reply-after']));
        else : return None;
 
#-- deletes discord messages in bulk -- 
async def deleteBulkMessages(channelID, msgs) :
    while True:
        headers = {
            'Authorization' : tokenType + discKey,
        }
        data = {
            'messages' : msgs
        }
        r = await requests.post(fullEndpoint + f'/channels/{channelID}/messages/bulk-delete', headers = headers, json = data);
        try : 
            if ('id' in r) : return r;
            elif ('code' in r and int(r['code']) == 31008) : time.sleep(int(r['reply-after']));
            else : return None;
        except : return None;

#-- delete discord message --     
async def deleteMessage(channelID, messageID) :
    while True:
        headers = {
            'Authorization' : tokenType + discKey
        }
        r = await requests.delete(fullEndpoint + f'/channels/{channelID}/messages/{messageID}', headers = headers);
        try :
            if ('code' in r and int(r['code']) == 31008) : time.sleep(int(r['reply-after']));
            else : return None;
        except : return None;

#-- create/get user DM --
async def getDM(uid):
    while True:
        headers = {
            'Authorization' : tokenType + discKey
        }
        data = { "recipient_id" : uid }
        r = await requests.post(fullEndpoint + f'/users/@me/channels', headers = headers, json = data);
        if ('id' in r) : return r;
        elif ('code' in r and int(r['code']) == 31008) : time.sleep(int(r['reply-after']));
        else : return None;

# -- get discord message --
async def getMessage(channelID,messageID):
    while True:
        headers = {
            'Authorization' : tokenType + discKey
        }
        r = await requests.get(fullEndpoint + f'/channels/{channelID}/messages/{messageID}', headers = headers);
        if ('id' in r) : return r;
        elif ('code' in r and int(r['code']) == 31008) : time.sleep(int(r['reply-after']));
        else : return None;

#-- get all channels of a guild -- 
async def getGuildChannels(guildID):
    while True:
        headers = {
            'Authorization' : tokenType + discKey
        }
        r = await requests.get(fullEndpoint + f'/guilds/{guildID}/channels', headers = headers);
        if (type(r) == list) : return r;
        elif ('code' in r and int(r['code']) == 31008) : time.sleep(int(r['reply-after']));
        else : return None;

# -- get discord channel--
async def getChannel(channelID) :
    while True:
        headers = { 'Authorization' : tokenType + discKey }
        r = await requests.get(fullEndpoint + f'/channels/{channelID}', headers = headers);
        if ('id' in r) : return r;
        elif ('code' in r and int(r['code']) == 31008) : asyncio.sleep(int(r['reply-after']));
        else : return None;
        
# -- get discord channel webhooks--
async def getChannelWebhooks(channelID) :
    while True:
        headers = { 'Authorization' : tokenType + discKey }
        r = await requests.get(fullEndpoint + f'/channels/{channelID}/webhooks', headers = headers);
        if ('code' in r and int(r['code']) == 31008) : asyncio.sleep(int(r['reply-after']));
        elif (len(r) > 0) : return r;
        else : return None;
 
#-- creates discord webhook -- 
async def createWebhook(channelID, name) :
    while True:
        headers = { 'Authorization' : tokenType + discKey };
        data = { "name" : name };
        r = await requests.post(fullEndpoint + f'/channels/{channelID}/webhooks', headers = headers, json = data);
        if ('code' in r and int(r['code']) == 31008) : asyncio.sleep(int(r['reply-after']));
        elif (len(r) > 0) : return r;
        else : return None;

#-- sends a message using a discord webhook --        
async def sendWebhookMsg(channelID, webhookID, webhookToken, msg = None, name = None, avatar = None, files = None, embeds = None, threadID = None) :
    while True:
        headers = { 'Authorization' : tokenType + discKey };
        query = { "wait" : True }
        if (threadID) : query['thread_id'] = threadID;
        
        data = {
            "content"    : msg,
            "username"   : name,
            "avatar_url" : avatar,
            "embeds"     : embeds,
        }
        send = dict();
                
        send['payload_json'] = (None, json.dumps(data), "application/json");  
        if (files) :
            for file in files : 
                att = attachments[files.index(file)];
                send[att['filename']] = (att['filename'], file, att['content_type']);
        
        mp_encoder = MultipartEncoder(fields = send); #encode for sending
        headers['Content-Type'] = mp_encoder.content_type;
          
        r = await requests.post(fullEndpoint + f"/webhooks/{webhookID}/{webhookToken}?{urlencode(query)}", headers = headers, data = mp_encoder.to_string());
        if ('id' in r) : return r;
        elif ("retry_after" in r or "reply_after" in r) : await asyncio.sleep(int(r['retry_after']) * 3);
        else : return None;
        
# -- get normal user --
async def getUser(uid) :
    while True:
        headers = { 'Authorization' : tokenType + discKey }
        r = await requests.get(fullEndpoint + f'/users/{uid}', headers = headers);
        if ('id' in r) : return r;
        elif ('code' in r and int(r['code']) == 31008) : asyncio.sleep(int(r['reply-after']));
        else : return None;

# -- send message --
async def sendMsg(channelID, message, reference = None, attachments = None, embeds = None): 
    while True:
        data = {
            "content" : message,
            "tts" : False
        }
        if (reference) : data['message_reference'] = { "message_id" : reference };
        if (embeds) : data['embeds'] = embeds;
        headers = { 'Authorization' : tokenType + discKey }
        if (attachments) :
            files = dict();
            data['attachments'] = [];
            files['payload_json'] = (None, json.dumps(data), "application/json"); 
            for file in attachments:
                data['attachments'].append({ #add payload json 
                    'id' : attachments.index(file),
                    'description' : "none",
                    'filename' : file['filename']
                });
                d = await requests.get(file['url']);
                d = d.content;
                files[file['filename']] = (file['filename'], d, file['content_type']);
            r = await requests.post(fullEndpoint + f'/channels/{channelID}/messages', headers = headers, files = files);
            if (r == None) : return None;
            if ('id' in r) : return r;
            elif ('retry-after' in r or 'reply-after' in r) : await asyncio.sleep(int(r['retry-after']));
            else : return None;
        else :
            r = await requests.post(fullEndpoint + f'/channels/{channelID}/messages', headers = headers, json = data);
            if (r == None) : return None;
            if ('id' in r) : return r;
            elif ("retry_after" in r or "reply_after" in r) : await asyncio.sleep(int(r['retry_after']) * 3);
            else : return None;
            
commands = {};
def addCommand(cb, plaintext = False): 
    print(f"registered command {cb.__name__}");
    commands[cb.__name__] = {
        "cb" : cb,
        "plaintext" : plaintext
    }

class Events :
    def __init__(this,onReady = None,onConnection = None,onHeartbeat = None,onMessage = None):
        
        this.commandQueue = [];
        
        this.KEEPALIVE = None;
        this.tempLoop = None;
    
        this.onReady = None;
        this.onConnection = None;
        this.onHeartbeat = None;
        this.sendPayload = None;
        this.onMessage = None;
        
        this.gatewayUrl = None;
        this.heartbeatInterval = None;
        this.session_id = None;
        this.resume_gateway_url = None;
        this.guilds = None;
        
        this.initialize = True;
        
        this.heartbeatLoop = None;
        this.eventLoop = None;
        this.commandsLoop = None;
        
        this.eventThread = None;
        this.heartbeatThread = None;
        this.commandsThread = None;
    
    def updatePresence(this,text) :
        p = {
            "op": 3,
            "d": {
                "since": 91879201,
                "activities": [{
                    "name": text,
                    "type": 2
                }],
                "status": "online",
                "afk": False
                }
        }
        this.KEEPALIVE.send(json.dumps(p));
        data = this.KEEPALIVE.recv();
        return json.loads(data);

    async def startHeartbeat(this):
        try :
            print("Heartbeat started");
            while True :
                time.sleep(30);
                this.KEEPALIVE.send('{"op":1,"d":' + str(this.heartbeatInterval) + '}');
        except Exception as e : 
            logger.log("-- heartbeat error");
            logger.log(e);
            logger.log("");
            logging.error("uh oh",exc_info=True);  
            
    async def startEvents(this) :
        
        try :
            while True:
                print("Events started");
                
                #-- hello exchange --
                
                this.KEEPALIVE = connect("wss://gateway.discord.gg/?encoding=json&v=9",ping_timeout = None,close_timeout = None);
                data = this.KEEPALIVE.recv();
                data = json.loads(data);
                
                logger.log("-- hello exchange");
                logger.log(data);
                logger.log("");
                
                if (data["op"] == 10) :
                    print("Connection made");
                    if (str(type(this.onConnection)) == "<class 'function'>") :
                        await this.onConnection();
                        
                this.heartbeatInterval = data['d']['heartbeat_interval'];
                this.gatewayUrl = json.loads(data['d']['_trace'][0])[0];
                
                #-- heartbeat set --
                this.KEEPALIVE.send('{"op":1,"d":' + str(this.heartbeatInterval) + '}');
                this.KEEPALIVE.recv();
                    
                
                #-- identity exchange --
                identify = {
                              "op": 2,
                              "d": {
                                "token": discKey,
                                "intents": 33281,
                                "properties": {
                                  "os": "Windows", # dont ask why
                                  "browser": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:132.0) Gecko/20100101 Firefox/132.0",
                                  "device": "Win64"
                                }
                              }
                            }
                
                this.KEEPALIVE.send(json.dumps(identify));
                data = this.KEEPALIVE.recv();
                data = json.loads(data);
                
                logger.log("-- identity exchange");
                logger.log(data);
                logger.log("");
                                    
                #-- if identity exchange success --
                
                if (data["op"] == 0) :
                
                    this.session_id = data['d']['session_id'];
                    this.resume_gateway_url = data['d']['resume_gateway_url'];
                    global user;
                    user = data['d']['user'];
                    this.guilds = data['d']['guilds'];
                    
                    this.updatePresence(config["Discord"]["status"]);
                
                    if (str(type(this.onReady)) == "<class 'function'>") :
                        await this.onReady(data);
                    
                    this.initialize = False;    
                    
                while True:
                    try : data = this.KEEPALIVE.recv();
                    except :
                        print("Event loop restarting. Keep alive connection closed. Reconnecting..");
                        break;
                    data = json.loads(data);
                    this.sequence = 0;
                    if (data) :
                        if (data['s']) : this.sequence = int(data['s']);
                        if (int(data['op']) == 11) :
                            if (str(type(this.onHeartbeat)) == "<class 'function'>") :
                                await this.onHeartbeat(data);
                        elif (int(data['op']) == 0) :
                            if (data['t'] == "MESSAGE_CREATE") :
                            
                                content = data['d']['content'];
                                if (re.search(prefix, content)) : 
                                    commandName = content[len(prefix):].split()[0];
                                    if (commandName in commands) :
                                    
                                        givenArgs = [];
                                    
                                        if (commands[commandName]["plaintext"]) :
                                            
                                            givenArgs.append(content.replace(prefix + commandName, ""));
                                            
                                        else :
                                            
                                            givenArgs = content[(len(prefix) + len(commandName)) + 1:].split(', ');
                                            
                                            if (len(givenArgs[0]) == 0) : givenArgs.pop(0);
                                        
                                            tuple(givenArgs);
                                            
                                        givenArgs.insert(0, (dict) (data['d']));
                                            
                                        this.commandQueue.append( (commands[commandName]["cb"], givenArgs) );
                            
                                elif (str(type(this.onMessage)) == "<class 'function'>") :
                                    await this.onMessage(data['d']);
                            elif (data['t'] == "MESSAGE_UPDATE") :
                                try : await editChatMsg(discKey,data['d'],data['d']['content']);
                                except : pass;
                            elif (data['t'] == "MESSAGE_REACTION_ADD") :
                                try : await addChatReaction(discKey,data['d']);
                                except : pass;
                            elif (data['t'] == "MESSAGE_REACTION_REMOVE") :
                                try : await remChatReaction(discKey,data['d']);
                                except : pass;  
        except Exception as e : 
            logger.log("-- events error");
            logger.log(e);
            logger.log("");
            logging.error("uh oh",exc_info=True); 
                            
    async def startCommands(this) :
        try : 
            print("Commands Started");
            while True: 
                remove = [];
                for command in this.commandQueue : 
                    amOfArgs = command[0].__code__.co_varnames[:command[0].__code__.co_argcount]
                    if (len(command[1]) >= len(amOfArgs)) :
                        try : await command[0](*command[1]);
                        except Exception as e :
                            await sendMsg(command[1][0]['channel_id'], f"A Server side error occured when processing this command: {e}");
                            logging.error("Command error",exc_info=True); 
                    else : 
                        await sendMsg(command[1][0]['channel_id'], f"You are missing arguments! expected at least {len(amOfArgs) - 1} arguments but found {len(command[1]) - 1}.");
                    remove.append(command);
                for r in remove : this.commandQueue.remove(r);
        except Exception as e : 
            logger.log("-- commands error");
            logger.log(e);
            logger.log("");
            logging.error("uh oh",exc_info=True);  
                
    def run(this) :
    
        logger.initialize();
    
        def setHeartbeat() :
            try :
                print("Setting heartbeat..");
                this.heartbeatLoop = asyncio.new_event_loop();
                asyncio.set_event_loop(this.heartbeatLoop);
                this.heartbeatLoop.run_until_complete(this.startHeartbeat());
                logger.log("-- heartbeat set");
            except Exception as e :
                print("{!r}; Heartbeat thread exited!".format(e));
                logging.error("uh oh",exc_info=True); 
                
                resetEverything();
                
        def setEvents() :
            try :
                print("Setting events..");
                this.eventLoop = asyncio.new_event_loop();
                asyncio.set_event_loop(this.eventLoop);
                this.eventLoop.create_task(this.startEvents()); 
                this.eventLoop.run_forever();
                logger.log("-- events set");
            except Exception as e :
                print("{!r}; Event thread exited.".format(e));
                logging.error("uh oh",exc_info=True); 
                
                resetEverything();
                
        def setCommands() : 
            try :
                print("Setting commands..");
                this.commandLoop = asyncio.new_event_loop();
                asyncio.set_event_loop(this.commandLoop);
                this.commandLoop.create_task(this.startCommands());
                this.commandLoop.run_forever();
                logger.log("-- commands set");
            except Exception as e :
                print("{!r}; Command thread exited.".format(e));
                logging.error("uh oh",exc_info=True); 
                
                resetEverything();
        
        def resetEverything() :
        
            print("resetting everything");
            
            logger.log("-- resetting everything");
        
            if (this.heartbeatLoop) : this.heartbeatLoop.stop();
            if (this.eventLoop) : this.eventLoop.stop();
            
            if (this.eventThread and not this.eventThread.is_alive()) : 
                this.eventThread.join();
                this.eventThread = threading.Thread(target = setEvents, name = 'event thread');
                this.eventThread.start();
            elif (not this.eventThread) : 
                this.eventThread = threading.Thread(target = setEvents, name = 'event thread');
                this.eventThread.start();
                
            if (this.heartbeatThread and not this.heartbeatThread.is_alive()) : 
                this.heartbeatThread.join();    
                this.heartbeatThread = threading.Thread(target = setHeartbeat, name = 'heartbeat thread');
                this.heartbeatThread.start();
            elif (not this.heartbeatThread) :
                this.heartbeatThread = threading.Thread(target = setHeartbeat, name = 'heartbeat thread');
                this.heartbeatThread.start();
             
            if (this.commandsThread and not this.commandsThread.is_alive()) : 
                this.commandsThread.join();    
                this.commandsThread = threading.Thread(target = setCommands, name = 'command thread');
                this.commandsThread.start();
            elif (not this.commandsThread) :
                this.commandsThread = threading.Thread(target = setCommands, name = 'command thread');
                this.commandsThread.start();
            
        this.eventThread = threading.Thread(target = setEvents, name = 'event thread');
        this.heartbeatThread = threading.Thread(target = setHeartbeat, name = 'heartbeat thread');
        this.commandsThread = threading.Thread(target = setCommands, name = 'command thread');
        
        this.eventThread.start();
        this.heartbeatThread.start();
        this.commandsThread.start();
        
        this.eventThread.join();
        this.heartbeatThread.join();
        this.commandsThread.join();