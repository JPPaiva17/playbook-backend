from rest_framework import filters, viewsets
from rest_framework.permissions import IsAuthenticated

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
        user = self.request.user
        qs = Playbook.objects.select_related('author').prefetch_related('plays')
        qs = qs.filter(visibility=Playbook.Visibility.PUBLIC) | qs.filter(author=user)

        params = self.request.query_params
        if v := params.get('visibility'):
            qs = qs.filter(visibility=v)

        return qs.distinct()
