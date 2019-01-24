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
from charmhelpers.core.hookenv import status_set, log, open_port, close_port

from charms.reactive import when, when_not, set_flag, clear_flag, endpoint_from_flag


@when_not('endpoint.http.joined')
def no_service_connected():
    log('No client connected.')
    clear_flag('http-proxy.ready')
    close_port(hookenv.config().get('port'))
    status_set(
        'blocked',
        'Please connect the http proxy charm to a client service.')


@when('endpoint.http.joined')
def configure_endpoint_relationship():
    log('Client connected.')
    endpoint_relation = endpoint_from_flag('endpoint.http.joined')

    conf = hookenv.config()
    host = conf.get('host')
    if host == "localhost" or host == "127.0.0.1":
        host = get_ingress_address(endpoint_relation)
    port = conf.get('port')

    endpoint_relation.configure(
        hostname=host,
        private_address=host,
        port=port)

    open_port(port)

    status_set('active', 'Ready (http://{}:{})'.format(host, port))
    set_flag('http-proxy.ready')


@when('endpoint.http.joined', 'config.changed')
def config_changed():
    log('Config changed.')
    configure_endpoint_relationship()


def get_ingress_address(relation):
    try:
        network_info = hookenv.network_get(relation.relation_name)
    except NotImplementedError:
        network_info = []

    if network_info and 'ingress-addresses' in network_info:
        # just grab the first one for now, maybe be more robust here?
        return network_info['ingress-addresses'][0]
    else:
        # if they don't have ingress-addresses they are running a juju that
        # doesn't support spaces, so just return the private address
        return hookenv.unit_get('private-address')
