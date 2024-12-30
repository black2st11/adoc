from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import authentication_classes

from assignment.authentication import JWTAuthentication
from assignment.permission import IsAnonymousOnlyGetPermission
from community.services.post_service import PostService


class PostsAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAnonymousOnlyGetPermission]

    def post(self, request):
        author_id = request.user_id
        title = request.data.get('title')
        content = request.data.get('content')
        post_id = PostService().create_post(title=title, content=content, author_id=author_id)
        return Response(status=201, data={'_id': post_id})

    def get(self, request):
        page = int(request.query_params.get('page', 1))
        size = int(request.query_params.get('size', 10))
        order_by = request.query_params.get('order_by', 'created_at')
        order = int(request.query_params.get('order', -1))
        author_id = int(request.query_params.get('author_id')) if request.query_params.get('author_id') else None
        dto = PostService().get_posts(page=page, size=size, order_by=order_by, order=order, author_id=author_id)
        return Response(status=201, data=dto.model_dump())
