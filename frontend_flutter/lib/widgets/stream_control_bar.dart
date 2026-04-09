import 'package:flutter/material.dart';

class StreamControlBar extends StatelessWidget {
  const StreamControlBar({super.key, required this.onStart, required this.onStop});

  final VoidCallback onStart;
  final VoidCallback onStop;

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        FilledButton.icon(onPressed: onStart, icon: const Icon(Icons.videocam), label: const Text('Start Stream')),
        const SizedBox(width: 12),
        OutlinedButton.icon(onPressed: onStop, icon: const Icon(Icons.videocam_off), label: const Text('Stop Stream')),
      ],
    );
  }
}
