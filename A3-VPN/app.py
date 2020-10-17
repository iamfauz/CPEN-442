from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ListProperty
from kivy.graphics import Color, Rectangle
from kivy.uix.textinput import TextInput
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.button import Button
from kivy.uix.switch import Switch
from kivy.uix.behaviors import ToggleButtonBehavior

import threading
import datetime
import ipaddress

from server import Server
from client import Client

# This is the entrypoint of our application
class VpnChatApp(App):

    def __init__(self, **kwargs):
        super(VpnChatApp, self).__init__(**kwargs)
        self.client = None
        self.server = None
        self.message_receiver = None # Thread that listens to the receive queue of connection

    # Callback function called when connection is succesfully established
    # This connects the Message reciever thread to the appropiate connection
    def on_connected_callback(self, ip_addr, port):
        sender_name = ""
        conn = None
        chat_window = self.chat_window
        if self.server_mode.state == "down":
            self.chat_window.write_info("Client connected from (%s, %i)" % (ip_addr, port))
            sender_name = "CLIENT"
            conn = self.server
        else:
            sender_name = "SERVER"
            conn = self.client
        # Once connection is established, run a Message reciever thread to listen on the queue
        self.message_receiver = MessageReceiver(sender_name, conn, chat_window)
        self.message_receiver.start()


    # Called when 'Connect' button is pressed
    def on_connect_btn_clicked(self, btn):

        self.disconnect_button.disabled = True

        # Get Port# from GUI
        port = self.get_config_widget_input(self.port)
        try:
                port = int(port)
        except ValueError:
                self.chat_window.write_info("Invalid port: " + port)
                return

        # Get Shared key from GUI
        shared_key = self.get_config_widget_input(self.shared_value)
        shared_key = str(shared_key)
        shared_key = shared_key.encode("utf8")
        shared_key = shared_key.zfill(16) #pad the key to be 16 bytes
        if not shared_key:
                self.chat_window.write_info("Enter Shared key")
                return

        # Get IP from GUI
        if (self.client_mode.state == 'down'):
            ip_address = self.get_config_widget_input(self.ip_address)
            ip_address = str(ip_address) # Probablu need to sanitaize input i.e check if valid IP or not
            if not ip_address:
                self.chat_window.write_info("Enter Valid IP Adress")
                return

        if (self.server_mode.state == 'down'):
            # Initialize Server and setup server
            self.server = Server(
                    port,
                    shared_key,
                    self.on_connected_callback,

            )
            message = self.server.setup()
            self.chat_window.write_info(message)
            self.server.start()
        else:
            # Initialize Client and initaiate connection
            self.client = Client(
                    ip_address,
                    port,
                    shared_key,
            )
            message = self.client.connect()
            self.chat_window.write_info(message)
            self.on_connected_callback(ip_address, port)

    # Client Toggle button onClick fuction
    def toggle_client_button(self, *args):
        state = args[1]
        if state == "down":
            self.control_panel.add_widget(self.ip_address, 7)
            self.chat_window.write_info("You are now in Client Mode")

     # Server Toggle button onClick fuction
    def toggle_server_button(self, *args):
        state = args[1]
        if state == "down":
            self.control_panel.remove_widget(self.ip_address)
            self.chat_window.write_info("You are now in Server Mode")

    # Called when Send button is clicked
    def on_send_btn_clicked(self, btn):
        msg = self.chat_input.text
        self.chat_window.write_message("ME", msg)
        if self.server_mode.state == 'down':
                self.server.send(msg)
        else:
                self.client.send(msg)
        self.chat_input.text = "" # Clear Text Input

    # Widget used for IP, Port, Shared Secret Input
    def ConfigWidget(self,text=None):
        box_layout = BoxLayout(orientation="vertical", padding=30)
        self.label = Label(text=text, size=(300, 50),size_hint=(1, None))
        box_layout.add_widget(self.label)
        self.textinput = TextInput(multiline=False, size=(300, 50), size_hint=(1, None))
        box_layout.add_widget(self.textinput)
        return box_layout

    def get_config_widget_input(self, config_widget):
        for child in config_widget.children:
            if isinstance(child, TextInput):
                return str(child.text)

    def build(self):
        # Root Widget
        self.root = BoxLayout(
                orientation="horizontal",
                spacing=10,
                padding=10
        )

        # Control Panel Widget
        self.control_panel = ColoredBoxWidget(
                            orientation="vertical",
                            background_color=(96,96,96,0),
                            size_hint=(0.3, 1),
                            padding=10,
        )

        # Client/Server Toggle Buttons
        self.client_mode = ToggleButton(
                text='Client',
                group='mode',
                state='down',
                allow_no_selection=False,
                size=(300,50),
                size_hint=(1, None)
        )
        self.server_mode = ToggleButton(
                text='Server',
                group='mode',
                allow_no_selection=False,
                size=(300,50),
                size_hint=(1, None)
        )
        self.client_mode.bind(state=self.toggle_client_button)
        self.server_mode.bind(state=self.toggle_server_button)
        self.control_panel.add_widget(self.client_mode)
        self.control_panel.add_widget(self.server_mode)
        self.control_panel.add_widget(Widget())

        # IP Address Input
        self.ip_address = self.ConfigWidget(text="Server IP Address")
        self.control_panel.add_widget(self.ip_address)
        self.control_panel.add_widget(Widget())

        # Port Input
        self.port = self.ConfigWidget(text="Server Port")
        self.control_panel.add_widget(self.port)
        self.control_panel.add_widget(Widget())

        # Shared Value Input
        self.shared_value = self.ConfigWidget(text="Shared Secret Value")
        self.control_panel.add_widget(self.shared_value)


        # Connect and Disconnect Buttons
        self.connect_button = Button(
                text="Connect",
                background_color=(0,1,0,1),
                size=(300, 85),
                size_hint=(1, None)
        )
        self.connect_button.bind(on_press=self.on_connect_btn_clicked)
        self.disconnect_button = Button(
                text="Disconnect",
                background_color=(1,0,0,1),
                size=(300, 85),
                size_hint=(1, None),

        )
        self.control_panel.add_widget(self.connect_button)
        self.control_panel.add_widget(self.disconnect_button)

        # Chat Layout Panel
        self.chat_layout = BoxLayout(
                orientation="vertical",
                spacing=10,
                size_hint=(0.7, 1)
        )
        self.chat_window = ChatWindow()
        self.input_layout = BoxLayout(
                orientation="horizontal",
                spacing=10,
                size=(0, 50),
                size_hint=(1, None)
        )
        self.chat_input = TextInput(size_hint=(0.8, 1))
        self.send_button = Button(size_hint=(0.2, 1), text="Send")
        self.send_button.bind(on_press=self.on_send_btn_clicked)
        self.input_layout.add_widget(self.chat_input)
        self.input_layout.add_widget(self.send_button)
        self.chat_layout.add_widget(self.chat_window)
        self.chat_layout.add_widget(self.input_layout)

        self.root.add_widget(self.chat_layout)
        self.root.add_widget(self.control_panel)

        return self.root

class ColoredBoxWidget(BoxLayout):

    def __init__(self, background_color=(160,160,160,0.5), **kwargs):
        super(ColoredBoxWidget, self).__init__(**kwargs)
        self.background_color = background_color
        with self.canvas:
            Color(*background_color)
            self.rect = Rectangle(pos=self.pos, size=self.size)

        self.bind(pos=self.update_rect,
                  size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

class ChatWindow(TextInput):

    def __init__(self, **kwargs):
        self.lock = threading.Lock()
        super(ChatWindow, self).__init__(**kwargs)

    def write(self, message):
        self.lock.acquire()
        try:
            self.text += message + "\n"
        except UnicodeDecodeError:
            pass
        self.lock.release()

    def write_message(self, tag, message):
        time = datetime.datetime.now().time().strftime('%H:%M')
        header = "(%s) [%s]     " %(time, tag)
        self.write(header + message)

    def write_info(self, message):
        time = datetime.datetime.now().time().strftime('%H:%M')
        info_msg = "(%s) [INFO]     " % (time)
        self.write(info_msg + message)

# Thread that listens to the recieve queue of the connection and
# Outputs stuff on the Chat Window
class MessageReceiver(threading.Thread):

    def __init__(self, tag, conn, chat_window):
        threading.Thread.__init__(self)
        self.tag = tag
        self.conn = conn
        self.queue = self.conn.receive_queue
        self.chat_window = chat_window
        self.keep_alive = True

    def run(self):
        while self.keep_alive:
            msg = self.conn.receive()
            if msg:
                self.chat_window.write_message(self.tag, msg)

    def close(self):
        self.keep_alive = False

if __name__ == "__main__":
   VpnChatApp().run()
