from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from plays.models import Play

from .models import Playbook
from .permissions import IsAuthorOrReadOnly
from .serializers import PlaybookSerializer


class PlaybookViewSet(viewsets.ModelViewSet):
    serializer_class = PlaybookSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'updated_at', 'title']
    ordering = ['-created_at']

    def get_queryset(self):
        """Apenas playbooks públicos."""
        return (
            Playbook.objects.select_related('author')
            .prefetch_related('plays')
            .filter(visibility=Playbook.Visibility.PUBLIC)
        )

    @action(detail=False, methods=['get'], url_path='my')
    def my_playbooks(self, request):
        """Todos os playbooks do usuário autenticado (públicos e privados)."""
        qs = (
            Playbook.objects.select_related('author')
            .prefetch_related('plays')
            .filter(author=request.user)
        )

        for backend in self.filter_backends:
            qs = backend().filter_queryset(request, qs, self)

        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='plays/add')
    def add_play(self, request, pk=None):
        """Adiciona uma play ao playbook."""
        playbook = self.get_object()
        play_id = request.data.get('play_id')

        try:
            play = Play.objects.get(pk=play_id)
        except Play.DoesNotExist:
            return Response({'detail': 'Play não encontrada.'}, status=status.HTTP_404_NOT_FOUND)

        if play.visibility == Play.Visibility.PRIVATE and play.author != request.user:
            return Response(
                {'detail': 'Não é possível adicionar plays privadas de outros usuários.'},
                status=status.HTTP_403_FORBIDDEN,
            )

        playbook.plays.add(play)
        return Response({'detail': 'Play adicionada ao playbook.'})

    @action(detail=True, methods=['post'], url_path='plays/remove')
    def remove_play(self, request, pk=None):
        """Remove uma play do playbook."""
        playbook = self.get_object()
        play_id = request.data.get('play_id')

        try:
            play = Play.objects.get(pk=play_id)
        except Play.DoesNotExist:
            return Response({'detail': 'Play não encontrada.'}, status=status.HTTP_404_NOT_FOUND)

        if not playbook.plays.filter(pk=play.pk).exists():
            return Response(
                {'detail': 'Essa play não está neste playbook.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        playbook.plays.remove(play)
        return Response({'detail': 'Play removida do playbook.'})
