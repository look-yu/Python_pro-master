# -*—coding:utf-8 -*-
# Created: 07-04-2017
#      by: python 3.4.3 and PyQt5-5.4
import sys
import os      # Python执行系统命令方法所用到的包
import subprocess  # 用于执行系统命令
print("程序开始运行...")
try:
    from PyQt5 import QtCore,QtGui,QtWidgets 
    print("PyQt5导入成功")
except ImportError as e:
    print(f"PyQt5导入失败: {e}")
    sys.exit(1)

class Ui_shut(object):   #类 继承object类
	flag = True
	set_time = ""
	def setupUi(self,shut):  #方法
	    #设置窗体的大小
		shut.setObjectName("shut")
		shut.resize(500,250)              
		shut.setFixedSize(500,250)
		
		# 设置窗体背景色
		shut.setStyleSheet("background-color: #f0f8ff;")

		# 添加标题标签
		self.title_label = QtWidgets.QLabel(shut)
		self.title_label.setGeometry(QtCore.QRect(0, 20, 500, 40))
		self.title_label.setFont(QtGui.QFont("微软雅黑", 16, QtGui.QFont.Bold))
		self.title_label.setAlignment(QtCore.Qt.AlignCenter)
		self.title_label.setObjectName("title_label")

		self.label = QtWidgets.QLabel(shut)
		self.label.setGeometry(QtCore.QRect(100, 80, 41, 41)) #标签的位置
		self.label.setFont(QtGui.QFont("微软雅黑", 12, QtGui.QFont.Bold))
		self.label.setObjectName("label")

		self.lineEdit = QtWidgets.QLineEdit(shut)
		self.lineEdit.setGeometry(QtCore.QRect(140, 80, 80, 41))
		self.lineEdit.setFont(QtGui.QFont("微软雅黑", 12, QtGui.QFont.Bold))
		self.lineEdit.setStyleSheet("border: 2px solid #4682b4; border-radius: 5px; padding: 5px;")
		self.lineEdit.setObjectName("lineEdit")

		self.label_2 = QtWidgets.QLabel(shut)
		self.label_2.setGeometry(QtCore.QRect(230, 90, 31, 31))
		self.label_2.setFont(QtGui.QFont("微软雅黑", 12, QtGui.QFont.Bold))
		self.label_2.setObjectName("label_2")

		self.lineEdit_2 = QtWidgets.QLineEdit(shut)
		self.lineEdit_2.setGeometry(QtCore.QRect(260, 80, 80, 41))
		self.lineEdit_2.setFont(QtGui.QFont("微软雅黑", 12, QtGui.QFont.Bold))
		self.lineEdit_2.setStyleSheet("border: 2px solid #4682b4; border-radius: 5px; padding: 5px;")
		self.lineEdit_2.setObjectName("lineEdit_2")

		self.label_3 = QtWidgets.QLabel(shut)
		self.label_3.setGeometry(QtCore.QRect(350, 90, 31, 31))
		self.label_3.setFont(QtGui.QFont("微软雅黑", 12, QtGui.QFont.Bold))
		self.label_3.setObjectName("label_3")

		self.pushButton = QtWidgets.QPushButton(shut,clicked=self.sd)  #为pushButton添加监听事件click。
		self.pushButton.setGeometry(QtCore.QRect(180, 140, 140, 45))
		self.pushButton.setFont(QtGui.QFont("微软雅黑", 12, QtGui.QFont.Bold))
		self.pushButton.setStyleSheet("background-color: #4682b4; color: white; border-radius: 10px;")
		self.pushButton.setObjectName("pushButton")

		self.label_4 = QtWidgets.QLabel(shut)
		self.label_4.setGeometry(QtCore.QRect(0, 200, 500, 31))
		self.label_4.setFont(QtGui.QFont("微软雅黑", 11))
		self.label_4.setAlignment(QtCore.Qt.AlignCenter)
		self.label_4.setObjectName("label_4")

		self.retranslateUi(shut)
		QtCore.QMetaObject.connectSlotsByName(shut) #connectSlotsByName是一个QMetaObject类里的静态函数，其作用是用来将QObject * o里的子QObject的某些信号按照其objectName连接到o的槽上。
        

	def retranslateUi(self,shut):
		_translate = QtCore.QCoreApplication.translate
		shut.setWindowTitle(_translate("shut", "Windows定时关机器"))
		self.title_label.setText(_translate("shut", "Windows定时关机器"))
		self.label.setText(_translate("shut", "在："))
		self.label_2.setText(_translate("shut", "时"))
		self.label_3.setText(_translate("shut", "分"))
		self.label_4.setText(_translate("shut", "请输入关机时间"))
		self.pushButton.setText(_translate("shut", "设置"))
	def sd(self,shut):        #self.sd为触发该事件后，需要执行的操作。
		h = self.lineEdit.text()
		m = self.lineEdit_2.text()
		print(f"设置关机时间: {h}:{m}")
		if self.flag:
			self.flag = False
			try:                     #捕获所有异常
				# 验证输入是否为数字
				if not h.isdigit() or not m.isdigit():
					self.label_4.setText('错误：请输入有效的数字')
					return
				
				# 验证时间范围
				if int(h) < 0 or int(h) > 23 or int(m) < 0 or int(m) > 59:
					self.label_4.setText('错误：请输入有效的时间范围（0-23时，0-59分）')
					return
				
				# 保存设置的时间
				self.set_time = f"{h}:{m}"
				
				# 使用schtasks命令创建计划任务，这样即使程序关闭也能执行
				# 创建一个批处理文件来执行关机命令
				batch_content = f'''@echo off
shutdown -s -t 300 -c "系统将在5分钟后关机，请保存工作并关闭程序"'''
				batch_path = os.path.join(os.getenv('TEMP'), 'shutdown_task.bat')
				with open(batch_path, 'w') as f:
					f.write(batch_content)
				
				# 使用schtasks创建计划任务
				task_name = "AutoShutdownTask"
				subprocess.run(['schtasks', '/delete', '/tn', task_name, '/f'], capture_output=True)
				subprocess.run([
					'schtasks', '/create', '/tn', task_name, 
					'/tr', batch_path, 
					'/sc', 'once', 
					'/st', f"{h}:{m}",
					'/f'
				], capture_output=True)
				
				print(f"创建计划任务: {task_name} 在 {h}:{m} 执行")
				self.label_4.setText(f'设置成功! 系统将在今天 {h}:{m} 关机，关机前会有5分钟提示')
				self.pushButton.setText('移除')
				# 不清除输入框，让用户知道已设置的时间
			except Exception as e:
				print(f"错误: {e}")
				self.label_4.setText('设置失败，请检查输入或系统权限')
		else:
			self.flag = True
			try:
				# 取消关机
				print("执行命令: shutdown -a")
				subprocess.run(['shutdown', '-a'], capture_output=True)
				# 删除计划任务
				task_name = "AutoShutdownTask"
				subprocess.run(['schtasks', '/delete', '/tn', task_name, '/f'], capture_output=True)
				print(f"删除计划任务: {task_name}")
				self.label_4.setText('成功，已取消关机计划')
				self.pushButton.setText('设置')
				# 清除保存的时间
				self.set_time = ""
			except Exception as e:
				print(f"错误: {e}")
				self.label_4.setText('取消失败，请检查系统权限')

if __name__ == '__main__':   
    print("创建应用程序...")
    app = QtWidgets.QApplication(sys.argv)
    print("创建窗体...")
    Form = QtWidgets.QWidget()
    print("初始化UI...")
    ui = Ui_shut()
    ui.setupUi(Form) 
    print("显示窗体...")
    Form.show()
    print("进入事件循环...")
    sys.exit(app.exec_())
		


