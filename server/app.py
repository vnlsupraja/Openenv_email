from fastapi import FastAPI
from env.environment import EmailEnv
from env.tasks import EasyTask
import os

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

@app.post("/openenv/reset")
def openenv_reset():
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

@app.post("/openenv/step")
def openenv_step(action: dict):
    return step(action)

@app.get("/openenv/state")
def openenv_state():
    return env.state()

def main():
    import uvicorn
    port = int(os.getenv("PORT", "7860"))
    uvicorn.run("server.app:app", host="0.0.0.0", port=port, reload=False)

if __name__ == "__main__":
    main()

