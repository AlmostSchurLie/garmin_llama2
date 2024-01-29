Feeding data from GarminDB to llama2 and asking for feedback. 

Download your Garmin data with [GarminDB](https://github.com/tcgoetz/GarminDB), into a folder HealthData, which (for me) has a subfolder DBs that has one file, among others, named `summary.db`. This is the file that is used in the prompt to llama2. Replace the path in this line 
```
db_paths = {'summary': 'HealthData/DBs/summary.db'}
```
to wherever your `summary.db` from GarminDB is. Then run `llama2garmin.py`. The script makes use of the [ollama python library](https://github.com/ollama/ollama-python).


Disclaimer: This script is intended for research and is not meant to be used for medical advice.
