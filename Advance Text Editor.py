from tkinter import *
import tkinter.filedialog as alert
import tkinter.messagebox as msg
import pyautogui as auto
import speech_recognition as sr
import pyttsx3
class Main(Tk):
    def __init__(self):
        # root = self
        super().__init__()
        self.geometry('700x500')
        # self.minsize(700,500)
        self.title('Text Pro')

    def adding_hor_ver_scrollbar(self):
        self.scrollbar_verticle = Scrollbar(self)
        self.scrollbar_verticle.pack(side=RIGHT,fill=Y)

    def draw_text_area(self):
        self.text_area = Text(self,yscrollcommand=self.scrollbar_verticle.set,font = "arial 18",
                              fg="black",bg = 'white')
        self.scrollbar_verticle.config(command=self.text_area.yview)
        self.text_area.pack(fill=BOTH,expand=True)

    def get_text_entered(self):
        text = self.text_area.get(1.0,END)
        return text

    def open_file_code(self):
        # For reusability in open
        self.open_file = alert.askopenfile(mode='r', filetype=[('Text files', '*.txt'),
                                                               ("Python files", '*.py')])
        if self.open_file is not None:  # User choose a file
            content = self.open_file.read()
            self.text_area.delete(1.0, END)
            self.text_area.insert(1.0, content)

    def open_fle_main_function(self):
        content = self.text_area.get(1.0,END)
        # If user is already written somethin on the screen and he was opening the file
        # Then asking to user for saving existing file . for this we use save as function
        if len(content)==1: # If the window is emty nothing is wriiten in it then simply open file
            self.open_file_code() # Calling function to open dialogue box
        else:
            b = msg.askyesnocancel('Confirmation', 'Do you want to save this untitled file ?')
            print(b)
            if b:  # b = Yes
                # Opninng new file by saving existing file
                self.save_as()
                self.open_file_code()
            elif b == False:  # b = No
                # Opening new file wihtout saving existing file
                self.open_file_code()


    def save(self):
        try:
            path_string = str(self.open_file)
            lis = path_string.split("'")
            path = lis[1]
            for i in path:
                if i == '/':
                    path.replace(i, " \\")
            with open(path,'w') as file:
                new_content = self.text_area.get(1.0,END)
                file.write(new_content)
        except:
            msg.showinfo('Error',"A file can't be save without opening it")

    def new(self):
       content = self.text_area.get(1.0,END)
       if len(content) == 1:
           self.text_area.delete(1.0,END)
       else:
           b = msg.askyesnocancel('Confirmation','Do you want to save this untitled file ?')
           print(b)
           if b: # b = Yes
               self.save_as()
               self.text_area.delete(1.0, END)
           elif b == False: # b = No
               print('Yes')
               self.text_area.delete(1.0,END)

    def save_as(self):
        content = self.text_area.get(1.0, END)
        try:
            if len(content) > 1: # Content is not empty
                saveas_file = alert.asksaveasfile(filetype=[('Text files','*.txt'),('Python files','*.py')],
                                              defaultextension=[('Text files','*.txt'),('Python files','*.py')])
                saveas_file.write(content)
            else:
                msg.showinfo('Error','You cannot save empty file!')
        except:
            msg.showinfo('info','Something went wrong please try again')

    #Function for reciving the input from microphone and converting into text
    def text_to_speech(self,button):
        button.update()
        button['text'] = 'Listening...'
        button.update()
        r = sr.Recognizer()
        with sr.Microphone() as source:
            audio = r.listen(source)
        try:
            query = r.recognize_google(audio)
            button['text'] = 'Done,Start Again'
            button.update()
            self.text_area.insert(END , " "+query)

        except:
            msg.showerror("Falied !","Some error occured please try again")

    # Pop_UP window for sppech to text
    def pop_up_for_sptext(self):
        pop_uo = Tk()
        pop_uo.geometry('250x200+350+200')
        pop_uo.title("Speech->Text ")
        Label(pop_uo, font= "arial 10 bold", text="Click the button and start speaking\n"
                                                  "When you stop the audio is\nconverted into text\n"
                                                  "Make Sure to Connect with internet",).\
            pack(padx = 10,pady = 20)
        b1 = Button(pop_uo,text="Start Speaking",relief=GROOVE,font="arial 8 bold",bg = "yellow",
               command = lambda : self.text_to_speech(b1))
        b1.pack()

    # For text to speech
    def pop_up_for_textspeech(self):
        pop_uo = Tk()
        pop_uo.geometry('250x200+350+200')
        pop_uo.title("Speech->Text ")
        Label(pop_uo, font= "arial 10 bold", text="Click ont the start button.\n"
                                                  "You will recieve a message when\n text converted"
                                                  "into audio."
                                                  "",).\
            pack(padx = 10,pady = 20)


        b1 = Button(pop_uo,text="Start convertion",relief=GROOVE,font="arial 8 bold",bg = "yellow",
               command = lambda : self.text_to_speech(b1))
        b1.pack()

    #Function to change font color
    def Fontcolor(self):
        # Making the window for it
        pop_uo = Tk()
        pop_uo.geometry('250x200+350+200')
        pop_uo.title("Font color ")
        Label(pop_uo,text = "Enter the font color and click\non the apply button",
              font = "Arial 13 bold").pack(pady=20)
        x = StringVar()
        entry = Entry(pop_uo , textvariable = x,bd=3,width=20,font = "arial 15")
        entry.pack()

        #This is to get entry and try to apply this on text area this is called by submit button
        def change_color():
            a = entry.get()
            try:
                self.text_area.update()
                self.text_area["fg"] = a
            except:
                msg.showerror("Error","Invalid Color!")
            pop_uo.destroy()


        B2 = Button(pop_uo,text="Apply",relief = GROOVE, bg="black" ,fg = "yellow",font = "arial 10"
                   ,command = change_color)
        B2.pack(pady=10)

    # For changing font size
    def Fontsize(self):
        #Making the window for it
        pop_uo = Tk()
        pop_uo.geometry('250x200+350+200')
        pop_uo.title("Font color ")
        Label(pop_uo,text = "Enter the font size and click\non the apply button",
              font = "Arial 13 bold").pack(pady=20)
        Label(pop_uo, text="Size must be between 10 to 100.",
              font="Arial 10 bold").pack()
        x = IntVar()
        entry = Entry(pop_uo , textvariable = x,bd=3,width=20,font = "arial 15")
        entry.pack()

        #This is to get entry and try to apply this on text area this is called by submit button
        def change_color():
            a = int(entry.get())
            if(a<10 or a>100):
                msg.showinfo("Error!","Ivalid size")
                pop_uo.destroy()
                return
            try:
                self.text_area.update()
                b = str(a)
                self.text_area["font"] = f"arial {b}"
            except:
                msg.showerror("Error","Some error occured try again")
            pop_uo.destroy()


        B2 = Button(pop_uo,text="Apply",relief = GROOVE, bg="black" ,fg = "yellow",font = "arial 10"
                   ,command = change_color)
        B2.pack(pady=10)

    #Function for changing background color
    def bgcolor(self):
        # Making the window for it
        pop_uo = Tk()
        pop_uo.geometry('250x200+350+200')
        pop_uo.title("Font color ")
        Label(pop_uo, text="Enter the Background color and click\non the apply button",
              font="Arial 13 bold").pack(pady=20)
        x = StringVar()
        entry = Entry(pop_uo, textvariable=x, bd=3, width=20, font="arial 15")
        entry.pack()

        # This is to get entry and try to apply this on text area this is called by submit button
        def change_color():
            a = entry.get()
            try:
                self.text_area.update()
                self.text_area["bg"] = a
            except:
                msg.showerror("Error", "Invalid Color!")
            pop_uo.destroy()

        B2 = Button(pop_uo, text="Apply", relief=GROOVE, bg="black", fg="yellow", font="arial 10"
                    , command=change_color)
        B2.pack(pady=10)

    def making_main_menu(self):
        self.main_menu = Menu(self)
        # Adding items in 1st File submenu
        self.sub_menu_1 = Menu(self.main_menu,tearoff=0)
        self.sub_menu_1.add_command(label='New',command=self.new)
        self.sub_menu_1.add_command(label='Open',command=self.open_fle_main_function)
        self.sub_menu_1.add_command(label='Save',command=self.save)
        self.sub_menu_1.add_command(label='Save as',command=self.save_as)
        self.sub_menu_1.add_command(label='Exit',command=self.exit)
        self.main_menu.add_cascade(label='File',menu = self.sub_menu_1 )
        # Adding items in second submenu edit
        self.sub_menu_2 = Menu(self.main_menu,tearoff=0)
        self.sub_menu_2.add_command(label='Undo',command=self.undo)
        self.sub_menu_2.add_command(label='Select all',command=self.select_all)
        self.sub_menu_2.add_separator()
        self.sub_menu_2.add_command(label='Cut',command=self.cut)
        self.sub_menu_2.add_command(label='Copy',command=self.copy)
        self.sub_menu_2.add_command(label='Paste',command=self.paste)
        self.sub_menu_2.add_command(label='Font Color', command=self.Fontcolor)
        self.sub_menu_2.add_command(label='Font Size', command=self.Fontsize)
        self.sub_menu_2.add_command(label='Background Color', command=self.bgcolor)
        self.main_menu.add_cascade(menu=self.sub_menu_2,label='Edit')
        # Adding items in main menu
        self.main_menu.add_command(label='Text->Speech',command=self.pop_up_for_textspeech )
        self.main_menu.add_command(label='Speech->Text', command=self.pop_up_for_sptext)
        self.main_menu.add_command(label='About',command = self.pop_window)
        self.main_menu.add_command(label='Exit',command=self.exit)
        self.config(menu=self.main_menu)

    def undo(self):
        if len(self.text_area.get(1.0,END))>1:
            auto.hotkey('ctrl','z')
        else:
            msg.showinfo('Error','Undo cannot run of empty window!')
    def select_all(self):
        auto.hotkey('ctrl','a')
    def copy(self):
        try:
            self.text_area.selection_get()
            auto.hotkey('ctrl','c')
        except:
            msg.showinfo('Error','Something went wrong!')
    def paste(self):
        try:
            auto.hotkey('ctrl','v')
        except:
            msg.showinfo('Error','Something went wrong!')
    def cut(self):
        try:
            self.text_area.selection_get() # Making sure that user has selected some text if he does not selected text
            # then execpt block will run and error wil show him because text_area.selection_get() function return error
            # when nothing is selected. so if nothing is selected then error will show
            auto.hotkey('ctrl','x')
        except:
            msg.showinfo('Error','Something went wrong!')
    def exit(self):
        if len(self.text_area.get(1.0,END)) ==1:
            self.destroy()
        else:
            a = msg.askyesnocancel('Confirm','Do you want to save the existing file or not?')
            if a:
                self.save_as()
                self.destroy()
            elif a == False:
                self.destroy()

    def pop_window(self,):

       pop_uo = Tk()
       pop_uo.geometry('250x200+350+200')
       pop_uo.title("About us")
       Label(pop_uo,text=''' 
       Mahesh is the editor and he is very funny\nand he is pagal and
       he cannot\n cook and he is now facing many problems during his\n
       job so \n final conclusion is that mahesh is pagal'''
             ).pack()

       def dest():
           pop_uo.destroy()
       Button(pop_uo,text="Ok",command=dest).pack()
       pop_uo.mainloop()


if __name__ == '__main__':
    notepad = Main()
    notepad.adding_hor_ver_scrollbar()
    notepad.draw_text_area()
    notepad.making_main_menu()
    notepad.mainloop()
