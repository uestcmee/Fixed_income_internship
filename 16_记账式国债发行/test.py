import re, time
import webbrowser
import win32gui, win32con, win32com.client


def _window_enum_callback(hwnd, wildcard):
    '''
    Pass to win32gui.EnumWindows() to check all the opened windows
    把想要置顶的窗口放到最前面，并最大化
    '''
    if re.match(wildcard, str(win32gui.GetWindowText(hwnd))) is not None:
        win32gui.BringWindowToTop(hwnd)
        # 先发送一个alt事件，否则会报错导致后面的设置无效：pywintypes.error: (0, 'SetForegroundWindow', 'No error message is available')
        shell = win32com.client.Dispatch("WScript.Shell")
        shell.SendKeys('%')
        # 设置为当前活动窗口
        win32gui.SetForegroundWindow(hwnd)
        # 最大化窗口
        win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)


if __name__ == '__main__':
    time.sleep(3)

    webbrowser.open("https://www.baidu.com/")
    # win32gui.EnumWindows(_window_enum_callback, ".*%s.*" % 'Excel')  # 此处为你要设置的活动窗口名