# Design Document

## Overview
This project is a floorplan editor with real-time updates, built with Django. It leverages Django REST Framework for API endpoints and Django Channels for WebSocket communication.

## Architecture
- **Backend Framework:** Django, including Django REST Framework and Django Channels.
- **Frontend:** HTML, Bootstrap, jQuery, and Chart.js.
- **Real-Time Communication:** WebSockets (via Django Channels) for updating box positions in real-time.
- **Database:** SQLite for development.

## Key Components
- **Models:** 
  - `Box`: Represents a movable/resizable element with properties such as x, y coordinates, width, height, and color.
  - `OperationLog`: Logs actions performed on boxes (drag, resize, restore).
- **Views:** 
  - User registration and login.
  - Floorplan rendering and box update endpoints.
- **WebSocket Consumers:** 
  - `LayoutConsumer` to handle real-time communication for box updates.

## Design Decisions
- **Django REST Framework:** For exposing RESTful APIs that return box and log data.
- **Channels:** To enable real-time updates across multiple clients.
- **Client-Side Interaction:** jQuery UI is used for drag-and-drop and resize functionality, with AJAX calls to update the backend.
