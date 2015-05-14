import os
import stat
import time
# a dropfile program  that creats a dropbox and sorts files based upon the time created and writes file info and time drop to sql database







import wx
import shutil ,datetime
from datetime import datetime,timedelta 
import sqlite3
from ObjectListView import ObjectListView, ColumnDefn

##database setup 
conn =sqlite3.connect('timestamp.db')
cur =conn.cursor()
cur.execute("DROP TABLE IF EXISTS file_tmstmp ")
cur.execute("CREATE TABLE file_tmstmp( name TEXT, time_drop INT, meets_deadline TEXT ,Dest_fld TEXT)")


################drop box setup ########################################################
class MyFileDropTarget(wx.FileDropTarget):
    """"""
 
    #----------------------------------------------------------------------
    def __init__(self, window):
        """Constructor"""
        wx.FileDropTarget.__init__(self)
        self.window = window
 
    #----------------------------------------------------------------------
    def OnDropFiles(self, x, y, filenames):
        """
        When files are dropped, update the display """

       #for path in filenames:
        
        
    
            
        print "Files loaded"
            
    




        self.window.updateDisplay(filenames)
        
        
       
########################################################################
class FileInfo(object):
    """"""
 
    #----------------------------------------------------------------------
    def __init__(self, path, date_created, date_modified, size,current):
        """Constructor"""
        self.name = os.path.basename(path)
        self.path = path
        self.date_created = date_created
        self.date_modified = date_modified
        self.size = size
        self.current =current
 
########################################################################
class MainPanel(wx.Panel):
    """"""
 
    #----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent=parent)
        self.file_list = []
 
        file_drop_target = MyFileDropTarget(self)
        self.olv = ObjectListView(self, style=wx.LC_REPORT|wx.SUNKEN_BORDER)
        self.olv.SetDropTarget(file_drop_target)
        self.setFiles()
 
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.olv, 1, wx.EXPAND)
        self.SetSizer(sizer)

         
    #-------loop for files in dropbox ---------------------------------------------------------------
    def updateDisplay(self, file_list):
        global dest
        """"""
        #yesterday =datetime.now().date() + timedelta(days=-1)
        current = datetime.today()
        #time_limit = current - datetime.timedelta(days=1)
        #needs work time compariasion is not correct
        
         
        for path in file_list:
            file_stats = os.stat(path)
            creation_time = time.strftime("%m/%d/%Y %I:%M %p",
                                          time.localtime(file_stats[stat.ST_CTIME]))
            modified_time = time.strftime("%m/%d/%Y %I:%M %p",
                                          time.localtime(file_stats[stat.ST_MTIME]))
            current = time.strftime("%m/%d/%Y %I:%M %p",
                                          time.localtime())
            file_size = file_stats[stat.ST_SIZE]
            
            
            filemod = datetime.fromtimestamp(os.stat(path).st_mtime)
            now = datetime.today()
            max_delay = timedelta(days= 1)
            
            if file_size > 1024:
                file_size = file_size / 1024.0
                file_size = "%.2f KB" % file_size
                print "verfiying..."
                
            if  now-filemod < max_delay:
                 print 'File is Good'
                 print 'Copying files from:'+ path 
                 shutil.copy(path, dest)
                 cur.execute("INSERT INTO file_tmstmp VALUES (? , ? , ?,?)",(path,current,"YES","FOLEDER SET TO"+ dest))
#SQL insert approved files                 
                 print 'Copied files' + dest
            else :
                
                 print 'This file is too old to transfer:'            
            cur.execute("INSERT INTO file_tmstmp VALUES (? , ? , ?,?)",(path,current,"NO","FILE TO OLD"))
#sql insert for disapporved files           
            
            self.file_list.append(FileInfo(path,
                                           creation_time,
                                           modified_time,
                                           file_size,current))
        cur.execute
        self.olv.SetObjects(self.file_list)
        
                    
    #----------------------------------------------------------------------
    def setFiles(self):
        """"""
        self.olv.SetColumns([
            ColumnDefn("Name", "left", 220, "name"),
            ColumnDefn("Date created", "left", 150, "date_created"),
            ColumnDefn("Date modified", "left", 150, "date_modified"),
            ColumnDefn("Size", "left", 100, "size"),
            ColumnDefn("DROP Time ", "left", 100, "current")
            ])
        self.olv.SetObjects(self.file_list)
 
########################################################################
class MainFrame(wx.Frame):
    """"""
 
    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        wx.Frame.__init__(self, None, title="Transfer files", size=(800,600))
        panel = MainPanel(self)
        self.Show()

#####-----menubar---------------------------------------------------------------------
        self.statusbar = self.CreateStatusBar()
        
        menuFile = wx.Menu()
        menuFile.Append(1, "&Destination...")
        menuFile.AppendSeparator()
        menuFile.Append(3, "E&xit")
        menuBar = wx.MenuBar()
        menuBar.Append(menuFile, "&File")
        self.Bind(wx.EVT_MENU, self.select, id=1)
        menuFile.Append(2, "&Print DATABASE")
        self.Bind(wx.EVT_MENU, self.db, id=2)
        self.SetMenuBar(menuBar)

#database print button      
        self.Show()
    def db(self,event):
        cur.execute("SELECT* FROM file_tmstmp;")
        print "Database accessed" 
        print(cur.fetchall())
        conn.commit()
       
    def select(self,event):
        global dest
        dlg = wx.DirDialog(self, "Choose a directory:",style=wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            print "Destination Folder is  %s" % dlg.GetPath()
        dlg.Destroy()

        dest = dlg.GetPath()
        return dest
        print (dest)

   
#----------------------------------------------------------------------
def main():
    """"""
    app = wx.App(False)
    frame = MainFrame()
    app.MainLoop()
    conn.commit()
if __name__ == "__main__":
    main()
