import 'package:flutter/material.dart';

class OBSLiveStatusCard extends StatelessWidget {
  const OBSLiveStatusCard({super.key, required this.ready, required this.mode});

  final bool ready;
  final String mode;

  @override
  Widget build(BuildContext context) {
    return Card(
      child: ListTile(
        title: Text('OBS Live Output: ${ready ? "Ready" : "Not Ready"}'),
        subtitle: Text('Video Mode: $mode'),
      ),
    );
  }
}
