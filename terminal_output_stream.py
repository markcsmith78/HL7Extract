
#extends OutputStream to create a class-specific implementation of output()
class TerminalOutputStream(OutputStream):
    
    def __init__(self, hl7dict):
        self.hl7_dict = hl7dict

    def output(self):

        for key in self.hl7_dict:
            print(f"{key} -> {self.hl7_dict[key]} 
     
