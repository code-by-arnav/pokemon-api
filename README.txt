how to use code :
get the repo , open the folder , open the terminal
to get libraries downloaded type python -m venv venv than .\venv\Scripts\Activate.ps1 than pip install -r requirements.txt
ALL SET NOW TO ACTIVATE WEBSITE type uvicorn app.main:app --reload
to open the web type http://127.0.0.1:8000/(.......)

things u can do in (.....):
/health checks the server is working
/pokemon/<pokemon full name or ID> gives details of pokemon , if full name of pokemon is not know than use
/pokemon/search?name=<....>
/pokemon?type=<type of pokemon> if name is not know

ERROR can occur
/pokemon/<not a pokemon fullname> than 404 will be returen
/pokemon?type=banana not a valid type
/pokemon/search?name=zzzzz no matches
/pokemon/search?name=  empty name
if pokiapi is don=wn than 502 and if slow than 504

HOW THINGS WORK OUT 
1 )after typing "uvicorn app.main:app --reload" in terminal than uvicorn gets activate which actually get and give requests and result
now python runs main.py top to bottom and every othe rfiles fn get registerd for now  and app = FastAPI() creates like a object as @app.exception_handler(...) and @app.get(...) line registers a function in FastAPI’s lists: “for this error, run this handler” and “for this method and path, run this function.”
nothing has been run yet 
2 )now u type a url like http://127.0.0.1:8000/pokemon/pikachu , it sends it to 127.0.0.1, port 8000. 127.0.0.1 means “this computer”, so the request never leaves your machine
fastapi looks through its list of registered routes for one that matches GET /pokemon/pikachu. It checks in order. /health doesn’t match, and /pokemon/search doesn’t match, because the path says pikachu, not search. /pokemon/{name_or_id} matches, with name_or_id = "pikachu"
FastAPI calls your route function, in main.py
route fn calls get_pokemon
now get_pokemon builds the PokéAPI address https://pokeapi.co/api/v2/pokemon/pikachu
fetch uses HTTPX to send the request, and that your backend is now the client. Then PokéAPI answers with raw data
for errors related to timed out,connection failed fetch raises error handlors
otherwise get_pokemon do the furthur stuff and error related to wrong url fromuser
than fastapi do the fn which is executed and uvicorn than response witht he result