from rest_framework import filters, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Play
from .permissions import IsAuthorOrReadOnly
from .serializers import PlaySerializer


def _apply_filters(qs, params):
    """Aplica filtros de granadas, players e mapa ao queryset."""
    if m := params.get('map'):
        qs = qs.filter(map=m)
    if p := params.get('players_required'):
        qs = qs.filter(players_required=p)
    if v := params.get('smokes'):
        qs = qs.filter(smokes__gte=v)
    if v := params.get('flashbangs'):
        qs = qs.filter(flashbangs__gte=v)
    if v := params.get('he_grenades'):
        qs = qs.filter(he_grenades__gte=v)
    if v := params.get('molotovs'):
        qs = qs.filter(molotovs__gte=v)
    if v := params.get('decoys'):
        qs = qs.filter(decoys__gte=v)
    return qs


class PlayViewSet(viewsets.ModelViewSet):
    serializer_class = PlaySerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'players_required', 'smokes', 'flashbangs', 'he_grenades', 'molotovs', 'decoys']
    ordering = ['-created_at']

    def get_queryset(self):
        """Apenas plays públicas."""
        qs = Play.objects.select_related('author').filter(
            visibility=Play.Visibility.PUBLIC
        )
        return _apply_filters(qs, self.request.query_params)

    @action(detail=False, methods=['get'], url_path='my')
    def my_plays(self, request):
        """Todas as plays do usuário autenticado (públicas e privadas)."""
        qs = Play.objects.select_related('author').filter(author=request.user)
        qs = _apply_filters(qs, request.query_params)

        # Respeita search e ordering do DRF
        for backend in self.filter_backends:
            qs = backend().filter_queryset(request, qs, self)

        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)
