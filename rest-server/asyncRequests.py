import aiohttp;
import asyncio;
import json as JSON;

async def get(url, headers = {}, json = None) :
    headers['content-type'] = "application/json; charset=UTF-8";
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers = headers, json = json) as response:
            data = await response.read();
            return JSON.loads(data);
            
async def post(url, headers = {}, json = None) :
    headers['content-type'] = "application/json; charset=UTF-8";
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers = headers, json = json) as response:
            data = await response.read();
            try    : return JSON.loads(data);
            except : return None;
            
async def put(url, headers = {}, json = None) :
    headers['content-type'] = "application/json; charset=UTF-8";
    async with aiohttp.ClientSession() as session:
        async with session.put(url, headers = headers, json = json) as response:
            data = await response.read();
            try    : return JSON.loads(data);
            except : return None;
            
async def patch(url, headers = {}, json = None) :
    headers['content-type'] = "application/json; charset=UTF-8";
    async with aiohttp.ClientSession() as session:
        async with session.patch(url, headers = headers, json = json) as response:
            data = await response.read();
            try    : return JSON.loads(data);
            except : return None;
            
async def delete(url, headers = {}, json = None) :
    headers['content-type'] = "application/json; charset=UTF-8";
    async with aiohttp.ClientSession() as session:
        async with session.delete(url, headers = headers, json = json) as response:
            data = await response.read();
            try    : return JSON.loads(data);
            except : return None;