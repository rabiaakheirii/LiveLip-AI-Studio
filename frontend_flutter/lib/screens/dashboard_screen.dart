import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_live_lipsync_assistant/screens/logs_screen.dart';
import 'package:flutter_live_lipsync_assistant/screens/response_screen.dart';
import 'package:flutter_live_lipsync_assistant/screens/settings_screen.dart';
import 'package:flutter_live_lipsync_assistant/screens/transcript_screen.dart';
import 'package:flutter_live_lipsync_assistant/state/app_controller.dart';
import 'package:flutter_live_lipsync_assistant/widgets/camera_selector.dart';
import 'package:flutter_live_lipsync_assistant/widgets/control_bar.dart';
import 'package:flutter_live_lipsync_assistant/widgets/obs_status_card.dart';
import 'package:flutter_live_lipsync_assistant/widgets/preview_panel.dart';
import 'package:flutter_live_lipsync_assistant/widgets/preview_status_card.dart';
import 'package:flutter_live_lipsync_assistant/widgets/status_badge.dart';

class DashboardScreen extends ConsumerWidget {
  const DashboardScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final state = ref.watch(appControllerProvider);
    final controller = ref.read(appControllerProvider.notifier);

    return DefaultTabController(
      length: 5,
      child: Scaffold(
        appBar: AppBar(
          title: const Text('Live LipSync Assistant (Desktop MVP)'),
          actions: [StatusBadge(status: state.status)],
          bottom: const TabBar(
            tabs: [
              Tab(text: 'Dashboard'),
              Tab(text: 'Transcript'),
              Tab(text: 'Response'),
              Tab(text: 'Settings'),
              Tab(text: 'Logs'),
            ],
          ),
        ),
        body: TabBarView(
          children: [
            Padding(
              padding: const EdgeInsets.all(16),
              child: ListView(
                children: [
                  ControlBar(onStart: controller.start, onStop: controller.stop),
                  const SizedBox(height: 16),
                  OBSStatusCard(connected: state.obsConnected, scenes: state.obsScenes),
                  const SizedBox(height: 16),
                  CameraSelector(
                    cameras: state.cameras,
                    selectedIndex: state.selectedCameraIndex,
                    onSelected: controller.selectCamera,
                  ),
                  const SizedBox(height: 16),
                  PreviewStatusCard(status: state.previewStatus, progress: state.renderProgress),
                  const SizedBox(height: 16),
                  const Card(
                    child: ListTile(
                      title: Text('Webcam Preview Placeholder'),
                      subtitle: Text('Phase 2 renders chunk URLs. Embed player widget in Phase 3.'),
                    ),
                  ),
                  const SizedBox(height: 16),
                  PreviewPanel(
                    latest: state.latestPreview,
                    history: state.previewHistory,
                    backendBaseUrl: 'http://127.0.0.1:8000',
                  ),
                  const SizedBox(height: 16),
                  Text('Timings: ${state.timings}'),
                ],
              ),
            ),
            const TranscriptScreen(),
            const ResponseScreen(),
            const SettingsScreen(),
            const LogsScreen(),
          ],
        ),
      ),
    );
  }
}
