import json
from channels.generic.websocket import AsyncWebsocketConsumer

class LayoutConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Add all connected users to the "layout" group.
        await self.channel_layer.group_add("layout", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("layout", self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        # Broadcast the update to all users in the group.
        await self.channel_layer.group_send(
            "layout",
            {
                "type": "layout_update",
                "data": data
            }
        )

    async def layout_update(self, event):
        # Send the update data to the client.
        await self.send(text_data=json.dumps(event["data"]))
