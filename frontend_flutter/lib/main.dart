import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_live_lipsync_assistant/screens/dashboard_screen.dart';
import 'package:flutter_live_lipsync_assistant/state/app_controller.dart';

void main() {
  runApp(const ProviderScope(child: LiveLipSyncApp()));
}

class LiveLipSyncApp extends ConsumerWidget {
  const LiveLipSyncApp({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    ref.read(appControllerProvider.notifier).initialize();

    return MaterialApp(
      title: 'Flutter Live LipSync Assistant',
      theme: ThemeData.dark(useMaterial3: true),
      home: const DashboardScreen(),
    );
  }
}
