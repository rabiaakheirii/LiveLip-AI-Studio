import 'package:flutter/material.dart';
import 'package:flutter_live_lipsync_assistant/models/camera_device.dart';

class CameraSelector extends StatelessWidget {
  const CameraSelector({
    super.key,
    required this.cameras,
    required this.selectedIndex,
    required this.onSelected,
  });

  final List<CameraDevice> cameras;
  final int selectedIndex;
  final ValueChanged<int> onSelected;

  @override
  Widget build(BuildContext context) {
    if (cameras.isEmpty) {
      return const Card(child: ListTile(title: Text('No cameras detected')));
    }

    return Card(
      child: Padding(
        padding: const EdgeInsets.all(12),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text('Camera Selection', style: TextStyle(fontWeight: FontWeight.bold)),
            DropdownButton<int>(
              value: selectedIndex,
              items: cameras
                  .map((c) => DropdownMenuItem(value: c.index, child: Text('${c.name} (${c.available ? "ready" : "mock"})')))
                  .toList(),
              onChanged: (value) {
                if (value != null) onSelected(value);
              },
            ),
          ],
        ),
      ),
    );
  }
}
