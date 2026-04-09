class CameraDevice {
  final String id;
  final int index;
  final String name;
  final bool available;

  const CameraDevice({
    required this.id,
    required this.index,
    required this.name,
    required this.available,
  });

  factory CameraDevice.fromJson(Map<String, dynamic> json) {
    return CameraDevice(
      id: json['id'] as String,
      index: json['index'] as int,
      name: json['name'] as String,
      available: json['available'] as bool? ?? true,
    );
  }
}
