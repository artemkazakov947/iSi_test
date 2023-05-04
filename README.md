# iSi_test
    API for small chat.
    - In this project was implemented JWT Auth. 
    - Permission IsAuthenticated was provided on project level.
    - Thread can’t have more than 2 participants. 
    - New thread would not be created with particular user, if old one exist. 
    - Implemented CRUD operations. 
    - Django admin panel was customized.
    - Pagination


### Components
    http://127.0.0.1:8000/api/users/register/ (Register)
    http://127.0.0.1:8000/api/users/token/ (Take access and refresh token)
    http://127.0.0.1:8000/api/threads/ (Thread List and create new thread)
    http://127.0.0.1:8000/api/thread/int:pk/ (Detail of thread)
    http://127.0.0.1:8000/api/thread/int:pk/messages/ (Message list of thread and create new message)
    http://127.0.0.1:8000/api/thread/int:pk/messages/int:pk/ (Detail of message)
    http://127.0.0.1:8000/api/thread/int:pk/messages/int:pk/mark_as_read/ (Update Message.is_read = True)
    http://127.0.0.1:8000/api/unread_message/ (Count of unread message)

### Installing
    git clone https://github.com/artemkazakov947/iSi_test.git
    cd iSi_test
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    python manage.py migrate
    python manage.py runserver

### Admin credentials:
    e-mail: admin@admin.com
    password: admin12345