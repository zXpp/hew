# -*- coding: utf-8 -*-
#import win32com.client
# import faulthandler
# faulthandler.enable()
from win32com.client import Dispatch
from rmdjr import rmdAndmkd as rmdir#import timeremove and makedir
from PIL import Image
import os

OFFICE=["PowerPoint.Application","Word.Application","Excel.Application"]
ppFixedFormatTypePDF = 2
class easyPPT():
	def __init__(self):
		self.ppt = Dispatch('PowerPoint.Application')
		self.ppt.DisplayAlerts=False
	def open(self,filename=None,outDir0=None,label=None):
		try:
			if filename and os.path.isfile(filename):
				self.filename = filename#给定文件名，chuangeilei
				self.ppt_prefix=os.path.basename(self.filename).rsplit('.')[0]
				self.outdir0=outDir0 if outDir0 else os.path.pardir(self.filename)#输出跟路径
				self.outdir0=self.outdir0.replace('/','\\')
				self.label = label if label else self.ppt_prefix
				self.outdir1=os.path.join(self.outdir0,self.label)#输出跟文件夹路径+用户定义-同ppt文件名
				self.pres = self.ppt.Presentations.Open(self.filename, WithWindow=False)
			else:
				self.pres = self.ppt.Presentations.Add()
				self.filename = ''
			self.Slides=self.pres.Slides
			self.count_Slid = self.Slides.Count
			# self.allppt=range(1,self.count_Slid+1)#所有的PPT编号
			# ###########################################
			# if pptrange and len(pptrange):
			# 	self.selppt=filter(lambda x:x>0 and x<self.count_Slid+1,str2pptind(pptrange))
			# else:
			# 	self.selppt=self.allppt
			##################################################
			self.width,self.height = [self.pres.PageSetup.SlideWidth*3,self.pres.PageSetup.SlideHeight*3]
			rmdir(self.outdir1)
			self.outfordir2=os.path.join(self.outdir1,"OutFormats")#输出放多格式的二级目录,默认为"OurFormats"
			rmdir(self.outfordir2)
			self.outfile_prefix=os.path.join(self.outfordir2,self.label)#具体到文件格式的文件前缀（除了生成格式外的）
		except Exception,e:
			return e
	def closepres(self):
		self.pres.Close()
	def closeppt(self):
		self.ppt.Quit()
	def saveAs(self,Format=None,flag="f"):
		try:
			if flag=="f" and Format:
				newname=u".".join([self.outfile_prefix,Format.lower()])#目标格式的完整路径
			if Format in ["PDF","pdf","Pdf"]:
				try:
					self.pres.SaveAs(FileName=newname,FileFormat=32)
				except:
					newname=newname.replace('/','\\')
					self.pres.SaveAs(FileName=newname, FileFormat=32)
			if Format in ["txt", "TXT", "Txt"]:
				self.exTXT()
		except Exception,e:
			print e
			#return e

	def pngExport(self,imgDir=None,newsize=None,imgtype="png",merge=0):#导出原图用这个
		newsize=newsize if newsize else self.width
		radio=newsize/self.width
		if self.outdir1:
			self.outslidir2=os.path.join(self.outdir1,"Slides")#存放原图的二级目录
			if not imgDir:
				rmdir(self.outslidir2)
				Path,Wid,Het=self.outslidir2,self.width,self.height
				self.outfile_prefix=self.outfile_prefix+'_raw'
				#self.allslid=map(lambda x:os.path.join(Path,x),os.listdir(Path))#所有原图的绝对路径
			else:
				self.imDir=imgDir
				self.outresizedir2=os.path.join(self.outdir1,self.imDir)#所以缩放图的绝对路径
				rmdir(self.outresizedir2)
				Path,Wid,Het=self.outresizedir2,newsize,round(self.height*radio,0)
				#self.allres=map(lambda x:os.path.join(Path,x),os.listdir(Path))
			self.pres.Export(Path,imgtype,Wid,Het)#可设参数导出幻灯片的宽度（以像素为单位）
			self.renameFiles(Path,torep=u"幻灯片")
			outfile=u"".join([self.outfile_prefix,u'.',imgtype])
			redpi(Path,merge,pictype=imgtype,outimg=outfile)
	"""
	def redpi(path,append=0,pictype="png",outimg=None):##将大于、小于96dpi的都转换成96dpi
		files=map(lambda x:os.path.join(path,x),os.listdir(path))
		imgs,width, height=[], 0,0
		for file in files:
			img=Image.open(file)
			img2=img.copy()
			img.save(file)
			if append:
				img2 = img2.convert('RGB') if img2.mode != "RGB" else img2
				imgs.append(img2)
				width = img2.size[0] if img2.size[0] > width else width
				height += img2.size[1]
				del img2
		if append:
			pasteimg(imgs,width,height,outimg)"""
	def renameFiles(self,imgdir_name,torep=None):#torep:带替换的字符
		srcfiles = os.listdir(imgdir_name)
		for srcfile in srcfiles:
			inde = srcfile.split(torep)[-1].split('.')[0]#haha1.png
			suffix=srcfile[srcfile.index(inde)+len(inde):].lower()
			#sufix = os.path.splitext(srcfile)[1]
			# 根据目录下具体的文件数修改%号后的值，"%04d"最多支持9999
			newname="".join([self.label,"_",inde.zfill(2),suffix])
			destfile = os.path.join(imgdir_name,newname)
			srcfile = os.path.join(imgdir_name, srcfile)
			os.rename(srcfile, destfile)
			#index += 1
#		for each in os.listdir(imgdir_name):
	def slid2PPT(self,outDir=None,substr=""):#选择的编号的幻灯片单独发布为ppt文件，
		try:
			if not outDir:
				outDir=os.path.join(self.outdir1 ,"Slide2PPT")
			if not os.path.isdir(outDir):#只需要判断文件夹是否存在，默认是覆盖生成。
				os.makedirs(outDir)
			#if not sublst or not len(sublst):#如果不指定，列表为空或者是空列表
			sublst=str2pptind(substr)
			sublst=filter(lambda x:x>0 and x<self.count_Slid+1,sublst)#筛选出小于幻灯片总数的序号
			map(lambda x:self.Slides(x).PublishSlides(outDir,True,True),sublst)
			self.renameFiles(outDir,torep=self.ppt_prefix)
		except Exception,e:
			return e
	def exTXT(self):
		f=open("".join([self.outfile_prefix,r".txt"]),"wb+")
		for x in range(1,self.count_Slid+1):#
			s=[]
			shape_count = self.Slides(x).Shapes.Count
			page=u"".join([u"\r\n\r\nPage ",str(x),u":\r\n"])#
			s.append(page)
			for j in range(1, shape_count + 1):
				txornot=self.Slides(x).Shapes(j).HasTextFrame
				if txornot:#可正可负，只要不为0
					txrg=self.Slides(x).Shapes(j).TextFrame.TextRange.Text
					if txrg and len(txrg):#not in [u' ',u'',u"\r\n"]:
						s.append(txrg)
			f.write(u"\r\n".join(s).encode("utf-8"))
			#print (u"\r\n".join(s))
		f.close()		#s=[]
		# else :#如果没有字的情况
		# 	return
	def delslides(self):
		rmdir(self.outslidir2,mksd=0)
	def delresize(self):
		rmdir(self.outresizedir2,mksd=0)
def str2pptind(strinput=""):##将输入处理范围的幻灯片编号转为顺序的、不重复的list列表
	selppt=[]
	if strinput and strinput not in [""," "]:
		pptind=strinput.split(",")
		tmp1=map(lambda x:x.split(r"-"),pptind)
		for each in tmp1:
			each1=map(int,each)
			selppt+=range(each1[0],each1[-1]+1)
		selppt=set(sorted(selppt))
	selppt=list(selppt)
	return selppt
def pasteimg(inlst,width,height,output_file):
		merge_img,cur_height = Image.new('RGB', (width, height), 0xffffff),0
		for img in inlst:
			# 把图片粘贴上去
			merge_img.paste(img, (0, cur_height))
			cur_height += img.size[1]
		merge_img.save(output_file)#自动识别扩展名
		merge_img=None
def redpi(path,append=0,pictype="png",outimg=None):##将大于、小于96dpi的都转换成96dpi
		files=map(lambda x:os.path.join(path,x),os.listdir(path))
		imgs,width, height=[], 0,0
		for file in files:
			img=Image.open(file)
			scale=img.info['dpi']
			scale2=max(scale[0],96)
			img2=img.copy()
			img.save(file,dpi=(scale2,scale2))
			img=None
			if append:
				img2 = img2.convert('RGB') if img2.mode != "RGB" else img2
				imgs.append(img2)
				width = img2.size[0] if img2.size[0] > width else width
				height += img2.size[1]
				img2=None
		if append:
			pasteimg(imgs,width,height,outimg)
def png2pngs(filespath,output_file,flag="png"):
	if isinstance(filespath,list):
		files=filespath
	else:
		tmp=os.listdir(filespath)
		files = map(lambda x:os.path.join(filespath,x),tmp)
	imgs = []
	width, height= 0,0
	# 计算总宽度和长度
	try:
		for file in files:
			img = Image.open(file)
			img = img.convert('RGB') if img.mode != "RGB" else img
			imgs.append(img)
			width = img.size[0] if img.size[0] > width else width
			height += img.size[1]

		# 新建一个白色底的图片
		merge_img,cur_height = Image.new('RGB', (width, height), 0xffffff),0
		for img in imgs:
			# 把图片粘贴上去
			merge_img.paste(img, (0, cur_height))
			cur_height += img.size[1]
		merge_img.save(output_file)#自动识别扩展名
	except Exception,e:
		return e

if __name__ == "__main__":
	label=u"深度学习的基本理论与方法"
	imdir=u"反对果"
	outDir = u"D:\\test"#u"G:\\简历"+u"\\"+u'张雪--兼辅PPT.ppt'
	inpu=u"1,2,4,6-9,5,8-11,22-25"
	pprange=str2pptind(inpu)
	pptx=easyPPT()
	pptx.open(u"G:\\论文\\深度学习的基本理论与方法.pptx",outDir,label)
	#pptx.delslid()
	# print pptx.width,pptx.height,pptx.count_Slid,pptx.pres.PageSetup.SlideHeight
	# print pptx.pres.PageSetup.SlideWidth

	#pptind=pptx.str2pptind(inpu)
	#pptind2=pptx.str2pptind("")
	format=["png","html","xml","ppt/pptx","txt","pdf"]#formatpptx.saveAs(Format="PNG")
	pptx.saveAs(Format=format[-2])#txt
	# pptx.saveAs(Format=format[-1])#导出pdf
	# pptx.pngExport()#留空为原尺寸导出
	# pptx.pngExport(u"啦啦 啦",700)#imgedirnaem ,newidth.
	# pptx.slid2PPT()
	#pptx.slid2PPT(sublst=pptind)
	#pptx.weboptions()
	#print "dpi:",pptx.dpi_size[0],pptx.dpi_size[1]
	#pptx.ppt.PresentationBeforeClose(pptx.pres, False)
	#pptx.close()
