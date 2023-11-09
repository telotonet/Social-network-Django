# import asyncio
# from django.http import HttpResponseServerError, StreamingHttpResponse
# from notifications.models import Notification
# from asgiref.sync import sync_to_async
# from django.http import StreamingHttpResponse

# async def event_stream(request):
#     async def wait_for_notification():
#         new_notification = await sync_to_async(
#             lambda: Notification.objects.filter(user=request.user, is_read=False).values().first()
#         )()
#         return new_notification

#     async def stream_generator():
#         while True:
#             try:
#                 notification = await wait_for_notification()
#                 if notification:
#                     yield f'data: {notification}\n\n'
#                 else:
#                     yield '\n'
#                 await asyncio.sleep(1)
#             except Exception as e:
#                 yield f'data: {str(e)}\n\n'
#                 break

#     response = StreamingHttpResponse(stream_generator(), content_type='text/event-stream')
#     response['Cache-Control'] = 'no-cache'
#     response['Connection'] = 'keep-alive'
#     response['Transfer-Encoding'] = 'chunked'
#     return response
