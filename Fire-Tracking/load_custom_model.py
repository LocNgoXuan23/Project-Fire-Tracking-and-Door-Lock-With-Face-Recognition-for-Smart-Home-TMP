import torch 

def loadCustomModel(path, force_reload=True, conf=0.25, iou=0.45, agnostic=False, multi_label=False, classes=None, max_det=1000, amp=False, device=0):
	model = torch.hub.load('ultralytics/yolov5', 'custom', path=path, force_reload=force_reload, device=device)
	
	model.conf = conf
	model.iou = iou
	model.agnostic = agnostic
	model.multi_label = multi_label
	model.classes = classes
	model.max_det = max_det
	model.amp = amp

	return model







