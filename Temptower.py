# Cura PostProcessingPlugin
# Author:   Christian Köhlke
# Date:     July 13, 2019

# Description:  postprocessing-script to easily use an temptower and not use 10 changeAtZ-scripts
#
#
#
# The default values are for this temptower
#
# https://www.thingiverse.com/thing:2493504
#
#



from ..Script import Script
from UM.Application import Application

class Temptower(Script):
    def __init__(self):
        super().__init__()

    def getSettingDataString(self):
        return """{
            "name": "Temptower",
            "key": "Temptower",
            "metadata": {},
            "version": 2,
            "settings":
            {
                "startTemperature":
                {
                    "label": "starting Temperature",
                    "description": "the starting Temperature of the TempTower.",
                    "type": "int",
                    "default_value": 220,
                    "minimum_value": 100,
                    "maximum_value": 300,
                    "minimum_value_warning": 150,
                    "maximum_value_warning": 250
                },
                "temperaturechange":
                {
                    "label": "Temperature increment",
                    "description": "the temperature change of each block, can be positive or negative. I you want 220 and then 210, you need to set this to -10.",
                    "type": "int",
                    "default_value": -5,
                    "minimum_value": -100,
                    "maximum_value": 100,
                    "minimum_value_warning": -20,
                    "maximum_value_warning": 20
                },
                "changelayer":
                {
                    "label": "Change Layer",
                    "description": "how many layers needs to be printed before the temperature should be changed.",
                    "type": "float",
                    "default_value": 34,
                    "minimum_value": 1,
                    "maximum_value": 1000,
                    "minimum_value_warning": 5,
                    "maximum_value_warning": 100
                },
                "changelayeroffset":
                {
                    "label": "Change Layer Offset",
                    "description": "if the Temptower has a base, put the layer high off it here",
                    "type": "float",
                    "default_value": 4,
                    "minimum_value": 0,
                    "maximum_value": 1000,
                    "maximum_value_warning": 100
                }
                
            }
        }"""

    def execute(self, data):
        
        startTemperature = self.getSettingValueByKey("startTemperature")
        temperaturechange = self.getSettingValueByKey("temperaturechange")
        changelayer = self.getSettingValueByKey("changelayer")
        changelayeroffset = self.getSettingValueByKey("changelayeroffset")

                    
        currentTemperature = startTemperature

        for layer in data:
            layer_index = data.index(layer)

            lines = layer.split("\n")
            for line in lines:
                if line.startswith(";LAYER:"):
                    line_index = lines.index(line)
                    
                    if (layer_index==changelayeroffset):
                        lines.insert(line_index + 1, "M104 S"+str(currentTemperature))
                        
                    if ((layer_index-changelayeroffset) % changelayer == 0) and ((layer_index-changelayeroffset)>0):
                        currentTemperature += temperaturechange
                        lines.insert(line_index + 1, "M104 S"+str(currentTemperature))
                        
                            
            
            result = "\n".join(lines)
            data[layer_index] = result

        return data
