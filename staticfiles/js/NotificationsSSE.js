
const eventSource = new EventSource('/sse/notifications/');

eventSource.addEventListener('message', (event) => {
  console.log('Received notification:', event.data);
  // Обработка полученного уведомления
});

eventSource.addEventListener('error', (event) => {
  console.error('SSE error:', event);
  // Обработка ошибки подключения к SSE
});
