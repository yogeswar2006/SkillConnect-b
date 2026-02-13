from urllib.parse import parse_qs
from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async
from django.conf import settings
import jwt


class JWTAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):

        # Lazy imports (AFTER Django is ready)
        from django.contrib.auth.models import AnonymousUser
        from django.contrib.auth import get_user_model

        query_string = scope.get("query_string", b"").decode()
        query_params = parse_qs(query_string)

        token = query_params.get("token")

        if not token:
            scope["user"] = AnonymousUser()
            return await super().__call__(scope, receive, send)

        try:
            payload = jwt.decode(
                token[0],
                settings.SECRET_KEY,
                algorithms=["HS256"],
            )

            User = get_user_model()

            user = await database_sync_to_async(User.objects.get)(
                id=payload["user_id"]
            )

            scope["user"] = user

        except Exception as e:
            print("JWT WS AUTH ERROR:", e)
            scope["user"] = AnonymousUser()

        return await super().__call__(scope, receive, send)
