from community.services.post_service import PostService
from rest_framework.response import Response
from rest_framework.views import APIView

from assignment.authentication import JWTAuthentication
from assignment.permission import IsAnonymousOnlyGetPermission


class PostsDetailAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAnonymousOnlyGetPermission]

    def put(self, request, post_id):
        author_id = request.user_id
        title = request.data.get("title")
        content = request.data.get("content")
        PostService().update_post(
            post_id=post_id, title=title, content=content, author_id=author_id
        )
        return Response(status=200, data={"message": "게시글 수정을 완료했습니다."})

    def get(self, request, post_id):
        post = PostService().get_post(post_id=post_id)
        return Response(status=200, data=post)

    def delete(self, request, post_id):
        author_id = request.user_id
        PostService().delete_post(post_id=post_id, author_id=author_id)
        return Response(status=200, data={"message": "게시글 삭제를 완료했습니다."})
