# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 3.10.1-0-g8feb16b3)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

from MyFrame import MyFrame

###########################################################################
## Class LoginDialog
###########################################################################


class LoginDialog(wx.Dialog):
    def __init__(self, parent, choices, callback):
        wx.Dialog.__init__(
            self,
            parent,
            id=wx.ID_ANY,
            title="Login",
            pos=wx.DefaultPosition,
            size=wx.Size(-1, -1),
            style=wx.DEFAULT_DIALOG_STYLE | wx.STAY_ON_TOP,
        )
        self.callback = callback
        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.SetFont(
            wx.Font(
                11,
                wx.FONTFAMILY_DEFAULT,
                wx.FONTSTYLE_NORMAL,
                wx.FONTWEIGHT_NORMAL,
                False,
                wx.EmptyString,
            )
        )

        bSizer24 = wx.BoxSizer(wx.VERTICAL)

        bSizer26 = wx.BoxSizer(wx.HORIZONTAL)

        bSizer26.Add((0, 0), 1, wx.EXPAND, 5)

        self.m_staticText13 = wx.StaticText(
            self, wx.ID_ANY, "User:", wx.DefaultPosition, wx.DefaultSize, 0
        )
        self.m_staticText13.Wrap(-1)

        self.m_staticText13.SetFont(
            wx.Font(
                11,
                wx.FONTFAMILY_DEFAULT,
                wx.FONTSTYLE_NORMAL,
                wx.FONTWEIGHT_NORMAL,
                False,
                wx.EmptyString,
            )
        )

        bSizer26.Add(self.m_staticText13, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        bSizer26.Add((0, 0), 1, wx.EXPAND, 5)

        # comboboxChoices = ["ADMIN", "DMH"]
        self.combobox = wx.ComboBox(
            self,
            wx.ID_ANY,
            "Combo!",
            wx.DefaultPosition,
            wx.Size(145, -1),
            choices,
            wx.CB_DROPDOWN | wx.CB_READONLY | wx.CB_SORT,
        )
        self.combobox.SetSelection(0)
        self.combobox.SetFont(
            wx.Font(
                11,
                wx.FONTFAMILY_DEFAULT,
                wx.FONTSTYLE_NORMAL,
                wx.FONTWEIGHT_NORMAL,
                False,
                wx.EmptyString,
            )
        )

        bSizer26.Add(self.combobox, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        bSizer24.Add(bSizer26, 1, wx.EXPAND, 5)

        bSizer261 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText131 = wx.StaticText(
            self, wx.ID_ANY, "Password:", wx.DefaultPosition, wx.DefaultSize, 0
        )
        self.m_staticText131.Wrap(-1)

        self.m_staticText131.SetFont(
            wx.Font(
                11,
                wx.FONTFAMILY_DEFAULT,
                wx.FONTSTYLE_NORMAL,
                wx.FONTWEIGHT_NORMAL,
                False,
                wx.EmptyString,
            )
        )

        bSizer261.Add(self.m_staticText131, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        bSizer261.Add((0, 0), 1, wx.EXPAND, 5)

        self.password_field = wx.TextCtrl(
            self,
            wx.ID_ANY,
            wx.EmptyString,
            wx.DefaultPosition,
            wx.Size(150, -1),
            wx.TE_PASSWORD | wx.TE_PROCESS_ENTER,
        )
        self.password_field.SetFont(
            wx.Font(
                11,
                wx.FONTFAMILY_DEFAULT,
                wx.FONTSTYLE_NORMAL,
                wx.FONTWEIGHT_NORMAL,
                False,
                wx.EmptyString,
            )
        )

        bSizer261.Add(self.password_field, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        bSizer24.Add(bSizer261, 1, wx.EXPAND, 5)

        bSizer25 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_button28 = wx.Button(
            self, wx.ID_ANY, "OK", wx.DefaultPosition, wx.Size(100, 35), 0
        )

        self.m_button28.SetDefault()
        self.m_button28.SetFont(
            wx.Font(
                11,
                wx.FONTFAMILY_DEFAULT,
                wx.FONTSTYLE_NORMAL,
                wx.FONTWEIGHT_NORMAL,
                False,
                wx.EmptyString,
            )
        )

        bSizer25.Add(self.m_button28, 0, wx.ALL, 5)

        bSizer25.Add((0, 0), 1, wx.EXPAND, 5)

        self.cancel_button = wx.Button(
            self, wx.ID_ANY, "Cancel", wx.DefaultPosition, wx.Size(100, 35), 0
        )
        self.cancel_button.SetFont(
            wx.Font(
                11,
                wx.FONTFAMILY_DEFAULT,
                wx.FONTSTYLE_NORMAL,
                wx.FONTWEIGHT_NORMAL,
                False,
                wx.EmptyString,
            )
        )

        bSizer25.Add(self.cancel_button, 0, wx.ALL, 5)

        bSizer24.Add(bSizer25, 1, wx.EXPAND, 5)

        self.SetSizer(bSizer24)
        self.Layout()
        bSizer24.Fit(self)

        self.Centre(wx.BOTH)

        # Connect Events
        self.Bind(wx.EVT_CLOSE, self.wxEVENT_CLOSE)
        self.password_field.Bind(wx.EVT_TEXT_ENTER, self.wxTE_PROCESS_ENTER)
        self.m_button28.Bind(wx.EVT_BUTTON, self.wxEVT_LOGIN_ENTER)
        self.cancel_button.Bind(wx.EVT_BUTTON, self.wxEVT_COMMAND_CANCEL)

    def __del__(self):
        pass

    # Virtual event handlers, override them in your derived class
    def wxEVENT_CLOSE(self, event):
        event.Skip()

    def wxEVT_LOGIN_ENTER(self, event):
        user=self.combobox.GetValue()
        password=self.password_field.GetValue()
        self.callback(user, password)
        event.Skip()

    def wxEVT_COMMAND_CANCEL(self, event):
        event.Skip()

    def wxTE_PROCESS_ENTER(self, event):
        user=self.combobox.GetValue()
        password=self.password_field.GetValue()
        self.callback(user, password)
        event.Skip()


def cb(user, password):
    print(f'User: {user}, Password: {password}')

if __name__ == "__main__":
    app = wx.App(False)
    parent_frame = MyFrame()  # Create an instance of MyFrame
    dialog = LoginDialog(parent_frame, ["ADMIN", "DMH"], cb)
    dialog.ShowModal()  # Show the dialog
    app.MainLoop()
