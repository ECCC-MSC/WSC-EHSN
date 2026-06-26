# All works in this code have been curated by ECCC and licensed under the GNU General Public License v3.0. 
# Read more: https://www.gnu.org/licenses/gpl-3.0.en.html

import wx
import re

class SVOPanel(wx.Panel):
    def __init__(self, parent, func, *args, **kwargs):
        super(SVOPanel, self).__init__(*args, **kwargs)
        self.parent = parent
        # Set func to *
        self.func = "*"
        self.manager = None
        # Get the passed in name type
        self.name = func

        # ---------------------------------------------------------

        # Type headers
        self.table1_header1 = 'Type of Visit:'
        self.table1_header2 = 'Assumptions:'

        # Type checkbox titles
        self.table1_title1 = 'Planned'
        self.table1_title2 = 'Unplanned'

        # Type comments
        self.table1_comment1 = ' Visit is intentionally planned based on known or anticipated data quality needs, hydraulic conditions,\n or measurement opportunities'
        self.table1_comment2 = ' Visit is triggered by a high/low flow event requiring discharge measurement, equipment failure, gauge destroyed, etc.'

        # Sizes
        #self.table1_title_width = 105
        self.table1_title_width = 170
        self.table1_comment_width = 955 - 24 - self.table1_title_width

        # ---------------------------------------------------------

        # Outcome headers
        self.table2_header1 = 'Visit Reason:'
        self.table2_header2 = 'Assumptions:'

        # Outcome checkbox titles
        self.table2_title1 = 'Data Maintenance'
        self.table2_title2 = 'Equipment/Instrumentation'
        self.table2_title3 = 'Infrastructure'

        # Outcome comments
        self.table2_comment1 = ' Includes rating and stage maintenance'
        self.table2_comment2 = ' Equipment serviced during visit (power, telemetry, logger, sensor)'
        self.table2_comment3 = ' Infrastructure fixed/maintenance during visit (gauge, grounds, access, infrastructure)'

        # Sizes
        self.table2_title_width = 170
        self.table2_comment_width = 955 - 24 - self.table2_title_width

        # ---------------------------------------------------------

        # Type headers
        self.table3_header1 = 'Special Service Request:'
        self.table3_header2 = 'Assumptions:'

        # Type checkbox titles
        self.table3_title1 = 'Partner Request'
        self.table3_title2 = 'Management'

        # Type comments
        self.table3_comment1 = ' Funding partner has requested a visit for data quality purposes'
        self.table3_comment2 = ' Management (any level) has requested a visit outside the anticipated planned visits for operation/maintenance of the hydrometric\n station and data quality needs: Head of Operations, District Manager has requested a visit for operational purposes'

        # Sizes
        #self.table3_title_width = 105
        self.table3_title_width = 170
        self.table3_comment_width = 955 - 24 - self.table3_title_width

        # ---------------------------------------------------------

        # Text box labels
        self.commentLbl = "Comments:"
        self.summaryLbl = "Summary changes (Station Health Remarks):"

        # Fonts
        self.fontTitle = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        #self.fontItem = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL)

        #Font stuff
        #f = self.GetFont()
        #dc = wx.WindowDC(self)
        #dc.SetFont(f)
        #self.width, self.TextLabelRowHeight = dc.GetTextExtent("Ag")
        #self.TextLabelRowHeight *= 1.34
        
        self.InitUI()


    def InitUI(self):
        self.layoutSizer = wx.BoxSizer(wx.VERTICAL)
        self.header1_colSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.table1_colSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.header2_colSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.table2_colSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.header3_colSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.table3_colSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.textbox_sizer = wx.BoxSizer(wx.VERTICAL)

        # --------------------------------------------------------------------

        ########################
        ####### HEADER 1 #######
        ########################

        # Checkboxes (empty)
        self.header1_cb_sizer = wx.BoxSizer(wx.VERTICAL)
        self.header1_cb_panel = wx.Panel(self, style=wx.BORDER_NONE, size=(24, -1))
        self.header1_cb_panel.SetSizer(self.header1_cb_sizer)
        self.header1_colSizer.Add(self.header1_cb_panel, 0, wx.EXPAND)

        # Text column 1
        self.header1_col1_sizer = wx.BoxSizer(wx.VERTICAL)
        self.header1_col1_panel = wx.Panel(self, style=wx.BORDER_NONE, size=(-1, -1))
        self.header1_col1_panel.SetSizer(self.header1_col1_sizer)
        self.header1_colSizer.Add(self.header1_col1_panel, 0, wx.EXPAND)

        # Text column 2
        self.header1_col2_sizer = wx.BoxSizer(wx.VERTICAL)
        self.header1_col2_panel = wx.Panel(self, style=wx.BORDER_NONE, size=(-1, -1))
        self.header1_col2_panel.SetSizer(self.header1_col2_sizer)
        self.header1_colSizer.Add(self.header1_col2_panel, 1, wx.EXPAND)

        # --------------------
        # Adding header values
        # --------------------

        # Header column 1
        header1_head_col1 = wx.StaticText(self.header1_col1_panel, label=self.table1_header1, size=(self.table1_title_width, 20), style=wx.ALIGN_CENTER_HORIZONTAL)
        header1_head_col1.SetFont(self.fontTitle)
        self.header1_col1_sizer.Add(header1_head_col1, 1)
        
        # Header column 2
        header1_head_col2 = wx.StaticText(self.header1_col2_panel, label=self.table1_header2, size=(self.table1_comment_width, 20), style=wx.ALIGN_CENTER_HORIZONTAL)
        header1_head_col2.SetFont(self.fontTitle)
        self.header1_col2_sizer.Add(header1_head_col2, 1)


        #######################
        ####### TABLE 1 #######
        #######################

        # Checkboxes
        self.table1_cb_sizer = wx.BoxSizer(wx.VERTICAL)
        self.table1_cb_panel = wx.Panel(self, style=wx.SIMPLE_BORDER, size=(24, -1))
        self.table1_cb_panel.SetSizer(self.table1_cb_sizer)
        self.table1_colSizer.Add(self.table1_cb_panel, 0, wx.EXPAND)

        # Text column 1
        self.table1_col1_sizer = wx.BoxSizer(wx.VERTICAL)
        self.table1_col1_panel = wx.Panel(self, style=wx.BORDER_NONE, size=(-1, -1))
        self.table1_col1_panel.SetSizer(self.table1_col1_sizer)
        self.table1_colSizer.Add(self.table1_col1_panel, 0, wx.EXPAND)

        # Text column 2
        self.table1_col2_sizer = wx.BoxSizer(wx.VERTICAL)
        self.table1_col2_panel = wx.Panel(self, style=wx.BORDER_NONE, size=(-1, -1))
        self.table1_col2_panel.SetSizer(self.table1_col2_sizer)
        self.table1_colSizer.Add(self.table1_col2_panel, 1, wx.EXPAND)
        
        # -------------------
        # Adding table values
        # -------------------

        # Checkbox row 1
        self.table1_cb1 = wx.CheckBox(self.table1_cb_panel, size=(24, 34))
        self.table1_cb1.Bind(wx.EVT_CHECKBOX, self.OnTypeChange)
        self.table1_cb1.SetValue(False)
        self.table1_cb_sizer.Add(self.table1_cb1, 0, wx.EXPAND|wx.LEFT, 4)

        # Comment row 1 column 1
        table1_row1_col1 = wx.StaticText(self.table1_col1_panel, label=self.table1_title1, size=(self.table1_title_width, 34), style=wx.SIMPLE_BORDER|wx.ALIGN_CENTER_HORIZONTAL)
        #table1_row1_col1.SetFont(self.fontItem)
        self.table1_col1_sizer.Add(table1_row1_col1, 1)

        # Comment row 1 column 2
        table1_row1_col2 = wx.StaticText(self.table1_col2_panel, label=self.table1_comment1, size=(self.table1_comment_width, 34), style=wx.SIMPLE_BORDER)
        #table1_row1_col2.SetFont(self.fontItem)
        self.table1_col2_sizer.Add(table1_row1_col2, 1)

        # -----------------------

        # Checkbox row 2
        self.table1_cb2 = wx.CheckBox(self.table1_cb_panel, size=(24, 20))
        self.table1_cb2.Bind(wx.EVT_CHECKBOX, self.OnTypeChange)
        self.table1_cb2.SetValue(False)
        self.table1_cb_sizer.Add(self.table1_cb2, 0, wx.EXPAND|wx.LEFT, 4)

        # Comment row 2 column 1
        table1_row2_col1 = wx.StaticText(self.table1_col1_panel, label=self.table1_title2, size=(self.table1_title_width, 20), style=wx.SIMPLE_BORDER|wx.ALIGN_CENTER_HORIZONTAL)
        #table1_row2_col1.SetFont(self.fontItem)
        self.table1_col1_sizer.Add(table1_row2_col1, 0) # This is set to 0 to allow the row to be its own size

        # Comment row 2 column 2
        table1_row2_col2 = wx.StaticText(self.table1_col2_panel, label=self.table1_comment2, size=(self.table1_comment_width, 20), style=wx.SIMPLE_BORDER)
        #table1_row2_col2.SetFont(self.fontItem)
        self.table1_col2_sizer.Add(table1_row2_col2, 0) # This is set to 0 to allow the row to be its own size

        # --------------------------------------------------------------------

        ########################
        ####### HEADER 2 #######
        ########################

        # Checkboxes (empty)
        self.header2_cb_sizer = wx.BoxSizer(wx.VERTICAL)
        self.header2_cb_panel = wx.Panel(self, style=wx.BORDER_NONE, size=(24, -1))
        self.header2_cb_panel.SetSizer(self.header2_cb_sizer)
        self.header2_colSizer.Add(self.header2_cb_panel, 0, wx.EXPAND)

        # Text column 1
        self.header2_col1_sizer = wx.BoxSizer(wx.VERTICAL)
        self.header2_col1_panel = wx.Panel(self, style=wx.BORDER_NONE, size=(-1, -1))
        self.header2_col1_panel.SetSizer(self.header2_col1_sizer)
        self.header2_colSizer.Add(self.header2_col1_panel, 0, wx.EXPAND)

        # Text column 2
        self.header2_col2_sizer = wx.BoxSizer(wx.VERTICAL)
        self.header2_col2_panel = wx.Panel(self, style=wx.BORDER_NONE, size=(-1, -1))
        self.header2_col2_panel.SetSizer(self.header2_col2_sizer)
        self.header2_colSizer.Add(self.header2_col2_panel, 1, wx.EXPAND)
        
        # --------------------
        # Adding header values
        # --------------------

        # Header column 1
        header2_head_col1 = wx.StaticText(self.header2_col1_panel, label=self.table2_header1, size=(self.table2_title_width, 20), style=wx.ALIGN_CENTER_HORIZONTAL)
        header2_head_col1.SetFont(self.fontTitle)
        self.header2_col1_sizer.Add(header2_head_col1, 1)
        
        # Header column 2
        header2_head_col2 = wx.StaticText(self.header2_col2_panel, label=self.table2_header2, size=(self.table2_comment_width, 20), style=wx.ALIGN_CENTER_HORIZONTAL)
        header2_head_col2.SetFont(self.fontTitle)
        self.header2_col2_sizer.Add(header2_head_col2, 1)


        #######################
        ####### TABLE 2 #######
        #######################

        # Checkboxes
        self.table2_cb_sizer = wx.BoxSizer(wx.VERTICAL)
        self.table2_cb_panel = wx.Panel(self, style=wx.SIMPLE_BORDER, size=(24, -1))
        self.table2_cb_panel.SetSizer(self.table2_cb_sizer)
        self.table2_colSizer.Add(self.table2_cb_panel, 0, wx.EXPAND)

        # Text column 1
        self.table2_col1_sizer = wx.BoxSizer(wx.VERTICAL)
        self.table2_col1_panel = wx.Panel(self, style=wx.BORDER_NONE, size=(-1, -1))
        self.table2_col1_panel.SetSizer(self.table2_col1_sizer)
        self.table2_colSizer.Add(self.table2_col1_panel, 0, wx.EXPAND)

        # Text column 2
        self.table2_col2_sizer = wx.BoxSizer(wx.VERTICAL)
        self.table2_col2_panel = wx.Panel(self, style=wx.BORDER_NONE, size=(-1, -1))
        self.table2_col2_panel.SetSizer(self.table2_col2_sizer)
        self.table2_colSizer.Add(self.table2_col2_panel, 1, wx.EXPAND)

        # -------------------
        # Adding table values
        # -------------------

        # Checkbox row 1
        self.table2_cb1 = wx.CheckBox(self.table2_cb_panel, size=(24, 20))
        self.table2_cb1.Bind(wx.EVT_CHECKBOX, self.OnReasonChange)
        self.table2_cb1.SetValue(False)
        self.table2_cb_sizer.Add(self.table2_cb1, 0, wx.EXPAND|wx.LEFT, 4)

        # Comment row 1 column 1
        table2_row1_col1 = wx.StaticText(self.table2_col1_panel, label=self.table2_title1, size=(self.table2_title_width, 20), style=wx.SIMPLE_BORDER|wx.ALIGN_CENTER_HORIZONTAL)
        #table2_row1_col1.SetFont(self.fontItem)
        self.table2_col1_sizer.Add(table2_row1_col1, 1)

        # Comment row 1 column 2
        table2_row1_col2 = wx.StaticText(self.table2_col2_panel, label=self.table2_comment1, size=(self.table2_comment_width, 20), style=wx.SIMPLE_BORDER)
        #table2_row1_col2.SetFont(self.fontItem)
        self.table2_col2_sizer.Add(table2_row1_col2, 1)

        # -----------------------

        # Checkbox row 2
        self.table2_cb2 = wx.CheckBox(self.table2_cb_panel, size=(24, 20))
        self.table2_cb2.Bind(wx.EVT_CHECKBOX, self.OnReasonChange)
        self.table2_cb2.SetValue(False)
        self.table2_cb_sizer.Add(self.table2_cb2, 0, wx.EXPAND|wx.LEFT, 4)

        # Comment row 2 column 1
        table2_row2_col1 = wx.StaticText(self.table2_col1_panel, label=self.table2_title2, size=(self.table2_title_width, 20), style=wx.SIMPLE_BORDER|wx.ALIGN_CENTER_HORIZONTAL)
        #table2_row2_col1.SetFont(self.fontItem)
        self.table2_col1_sizer.Add(table2_row2_col1, 1)

        # Comment row 2 column 2
        table2_row2_col2 = wx.StaticText(self.table2_col2_panel, label=self.table2_comment2, size=(self.table2_comment_width, 20), style=wx.SIMPLE_BORDER)
        #table2_row2_col2.SetFont(self.fontItem)
        self.table2_col2_sizer.Add(table2_row2_col2, 1)

        # -----------------------
        
        # Checkbox row 3
        self.table2_cb3 = wx.CheckBox(self.table2_cb_panel, size=(24, 20))
        self.table2_cb3.Bind(wx.EVT_CHECKBOX, self.OnReasonChange)
        self.table2_cb3.SetValue(False)
        self.table2_cb_sizer.Add(self.table2_cb3, 0, wx.EXPAND|wx.LEFT, 4)

        # Comment row 3 column 1
        table2_row3_col1 = wx.StaticText(self.table2_col1_panel, label=self.table2_title3, size=(self.table2_title_width, 20), style=wx.SIMPLE_BORDER|wx.ALIGN_CENTER_HORIZONTAL)
        #table2_row3_col1.SetFont(self.fontItem)
        self.table2_col1_sizer.Add(table2_row3_col1, 1)

        # Comment row 3 column 2
        table2_row3_col2 = wx.StaticText(self.table2_col2_panel, label=self.table2_comment3, size=(self.table2_comment_width, 20), style=wx.SIMPLE_BORDER)
        #table2_row3_col2.SetFont(self.fontItem)
        self.table2_col2_sizer.Add(table2_row3_col2, 1)

        # --------------------------------------------------------------------

        ########################
        ####### HEADER 3 #######
        ########################

        # Checkboxes (empty)
        self.header3_cb_sizer = wx.BoxSizer(wx.VERTICAL)
        self.header3_cb_panel = wx.Panel(self, style=wx.BORDER_NONE, size=(24, -1))
        self.header3_cb_panel.SetSizer(self.header3_cb_sizer)
        self.header3_colSizer.Add(self.header3_cb_panel, 0, wx.EXPAND)

        # Text column 1
        self.header3_col1_sizer = wx.BoxSizer(wx.VERTICAL)
        self.header3_col1_panel = wx.Panel(self, style=wx.BORDER_NONE, size=(-1, -1))
        self.header3_col1_panel.SetSizer(self.header3_col1_sizer)
        self.header3_colSizer.Add(self.header3_col1_panel, 0, wx.EXPAND)

        # Text column 2
        self.header3_col2_sizer = wx.BoxSizer(wx.VERTICAL)
        self.header3_col2_panel = wx.Panel(self, style=wx.BORDER_NONE, size=(-1, -1))
        self.header3_col2_panel.SetSizer(self.header3_col2_sizer)
        self.header3_colSizer.Add(self.header3_col2_panel, 1, wx.EXPAND)

        # --------------------
        # Adding header values
        # --------------------

        # Header column 1
        header3_head_col1 = wx.StaticText(self.header3_col1_panel, label=self.table3_header1, size=(self.table3_title_width, 20), style=wx.ALIGN_CENTER_HORIZONTAL)
        header3_head_col1.SetFont(self.fontTitle)
        self.header3_col1_sizer.Add(header3_head_col1, 1)
        
        # Header column 2
        header3_head_col2 = wx.StaticText(self.header3_col2_panel, label=self.table3_header2, size=(self.table3_comment_width, 20), style=wx.ALIGN_CENTER_HORIZONTAL)
        header3_head_col2.SetFont(self.fontTitle)
        self.header3_col2_sizer.Add(header3_head_col2, 1)


        #######################
        ####### TABLE 3 #######
        #######################

        # Checkboxes
        self.table3_cb_sizer = wx.BoxSizer(wx.VERTICAL)
        self.table3_cb_panel = wx.Panel(self, style=wx.SIMPLE_BORDER, size=(24, -1))
        self.table3_cb_panel.SetSizer(self.table3_cb_sizer)
        self.table3_colSizer.Add(self.table3_cb_panel, 0, wx.EXPAND)

        # Text column 1
        self.table3_col1_sizer = wx.BoxSizer(wx.VERTICAL)
        self.table3_col1_panel = wx.Panel(self, style=wx.BORDER_NONE, size=(-1, -1))
        self.table3_col1_panel.SetSizer(self.table3_col1_sizer)
        self.table3_colSizer.Add(self.table3_col1_panel, 0, wx.EXPAND)

        # Text column 2
        self.table3_col2_sizer = wx.BoxSizer(wx.VERTICAL)
        self.table3_col2_panel = wx.Panel(self, style=wx.BORDER_NONE, size=(-1, -1))
        self.table3_col2_panel.SetSizer(self.table3_col2_sizer)
        self.table3_colSizer.Add(self.table3_col2_panel, 1, wx.EXPAND)
        
        # -------------------
        # Adding table values
        # -------------------

        # Checkbox row 1
        self.table3_cb1 = wx.CheckBox(self.table3_cb_panel, size=(24, 20))
        self.table3_cb1.Bind(wx.EVT_CHECKBOX, self.OnSSRChange)
        self.table3_cb1.SetValue(False)
        self.table3_cb_sizer.Add(self.table3_cb1, 0, wx.EXPAND|wx.LEFT, 4)

        # Comment row 1 column 1
        table3_row1_col1 = wx.StaticText(self.table3_col1_panel, label=self.table3_title1, size=(self.table3_title_width, 20), style=wx.SIMPLE_BORDER|wx.ALIGN_CENTER_HORIZONTAL)
        #table3_row1_col1.SetFont(self.fontItem)
        self.table3_col1_sizer.Add(table3_row1_col1, 0) # This is set to 0 to allow the row to be its own size

        # Comment row 1 column 2
        table3_row1_col2 = wx.StaticText(self.table3_col2_panel, label=self.table3_comment1, size=(self.table3_comment_width, 20), style=wx.SIMPLE_BORDER)
        #table3_row1_col2.SetFont(self.fontItem)
        self.table3_col2_sizer.Add(table3_row1_col2, 0) # This is set to 0 to allow the row to be its own size

        # -----------------------

        # Checkbox row 2
        self.table3_cb2 = wx.CheckBox(self.table3_cb_panel, size=(24, 34))
        self.table3_cb2.Bind(wx.EVT_CHECKBOX, self.OnSSRChange)
        self.table3_cb2.SetValue(False)
        self.table3_cb_sizer.Add(self.table3_cb2, 0, wx.EXPAND|wx.LEFT, 4)

        # Comment row 2 column 1
        table3_row2_col1 = wx.StaticText(self.table3_col1_panel, label=self.table3_title2, size=(self.table3_title_width, 34), style=wx.SIMPLE_BORDER|wx.ALIGN_CENTER_HORIZONTAL)
        #table3_row2_col1.SetFont(self.fontItem)
        self.table3_col1_sizer.Add(table3_row2_col1, 1)

        # Comment row 2 column 2
        table3_row2_col2 = wx.StaticText(self.table3_col2_panel, label=self.table3_comment2, size=(self.table3_comment_width, 34), style=wx.SIMPLE_BORDER)
        #table3_row2_col2.SetFont(self.fontItem)
        self.table3_col2_sizer.Add(table3_row2_col2, 1)

        # --------------------------------------------------------------------

        ###################################
        ####### COMMENT AND SUMMARY #######
        ###################################
        
        comment_txt = wx.StaticText(self, label=self.commentLbl)
        comment_txt.SetFont(self.fontTitle)
        self.comment_box = wx.TextCtrl(self, size=(-1, 20), style=wx.TE_MULTILINE|wx.TE_BESTWRAP)
        self.comment_box.Bind(wx.EVT_TEXT, self.OnCommentChange)
        self.textbox_sizer.Add(comment_txt, 0, wx.EXPAND|wx.LEFT|wx.TOP, 5)
        self.textbox_sizer.Add(self.comment_box, 1, wx.EXPAND|wx.TOP, 3)

        summary_txt = wx.StaticText(self, label=self.summaryLbl)
        summary_txt.SetFont(self.fontTitle)
        self.summary_box = wx.TextCtrl(self, size=(-1, 20), style=wx.TE_MULTILINE|wx.TE_BESTWRAP|wx.TE_READONLY)
        self.summary_box.SetBackgroundColour((225, 225, 225))
        self.textbox_sizer.Add(summary_txt, 0, wx.EXPAND|wx.LEFT|wx.TOP, 5)
        self.textbox_sizer.Add(self.summary_box, 1, wx.EXPAND|wx.TOP, 3)

        # -----------------------

        self.layoutSizer.Add((5, 5), 0, wx.EXPAND)
        self.layoutSizer.Add(self.header1_colSizer, 0, wx.EXPAND)
        self.layoutSizer.Add(self.table1_colSizer, 0, wx.EXPAND)
        self.layoutSizer.Add((20, 20), 0, wx.EXPAND)
        self.layoutSizer.Add(self.header2_colSizer, 0, wx.EXPAND)
        self.layoutSizer.Add(self.table2_colSizer, 0, wx.EXPAND)
        self.layoutSizer.Add((20, 20), 0, wx.EXPAND)
        self.layoutSizer.Add(self.header3_colSizer, 0, wx.EXPAND)
        self.layoutSizer.Add(self.table3_colSizer, 0, wx.EXPAND)
        self.layoutSizer.Add((20, 20), 0, wx.EXPAND)
        self.layoutSizer.Add(self.textbox_sizer, 1, wx.EXPAND)

        self.SetSizer(self.layoutSizer)



    def OnTypeChange(self, evt):
        
        # Have it not be multiple choice
        cb_id = evt.GetId()
        if cb_id != self.table1_cb1.GetId():
            self.table1_cb1.SetValue(False)
        if cb_id != self.table1_cb2.GetId():
            self.table1_cb2.SetValue(False)

        self.addTextSummary()

    def OnReasonChange(self, evt):
        self.addTextSummary()

    def OnSSRChange(self, evt):

        # Have it not be multiple choice
        cb_id = evt.GetId()
        if cb_id != self.table3_cb1.GetId():
            self.table3_cb1.SetValue(False)
        if cb_id != self.table3_cb2.GetId():
            self.table3_cb2.SetValue(False)

        self.addTextSummary()  

    def OnCommentChange(self, evt):
        self.addTextSummary()


    def addTextSummary(self):
        added_text = []

        # Clear all the text entered prior
        current_text = self.parent.manager.manager.envCondManager.stationHealthRemarksCtrl
        cleared_text = re.sub(r"\@#.*?\#@", "", current_text)
        full_text = cleared_text.rstrip("\n")
        
        # Add newline if not there
        if (not full_text.endswith('\n')) and (len(full_text) > 0):
            added_text.append('\n')

        # Add the type line (only one is chosen)
        if self.table1_cb1.IsChecked():
            added_text.append('@# Type of Visit: ' + self.table1_title1 + ' #@\n')
        elif self.table1_cb2.IsChecked():
            added_text.append('@# Type of Visit: ' + self.table1_title2 + ' #@\n')

        # Build and add reason line
        reason_list = []
        if self.table2_cb1.IsChecked():
            reason_list.append(self.table2_title1)
        if self.table2_cb2.IsChecked():
            reason_list.append(self.table2_title2)
        if self.table2_cb3.IsChecked():
            reason_list.append(self.table2_title3)
        if len(reason_list) > 0:
            reason_txt = '@# Visit Reason: '
            for i, txt in enumerate(reason_list):
                if i < len(reason_list)-1 and len(reason_list) > 1:
                    reason_txt = reason_txt + txt + ', '
                else:
                    reason_txt = reason_txt + txt
            reason_txt = reason_txt + ' #@\n'
            added_text.append(reason_txt)
        
        # Add the special service request line (only one is chosen)
        if self.table3_cb1.IsChecked():
            added_text.append('@# Special Service Request: ' + self.table3_title1 + ' #@\n')
        elif self.table3_cb2.IsChecked():
            added_text.append('@# Special Service Request: ' + self.table3_title2 + ' #@\n')

        # Add the comment
        if self.comment_box.GetValue() != '':
            comment_txt = self.comment_box.GetValue()
            cleaned_txt = comment_txt.replace("\n", " ")
            final_comment = '@# Comment: ' + cleaned_txt + ' #@\n'
            added_text.append(final_comment)

        # Add all lines to full text
        for txt in added_text:
            full_text = full_text + txt
        
        # Set the text
        self.summary_box.SetValue(full_text)
        self.parent.manager.manager.envCondManager.stationHealthRemarksCtrl = full_text



def main():
    app = wx.App()

    frame = wx.Frame(None, size=(850, 600))
    SVOPanel(wx.frame, "DEBUG", frame)

    frame.Show()
    app.MainLoop()

if __name__ == "__main__":
    main()