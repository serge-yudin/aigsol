<h1>Demanda Real Visualization API</h1>

<p>This API provides access to a visualization of the Demanda Real, which is a real-time demand forecast of the Spanish electricity grid. The visualization is available through the '/indicators' endpoint, which requires the following parameters:</p>

<ul>
	<li>id: int</li>
	<li>start_date: date</li>
	<li>end_date: date</li>
</ul>

<p>To access the visualization, make a GET request to the '/indicators' endpoint with the required parameters in the query string, as shown in the following example:</p>

<pre><code>api_uri:port/indicators?id=1923&amp;start_date=2020-01-01&amp;end_date=2020-01-10</code></pre>

<p>If successful, the endpoint will return a PNG image of the Demanda Real visualization. If an error occurs, the endpoint will return an HTTPException with a status code and error message.</p>

<p>In addition, the API provides a '/' endpoint that returns a JSON response containing a message indicating how to access the visualization of Demanda Real.</p>

<h2>Usage</h2>

<ol>
<li>Clone the repository.</li>
<li>Create an isolated environment python3 -m venv {env_name}</li>
    <li>Activate your environment user@pc$ source {env_name}/bin/activate
		<li>Install the required packages with <code>pip install -r requirements.txt</code>.</li>
		<li>Set the API key in the <code>credentials.py</code> file.</li>
		<li>Run the API with <code>uvicorn main:app --reload</code>.</li>
		<li>Access the API with a GET request to the 'http://localhost:8000/' endpoint.</li>
    <li>To test API use 'http://localhost:8000/docs](http://localhost:8000/docs#/default/get_indicators_indicators_get' link</li>
	</ol>
