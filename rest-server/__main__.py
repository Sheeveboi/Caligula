import disc;
import asyncio;
import fb;
import web;
import threading;
import db;
import cmd;

discord = None;

async def onReady(c) :
    
    print("Ready!");

if __name__ == '__main__' :
    
    db.cacheFunctions();
    
    discord = disc.Events();
    
    discord.onReady = onReady;
    
    threading.Thread(target = web.run, name = "webserver thread").start();
    
    try : discord.run();
    except KeyboardInterrupt : print("testMain stopped by user");