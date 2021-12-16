import numpy as np


# dim = 0 -> shift up/down
# dim = 1 -> shift left/right
def shift_old(arr, dim, amnt, fill_value=0):
	ret = np.empty_like(arr)
	if dim == 0:
		if amnt > 0:
			ret[:amnt,:] = fill_value
			ret[amnt:,:] = arr[:-amnt,:]
		elif amnt < 0:
			ret[amnt:,:] = fill_value
			ret[:amnt,:] = arr[-amnt:,:]
		else:
			ret[:] = arr # just copy
	elif dim == 1:
		if amnt > 0:
			ret[:,:amnt] = fill_value
			ret[:,amnt:] = arr[:,:-amnt]
		elif amnt < 0:
			ret[:,amnt:] = fill_value
			ret[:,:amnt] = arr[:,-amnt:]
		else:
			ret[:] = arr # just copy
	else:
		ret[:,:] = arr; # just copy
	return ret
	
def shift2(arr, amntx, amnty, fill_value=0):
	ret = np.empty_like(arr)
	if amntx > 0:
		if amnty > 0:
			ret[:,:amntx] = fill_value
			ret[:amnty,:] = fill_value
			ret[amnty:,amntx:] = arr[:-amnty,:-amntx]
		elif amnty < 0:
			ret[amnty:,:] = fill_value
			ret[:,:amntx] = fill_value
			ret[:amnty,amntx:] = arr[-amnty:,:-amntx]
		else:
			ret[:,:amntx] = fill_value
			ret[:,amntx:] = arr[:,:-amntx]
	elif amntx < 0:
		if amnty > 0:
			ret[:amnty,:] = fill_value
			ret[:,amntx:] = fill_value
			ret[amnty:,:amntx] = arr[:-amnty,-amntx:]
		elif amnty < 0:
			ret[amnty:,:] = fill_value
			ret[:,amntx:] = fill_value
			ret[:amnty,:amntx] = arr[-amnty:,-amntx:]
		else:
			ret[:,amntx:] = fill_value
			ret[:,:amntx] = arr[:,-amntx:]
	else: # amntx == 0
		if amnty > 0:
			ret[:amnty,:] = fill_value
			ret[amnty:,:] = arr[:-amnty,:]
		elif amnty < 0:
			ret[amnty:,:] = fill_value
			ret[:amnty,:] = arr[-amnty:,:]
		else: # amnty == 0
			ret[:,:] = arr; # just copy
	return ret
	
def shiftup(arr, amnt, fill_value=0):
	return shift2(arr, 0, amnt, fill_value)
	
def shiftdown(arr, amnt, fill_value=0):
	return shift2(arr, 0, -amnt, fill_value)
	
def shiftright(arr, amnt, fill_value=0):
	return shift2(arr, amnt, 0, fill_value)
	
def shiftleft(arr, amnt, fill_value=0):
	return shift2(arr, -amnt, 0, fill_value)


	
	
	
