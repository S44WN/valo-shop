import re
import aiohttp
import asyncio
import json




async def run(username, password):

    # Creating an object called session to hold our cookies
    session = aiohttp.ClientSession()
    data = {
        'client_id': 'play-valorant-web-prod',
        'nonce': '1',
        'redirect_uri': 'https://playvalorant.com/opt_in',
        'response_type': 'token id_token',
    }


    # Let's make a post request to get those fucking required cookies
    await session.post('https://auth.riotgames.com/api/v1/authorization', json=data)



    ######################################
    # Now that we have the cookies, let's get access token, id token, and expiration time
    data = {
        'type': 'auth',
        'username': username,
        'password': password
    }


    async with session.put('https://auth.riotgames.com/api/v1/authorization', json=data) as r:
        data = await r.json()


    #print(data)
    pattern = re.compile('access_token=((?:[a-zA-Z]|\d|\.|-|_)*).*id_token=((?:[a-zA-Z]|\d|\.|-|_)*).*expires_in=(\d*)')

    data = pattern.findall(data['response']['parameters']['uri'])[0]

    access_token = data[0]

    print('Access Token: ' + access_token)

    id_token = data[1]

    expires_in = data[2]

    print(expires_in)




    ###########################################
    # For upcoming requests we need to set headers, so lets create a dictionary called headers
    headers = {
        'Authorization': f'Bearer {access_token}',
    }



    # Lets make the request and get entitlement token
    async with session.post('https://entitlements.auth.riotgames.com/api/token/v1', headers=headers, json={}) as r:
        data = await r.json()
    entitlements_token = data['entitlements_token']
    print('Entitlements Token: ' + entitlements_token)



  # Getting id
    async with session.post('https://auth.riotgames.com/userinfo', headers=headers, json={}) as r:
        data = await r.json()
    user_id = data['sub']
    print('User ID: ' + user_id)



    # Adding the entitlement token to headers. So we have entitlement token and access token  in our header
    headers['X-Riot-Entitlements-JWT'] = entitlements_token
    


    # Example Request. (Access Token and Entitlements Token need to be included! We are now ready to make any fucking request)
    async with session.get(f'https://pd.ap.a.pvp.net/store/v2/storefront/{user_id}', headers=headers) as r:
        data = await r.json()
        
    print('_'*10)
    print(data['SkinsPanelLayout']['SingleItemOffers'])

    await session.close()

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(run('AryanBa3a', 'NewValoPass#839'))

