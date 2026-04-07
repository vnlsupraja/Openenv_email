from fastapi import FastAPI
from env.environment import EmailEnv
from env.tasks import EasyTask

app = FastAPI()
env = EmailEnv(EasyTask())

@app.get("/")
def root():
    return {"status": "running", "environment": "OpenEnv Email Triage"}

@app.get("/state")
def state():
    return env.state()

@app.post("/reset")
def reset():
    return env.reset()

@app.post("/step")
def step(action: dict):
    from env.models import Action
    obs, reward, done, info = env.step(Action(**action))
    return {
        "observation": obs.dict(),
        "reward": reward.dict(),
        "done": done,
        "info": info
    }

def main():
    import uvicorn
    uvicorn.run("server.app:app", host="0.0.0.0", port=8000, reload=True)

if __name__ == "__main__":
    main()

