# Part of the jsonrpc2-zeromq-python project.
# (c) 2012 Dan Brown, All Rights Reserved.
# Please see the LICENSE file in the root of this project for license
# information.

from __future__ import division
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
from builtins import *  # NOQA
from past.utils import old_div

from time import sleep
import threading

import jsonrpc2_zeromq
import jsonrpc2_zeromq.common


class LongTimeServerMixin(object):

    long_time = 500  # milliseconds

    def handle_take_a_long_time_method(self):
        sleep(old_div(self.long_time, 1000.0))


class RPCTestServer(jsonrpc2_zeromq.RPCServer, LongTimeServerMixin):

    def handle_echo_method(self, msg):
        return msg

    def handle_dict_args_method(self, an_int=None, a_bool=None, a_float=None,
                                a_str=None):
        return dict(an_int=an_int, a_bool=a_bool, a_float=a_float, a_str=a_str)

    def handle_return_null_method(self):
        return None


class RPCNotificationTestServer(jsonrpc2_zeromq.RPCNotificationServer):

    def handle_echo_method(self, msg):
        return msg


class NotificationOnlyPullTestServer(
        jsonrpc2_zeromq.NotificationOnlyPullServer):

    def handle_event_method(self, event_type, event_value):
        # Do things!
        pass


class NotificationReceiverClientTestServer(
        jsonrpc2_zeromq.RPCNotificationServer, LongTimeServerMixin):

    notification_reply_sleep_time = 0.5

    reply_thread = None

    def _send_back_notifications(self, client_id, method, num_notifications):
        for i in range(num_notifications):
            sleep(self.notification_reply_sleep_time)
            notification = jsonrpc2_zeromq.common.Request(method, params=[i],
                                                          notify=True)
            self.socket.send_multipart(
                [client_id,
                 jsonrpc2_zeromq.common.json_rpc_dumps(notification)])

    def _start_sending_notifications_thread(self, client_id, method,
                                            num_notifications):
        self.reply_thread = threading.Thread(
            target=lambda: self._send_back_notifications(client_id, method,
                                                         num_notifications))
        self.reply_thread.start()

    def _handle_method_and_response(self, client_id, req):
        # Slight hack to keep the client_id for _send_back_notifications
        self.client_id = client_id
        return super(NotificationReceiverClientTestServer,
                     self)._handle_method_and_response(client_id, req)

    def handle_subscribe_method(self, num_notifications):
        self._start_sending_notifications_thread(self.client_id, "event",
                                                 num_notifications)

    def handle_subscribe_bad_event_method(self, num_notifications):
        self._start_sending_notifications_thread(self.client_id, "bad_event",
                                                 num_notifications)

    def stop(self):
        if self.reply_thread and self.reply_thread.is_alive:
            self.reply_thread.join()
        return super(NotificationReceiverClientTestServer, self).stop()


class NotificationReceiverTestClient(
        jsonrpc2_zeromq.NotificationReceiverClient):

    num_notifications_received = 0

    def handle_event_notification(self, num):
        self.num_notifications_received += 1
