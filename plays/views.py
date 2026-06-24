from rest_framework import filters, viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Play
from .permissions import IsAuthorOrReadOnly
from .serializers import PlaySerializer


class PlayViewSet(viewsets.ModelViewSet):
    serializer_class = PlaySerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'players_required', 'smokes', 'flashbangs', 'he_grenades', 'molotovs', 'decoys']
    ordering = ['-created_at']

    def get_queryset(self):
        user = self.request.user
        qs = Play.objects.select_related('author')

        qs = qs.filter(visibility=Play.Visibility.PUBLIC) | qs.filter(author=user)

        params = self.request.query_params
        if v := params.get('visibility'):
            qs = qs.filter(visibility=v)
        if p := params.get('players_required'):
            qs = qs.filter(players_required=p)
        if params.get('smokes'):
            qs = qs.filter(smokes__gte=params['smokes'])
        if params.get('flashbangs'):
            qs = qs.filter(flashbangs__gte=params['flashbangs'])
        if params.get('he_grenades'):
            qs = qs.filter(he_grenades__gte=params['he_grenades'])
        if params.get('molotovs'):
            qs = qs.filter(molotovs__gte=params['molotovs'])
        if params.get('decoys'):
            qs = qs.filter(decoys__gte=params['decoys'])

        return qs.distinct()
