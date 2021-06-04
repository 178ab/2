from tkinter import Toplevel
from tkinter.scrolledtext import ScrolledText
from tkinter import Text
from tkinter import Button
from tkinter import END
from time import localtime, time, strftime
from tkinter import UNITS


class WindowChat(Toplevel):

    def __init__(self):
        super(WindowChat, self).__init__()

        # 设置窗口大小
        self.geometry('%dx%d' % (795,505))

        # 设置窗口不可修改
        self.resizable(False, False)

        # 添加组件
        self.add_widget()



    def add_widget(self):
        """添加组件的方法"""
        # 聊天区
        chat_text_area = ScrolledText(self)
        chat_text_area['width'] = 110
        chat_text_area['height'] = 30
        chat_text_area.grid(row=0, column=0, columnspan = 2)

        chat_text_area.tag_config('green', foreground='#088B00')
        chat_text_area.tag_config('system', foreground = 'red')
        self.children['chat_text_area'] = chat_text_area

        # 输入区
        chat_input_area = Text(self, name='chat_input_area')
        chat_input_area['width'] = 100
        chat_input_area['height'] = 7
        chat_input_area.grid(row=1, column=0, pady=10)

        # 发送按钮
        send_button = Button(self, name='send_button')
        send_button['text'] = '发送'
        send_button['width'] = 5
        send_button['height'] = 2
        send_button.grid(row=1, column=1)

    def set_title(self, tital):
        """设置标题"""
        self.title('欢迎 %s 进入聊天室！' % tital)

    def on_send_button_click(self, command):
        """注册事件，当发送按钮被点击时，执行command函数"""
        self.children['send_button']['command'] = command

    def get_input(self):
        """获取输入框的内容"""
        return self.children['chat_input_area'].get(0.0, END)

    def clear_input(self):
        """清空输入框内容"""
        self.children['chat_input_area'].delete(0.0, END)

    def append_message(self, sender, messages):
        """添加一条消息到聊天区"""
        send_time = strftime('%y-%m-%d %h:%m:%s', localtime(time()))
        send_info = "%s: %s\n" % (sender, send_time)
        self.children['chat_text_area'].insert(END, send_info, 'green')
        self.children['chat_text_area'].insert(END, ' '+messages+'\n')

        # 向下滚动屏幕
        self.children['chat_text_area'].yview_scroll(3, UNITS)

    def on_window_close(self, command):
        """注册关闭窗口时执行的指令"""
        self.protocol('WM_DELETE_WINDOW', command)


if __name__ == '__main__':
    WindowChat().mainloop()
