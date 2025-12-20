import time;
import fb;
import disc;
import util;
import json;
import asyncio;
import os;
import logging;
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
            
            postHandlers[paths[0]](self);
            
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
    
def serveFiles(c) :
    
    file = None;
    try    : file = open(os.path.join( here, c.path[1:len(c.path)] ), "rb");
    except : 
        sendError(c, 404, "what else could you possibly need?");
        return;
        
    data = file.read();      
    
    c.send_response(200);
    c.send_header('Content-Length', len(data));
    c.send_header('Content-Type', c.headers['Accept']);
    c.end_headers();
    
    c.wfile.write(data);
    
addGetHandler(serveFiles, "/src");

def serveSite(c) :
    
    parsedUrl = urlparse(c.path);
    query = parse_qs(parsedUrl.query);
    
    site = open(os.path.join(here,"src/index.html"), 'rb').read();
    
    print(site);
    
    sessionTokens[c.client_address[0]] = util.genKey(20);
    
    c.send_response(200);
    c.send_header('Content-Length', len(site));
    c.end_headers();
    
    c.wfile.write(site);
    
addGetHandler(serveSite, "/");

def handleFunctionRequest(c) :
    
    requiredHeaders = ['Function', 'Database'];
    arguments = [];
        
    if (not db.functionExists(functionName)) : return sendError(c, 400, "Function does not exist.");
    
    argumentMappings = db.getFunction(functionName)['arguments'];
    
    requiredHeaders += [argument for argument in argumentMappings];
    
    for header in requiredHeaders :
        
        if (not header in c.headers) : 
            return sendError(c, 400, f"'{argument}' header not present in request.");
        
        elif (header in argumentMappings) :
            
            mapping = argumentMappings[argument];
            
            if (type(mapping) == list) :
                for index in mapping : 
                    arguments.insert(index, c.headers[argument]);
            
            elif (type(mapping) == int) :
                arguments.insert(mapping, c.headers[argument]);
            
            else :
                return sendError(c, 500, f"Incorrect argument type for argument {argument}");
     

    tuple(arguments);
     
    db.runFunction(c.headers["Function"], arguments, c.headers['Database']);
    
    
addPostHandler(handleFunctionRequest, "/functions");

def run() :  
    running = True;
    webServer = HTTPServer((hostName, serverPort), MyServer);
    print("Webserver Started");
    webServer.serve_forever()