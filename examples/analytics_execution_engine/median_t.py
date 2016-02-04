# ------------------------------------------------------------------------------
# Name:       median_t.py
# Purpose:    median t example for Analytics Engine & Execution Engine.
#             pre-integration with NDExpr.
#             post-integration with Data Access API.
#
# Author:     Peter Wang
#
# Created:    22 December 2015
# Copyright:  2015 Commonwealth Scientific and Industrial Research Organisation
#             (CSIRO)
# License:    This software is open source under the Apache v2.0 License
#             as provided in the accompanying LICENSE file or available from
#             https://github.com/data-cube/agdc-v2/blob/master/LICENSE
#             By continuing, you acknowledge that you have read and you accept
#             and will abide by the terms of the License.
#
# ------------------------------------------------------------------------------

from __future__ import absolute_import
from __future__ import print_function

if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.dirname(path.abspath(__file__)))))

from pprint import pprint
from datetime import datetime
from datacube.analytics.analytics_engine import AnalyticsEngine
from datacube.execution.execution_engine import ExecutionEngine
from datacube.analytics.utils.analytics_utils import plot

from glue.core import Data, DataCollection
from glue.qt.glue_application import GlueApplication


def main():
    a = AnalyticsEngine()
    e = ExecutionEngine()

    # Lake Burley Griffin
    dimensions = {'longitude': {'range': (149.07, 149.18)},
                  'latitude':  {'range': (-35.32, -35.28)},
                  'time':      {'range': (datetime(1990, 1, 1), datetime(1990, 12, 31))}}

    arrays = a.create_array(('LANDSAT 5', 'NBAR'), ['band_40'], dimensions, 'get_data')

    median_t = a.apply_generic_reduction(arrays, ['time'], 'median(array1)', 'medianT')

    result = e.execute_plan(a.plan)

    plot(e.cache['medianT'])

    b40_result = e.cache['get_data']['array_result']['band_40']
    median_result = e.cache['medianT']['array_result']['medianT']

    b40_data = Data(x=b40_result[:, ::-1, :], label='B40')
    median_data = Data(x=median_result[::-1, :], label='medianT')

    long_data = Data(x=b40_result.coords['longitude'], label='long')
    lat_data = Data(x=b40_result.coords['latitude'], label='lat')
    time_data = Data(x=b40_result.coords['time'], label='time')

    collection = DataCollection([median_data, b40_data, long_data, lat_data, time_data, ])
    app = GlueApplication(collection)
    app.start()


if __name__ == '__main__':
    main()
