import re

from rest_framework import serializers

from .models import Play

YOUTUBE_PATTERN = re.compile(
    r'^https?://(www\.)?(youtube\.com/watch\?v=|youtu\.be/)[\w\-]{11}'
)


class PlaySerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Play
        fields = (
            'id',
            'title',
            'description',
            'content',
            'visibility',
            'map',
            'video_url',
            'players_required',
            'smokes',
            'flashbangs',
            'he_grenades',
            'molotovs',
            'decoys',
            'author',
            'created_at',
            'updated_at',
        )
        read_only_fields = ('id', 'author', 'created_at', 'updated_at')

    def validate_video_url(self, value):
        if value and not YOUTUBE_PATTERN.match(value):
            raise serializers.ValidationError(
                'Informe um link válido do YouTube (youtube.com/watch?v=... ou youtu.be/...).'
            )
        return value

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)
