from io import BytesIO
from datetime import date

import requests
import pandas as pd
import matplotlib.pyplot as plt
from pydantic import ValidationError, BaseModel, validator
from scipy.fft import fft


class Indicators(BaseModel):
    """
    Represents the indicators to be fetched from the API.

    Attributes:
        id (int): The ID of the indicator to fetch.
        start_date (date): The start date of the period for which to fetch the data.
        end_date (date): The end date of the period for which to fetch the data.

    Raises:
        ValueError: If the start date is not before the end date.
    """

    id: int
    start_date: date
    end_date: date

    @validator('start_date')
    def start_date_must_be_before_end_date(cls, v, values):
        if 'end_date' in values and v >= values['end_date']:
            raise ValueError('start_date must be before end_date')
        return v

    @validator('end_date')
    def end_date_must_be_after_start_date(cls, v, values):
        if 'start_date' in values and v <= values['start_date']:
            raise ValueError('end_date must be after start_date')
        return v


class EsiosReeDataFetcher:
    '''Fetches data from https://api.esios.ree.es/

    Attributes:
        api_key (str): The API key to use for authentication.

    Raises:
        TypeError: If no API key is provided.

    '''

    def __init__(self, api_key: str = None):
        self.__api_key = api_key
        self.__data = None
        self.__main_url = 'https://api.esios.ree.es/'
        self.__str = ''
        self.__check_api_key()

    def __check_api_key(self):
        if self.__api_key is None:
            raise TypeError(
                'Provide an API key. You can request your personal token at consultasios@ree.es')

    @property
    def data(self):
        """
        Returns the fetched data from the ESIOS API.
        """
        return self.__data

    def __fetch_data(self, url):
        url_to_fetch = url
        headers = {'x-api-key': self.__api_key, 'Accept': 'application/json; application/vnd.esios-api-v1+json',
                   'Content-type': 'application/json'}
        result = requests.get(url_to_fetch, headers=headers)
        if not result.ok:
            return False, result.reason

        self.__data = result.json()
        return True, None

    def get_data_of_indicators(self, id=None, start_date=None, end_date=None):
        """
        Fetches data from the ESIOS API for the given indicators and time period.

        Args:
            id (int): The ID of the indicator to fetch.
            start_date (date): The start date of the period for which to fetch the data.
            end_date (date): The end date of the period for which to fetch the data.

        Returns:
            A tuple with a boolean indicating if the operation was successful, and either the fetched data or an error message.
        """
        try:
            indicators = Indicators(
                id=id, start_date=start_date, end_date=end_date)
            url = f'{self.__main_url}indicators/{indicators.id}?start_date={indicators.start_date}&end_date={indicators.end_date}'
            success, message = self.__fetch_data(url)
            if not success:
                return (success, message)
            self.__str = f'Demanda Real {indicators.id}. De {indicators.start_date} a {indicators.end_date}'
            return (True, self.data)
        except ValidationError as e:
            return (False, e.errors())

    def __repr__(self):
        return f'EsiosReeDataFetcher - {self.__api_key}\n Data - {type(self.data)}'

    def meta_info(self):
        '''Returns ID, start_date and end_date of the last successful data fetch.'''
        return self.__str


class EsiosReeVisualizer:
    """
    Visualizes data from the ESIOS API.

    Attributes:
        plt (module): The matplotlib.pyplot module to use for visualization.
    """

    def __init__(self):
        self.plt = plt

    def fft_out(self, vals):
        """
        Computes the fast Fourier transform of the given data.

        Args:
            vals (array): The array of data to transform.

        Returns:
            The transformed data.
        """
        return fft(vals)

    def draw_indicators(self, data, title=''):
        """
        Draws the visualizations for the fetched data.

        Args:
            data (dict): The fetched data to visualize.
            title (str): The title to use for the visualization.

        Returns:
            The visualizations in bytes format.
        """
        df = pd.DataFrame.from_records(data['indicator']['values'])
        fig, axes = self.plt.subplots(2, 1)
        fig.suptitle(title)
        # image of demanda real
        axes[0].plot(df.datetime.values, df.value.values)

        # fast fourier transformation image
        axes[1].plot(df.datetime.values, self.fft_out(df.value.values))
        return self.save_as_bytes(fig)

    def save_as_bytes(self, fig):
        """
        Saves the visualization as bytes format.

        Args:
            fig (Figure): The matplotlib figure to save.

        Returns:
            The saved figure in bytes format.
        """
        img_bin = BytesIO()
        fig.savefig(img_bin, format='PNG')
        return img_bin

    def save_as_img(self):
        pass
