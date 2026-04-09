import 'package:flutter/material.dart';

class WorkerModeStatusCard extends StatelessWidget {
  const WorkerModeStatusCard({super.key, required this.mode, required this.remoteAvailable});

  final String mode;
  final bool remoteAvailable;

  @override
  Widget build(BuildContext context) {
    return Card(
      child: ListTile(
        title: Text('Worker mode: $mode'),
        subtitle: Text('Remote available: $remoteAvailable'),
      ),
    );
  }
}
