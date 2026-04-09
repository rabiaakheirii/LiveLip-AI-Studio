import 'package:flutter/material.dart';

class PreviewStatusCard extends StatelessWidget {
  const PreviewStatusCard({super.key, required this.status, required this.progress});

  final String status;
  final int progress;

  @override
  Widget build(BuildContext context) {
    return Card(
      child: ListTile(
        title: Text('Preview status: $status'),
        subtitle: LinearProgressIndicator(value: (progress.clamp(0, 100)) / 100),
        trailing: Text('$progress%'),
      ),
    );
  }
}
