# ----------------------------------------------------------------------
# pytest-csv - https://github.com/nicoulaj/pytest-csv
# copyright (c) 2018 pytest-csv contributors
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# ----------------------------------------------------------------------

from . import _hooks
from ._reporter import CSVReporter
from .column import *


def pytest_addoption(parser):
    group = parser.getgroup('terminal reporting')
    group.addoption(
        '--csv',
        dest='csv_path',
        action='store',
        metavar='path',
        default=None,
        help='create CSV report file at given path'
    )
    group.addoption(
        '--csv-columns',
        dest='csv_columns',
        action='store',
        type=str,
        nargs='+',
        default=[ID, MODULE, NAME, FILE, DOC, MARKERS, STATUS, MESSAGE, DURATION],
        help='define columns in output CSV'
    )


def pytest_addhooks(pluginmanager):
    pluginmanager.add_hookspecs(_hooks)


def pytest_configure(config):
    csv_path = config.option.csv_path
    csv_columns = config.option.csv_columns

    if csv_path and not hasattr(config, 'slaveinput'):
        columns_registry = dict(BUILTIN_COLUMNS_REGISTRY)
        config.hook.pytest_csv_register_columns(columns=columns_registry)

        columns = [columns_registry[id.strip()] for ids in csv_columns for id in ids.split(',')]

        config._csv_reporter = CSVReporter(csv_path=csv_path, columns=columns)
        config.pluginmanager.register(config._csv_reporter)


def pytest_unconfigure(config):
    csv_reporter = getattr(config, '_csv_reporter', None)
    if csv_reporter:
        del config._csv_reporter
        config.pluginmanager.unregister(csv_reporter)
