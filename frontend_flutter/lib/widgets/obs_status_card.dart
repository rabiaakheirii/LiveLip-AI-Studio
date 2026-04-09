import 'package:flutter/material.dart';

class OBSStatusCard extends StatelessWidget {
  const OBSStatusCard({super.key, required this.connected, required this.scenes});

  final bool connected;
  final List<String> scenes;

  @override
  Widget build(BuildContext context) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(12),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Icon(connected ? Icons.check_circle : Icons.error, color: connected ? Colors.green : Colors.red),
                const SizedBox(width: 8),
                Text(connected ? 'OBS Connected' : 'OBS Disconnected'),
              ],
            ),
            const SizedBox(height: 8),
            Text('Scenes: ${scenes.join(', ')}'),
          ],
        ),
      ),
    );
  }
}
