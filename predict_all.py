import torch
import faces_model
from PIL import Image
import data
import torchvision.transforms as transforms
from torch.autograd import Variable
from net_sphere import sphere20a
from open_face_model import OpenFace
import matplotlib.pyplot as plt

import torchvision

import torch.nn as nn

from DTNet.datasets import celebA
from data_utils import *


class ZeroPadBottom(object):
    ''' Zero pads batch of image tensor Variables on bottom to given size. Input (B, C, H, W) - padded on H axis. '''
    def __init__(self, size, use_gpu=True):
        self.size = size
        self.use_gpu = use_gpu
        
    def __call__(self, sample):
        B, C, H, W = sample.size()
        diff = self.size - H
        padding = Variable(torch.zeros(B, C, diff, W), requires_grad=False)
        if self.use_gpu:
            padding = padding.cuda()
        zero_padded = torch.cat((sample, padding), dim=2)
        return zero_padded

def predict_cartoon(image):
	f_model = sphere20a(feature=True)
	f_model.load_state_dict(torch.load('./pretrained_model/sphere20a_20171020.pth'))
	for param in f_model.parameters():
    	param.requires_grad = False
	f_model = f_model.cuda()
	model = torch.load('./log/fin_model.tar')
	# plt.imshow(image)
	# plt.show()
	img = image.convert('RGB')
	toPIL = transforms.ToPILImage()
	toTensor = transforms.ToTensor()
	pad112 = ZeroPadBottom(112)
	msface_transform = transforms.Compose(
	                [data.ResizeTransform(96), data.NormalizeRangeTanh()])
	image = msface_transform(img)
	#plt.imshow(np.transpose(image, (1, 2, 0)))
	image = toTensor(toPIL(image))
	image = image.unsqueeze(0)
	image = Variable(image.float().cuda())
	image = pad112(image)
	#image.size()
	s_f = f_model(image)
	g_model = model['G_model']
	out = g_model(s_f)
	a = out.detach()
	a = a.cpu().data
	a = (a + 1.0) * 0.5
	npimg_ms = a[0]
	zero_array = np.zeros(npimg_ms.shape)
	one_array = np.ones(npimg_ms.shape)

	npimg_ms = np.minimum(npimg_ms,one_array)
	npimg_ms = np.maximum(npimg_ms,zero_array)

	   # plt.imshow(np.transpose(npimg_ms, (1, 2, 0))) 
	   # plt.show()
	result = np.transpose(a[0], (1,2,0))
	    # a = np.expand_dims(a, axis=0) 
	#plt.imshow(result)
	return result

def predict_simpsons(image):
    print("called once")
    f_model = OpenFace(True, 0)
    f_model.load_state_dict(torch.load('./pretrained_model/openface.pth'))
    f_model = f_model.eval()
    model = torch.load('log/1543773462_318_63.tar')
#     train_set = celebA.CelebA(data_dir = './data/celebA/images', annotations_dir='./data/celebA/annotations', split='train', transform = transforms.Compose([ResizeTransform(96)]))
#     train_loader = torch.utils.data.DataLoader(train_set, batch_size=1, shuffle=True) #TODO: why does shuffle give out of bounds indices?
    msface_transform = transforms.Compose([data.ResizeTransform(96), data.NormalizeRangeTanh()])
    image = msface_transform(image)
    #plt.imshow(np.transpose(image, (1, 2, 0)))
#     image = transforms.toTensor(transforms.toPIL(image))
    image = image.unsqueeze(0)
    # data_iter = iter(train_loader)
    # img_tens = data_iter.next()
#     img_tens = img_tens.cuda()
    img_v = Variable(image.float().cuda(), requires_grad=False)
    f, f_736 = f_model(img_v)
    print(f.size(), f_736.size())
    s_G = model['G_model'](torch.cat((f, f_736), dim=1))
    up96 = nn.Upsample(size=(96,96), mode='bilinear')
    s_G = up96(s_G)
    s_G = s_G.cpu().data
    unnorm_emoji = UnNormalizeRangeTanh()
    res = unnorm_emoji(s_G[:16])
    npimg = torchvision.utils.make_grid(res, nrow=4).numpy()
    npimg = np.transpose(npimg, (1, 2, 0)) 
    zero_array = np.zeros(npimg.shape)
    one_array = np.ones(npimg.shape)
    npimg = np.minimum(npimg,one_array)
    npimg = np.maximum(npimg,zero_array)
#     plt.imshow(npimg)
    return npimg

def predict_emoji(image):
    print("emoji called once")
    f_model = OpenFace(True, 0)
    f_model.load_state_dict(torch.load('./pretrained_model/openface.pth'))
    f_model = f_model.eval()
    model = torch.load('log/1543773462_318_63.tar')
#     train_set = celebA.CelebA(data_dir = './data/celebA/images', annotations_dir='./data/celebA/annotations', split='train', transform = transforms.Compose([ResizeTransform(96)]))
#     train_loader = torch.utils.data.DataLoader(train_set, batch_size=1, shuffle=True) #TODO: why does shuffle give out of bounds indices?
    msface_transform = transforms.Compose([data.ResizeTransform(96), data.NormalizeRangeTanh()])
    image = msface_transform(image)
    #plt.imshow(np.transpose(image, (1, 2, 0)))
#     image = transforms.toTensor(transforms.toPIL(image))
    image = image.unsqueeze(0)
    # data_iter = iter(train_loader)
    # img_tens = data_iter.next()
#     img_tens = img_tens.cuda()
    img_v = Variable(image.float().cuda(), requires_grad=False)
    f, f_736 = f_model(img_v)
    print(f.size(), f_736.size())
    s_G = model['G_model'](torch.cat((f, f_736), dim=1))
    up96 = nn.Upsample(size=(96,96), mode='bilinear')
    s_G = up96(s_G)
    s_G = s_G.cpu().data
    unnorm_emoji = UnNormalizeRangeTanh()
    res = unnorm_emoji(s_G[:16])
    npimg = torchvision.utils.make_grid(res, nrow=4).numpy()
    npimg = np.transpose(npimg, (1, 2, 0)) 
    zero_array = np.zeros(npimg.shape)
    one_array = np.ones(npimg.shape)
    npimg = np.minimum(npimg,one_array)
    npimg = np.maximum(npimg,zero_array)
#     plt.imshow(npimg)
    return npimg
