from fastapi import FastAPI, Query
from typing import List, Optional
from datetime import datetime
import httpx
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React app URL
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)



# Helper function to filter the data based on user inputs
def filter_data(data, start_date: str, end_date: str, min_revenue: int, max_revenue: int, min_net_income: int, max_net_income: int):
    start_date_obj = datetime.strptime(start_date, "%d-%m-%Y")
    end_date_obj = datetime.strptime(end_date, "%d-%m-%Y")
    
    filtered_data = []
    for record in data:
        record_date_obj = datetime.strptime(record['date'], "%Y-%m-%d")
        if start_date_obj <= record_date_obj <= end_date_obj:
            if min_revenue <= record['revenue'] <= max_revenue:
                if min_net_income <= record['netIncome'] <= max_net_income:
                    # Append the data as a dictionary
                    filtered_data.append({
                        "date": record['date'],
                        "revenue": record['revenue'],
                        "netIncome": record['netIncome'],
                        "eps": record['eps'],
                        "operatingIncome": record['operatingIncome']
                    })

    return filtered_data

# Endpoint to filter data based on user input
@app.get("/filter")
async def get_filtered_data(
    start_date: str = Query(..., example="15-02-2020"),
    end_date: str = Query(..., example="11-04-2022"),
    min_revenue: int = Query(..., example=300000000000),
    max_revenue: int = Query(..., example=400000000000),
    min_net_income: int = Query(..., example=50000000000),
    max_net_income: int = Query(..., example=100000000000)
):
    # URL for the Financial Modeling Prep API
    url = "https://financialmodelingprep.com/api/v3/income-statement/AAPL?period=annual&apikey=MsChYUKjNo1e4UnIt7tFEXdtD8Jfz1fx"
    
    # Fetch the data from the API using httpx
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        data = response.json()

    # Filter the data based on the user's criteria
    filtered_data = filter_data(data, start_date, end_date, min_revenue, max_revenue, min_net_income, max_net_income)
    
    return {"filtered_data": filtered_data}
