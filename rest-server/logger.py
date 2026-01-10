import os;
import asyncio;
import util;
import disc;
import threading;
import queue;

config = util.getConfig();
loggingMessages = queue.Queue();

def run() :

    global loggingMessages;

    async def loggingTask() :
        
        print("Logging started");
        
        while True :
            
            if (not loggingMessages.empty()) : 
                    
                await disc.sendMsg(config["Discord"]["logging_channel"], loggingMessages.get());
                    
                loggingMessages.task_done();

    def setDiscordLoggingLoop() :
        
        print("Setting logging..");
        
        loggingLoop = asyncio.new_event_loop();
        asyncio.set_event_loop(loggingLoop);
        
        loggingLoop.create_task(loggingTask());
        
        loggingLoop.run_forever();

    threading.Thread(target = setDiscordLoggingLoop, name = "logging thread").start();

def initialize() :
    
    f = open("logging.txt", "w");
    f.write("Initialized log\n\n");
    f.close();
    
    run();
    
def log(text) :
    
    f = open("logging.txt", "a");
    f.write(f"{str(text)} \n");
    f.close(); 
    
    loggingMessages.put(f"**Log: ** {str(text)}");