import time;
import db;
import disc;
import util;
import json;
import asyncio;
import os;
import logging;
import logger;
import psycopg2;
from http.server import BaseHTTPRequestHandler, HTTPServer;
from urllib.parse import urlparse;
from urllib.parse import parse_qs;
from urllib.parse import unquote;

running = False;

config = util.getConfig();

sessionTokens = {};

hostName   = config["Web"]["host"];
serverPort = int(config["Web"]["port"]);

here = os.path.dirname(os.path.abspath(__file__));

logging.basicConfig(level = logging.ERROR, filename='error.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s');

getHandlers  = {};
postHandlers = {};
deleteHandlers = {};

def getHost()     : return hostName;
def getPort()     : return serverPort;
def getSessions() : return sessionTokens;
def getRunning()  : return running;

def addGetHandler(func, path) : 
    if (len(func.__code__.co_varnames[:func.__code__.co_argcount]) != 1) : 
        raise Exception("Specified callback function must only have one context parameter");
        return;
    getHandlers[path] = func;
    
def addPostHandler(func, path) : 
    if (len(func.__code__.co_varnames[:func.__code__.co_argcount]) != 1) : 
        raise Exception("Specified callback function must only have one context parameter");
        return;
    postHandlers[path] = func;
    
def addDeleteHandler(func, path) : 
    if (len(func.__code__.co_varnames[:func.__code__.co_argcount]) != 1) : 
        raise Exception("Specified callback function must only have one context parameter");
        return;
    deleteHandlers[path] = func;
    
def sendError(c, code, message) :
    
    c.send_response(code);
    c.send_header('Code',    code);
    c.send_header('Message', message);
    c.end_headers();

class MyServer(BaseHTTPRequestHandler):
    
    def do_GET(self) :
        
        try : 
            
            endpoint = self.path.split("?")[0];
                
            if (endpoint in getHandlers) :
                getHandlers[endpoint](self);
                return;
            
            paths = [*getHandlers]
            
            def sortKey(n) :
                match = 0;
                for char in n :
                    if   (n.index(char) >= len(endpoint))  : match -= 1;
                    elif (char == endpoint[n.index(char)]) : match += 1;
                    else                                   : match -= 1;
                return match;
                    
            paths.sort(key = sortKey, reverse = True);
            
            getHandlers[paths[0]](self);
            
        except Exception as e : logging.error("uh oh",exc_info=True);  
        
    def do_POST(self) :
        
        try : 
            
            endpoint = self.path.split("?")[0];
                
            if (endpoint in postHandlers) :
                postHandlers[endpoint](self);
                return;
            
            paths = [*postHandlers]
            
            def sortKey(n) :
                match = 0;
                for char in n :
                    if   (n.index(char) >= len(endpoint))  : match -= 1;
                    elif (char == endpoint[n.index(char)]) : match += 1;
                    else                                   : match -= 1;
                return match;
                    
            paths.sort(key = sortKey, reverse = True);
            
            if (len(paths) != 0) : postHandlers[paths[0]](self);
            
        except Exception as e : logging.error("uh oh",exc_info=True);
        
    def do_DELETE(self) :
        
        try :
        
            endpoint = self.path.split("?")[0];
                
            if (endpoint in deleteHandlers) :
                deleteHandlers[endpoint](self);
                return;
            
            paths = [*deleteHandlers]
            
            def sortKey(n) :
                match = 0;
                for char in n :
                    if   (n.index(char) >= len(endpoint))  : match -= 1;
                    elif (char == endpoint[n.index(char)]) : match += 1;
                    else                                   : match -= 1;
                return match;
                    
            paths.sort(key = sortKey, reverse = True);
            
            deleteHandlers[paths[0]](self);
            
        except Exception as e : logging.error("uh oh",exc_info=True);

    #the path that matches the most characters to the desired path is the one that will be selected

def echo(c) :
    
    c.send_response(200);
    c.end_headers();
    
    c.wfile.write(b'its as if they never even knew they were interesting'); 
    
    logger.log("echo succsess");
    
addGetHandler(echo, "/echo");

def handlePostFunctionRequest(c) :
    
    requiredHeaders = ['Function', 'Database'];
    
    for header in requiredHeaders :
        if (not header in c.headers) : 
            return sendError(c, 400, f"'{argument}' header not present in request.");
    
    functionName = c.headers['Function'];
    
    logger.log(f"-- executing post REST function {functionName}");

    arguments = c.rfile.read(int(c.headers['Content-Length']));
    arguments = json.loads(arguments.decode('utf-8'));
            
    tuple(arguments.items());
     
    out = db.runFunction(c.headers["Function"], arguments, c.headers['Database'], "post");
    
    if (not out) :
        c.send_response_only(404, message = "Database function not found for request method 'POST'.");
        return;
    
    out = bytes(str(out), 'utf-8');
    print(out);
    
    c.send_response(200);
    c.end_headers();
    c.wfile.write(out);
    
addPostHandler(handlePostFunctionRequest, "/functions");

def handleGetFunctionRequest(c) :
    
    requiredHeaders = ['Function', 'Database'];
    
    for header in requiredHeaders :
        if (not header in c.headers) : 
            return sendError(c, 400, f"'{argument}' header not present in request.");
    
    functionName = c.headers['Function'];
    
    logger.log(f"-- executing get REST function {functionName}");

    arguments = c.rfile.read(int(c.headers['Content-Length']));
    arguments = json.loads(arguments.decode('utf-8'));
            
    tuple(arguments.items());
     
    out = db.runFunction(c.headers["Function"], arguments, c.headers['Database'], "get");
    
    if (not out) :
        c.send_response_only(404, message = "Database function not found for request method 'GET'.");
        return;
    
    out = bytes(str(out), 'utf-8');
    print(out);
    
    c.send_response(200);
    c.end_headers();
    c.wfile.write(out);
    
addGetHandler(handlePostFunctionRequest, "/functions");

def run() :  
    running = True;
    webServer = HTTPServer((hostName, serverPort), MyServer);
    print("Webserver Started");
    webServer.serve_forever()