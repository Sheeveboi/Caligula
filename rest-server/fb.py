import asyncio;
import threading;
import json;
import logging;
import util;
import asyncRequests as requests;
from urllib.parse import urlencode;

config = util.getConfig();

DB_endpoint = config['Firebase']['DB_endpoint'];
AUTH_endpoint = config['Firebase']['AUTH_endpoint'];
CREATE_endpoint = config['Firebase']['CREATE_endpoint'];

logging.basicConfig(level = logging.ERROR, filename='error.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s');

#-=- data firebase functions -=-

#-- get auth data -- 
async def setAuth(email, password) :
    j = {
        "email" : email,
        "password" : password,
        "returnSecureToken" : True
    }
    global auth;
    auth = await requests.post(AUTH_endpoint, json = j);

#-- retrieve data from firebase --
async def getDbData(path) :
    a = { 'auth' : auth['idToken'] };
    return await requests.get("{0}{1}.json?{2}".format(DB_endpoint,path, urlencode(a)));

#-- append or update data of endpoint --     
async def patchDbData(path,key,value) :
    a = { 'auth' : auth['idToken'] };
    return await requests.patch("{0}{1}.json?{2}".format(DB_endpoint,path, urlencode(a)),json = {key: value});

#-- replace or update data of endpoint --    
async def putDbData(path,key,value) :
    a = { 'auth' : auth['idToken'] };
    return await requests.put("{0}{1}.json?{2}".format(DB_endpoint,path, urlencode(a)),json = {key: value});  
 
#-- remove endpoint -- 
async def removeDbData(path) :
    a = { 'auth' : auth['idToken'] };
    return await requests.delete("{0}{1}.json?{2}".format(DB_endpoint,path, urlencode(a)));
  
#-- adds new auth user --
async def createDbUser(email,password) :
    j = {
        "email" : email,
        "password" : password,
        "returnSecureToken" : True
    }
    return await requests.post(CREATE_endpoint, json = j);
