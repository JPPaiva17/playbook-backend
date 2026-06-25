from rest_framework import serializers

from plays.models import Play
from plays.serializers import PlaySerializer

from .models import Playbook


class PlaybookSerializer(serializers.ModelSerializer):
    """Usado em listagem e escrita: plays como lista de IDs."""

    author = serializers.StringRelatedField(read_only=True)
    plays = serializers.PrimaryKeyRelatedField(many=True, queryset=Play.objects.all(), required=False)

    class Meta:
        model = Playbook
        fields = (
            'id',
            'title',
            'description',
            'visibility',
            'plays',
            'author',
            'created_at',
            'updated_at',
        )
        read_only_fields = ('id', 'author', 'created_at', 'updated_at')

    def validate_plays(self, value):
        user = self.context['request'].user
        invalidas = [play.id for play in value if play.visibility == Play.Visibility.PRIVATE and play.author != user]
        if invalidas:
            raise serializers.ValidationError(
                f'Plays privadas de outros autores não podem ser adicionadas: {invalidas}'
            )
        return value

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)


class PlaybookDetailSerializer(PlaybookSerializer):
    """Usado no detalhe: plays como objetos completos (read-only)."""

    plays = PlaySerializer(many=True, read_only=True)
