from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from datetime import datetime
from Pandas_Class import PandasDealer
from Txt_Class import TxtDealer
from Message_Class import SendEmail
from SQL_Class import SQLDealer

HEAD_FONT = ("Courier", 30, "bold")
HEADER_FONT = ("Arial", 15, "bold")
BOX_FONT = ("Arial", 15, "normal")
MAIL_FONT = ("Arial", 12, "normal")
COLUMNS = ("Receiver", "Subject", "Format", "Time")


class DesktopGmail:
    def __init__(self, window):
        self.window = window
        self.window.title("Desktop Gmail")
        self.window.geometry("1360x750")
        self.window.state("zoomed")
        # extra variables:
        self.receiver_name = StringVar()
        self.subject_name = StringVar()
        self.format_name = StringVar()
        self.sent_date = StringVar()
        self.actual_mail_body = StringVar()
        self.current_gmail = None
        self.current_format = None

        # define heading:
        self.main_frame = Frame(self.window, relief=RIDGE, bd=5)
        self.main_frame.place(x=10, y=10, width=1340, height=50)

        self.head_label = Label(self.main_frame, bd=0, text="GMAIL - DESKTOP VERSION", font=HEAD_FONT,
                                fg="firebrick", justify="center")
        self.head_label.place(x=205, y=5, width=1000, height=30)

        # define frames:
        # ============================================= LEFT FRAME ============================================ #
        self.left_frame = Frame(self.window, bg="gray", relief=RIDGE, bd=3)
        self.left_frame.place(x=10, y=65, width=413, height=625)

        self.inbox_header = Label(self.left_frame, text="Sent Messages", font=HEADER_FONT, bg="gray")
        self.inbox_header.place(x=5, y=5, width=398, height=25)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", backgroung="gray", foreground="black", rowheight=25, fieldbackground="white smoke")
        style.map("Treeview", background=[("selected", "medium sea green")])
        style.configure("Treeview.Heading", background="light steel blue", font=("Arial", 10, "bold"))

        self.sent_box_table = ttk.Treeview(self.left_frame, columns=COLUMNS)
        self.sent_box_table.place(x=5, y=33, width=398, height=250)
        self.sent_box_table.heading(COLUMNS[0], text=COLUMNS[0], anchor=CENTER)
        self.sent_box_table.heading(COLUMNS[1], text=COLUMNS[1], anchor=CENTER)
        self.sent_box_table.heading(COLUMNS[2], text=COLUMNS[2], anchor=CENTER)
        self.sent_box_table.heading(COLUMNS[3], text=COLUMNS[3], anchor=CENTER)
        self.sent_box_table.column(COLUMNS[0], width=10)
        self.sent_box_table.column(COLUMNS[1], width=10)
        self.sent_box_table.column(COLUMNS[2], width=10)
        self.sent_box_table.column(COLUMNS[3], width=10)
        self.sent_box_table["show"] = "headings"
        self.sent_box_table.bind("<ButtonRelease-1>", self.display_concrete_email)

        self.sent_header = Label(self.left_frame, text="Output", font=HEADER_FONT, bg="gray")
        self.sent_header.place(x=5, y=295, width=398, height=25)

        self.concrete_email = Text(self.left_frame, bg="white smoke")
        self.concrete_email.place(x=5, y=323, width=398, height=290)

        # ========================================== CENTER TOP FRAME ========================================= #
        self.top_frame = Frame(self.window, bg="gray", relief=RIDGE, bd=3)
        self.top_frame.place(x=425, y=65, width=603, height=198)
        # import image:
        self.logo_image = Image.open("./used_image/logo.png")
        self.logo_photo = ImageTk.PhotoImage(self.logo_image)
        self.gmail_image = Label(self.top_frame, image=self.logo_photo)
        self.gmail_image.image = self.logo_photo
        self.gmail_image.place(x=0, y=0)

        # ========================================= CENTER BOTTOM FRAME ======================================= #
        self.bottom_frame = Frame(self.window, bg="gray", relief=RIDGE, bd=3)
        self.bottom_frame.place(x=425, y=265, width=603, height=425)

        self.new_label = Label(self.bottom_frame, text="New Message", font=("Arial", 12, "bold"), justify="left",
                               bg="dim gray", fg="white smoke")
        self.new_label.place(x=0, y=0, width=595, height=50)

        self.to_label = Label(self.bottom_frame, text="To", font=MAIL_FONT, justify="left", bg="gray", fg="white smoke")
        self.to_label.place(x=0, y=60)

        self.receiver_entry = Entry(self.bottom_frame, font=MAIL_FONT, justify="left", textvariable=self.receiver_name,
                                    bg="gray", fg="white smoke", highlightthickness=0)
        self.receiver_entry.place(x=70, y=57, width=525, height=30)

        self.subject_label = Label(self.bottom_frame, text="Subject", font=MAIL_FONT, justify="left", bg="gray",
                                   fg="white smoke")
        self.subject_label.place(x=0, y=100)

        self.subject_entry = Entry(self.bottom_frame, font=MAIL_FONT, justify="left", textvariable=self.subject_name,
                                   bg="gray", fg="white smoke", highlightthickness=0)
        self.subject_entry.place(x=70, y=97, width=525, height=30)

        self.format_label = Label(self.bottom_frame, text="Format", font=MAIL_FONT, justify="left", bg="gray",
                                  fg="white smoke")
        self.format_label.place(x=0, y=140)

        self.format_entry = Entry(self.bottom_frame, font=MAIL_FONT, justify="left", textvariable=self.format_name,
                                  bg="gray", fg="white smoke", highlightthickness=0)
        self.format_entry.place(x=70, y=137, width=525, height=30)

        self.mail_text = Text(self.bottom_frame, font=MAIL_FONT, bg="white smoke")
        self.mail_text.place(x=0, y=177, width=595, height=200)

        self.button_frame = Frame(self.bottom_frame, relief=RIDGE)
        self.button_frame.place(x=0, y=382, width=595, height=30)

        self.send_button = Button(self.button_frame, text="Send", font=MAIL_FONT, width=21, bg="royal blue", fg="black",
                                  command=self.send_method)
        self.send_button.grid(row=0, column=0)

        self.clear_button = Button(self.button_frame, text="Clear", font=MAIL_FONT, width=21, bg="dark sea green",
                                   fg="black", command=self.clear_method)
        self.clear_button.grid(row=0, column=1)

        self.close_button = Button(self.button_frame, text="Close", font=MAIL_FONT, width=21, fg="black",
                                   bg="dark salmon", command=self.close_method)
        self.close_button.grid(row=0, column=2)

        # ============================================ RIGHT FRAME ============================================ #
        self.right_frame = Frame(self.window, bg="gray", relief=RIDGE, bd=3)
        self.right_frame.place(x=1030, y=65, width=320, height=625)

        self.email_header = Label(self.right_frame, text="Available Contacts", font=HEADER_FONT, bg="gray")
        self.email_header.place(x=5, y=5, width=305, height=20)

        self.email_box = Listbox(self.right_frame, bg="alice blue", font=BOX_FONT, fg="steel blue")
        self.email_box.place(x=5, y=30, width=305, height=340)
        self.email_box.bind("<<ListboxSelect>>", self.sensitive_email)

        self.form_header = Label(self.right_frame, text="Useful Templates", font=HEADER_FONT, bg="gray")
        self.form_header.place(x=5, y=388, width=305, height=20)

        self.form_box = Listbox(self.right_frame, bg="white", font=BOX_FONT, fg="dark olive green")
        self.form_box.place(x=5, y=413, width=305, height=200)
        self.form_box.bind("<<ListboxSelect>>", self.sensitive_format)

        # ---------------------------------------
        self.display_emails()
        self.display_formats()
        self.display_sent_gmails()

    # ================================= FUNCTIONALITY ==================================== #
    def display_emails(self):
        result = PandasDealer()
        available_emails = result.read_emails()
        counter = 1
        for email in available_emails:
            self.email_box.insert(counter, email)
            counter += 1

    def sensitive_email(self, event=""):
        self.email_box.focus()
        current_gmail = self.email_box.get(ACTIVE)
        self.receiver_name.set(current_gmail)

    def display_formats(self):
        result = TxtDealer()
        available_formats = result.read_txt()
        counter = 1
        for fmt in available_formats:
            self.form_box.insert(counter, fmt)
            counter += 1

    def sensitive_format(self, event=""):
        # to format section:
        self.form_box.focus()
        current_format = self.form_box.get(ACTIVE)
        self.format_name.set(current_format)
        # to text section:
        text_tool = TxtDealer()
        self.mail_text.delete("1.0", END)
        self.mail_text.insert(END, text_tool.return_default(current_format))

    def current_time(self):
        now = datetime.now()
        year = now.year
        month = now.month
        day = now.day
        hour = now.hour
        minute = now.minute
        current_moment = f"{day}/{month}/{year} {hour}:{minute}"
        return current_moment

    def display_sent_gmails(self):
        sql_tool = SQLDealer()
        sql_tool.display_data(self.sent_box_table)

    def get_updated_mail_body(self):
        answer = self.mail_text.get("1.0", END)
        return answer

    def send_method(self):
        confirm = messagebox.askyesno(title="Confirmation", message="Are You Sure To Send Email?")
        if confirm > 0:
            # send message:
            mail_receiver = self.receiver_name.get()
            mail_subject = self.subject_name.get()
            mail_body = self.get_updated_mail_body()

            # send command:
            send_tool = SendEmail(receiver=mail_receiver, subject=mail_subject, body=mail_body)
            send_tool.send_mail()
            messagebox.showinfo(title="FeedBack", message="Email has been sent Successfully!")

            # add info into sent box table:
            mail_type = self.format_name.get()
            current_time = self.current_time()
            main_body = self.get_updated_mail_body()
            sql_tool = SQLDealer()
            sql_tool.insert_data(receiver=mail_receiver, subject=mail_subject, letter_type=mail_type,
                                 sent_time=current_time, actual_text=main_body)
            # display sent data:
            self.display_sent_gmails()
        else:
            pass

    def display_concrete_email(self, event=""):
        # preparation:
        table_row = self.sent_box_table.focus()
        table_content = self.sent_box_table.item(table_row)
        current_row = table_content["values"]
        self.receiver_name.set(current_row[0])
        self.subject_name.set(current_row[1])
        self.format_name.set(current_row[2])
        self.sent_date.set(current_row[3])
        sql_tool = SQLDealer()
        actual_text = sql_tool.return_wanted_text(self.sent_date.get())
        self.actual_mail_body.set(actual_text)
        # display:
        self.concrete_email.delete("1.0", END)
        self.concrete_email.insert(END, f"To:\t\t" + self.receiver_name.get() + "\n")
        self.concrete_email.insert(END, f"Subject:\t\t" + self.subject_name.get() + "\n")
        self.concrete_email.insert(END, f"Format:\t\t" + self.format_name.get() + "\n")
        self.concrete_email.insert(END, f"Date:\t\t" + self.sent_date.get() + "\n" + "\n")
        self.concrete_email.insert(END, self.actual_mail_body.get())

    def clear_method(self):
        self.receiver_entry.delete(0, END)
        self.subject_entry.delete(0, END)
        self.format_entry.delete(0, END)
        self.mail_text.delete("1.0", END)
        self.concrete_email.delete("1.0", END)

    def close_method(self):
        confirm = messagebox.askyesno(title="Desktop Gmail", message="Do You Want To Close The Program?")
        if confirm > 0:
            self.window.destroy()
            return
        else:
            pass


def launch_gmail():
    app = Tk()
    DesktopGmail(app)
    app.mainloop()


if __name__ == "__main__":
    launch_gmail()
