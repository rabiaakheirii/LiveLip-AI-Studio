import 'package:flutter/material.dart';
import 'package:flutter_live_lipsync_assistant/models/pipeline_status.dart';

class StatusBadge extends StatelessWidget {
  const StatusBadge({super.key, required this.status});

  final PipelineStatus status;

  Color _color() {
    switch (status) {
      case PipelineStatus.error:
        return Colors.redAccent;
      case PipelineStatus.idle:
        return Colors.grey;
      default:
        return Colors.greenAccent;
    }
  }

  @override
  Widget build(BuildContext context) {
    return Chip(
      label: Text(status.name),
      backgroundColor: _color().withValues(alpha: 0.2),
      side: BorderSide(color: _color()),
    );
  }
}
