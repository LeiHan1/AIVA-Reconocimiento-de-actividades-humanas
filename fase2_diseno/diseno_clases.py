import cv2


class Position:
    def __init__(self, x_min, y_min, x_max, y_max):
        self.x_min = x_min
        self.y_min = y_min
        self.x_max = x_max
        self.y_max = y_max

    def set_position(self, x_min, y_min, x_max, y_max):
        self.x_min = x_min
        self.y_min = y_min
        self.x_max = x_max
        self.y_max = y_max

    def get_position(self):
        return self.x_min, self.y_min, self.x_max, self.y_max


class Person:
    def __init__(self, id, initial_position: Position, state: str):
        self.id = id
        self.initial_position = initial_position
        self.current_position = initial_position
        self.states = []
        self.states.append(state)

    def get_id(self):
        return self.id

    def get_initial_position(self):
        return self.initial_position

    def set_current_position(self, new_position):
        self.current_position = new_position

    def get_current_position(self):
        return self.current_position

    def add_states(self, state):
        self.states.append(state)

    def get_states(self):
        return self.states


class PersonTracker:
    def __init__(self):
        self.trackers = cv2.MultiTracker_create()

    def start_tracking(self, frame, initial_position: Position):
        pass


class ROI:
    def __init__(self, roi_position: Position):
        self.roi_position = roi_position
        self.list_id = []

    def check_intersection(self, object_position: Position):
        pass

    def calculate_area(self, pos_a: Position, pos_b: Position):
        # returns None if rectangles don't intersect
        pass


class DoorDetector(ROI):
    def __init__(self, roi_position: Position):
        super().__init__(roi_position)
        self.count_entry = 0
        self.count_exit = 0

    def check_up_down(self, object_position: Position):
        pass


class CorridorDetector():
    def __init__(self, position_left: Position, position_right: Position):
        self.LeftDetector = ROI(position_left)
        self.RightDetector = ROI(position_right)
        self.count_pass_through = 0

    def check_pass_through(self, id:int, direction:str):
        pass


class DetectSystem:
    def __init__(self, position_door: Position, position_left: Position, position_right: Position):
        self.list_persons = []
        self.tracker = PersonTracker()
        self.entrance_detector = DoorDetector(position_door)
        self.corridor_detector = CorridorDetector(position_left, position_right)
        self.hog = cv2.HOGDescriptor()
        self.hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

    def read_video(self, video_path):
        pass

    def image_process(self, frame):
        pass

    def detect_pedestrian(self, frame):
        pass

    def check_pedestrian_already_exists(self):
        pass

    def person_state_identification(self):
        pass

    def save_results(self):
        pass

    def run(self):
        pass
