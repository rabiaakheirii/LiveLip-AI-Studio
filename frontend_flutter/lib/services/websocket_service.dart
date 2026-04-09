import 'dart:async';
import 'dart:convert';

import 'package:web_socket_channel/web_socket_channel.dart';

class WebSocketService {
  WebSocketService({String? url}) : _url = url ?? 'ws://127.0.0.1:8000/ws/events';

  final String _url;
  WebSocketChannel? _channel;
  final _controller = StreamController<Map<String, dynamic>>.broadcast();

  Stream<Map<String, dynamic>> get events => _controller.stream;

  void connect() {
    _channel = WebSocketChannel.connect(Uri.parse(_url));
    _channel!.stream.listen((message) {
      final decoded = jsonDecode(message as String) as Map<String, dynamic>;
      _controller.add(decoded);
    }, onError: (Object e) {
      _controller.add({
        'event_type': 'error',
        'data': {'message': e.toString()}
      });
    });

    // Keepalive message so backend receive loop stays open.
    Timer.periodic(const Duration(seconds: 10), (_) => ping());
  }

  void ping() {
    _channel?.sink.add('ping');
  }

  void dispose() {
    _channel?.sink.close();
    _controller.close();
  }
}
