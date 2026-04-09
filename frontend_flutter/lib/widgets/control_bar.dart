import 'package:flutter/material.dart';

class ControlBar extends StatelessWidget {
  const ControlBar({
    super.key,
    required this.onStart,
    required this.onStop,
  });

  final VoidCallback onStart;
  final VoidCallback onStop;

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        FilledButton.icon(onPressed: onStart, icon: const Icon(Icons.play_arrow), label: const Text('Start')),
        const SizedBox(width: 12),
        OutlinedButton.icon(onPressed: onStop, icon: const Icon(Icons.stop), label: const Text('Stop')),
      ],
    );
  }
}
