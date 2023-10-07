import rumps
import datetime
import pyperclip
import keyring
import http.client
import json
# import hashlib

class ZeroTierApp(rumps.App):
    def __init__(self):
        super(ZeroTierApp, self).__init__("Z")
        self.network_id = keyring.get_password("ZeroTierApp", "network_id")  # Retrieve network_id from keyring
        self.api_token = keyring.get_password("ZeroTierApp", "api_token")  # Retrieve api_token from keyring
        
        if self.network_id and self.api_token:  # Check if credentials are set
            self.update_members(None)
        
        else:
            self.prompt_credentials()  # Prompt user for credentials if not set
        
        self.hashedname_ip_map = {}

        self.timer = rumps.Timer(self.update_members, 60)  # Set up a timer to call update_members every 60 seconds
        self.timer.start()  # Start the timer

    def prompt_credentials(self):
        self.update_info(None)  # Call update_info to prompt user for credentials

    def update_info(self, _):
        api_token_window = rumps.Window(message='Enter API Key:', title='Update API Key')
        # api_token_window.icon='icons8-key-100.png'
        api_token_response = api_token_window.run()
        if api_token_response.clicked:
            self.api_token = api_token_response.text
            keyring.set_password("ZeroTierApp", "api_token", self.api_token)  # Save api_token to keyring

        network_id_window = rumps.Window(message='Enter Network ID:', title='Update Network ID')
        network_id_response = network_id_window.run()
        if network_id_response.clicked:
            self.network_id = network_id_response.text
            keyring.set_password("ZeroTierApp", "network_id", self.network_id)  # Save network_id to keyring

        if self.network_id and self.api_token:  # Check if credentials are set
            self.update_members(None)

    def refresh(self, _):
        self.update_members(None)

    def update_members(self, _):
        self.menu = [
            rumps.MenuItem("Update Info", callback=self.update_info),
            None  # This adds a separator in the menu
        ]
        self.name_ip_map = {}
        members = self.get_network_members()
        self.menu.clear()
        self.menu.add(rumps.MenuItem("Force Refresh (auto every 60 sec)", callback=self.refresh))
        self.menu.add(None)  # Adds a separator

        for member in members:
            name = member.get('name', 'N/A')
            ip_assignment = 'N/A'
            if isinstance(member.get('config'), dict) and isinstance(member['config'].get('ipAssignments'), list) and member['config']['ipAssignments']:
                ip_assignment = member['config']['ipAssignments'][0]
            last_seen_timestamp = member.get('lastSeen', None)
            if last_seen_timestamp is not None:
                last_seen_datetime = datetime.datetime.utcfromtimestamp(last_seen_timestamp/1000)
                current_datetime = datetime.datetime.utcnow()
                time_diff = current_datetime - last_seen_datetime
                minutes, seconds = divmod(time_diff.seconds, 60)
                hours, minutes = divmod(minutes, 60)
                days, hours = divmod(hours, 24)
                if days > 0:
                    last_seen = f"seen {days} day{'s' if days > 1 else ''} ago"
                elif hours > 0:
                    last_seen = f"seen {hours:02} hr{'s' if hours > 1 else ''} ago"
                elif minutes > 0:
                    last_seen = f"seen {minutes:02} min{'s' if minutes > 1 else ''} ago"
                else:
                    last_seen = f"seen {seconds:02} sec{'s' if seconds > 1 else ''} ago"
            else:
                last_seen = 'N/A'

            # Create a main menu item for each member
            menu_item = rumps.MenuItem(title=f"{name} - {last_seen}")
            self.name_ip_map[hash(menu_item.title)] = ip_assignment


            # Create submenus for each piece of information
            ip_submenu = rumps.MenuItem(title=f"IP: {ip_assignment}")
            phys_addr_submenu = rumps.MenuItem(title=f"Physical Address: {member.get('physicalAddress', 'N/A')}")  # Assuming 'physicalAddress' is a key in the member dictionary
            description = rumps.MenuItem(title=f"Description: {member.get('description', 'N/A')}")  # Assuming 'physicalAddress' is a key in the member dictionary
            # Append the submenus to the main menu item
            menu_item.add(ip_submenu)
            menu_item.add(phys_addr_submenu)
            menu_item.add(description)


            # Add a callback to the main menu item to copy the IP when clicked
            def callback(_sender):
                val = self.name_ip_map[hash(_sender.title)]
                pyperclip.copy(val)
                rumps.notification("IP Copied", "IP address has been copied to clipboard", val)
                print("IP Copied", "IP address has been copied to clipboard", val)

            menu_item.set_callback(callback)

            # Add the main menu item (with submenus) to the main menu
            self.menu.add(menu_item)

        self.menu.add(rumps.MenuItem(title=f"Click item to copy IP"))
        self.menu.add(None)
        self.menu.add(rumps.MenuItem("Preferences", callback=self.update_info))
        self.menu.add(rumps.MenuItem("Quit", callback=rumps.quit_application))




    def get_network_members(self):
        url = f"https://my.zerotier.com/api/network/{self.network_id}/member"
        headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        }
        
        conn = http.client.HTTPSConnection("my.zerotier.com")
        conn.request("GET", "/api/network/b15644912ea32f67/member", headers=headers)
        response = conn.getresponse()
        if response.status == 200:
            return json.loads(response.read().decode('utf-8'))
        else:
            print(f'Error: {response.status}')
            rumps.notification("Error", "Failed to retrieve members", f"Status Code: ??")
        conn.close()
        return {}
if __name__ == "__main__":
    app = ZeroTierApp()
    app.run()
