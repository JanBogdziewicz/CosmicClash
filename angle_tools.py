class AngleTools:
    def add_angles(self, a, b):
        result = a + b
        if result >= 360:
            result -= 360
        return result

    def subtract_angle(self, a, b):
        result = a - b
        if result < 0:
            result += 360
        return result

    def calculate_bounce_angle(self, object_angle, collision_angle):
        object_angle = self.subtract_angle(object_angle, collision_angle)
        temp = 360 - object_angle
        result = self.add_angles(temp, collision_angle)
        return result