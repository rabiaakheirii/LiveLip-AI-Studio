import 'dart:convert';

import 'package:http/http.dart' as http;

class ApiService {
  ApiService({String? baseUrl}) : _baseUrl = baseUrl ?? 'http://127.0.0.1:8000';

  final String _baseUrl;

  Future<void> startPipeline() async {
    final resp = await http.post(Uri.parse('$_baseUrl/pipeline/start'));
    if (resp.statusCode >= 400) throw Exception('Start failed: ${resp.body}');
  }

  Future<void> stopPipeline() async {
    final resp = await http.post(Uri.parse('$_baseUrl/pipeline/stop'));
    if (resp.statusCode >= 400) throw Exception('Stop failed: ${resp.body}');
  }

  Future<Map<String, dynamic>> getCameraDevices() async {
    final resp = await http.get(Uri.parse('$_baseUrl/api/webcam/devices'));
    if (resp.statusCode >= 400) throw Exception('Cameras failed: ${resp.body}');
    return jsonDecode(resp.body) as Map<String, dynamic>;
  }

  Future<void> selectCamera(int index) async {
    final resp = await http.post(
      Uri.parse('$_baseUrl/api/webcam/select'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'index': index}),
    );
    if (resp.statusCode >= 400) throw Exception('Select camera failed: ${resp.body}');
  }

  Future<Map<String, dynamic>> getStreamStatus() async {
    final resp = await http.get(Uri.parse('$_baseUrl/api/stream/status'));
    if (resp.statusCode >= 400) throw Exception('Stream status failed: ${resp.body}');
    return jsonDecode(resp.body) as Map<String, dynamic>;
  }

  Future<void> startStream() async {
    final resp = await http.post(Uri.parse('$_baseUrl/api/stream/start'));
    if (resp.statusCode >= 400) throw Exception('Start stream failed: ${resp.body}');
  }

  Future<void> stopStream() async {
    final resp = await http.post(Uri.parse('$_baseUrl/api/stream/stop'));
    if (resp.statusCode >= 400) throw Exception('Stop stream failed: ${resp.body}');
  }

  String makePreviewUrl(String path) => '$_baseUrl$path';
  String latestFrameUrl() => '$_baseUrl/api/stream/latest-frame';
  String mjpegUrl() => '$_baseUrl/api/stream/mjpeg';
}
