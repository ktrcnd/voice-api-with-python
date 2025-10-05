from fastapi import FastAPI, Request
import uvicorn

app = FastAPI()

@app.post("/v1/leads")
async def receive_lead(request: Request):
    data = await request.json()
    print("Received from Vapi.ai:", data)

    # Example: process or save to DB
    name = data.get("name")
    phone = data.get("phone")
    reason = data.get("reason")
    preferred_start = data.get("preferred_start")
    preferred_end = data.get("preferred_end")

    # You can save this into a database or trigger another workflow
    return {"status": "success", "message": "Lead received"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
