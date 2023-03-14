"""
This API provides access to visualization of Demanda Real.

Endpoint '/':
    GET request to '/' will return a JSON response containing a message indicating how to access the visualization of Demanda Real. 

Endpoint '/indicators':
    GET request to '/indicators' requires the following parameters:
        - id: int
        - start_date: date
        - end_date: date
    Example request:
        api_uri:port/indicators?id=1923&start_date=2020-01-01&end_date=2020-01-10

    If successful, this endpoint will return a PNG image of the Demanda Real visualization.
    If an error occurs, the endpoint will return an HTTPException with a status code and error message.
"""

from datetime import date

from fastapi import FastAPI, Response, HTTPException
from fastapi.responses import JSONResponse

from esios_ree.input_validators import Indicators
from esios_ree.esios_ree import EsiosReeDataFetcher, EsiosReeVisualizer
from credentials import API_KEY

app = FastAPI()


@app.get('/')
def index():
    msg = '''To get visualization of Demanda Real use GET request to /indicators\\nproviding id: int, start_date: date, end_date: date.\\nExample: api_uri:port/indicators?id=1923&start_date=2020-01-01&end_date=2020-01-10
    '''
    return JSONResponse(content={'message': msg})


@app.get('/indicators')
def get_indicators(id: int, start_date: date, end_date: date):
    indicators = Indicators(id=id, start_date=start_date, end_date=end_date)
    try:
        fetcher = EsiosReeDataFetcher(API_KEY)
    except Exception as e:
        raise HTTPException(status_code=401, detail=e.message)
    res, error = fetcher.get_data_of_indicators(
        id=indicators.id, start_date=indicators.start_date, end_date=indicators.end_date)
    if res:
        viz = EsiosReeVisualizer()
        img = viz.draw_indicators(fetcher.data, fetcher.meta_info())
        return Response(content=img.getvalue(), media_type='image/png')
    raise HTTPException(status_code=422, detail=error)
