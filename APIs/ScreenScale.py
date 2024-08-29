class screenApi:
    def get_real_resolution(self):
        """获取真实的分辨率"""
        from win32.lib import win32con
        import win32gui, win32print
        hDC = win32gui.GetDC(0)
        wide = win32print.GetDeviceCaps(hDC, win32con.DESKTOPHORZRES)
        high = win32print.GetDeviceCaps(hDC, win32con.DESKTOPVERTRES)
        return {"wide": wide, "high": high}

    def get_screen_size(self):
        """获取缩放后的分辨率"""
        import win32api
        wide = win32api.GetSystemMetrics(0)
        high = win32api.GetSystemMetrics(1)
        return {"wide": wide, "high": high}

    def get_scaling(self):
        '''获取屏幕的缩放比例'''
        real_resolution = self.get_real_resolution()
        screen_size = self.get_screen_size()
        proportion = round(real_resolution['wide'] / screen_size['wide'], 2)
        return proportion

    def get_working_space_scale(self):
        """获取工作区尺寸"""
        import win32gui
        scaling = self.get_scaling()
        screen_width, screen_height = win32gui.GetWindowRect(win32gui.FindWindow("Shell_TrayWnd", ""))[2:0:-1]
        return int(screen_width * scaling), int(screen_height * scaling)
