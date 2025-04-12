flowchart TD
    %% --- Subgraphs ---
    subgraph CLIENT["Client Side"]
        Browser["Web Browser"]
        HTML["floorplan.html"]
        JS_WS["JavaScript<br>WebSocket Client"]
        LayoutConsumer["LayoutConsumer"]
    end

    subgraph SERVER["Server Side"]
        subgraph DjangoApp["Django Application"]
            Views["views.py<br>HTTP Request Handlers"]
            Routing["routing.py<br>WebSocket Routing"]
            Channels["Channels Layer"]
            AsyncConsumer["AsyncWebSocketConsumer"]
            
            subgraph DataLayer["Data Layer"]
                Models["models.py<br>Box, OperationLog"]
                REST["Django REST Framework<br>BoxSerializer, OperationLogSerializer"]
                DB[(SQLite Database<br>settings.py)]
            end
        end
    end

    %% --- Connections ---
    Browser -->|HTTP Requests| Views
    Views -->|HTTP Responses<br>(JSON/HTML)| HTML
    Browser <-->|WebSocket Connection| JS_WS
    JS_WS -->|Real-time events| LayoutConsumer
    LayoutConsumer -->|Channel routing| Routing
    Routing -->|Message dispatch| Channels
    Channels -->|Event handling| AsyncConsumer
    AsyncConsumer -->|Query/Update| Models
    AsyncConsumer -->|Serialize| REST
    Models <-->|ORM| DB
    REST -->|Serialize/Deserialize| Models
    Views -->|Query/Update| Models
    Views -->|Serialize| REST

    %% --- Styling ---
    %% Adjust the fill colors and strokes to match your preferred palette
    classDef clientSide fill:#ffe6e6,stroke:#888,stroke-width:1px,color:#000
    classDef serverSide fill:#e6f0ff,stroke:#888,stroke-width:1px,color:#000
    classDef dataLayer fill:#e6ffed,stroke:#888,stroke-width:1px,color:#000

    class Browser,HTML,JS_WS,LayoutConsumer clientSide
    class Views,Routing,Channels,AsyncConsumer serverSide
    class Models,REST,DB dataLayer
