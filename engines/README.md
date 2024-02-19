# Setup local

### Create a virtualenv

```
python -m venv env
```

### Activate virtual env (each time you want to start the project)

```
source env/bin/activate
```

### Install requirements

```
pip install -r requirements.txt
```

### Start an engine

```
cd engine_name
uvicorn app:engine.app --host 0.0.0.0 --port 3500 --reload
```

Now, you can go to `http://localhost:3500/docs/` to test engine deployement