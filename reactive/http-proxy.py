#!/usr/bin/env python3
# Copyright (C) 2017  Ghent University
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from charmhelpers.core import hookenv
from charmhelpers.core.hookenv import status_set, log, unit_private_ip, open_port, close_port

from charms.reactive import when, when_not, set_state, remove_state

@when_not('endpoint.available')
def no_service_connected():
    log('No client connected.')
    remove_state('http-proxy.ready')
    close_port(hookenv.config().get('port'))
    status_set(
        'blocked',
        'Please connect the http proxy charm to a client service.')

@when('endpoint.available')
def configure_endpoint_relationship(endpoint_relation):
    log('Client connected.')

    conf = hookenv.config()
    host = conf.get('host')
    if host == "localhost" or host == "127.0.0.1":
        host = unit_private_ip()
    port = conf.get('port')

    endpoint_relation.configure(
        hostname=host,
        private_address=host,
        port=port)

    open_port(port)

    status_set('active', 'Ready (http://{}:{})'.format(host, port))
    set_state('http-proxy.ready')

@when('endpoint.available', 'config.changed')
def config_changed(endpoint_relation):
    log('Config changed.')
    configure_endpoint_relationship(endpoint_relation)

