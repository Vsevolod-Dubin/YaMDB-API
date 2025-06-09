# reviews/urls.py

from django.urls import path
from reviews.views import ReviewViewSet, CommentViewSet

no_id = {'get': 'list', 'post': 'create'}
with_id = {'get': 'retrieve', 'patch': 'partial_update', 'delete': 'destroy'}

review_list = ReviewViewSet.as_view(no_id)
review_detail = ReviewViewSet.as_view(with_id)

comment_list = CommentViewSet.as_view(no_id)
comment_detail = CommentViewSet.as_view(with_id)

urlpatterns = [
    path('titles/<int:title_id>/reviews/', review_list, name='review-list'),
    path('titles/<int:title_id>/reviews/<int:pk>/',
         review_detail,
         name='review-detail'),
    path('titles/<int:title_id>/reviews/<int:review_id>/comments/',
         comment_list,
         name='comment-list'),
    path('titles/<int:title_id>/reviews/<int:review_id>/comments/<int:pk>/',
         comment_detail,
         name='comment-detail'),
]
