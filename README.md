# assignment5

### Run the app:

- Copy `.env.example` to `.env`
- Change the value of `POSTMARK_SERVER_TOKEN` to postmarker acces token
- run 
```shell
docker-composer up -d
```
### Create a superuser

```shell
docker-compose exec backend python manage.py createsuperuser
```
and follow the instructions

### Using the app:

- visit `http://localhost:3000` in your web browser.
- login using the superuser created earlier (as Admin)
- or register a new account in the user interface (as User)



## App Overview

### Backend

-   **Framework**: Django with Django Rest Framework (DRF)
    -   DRF facilitates easy creation of RESTful APIs, ensuring robustness and scalability.
-   **Authentication**: JWT with `djangorestframework-simplejwt`
    -   Utilizing JWT ensures secure communication between frontend and backend.
-   **User Types**: Admin, User
    -   Two distinct user types with tailored privileges and functionalities.
- **Models**:

	-   **User**: Represents users of the system with attributes such as username, email, username, and user type.
	-   **Ticket**: Represents a support ticket with attributes such as title, description, status, and created_by.
	-   **TicketReply**: Represents replies to support tickets with attributes such as text, created_at, associated ticket, created_by.
### Frontend

-   **Framework**: Vue.js
    -   Vue.js offers simplicity and flexibility for frontend development.
-   **State Management**: Pinia
    -   Pinia provides efficient state management within Vue.js components.
-   **HTTP Client**: Axios
    -   Axios handles asynchronous requests to the backend, ensuring smooth data exchange.
-   **UI Components**: Flowbite
    -   Flowbite offers pre-designed Vue components and layouts for intuitive user interfaces.
