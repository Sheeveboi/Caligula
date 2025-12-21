import re;
import random;
import fb;
import time;
import disc;
import os;
import json;
from datetime import datetime;

here = os.path.dirname(os.path.abspath(__file__));

# -- create random strings --
def genKey(length):
    a = "abcdefghijklmnopqrstuvwxyz";
    oup = '';
    for x in range(length):
        rand = random.randrange(26)
        oup += a[rand]
    return oup;

# -- remove mentions --
def noMentions(s) : 
    try : 
        while re.search("@everyone", s) or re.search("@here", s):
            s = re.sub("@everyone", "", s, 1)
            s = re.sub("@here", "", s, 1)
        return s; #final product
    except Exception as e: logging.error("uh oh",exc_info=True);

# -- remove weird links --    
def noSusLinks(s) :
    try :
        i = re.search("http:\/\/\S{0,}", s);
        while i: 
            s = re.sub("http:\/\/\S{0,}", "`[Link removed]`", s, 1); 
            i = re.search("http:\/\/\S{0,}", s);
            
        i = re.search("https:\/\/\S{0,}", s);
        while i: 
            if (re.search("https:\/\/www.youtube.com", i.group())) : break;
            if (re.search("https:\/\/youtu.be", i.group())) : break;
            if (re.search("https:\/\/twitter.com", i.group())) : break;
            if (re.search("https:\/\/fxtwitter.com", i.group())) : break;
            if (re.search("https:\/\/vxtwitter.com", i.group())) : break;
            if (re.search("https:\/\/tenor.com", i.group())) : break;
            if (re.search("https:\/\/media.discordapp.net", i.group())) : break;
            s = re.sub("https:\/\/\S{0,}", "`[Link removed]`", s, 1); 
            i = re.search("https:\/\/\S{0,}", s);
        return s;
        
    except Exception as e: logging.error("uh oh", exc_info=True);

# -- remove all links --
def noLinks(s) :
    try :
        i = re.search("http:\/\/\S{0,}", s);
        while i: 
            s = re.sub("http:\/\/\S{0,}", "`[Link removed]`", s, 1); 
            i = re.search("http:\/\/\S{0,}", s);
            
        i = re.search("https:\/\/\S{0,}", s);
        while i: 
            if (re.search("https:\/\/media.discordapp.com", i.group())) : break;
            s = re.sub("https:\/\/\S{0,}", "`[Link removed]`", s, 1); 
            i = re.search("https:\/\/\S{0,}", s);
        return s;
        
    except Exception as e: logging.error("uh oh", exc_info=True);
    
def getConfig() :
    
    f = open(os.path.join(here, "config.json" ));
    d = f.read();
    return json.loads(d);
    
def clip(string) :
    
    if (string[0] == " ")               : string = string[1:];
    if (string[len(string) - 1] == " ") : string = string[:len(string) - 1];
    
    return string;
    
def parseArgumentQuery(string) :
    
    arguments = {};
    composites = string.split("=");
        
    currentKey = clip(composites[0]);
    
    for i in range(1, len(composites) - 1) :
        
        composite = clip(composites[i]);
        
        if (composite[0] == "'") :
            
            nextQuotation = re.search("'", composite[1:]).span()[1] + 1
            argument = composite[0:nextQuotation];
            
            arguments[currentKey] = str(argument).replace("'","")
            
            composite = composite.replace(argument, "");
            composite = composite.replace(",", "");
            composite = clip(composite);
            currentKey = composite;
            
        else :
            
            composite = composite.split(",")
            
            arguments[currentKey] = int(composite[0])
            currentKey = clip(composite[1])
            
    finalComposite = clip(composites[len(composites) - 1]);

    if (finalComposite[0] == "'") :
            
        nextQuotation = re.search("'", finalComposite[1:]).span()[1] + 1
        argument = finalComposite[0:nextQuotation];
        
        arguments[currentKey] = str(finalComposite.replace("'",""));
        
    else :
        
        finalComposite = finalComposite.split(",")
        
        arguments[currentKey] = int(finalComposite[0]);
   
    return arguments

    
    