import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_live_lipsync_assistant/state/app_controller.dart';
import 'package:flutter_live_lipsync_assistant/widgets/transcript_panel.dart';

class TranscriptScreen extends ConsumerWidget {
  const TranscriptScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final state = ref.watch(appControllerProvider);
    return Padding(
      padding: const EdgeInsets.all(16),
      child: TranscriptPanel(
        partialText: state.partialTranscript,
        finalText: state.finalTranscript,
      ),
    );
  }
}
