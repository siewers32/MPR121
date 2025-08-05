

class SensorManager:
    def __init__(self, mpr121=None):
        self.mpr121 = mpr121

    def read_touch(self):
        """Read touch inputs from the MPR121 sensor."""
        touch_data = []
        for i in range(12):
            if self.mpr121[i].value:
                touch_data.append(i)
        return touch_data
