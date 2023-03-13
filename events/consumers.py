# app/simple_app/consumers.py
from channels.generic.websocket import JsonWebsocketConsumer
from django.template.loader import render_to_string
from .models import Event
from asgiref.sync import async_to_sync
 
class EventsConsumer(JsonWebsocketConsumer):
    room_name = 'broadcast'
 
    def connect(self):
        """Event when client connects"""
 
        # Accept the connection
        self.accept()
        # Assign the Broadcast group
        print(self.channel_name)
        async_to_sync(self.channel_layer.group_add)(self.room_name, self.channel_name)
        # Send you all the messages stored in the database.
        self.send_list_events()
        print("List sent")
        
 
    def disconnect(self, close_code):
        """Event when client disconnects"""
        # Remove from the Broadcast group
        async_to_sync(self.channel_layer.group_discard)(self.room_name, self.channel_name)
        
 
    def receive_json(self, data_received):
        """
            Event when data is received
            All information will arrive in 2 variables:
            'action', with the action to be taken
            'data' with the information
        """
        # Get data
        data = data_received['data']
        # Depending on the action, do a task or another
        match data_received['action']:
            case 'add event':
                print('Event added!')
                self.send_list_events()
            case 'list events':
                self.send_list_events()

    def send_html(self, event):
        """Event: Send html to client"""
        data = {
            'selector': event['selector'],
            'html': event['html'],
        }
        self.send_json(data)

    def send_list_events(self):
        print('Sending list')
        events = Event.objects.order_by('-created')
        async_to_sync(self.channel_layer.group_send)(
            self.room_name, {
                'type': 'send.html',
                'selector': '#events__list',
                'html': render_to_string('components/_list-events.html', { 'events': events })
            }
        )