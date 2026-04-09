import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_live_lipsync_assistant/state/app_controller.dart';
import 'package:flutter_live_lipsync_assistant/widgets/response_panel.dart';

class ResponseScreen extends ConsumerWidget {
  const ResponseScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final state = ref.watch(appControllerProvider);
    return Padding(
      padding: const EdgeInsets.all(16),
      child: ResponsePanel(
        partialText: state.partialResponse,
        finalText: state.finalResponse,
      ),
    );
  }
}
