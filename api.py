from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from ai_engine import classify_query
from salesforce_integration import sf_integration
import uvicorn

app = FastAPI(title="AI-Powered Helpdesk Automation", version="1.0.0")

class QueryRequest(BaseModel):
    customer_name: str
    query: str

class PredictionResponse(BaseModel):
    customer_name: str
    query: str
    category: str
    priority: str
    response: str
    confidence: float

class CaseCreationRequest(BaseModel):
    customer_name: str
    query: str
    escalated: bool = False

class CaseCreationResponse(BaseModel):
    customer_name: str
    query: str
    category: str
    priority: str
    response: str
    confidence: float
    salesforce_case_id: Optional[str] = None
    salesforce_status: Optional[str] = None
    escalated: bool

@app.post("/predict", response_model=PredictionResponse)
async def predict(request: QueryRequest):
    """
    Predict category, priority, and generate response for customer query.
    """
    try:
        result = classify_query(request.query)
        return PredictionResponse(
            customer_name=request.customer_name,
            query=request.query,
            category=result['category'],
            priority=result['priority'],
            response=result['response'],
            confidence=result['confidence']
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

@app.post("/create_case", response_model=CaseCreationResponse)
async def create_case(request: CaseCreationRequest):
    """
    Predict category, priority, generate response, and create Salesforce case.
    """
    try:
        # Get AI prediction
        result = classify_query(request.query)

        # Create Salesforce case
        sf_result = sf_integration.create_case(
            customer_name=request.customer_name,
            query=request.query,
            category=result['category'],
            priority=result['priority'],
            ai_response=result['response'],
            escalated=request.escalated
        )

        return CaseCreationResponse(
            customer_name=request.customer_name,
            query=request.query,
            category=result['category'],
            priority=result['priority'],
            response=result['response'],
            confidence=result['confidence'],
            salesforce_case_id=sf_result.get('case_id') if sf_result['success'] else None,
            salesforce_status=sf_result.get('status') if sf_result['success'] else None,
            escalated=request.escalated
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Case creation failed: {str(e)}")

@app.get("/")
async def root():
    return {"message": "AI-Powered Helpdesk Automation API", "status": "running"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
