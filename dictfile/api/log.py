#############################################################################
# Copyright (c) 2018 Eli Polonsky. All rights reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
#   * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   * See the License for the specific language governing permissions and
#   * limitations under the License.
#
#############################################################################

import logging
import sys

from dictfile.api import exceptions


DEFAULT_LOG_LEVEL = logging.INFO
DEFAULT_LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'


class Logger(object):

    """
    Provides logging capabilities.

    This is a thin wrapper on top a specific implementation. The idea is to hide implementation
    specific features from the API in order to be able to easily switch implementations.

    Args:
        name (str): The name of the logger.
    """

    _logger = None

    def __init__(self, name):

        if not name:
            raise exceptions.InvalidArgumentsException('name cannot be empty')

        self._name = name
        self._logger = logging.getLogger(name)
        self._logger.propagate = False
        self.add_console_handler(DEFAULT_LOG_LEVEL)
        self.set_level(DEFAULT_LOG_LEVEL)

    @property
    def logger(self):
        return self._logger

    def add_console_handler(self, level):
        ch = logging.StreamHandler(stream=sys.stdout)
        ch.setLevel(level)
        formatter = logging.Formatter(DEFAULT_LOG_FORMAT)
        ch.setFormatter(formatter)
        self._logger.addHandler(ch)

    def set_level(self, level):
        self._logger.setLevel(level)
        for handler in self._logger.handlers:
            handler.setLevel(level)

    def info(self, message, **kwargs):
        self._log(logging.INFO, message, **kwargs)

    def error(self, message, **kwargs):
        self._log(logging.ERROR, message, **kwargs)

    def debug(self, message, **kwargs):
        self._log(logging.DEBUG, message, **kwargs)

    def warn(self, message, **kwargs):
        self._log(logging.WARN, message, **kwargs)

    # we disable this because for some reason it prevents
    # testfixtures from properly capturing logs for tests.
    # pylint: disable=logging-format-interpolation
    def _log(self, level, message, **kwargs):
        self._logger.log(level, '{}{}'.format(message, self.format_key_values(**kwargs)))

    @staticmethod
    def format_key_values(**kwargs):

        if not kwargs:
            return ''

        kvs = []
        for key, value in kwargs.items():
            kvs.append('{}={}'.format(key, value))
        return ' [{}]'.format(', '.join(kvs))
