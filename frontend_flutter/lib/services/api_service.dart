import 'dart:convert';

import 'package:http/http.dart' as http;

class ApiService {
  ApiService({String? baseUrl}) : _baseUrl = baseUrl ?? 'http://127.0.0.1:8000';

  final String _baseUrl;

  Future<void> startPipeline() async {
    final resp = await http.post(Uri.parse('$_baseUrl/pipeline/start'));
    if (resp.statusCode >= 400) {
      throw Exception('Start failed: ${resp.body}');
    }
  }

  Future<void> stopPipeline() async {
    final resp = await http.post(Uri.parse('$_baseUrl/pipeline/stop'));
    if (resp.statusCode >= 400) {
      throw Exception('Stop failed: ${resp.body}');
    }
  }

  Future<Map<String, dynamic>> getSettings() async {
    final resp = await http.get(Uri.parse('$_baseUrl/settings'));
    if (resp.statusCode >= 400) {
      throw Exception('Settings failed: ${resp.body}');
    }
    return jsonDecode(resp.body) as Map<String, dynamic>;
  }
}
