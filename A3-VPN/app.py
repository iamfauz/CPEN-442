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

# This is the entrypoint of our application
class VpnChatApp(App):
    
    # Widget used for IP, Port, Shared Secret Input
    def ConfigWidget(self,text=None):
        box_layout = BoxLayout(orientation="vertical", padding=30)
        self.label = Label(text=text, size=(300, 50),size_hint=(1, None))
        box_layout.add_widget(self.label)
        self.textinput = TextInput(multiline=False, size=(300, 50), size_hint=(1, None))
        box_layout.add_widget(self.textinput)
        return box_layout

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
        #self.connect.bind(on_press=self.connect_callback)
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
        self.chat_panel = TextInput()
        self.input_layout = BoxLayout(
                orientation="horizontal",
                spacing=10,
                size=(0, 50),
                size_hint=(1, None)
        )
        self.chat_input = TextInput(size_hint=(0.8, 1))
        self.send_button = Button(size_hint=(0.2, 1), text="Send")
        self.input_layout.add_widget(self.chat_input)
        self.input_layout.add_widget(self.send_button)
        self.chat_layout.add_widget(self.chat_panel)
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

if __name__ == "__main__":
   VpnChatApp().run()