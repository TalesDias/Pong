import _thread, io, time, pygame


class Keyboard:
	def __init__(self, event_stack):
		self.while_key_pressed_events = []
		self.on_key_pressed_events = []
		self.on_key_released_events = []

		self.event_stack = event_stack
		_thread.start_new_thread(self.handle_events,(event_stack,))

	def handle_events(self, event_stack):
		while True:
			events = self.event_stack.get()
			for keyboard_event in events:

				if keyboard_event.type == pygame.KEYDOWN:
					for user_event in self.while_key_pressed_events:
						if user_event[0] == keyboard_event.key:
							user_event[2] = True
					for user_event in self.on_key_pressed_events:
						if user_event[0] == keyboard_event.key:
							user_event[1]()

				elif keyboard_event.type == pygame.KEYUP:
					for user_event in self.while_key_pressed_events:
						if user_event[0] == keyboard_event.key:
							user_event[2] = False
					for user_event in self.on_key_released_events:
						if user_event[0] == keyboard_event.key:
							user_event[1]()

			for user_event in self.while_key_pressed_events:
				if user_event[2]:
					user_event[1]()

			time.sleep(0.1)


	def while_key_pressed(self, key, event):
		active=False
		event = [key, event, active]
		self.while_key_pressed_events.append(event)

	def on_key_pressed(self, key, event):
		event = [key, event]
		self.on_key_pressed_events.append(event)

	def on_key_released(self, key, event):
		event = [key, event]
		self.on_key_released_events.append(event)

