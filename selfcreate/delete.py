import json
import requests
from dbconnect import run_query
data = """ You are a human brain replica named "Divya" You can perform all CURD operations in this Database schema but the ultimate thing is to decide yourslef whether the following input needs to be stored in a Human brain. 
You can create any extra tables or delete existing rows of data or update columsn add new ones Just like the way humans learn new things by just updating their brain. 
The schema is : 
{
  "meta": {
    "schema_version": "2.0.0",
    "dialect": "postgresql",
    "description": "Universal multimodal memory schema for selfcreate agent"
  },
  "tables": 
  "liked_locations":{
    "id":"SERIAL UNIQUE ID",
    "location" : "varchar(255)",'
    "type":".varchar(255)"
  }
  },
  "bootstrap_sql": [

  ]
}
Out put rules : 
- If a simple response is sufficent then generate a simple response and have the DB_QUERY set to "None" 
- If the given input requires both a response and a DB_QUERY then respond with both.
- No explnations to your responses. 
- Update the table columns if the input is similar to the table and requires another mentioning column
- Create table if it is not already created or updated
- Always repond in the same format like below : 
{{ "importance": "CONSIDER or NOT_CONSIDER", 
"memory_type": "TEMPORARY, SHORT_TERM, or LONG_TERM", 
"expire_time": number or null, 
"response": "your reply", 
"DB_QUERY": "SELECT ... or WITH ... or null" }}
 """
def generate_response(user_input):
    url = "https://myai.ganiisunkara.workers.dev"

    headers = {
        "Authorization": "Bearer 12345678",
        "Content-Type": "application/json",
    }

    data = {
        "prompt": user_input,
    }

    response = requests.post(url, headers=headers, json=data)
    res = json.loads(response.text)
    # print("LLM RAW RESPONSE:", res["DB_QUERY"])
    print("LLM RAW RESPONSE:", res)
    print(res['response']['DB_QUERY'])
    run_query(query = res['response']['DB_QUERY'])

finalPrompt = f'''
{
    data
}
The input is :
I would like to stay at sagar nagar beach for a minimum of 2 hours every weekend Add it to ur memory.
'''

generate_response(finalPrompt)
# generate_response("Hi how are YOu?")