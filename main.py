from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
import subprocess

class VPNApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')
        self.connect_button = Button(text='Connect', on_press=self.connect_to_vpn)
        self.disconnect_button = Button(text='Disconnect', on_press=self.disconnect_from_vpn)
        self.server_address_input = TextInput(hint_text='Server Address')
        self.username_input = TextInput(hint_text='Username')
        self.monitor_input = TextInput(hint_text='Monitor')
        self.password_input = TextInput(hint_text='Password', password=True)
        self.layout.add_widget(self.monitor_input)
        self.layout.add_widget(self.server_address_input)
        self.layout.add_widget(self.username_input)
        self.layout.add_widget(self.password_input)
        self.layout.add_widget(self.connect_button)
        self.layout.add_widget(self.disconnect_button)
        return self.layout

    def connect_to_vpn(self, instance):
        # Get user inputs for server address, username, password, etc.
        server_address = self.server_address_input.text
        username = self.username_input.text
        password = self.password_input.text

        # Run the OpenVPN command to connect
        cmd = f"openvpn --config {server_address} --auth-user-pass <(echo '{username}\\n{password}')"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

        # Check the result and display the appropriate message
        if result.returncode == 0:
            self.layout.add_widget(Label(text='Connected'))
        else:
            self.monitor_input.text = 'Connection failed'

    def disconnect_from_vpn(self, instance):
        # Run the OpenVPN command to disconnect
        cmd = "pkill -f 'openvpn --config'"
        subprocess.run(cmd, shell=True)

        # Display disconnection status
        self.monitor_input.text = 'Disconnected'

if __name__ == '__main__':
    VPNApp().run()
