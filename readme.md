# Blueprint Project

## Project Overview

Blueprint Project is a floorplan editor with real-time updates using Django Channels. It allows users to register, view, and interact with a dynamic floorplan where boxes can be dragged, resized, and updated in real time.

### Main Features

* **User Registration and Authentication:** New users can register and log in to access their personalized floorplan.
* **Real-Time Box Updates:** Changes to the box position and size are updated in real time using WebSockets via Django Channels.
* **Operation Logs:** Tracks all user interactions (e.g., drag, resize, restore) with detailed logs.
* **Interactive UI Components:** Utilizes jQuery for DOM manipulation, Bootstrap for styling, and Chart.js for visualizing operation history.

### Usage Scenarios

* **Architectural Planning:** Ideal for designing and visualizing floorplans interactively.
* **Interactive Dashboards:** Can be used as part of an IoT control panel or any application requiring real-time visual updates.
* **Collaborative Design Tools:** Supports multiple users with real-time updates, making it suitable for collaborative environments.

## Technical Stack

* **Programming Language:** Python
* **Framework:** Django (including Django REST Framework and Django Channels)
* **Other Tools:**
   * **django-environ:** For managing environment variables.
   * **Bootstrap:** For front-end styling.
   * **jQuery:** For DOM manipulation and AJAX requests.
   * **Chart.js:** For creating interactive visualizations.

## Installation and Usage Instructions

### Cloning the Repository

```bash
git clone https://github.com/yourusername/blueprint_project.git
cd blueprint_project
```

### Installing Dependencies

```bash
pip install -r requirements.txt
```

### Setting Up the Environment

* Create a `.env` file in the project root with the necessary settings. For example:

```ini
SECRET_KEY=your_secret_key_here
DEBUG=True
```

### Running Migrations and Starting the Server

* Run database migrations:

```bash
python manage.py migrate
```

* Start the development server:

```bash
python manage.py runserver
```

* **WebSocket Testing:** To test WebSocket functionality, run the server using Daphne:

```bash
daphne blueprint_project.asgi:application
```

This command will launch the ASGI server and enable real-time features via Django Channels.

### Running Tests

* To run unit and integration tests:

```bash
python manage.py test
```