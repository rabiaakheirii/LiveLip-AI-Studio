import 'package:flutter/material.dart';

class SettingsScreen extends StatelessWidget {
  const SettingsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return const Padding(
      padding: EdgeInsets.all(16),
      child: Card(
        child: ListTile(
          title: Text('Settings (MVP Placeholder)'),
          subtitle: Text('Add model, voice, OBS scene/source selectors bound to /settings endpoints.'),
        ),
      ),
    );
  }
}
