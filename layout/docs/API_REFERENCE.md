# API Reference

This document provides a comprehensive reference for all API endpoints available in the Blueprint Project. These endpoints allow interaction with the floorplan editor for creating, updating, and managing boxes, as well as tracking operation logs.

## Authentication

All API requests require the user to be authenticated. As shown in the floorplan.html implementation, the Blueprint Project uses Django's session-based authentication which is managed through cookies.

```
{% if not user.is_authenticated %}
<div class="container mt-5">
    <div class="text-center">
        <h3>Please login</h3>
        <a href="{% url 'login' %}" class="btn btn-primary m-2">Login</a>
        <a href="{% url 'register' %}" class="btn btn-secondary m-2">Register</a>
    </div>
</div>
{% else %}
<!-- Application content -->
{% endif %}
```

Additionally, CSRF protection is implemented for all AJAX requests as demonstrated in the JavaScript code.

## Core Endpoints

Based on the provided floorplan.html file, the following endpoints are utilized:

### Box Management

#### POST /update-box/ ({% url 'update_box' %})

- **Description:** Updates the position and size of a box and notifies other users via WebSockets.
- **Request Example:**
```json
{
  "id": 1,
  "x": 60,
  "y": 60,
  "width": 110,
  "height": 110,
  "action": "update"
}
```
- **Response Example:**
```json
{
  "status": "success",
  "message": "Update success"
}
```
- **Usage in code:**
```javascript
function updateBoxPosition(id, x, y, width, height) {
    const data = {
        id: id,
        x: x,
        y: y,
        width: width,
        height: height,
        action: "update"
    };

    // Send update via AJAX.
    $.ajax({
        url: "{% url 'update_box' %}",
        type: "POST",
        data: JSON.stringify(data),
        contentType: "application/json; charset=utf-8",
        success: function(response) {
            showNotification("Update success");
            console.log("Update success:", response);
        },
        error: function(xhr) {
            showNotification("Update error", false);
            console.error("Update error:", xhr);
        }
    });
}
```

### Operation Logs

#### GET /api/logs/

- **Description:** Retrieves operation logs for the authenticated user's boxes.
- **Parameters:** None identified in the implementation.
- **Response Example:** Array of log entries in JSON format:
```json
[
  {
    "id": 1,
    "box": 1,
    "action": "drag",
    "x": 50,
    "y": 50,
    "width": 100,
    "height": 100,
    "timestamp": "2025-04-05T12:34:56Z"
  }
]
```
- **Usage in code:**
```javascript
document.getElementById('btn-view-history').addEventListener('click', function(){
    $.ajax({
        url: '/api/logs/',
        type: 'GET',
        success: function(data) {
            // Process and display logs
            // ...
        }
    });
});
```

#### DELETE /api/logs/{id}/

- **Description:** Deletes a specific operation log entry.
- **Parameters:** 
  - `id` (path parameter): The identifier of the log entry to delete.
- **Response:** Success status with no content.
- **Usage in code:**
```javascript
function deleteOperationLog(logId) {
    $.ajax({
        url: '/api/logs/' + logId + '/',
        type: 'DELETE',
        success: function(response) {
            showNotification("Delete success");
            // Reload history to update the table
            $('#btn-view-history').click();
        },
        error: function(err) {
            console.error("Error deleting log:", err);
            showNotification("Delete error", false);
        }
    });
}
```

### Box Restoration

The HTML shows a function for restoring boxes to a previous state:

```javascript
function restoreOperationLog(boxId, x, y, width, height) {
    // Prepare data to restore the box's state.
    const data = {
        id: boxId,
        x: x,
        y: y,
        width: width,
        height: height,
        action: "restore"
    };
    $.ajax({
        url: "{% url 'update_box' %}",
        type: "POST",
        data: JSON.stringify(data),
        contentType: "application/json; charset=utf-8",
        success: function(response) {
            showNotification("Restore success");
            // Update the corresponding box element immediately.
            // ...
        },
        error: function(xhr) {
            showNotification("Restore error", false);
            console.error("Restore error:", xhr);
        }
    });
}
```

This uses the same endpoint as updating a box, but with an `action` value of "restore".

## WebSocket Communication

The Blueprint Project uses WebSockets for real-time communication between clients. The implementation in floorplan.html establishes a connection to the server and handles messages:

### Connection

To establish a WebSocket connection:

```javascript
const wsUrl = (window.location.protocol === "https:" ? "wss://" : "ws://") + window.location.host + "/ws/layout/";
const layoutSocket = new WebSocket(wsUrl);
```

### Message Format

Messages sent over the WebSocket connection follow this format:

```json
{
  "id": 1,
  "x": 60,
  "y": 60,
  "width": 110,
  "height": 110,
  "action": "update"
}
```

### Handling Messages

The application processes WebSocket messages to update box positions in real-time:

```javascript
layoutSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    // Assume data contains { id, x, y, width, height }
    const boxElem = $("#box-" + data.id);
    if (boxElem.length > 0) {
        boxElem.css({
            left: Math.round(data.x) + "px",
            top: Math.round(data.y) + "px",
            width: Math.round(data.width) + "px",
            height: Math.round(data.height) + "px"
        });
        boxElem.find('.box-info').html(
            "x: " + Math.round(data.x) + ", y: " + Math.round(data.y) +
            "<br>w: " + Math.round(data.width) + ", h: " + Math.round(data.height)
        );
    }
};
```

## Permission System

The Blueprint Project implements a permission system to control access to advanced features:

```javascript
// check if user belongs to Engineer or Admin group
const allowedAdvancedActions = {{ allowed_advanced_actions|yesno:"true,false" }};
```

This permission flag controls whether certain UI elements are displayed and whether users can perform operations like deleting logs or restoring boxes.

## Error Handling

The application displays status notifications for successful and failed operations:

```javascript
function showNotification(message, success=true) {
    const notify = $('#notification');
    notify.css({
        'background': success ? '#28a745' : '#dc3545'
    });
    notify.text(message).fadeIn(200).delay(1000).fadeOut(200);
}
```

These notifications appear for the following operations:
- Box updates
- Log deletions  
- Box restorations

## Additional Notes

The Blueprint Project supports several features not directly tied to API endpoints:

1. **Background Image Upload**: Users can upload a custom background image for the floorplan.
2. **Operation History Visualization**: A chart displaying the frequency of different operation types using Chart.js.
3. **Box Manipulation**: Boxes can be dragged and resized using jQuery UI, with changes confirmed via modal dialogs.