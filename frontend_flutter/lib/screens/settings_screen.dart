import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_live_lipsync_assistant/state/app_controller.dart';
import 'package:flutter_live_lipsync_assistant/widgets/camera_selector.dart';

class SettingsScreen extends ConsumerWidget {
  const SettingsScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final state = ref.watch(appControllerProvider);
    final controller = ref.read(appControllerProvider.notifier);

    return Padding(
      padding: const EdgeInsets.all(16),
      child: ListView(
        children: [
          const Card(
            child: ListTile(
              title: Text('Model / Voice / OBS selectors'),
              subtitle: Text('TODO: Bind fully to /settings with save/persist behavior.'),
            ),
          ),
          const SizedBox(height: 12),
          CameraSelector(
            cameras: state.cameras,
            selectedIndex: state.selectedCameraIndex,
            onSelected: controller.selectCamera,
          ),
          const SizedBox(height: 12),
          OutlinedButton.icon(
            onPressed: controller.refreshCameras,
            icon: const Icon(Icons.refresh),
            label: const Text('Refresh Cameras'),
          ),
        ],
      ),
    );
  }
}
