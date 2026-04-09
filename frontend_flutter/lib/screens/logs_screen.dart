import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_live_lipsync_assistant/state/app_controller.dart';

class LogsScreen extends ConsumerWidget {
  const LogsScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final logs = ref.watch(appControllerProvider).logs;

    return ListView.builder(
      padding: const EdgeInsets.all(16),
      itemCount: logs.length,
      itemBuilder: (context, index) => Padding(
        padding: const EdgeInsets.only(bottom: 6),
        child: Text(logs[index]),
      ),
    );
  }
}
