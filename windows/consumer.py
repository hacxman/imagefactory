#!/usr/bin/env python
# encoding: utf-8

# Copyright (C) 2010-2011 Red Hat, Inc.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; version 2 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA  02110-1301, USA.  A copy of the GNU General Public License is
# also available at http://www.gnu.org/copyleft/gpl.html.


from qpid.messaging import *
from qpid.util import URL
import base64
from subprocess import Popen, STDOUT, PIPE

connection = Connection('localhost', username='guest', password='guest')
connection.open()
session = connection.session(str(uuid4()))

receiver = session.receiver('amq.topic')

while True:
    message = receiver.fetch()
    session.acknowledge()
    sender = session.sender(message.reply_to)
    
    proc = Popen(base64.b64decode(message.content), shell=True, stderr=STDOUT, stdin=PIPE, stdout=PIPE)
    output, _ = proc.communicate()
    result = Message(base64.b64encode(output))
    result.properties["exit"] = proc.returncode
    sender.send(result)

connection.close()
