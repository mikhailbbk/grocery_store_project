from django.http import HttpResponse

def home(request):
    return HttpResponse("""
        <h1>Grocery Store API</h1>
        <p>Доступные эндпоинты:</p>
        <ul>
            <li><a href="/admin/">Админка</a></li>
            <li><a href="/api/">API (в разработке)</a></li>
        </ul>
    """)