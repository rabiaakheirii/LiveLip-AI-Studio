import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_live_lipsync_assistant/screens/logs_screen.dart';
import 'package:flutter_live_lipsync_assistant/screens/response_screen.dart';
import 'package:flutter_live_lipsync_assistant/screens/settings_screen.dart';
import 'package:flutter_live_lipsync_assistant/screens/transcript_screen.dart';
import 'package:flutter_live_lipsync_assistant/state/app_controller.dart';
import 'package:flutter_live_lipsync_assistant/widgets/camera_selector.dart';
import 'package:flutter_live_lipsync_assistant/widgets/control_bar.dart';
import 'package:flutter_live_lipsync_assistant/widgets/obs_live_status_card.dart';
import 'package:flutter_live_lipsync_assistant/widgets/obs_status_card.dart';
import 'package:flutter_live_lipsync_assistant/widgets/preview_panel.dart';
import 'package:flutter_live_lipsync_assistant/widgets/preview_status_card.dart';
import 'package:flutter_live_lipsync_assistant/widgets/status_badge.dart';
import 'package:flutter_live_lipsync_assistant/widgets/stream_control_bar.dart';
import 'package:flutter_live_lipsync_assistant/widgets/stream_metrics_panel.dart';
import 'package:flutter_live_lipsync_assistant/widgets/stream_status_card.dart';

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
                  if (state.degradedMode)
                    const Card(
                      color: Colors.orange,
                      child: ListTile(title: Text('Degraded mode enabled'), subtitle: Text('Backend is using fallback engine/mode.')),
                    ),
                  ControlBar(onStart: controller.start, onStop: controller.stop),
                  const SizedBox(height: 8),
                  StreamControlBar(onStart: controller.startStream, onStop: controller.stopStream),
                  const SizedBox(height: 16),
                  StreamStatusCard(
                    running: state.streamRunning,
                    engine: state.streamEngine,
                    degraded: state.degradedMode,
                    message: state.streamMessage,
                  ),
                  const SizedBox(height: 8),
                  StreamMetricsPanel(
                    queuePressure: state.queuePressure,
                    droppedFrames: state.droppedFrames,
                    avDriftMs: state.avDriftMs,
                  ),
                  const SizedBox(height: 8),
                  OBSLiveStatusCard(ready: state.obsLiveReady, mode: state.obsLiveMode),
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
                      title: Text('Live Stream Preview Endpoint'),
                      subtitle: Text('Use backend MJPEG: /api/stream/mjpeg, latest frame: /api/stream/latest-frame'),
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
