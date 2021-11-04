import asyncio
from bleak import BleakScanner
import database


class Scanner:

    def __init__(self):
        self.scanned = None
        self.duration = None

    def scan(self, window=3):
        self.duration = window

        async def s(window):
            async with BleakScanner() as scanner:
                await asyncio.sleep(window)
            devices = []
            for i in range(len(scanner.discovered_devices)):
                device = scanner.discovered_devices[i]
                devices.append({'name': device.name, 'address': device.address, 'rssi': device.rssi, 'metadata': device.metadata})

            return devices

        self.scanned = asyncio.run(s(window))
        return self.scanned

    def safe(self):
        # add new devices into db
        print('safe mode')
        database.add_snapshot(self.duration)
        added = 0
        for device in self.scanned:
            if(database.add_device(device['address'], device['name'], str(device['metadata']), 0) == 1):
                    added += 1
                    print(device)
            database.make_appearence(device['address'], device['rssi'])

        return added

    def sentry(self):
        # compare devices to devices in db to see if any are new, return True if yes
        danger = False
        for device in self.scanned:
            d = database.get_device(device['address'])
            if d == False:
                if device['rssi'] > -80:
                    print(device)
                    danger = True
            if danger == True:
                return True
        return False



    def standby(self):
        # dont do shit
        print('standby')
        pass

