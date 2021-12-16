
from dataclasses import dataclass

@dataclass
class Turn:
	from_x: int # from 0 to 7
	from_y: int # from 0 to 7
	to_x: int # ""
	to_y: int # ""
	give_up: bool = False
	
	def __repr__(self):
		if self.give_up:
			return "Gave Up!"
		return chr(ord('a')+self.from_x) + str(self.from_y+1) + \
				"-" + chr(ord('a')+self.to_x) + str(self.to_y+1)
	
		