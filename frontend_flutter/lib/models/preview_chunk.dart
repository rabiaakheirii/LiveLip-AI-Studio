class PreviewChunk {
  final String chunkId;
  final String fileName;
  final String previewUrl;
  final String source;

  const PreviewChunk({
    required this.chunkId,
    required this.fileName,
    required this.previewUrl,
    required this.source,
  });

  factory PreviewChunk.fromJson(Map<String, dynamic> json) {
    return PreviewChunk(
      chunkId: json['chunk_id'] as String,
      fileName: json['file_name'] as String,
      previewUrl: json['preview_url'] as String,
      source: json['source'] as String? ?? 'webcam',
    );
  }
}
