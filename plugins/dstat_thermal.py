### Author: Dag Wieers <dag@wieers.com>

class dstat_plugin(dstat):
    def __init__(self):
        self.name = 'thermal'
        self.type = 'd'
        self.width = 3
        self.scale = 20

        # This is extremely dirty and hard-coded, but is usually better than nothing
        if os.path.exists('/sys/devices/virtual/thermal/thermal_zone0/'):
            self.vars = ['temp', 'trip_point_0_temp']
            self.nick = ['deg', 'lim']

        elif os.path.exists('/proc/acpi/ibm/thermal'):
            self.namelist = ['cpu', 'pci', 'hdd', 'cpu', 'ba0', 'unk', 'ba1', 'unk']
            self.nick = []
            for line in dopen('/proc/acpi/ibm/thermal'):
                l = line.split()
                for i, name in enumerate(self.namelist):
                    if int(l[i+1]) > 0:
                        self.nick.append(name)
            self.vars = self.nick

        elif os.path.exists('/proc/acpi/thermal_zone/'):
            self.vars = os.listdir('/proc/acpi/thermal_zone/')
#           self.nick = [name.lower() for name in self.vars]
            self.nick = []
            for name in self.vars:
                self.nick.append(name.lower())

        else:
            raise Exception, 'Needs kernel ACPI or IBM-ACPI support'

    def check(self):
        if not os.path.exists('/proc/acpi/ibm/thermal') and \
           not os.path.exists('/proc/acpi/thermal_zone/') and \
           not os.path.exists('/sys/devices/virtual/thermal/thermal_zone0/'):
            raise Exception, 'Needs kernel ACPI or IBM-ACPI support'

    def extract(self):
        if os.path.exists('/sys/devices/virtual/thermal/thermal_zone0/'):
            for zone in self.vars:
                if os.path.isdir('/sys/devices/virtual/thermal/thermal_zone0/'+zone) == False:
                    for line in dopen('/sys/devices/virtual/thermal/thermal_zone0/'+zone).readlines():
                        l = line.split()
                        if l[0].isdigit() == True:
                            self.val[zone] = int(l[0]) / 1000
                        else:
                            self.val[zone] = 0
        elif os.path.exists('/proc/acpi/ibm/thermal'):
            for line in dopen('/proc/acpi/ibm/thermal'):
                l = line.split()
                for i, name in enumerate(self.namelist):
                    if int(l[i+1]) > 0:
                        self.val[name] = int(l[i+1])
        elif os.path.exists('/proc/acpi/thermal_zone/'):
            for zone in self.vars:
                for line in dopen('/proc/acpi/thermal_zone/'+zone+'/temperature').readlines():
                    l = line.split()
                    self.val[zone] = int(l[1])

# vim:ts=4:sw=4:et
