import random
import smtplib
import ssl
from functools import partial
from tkinter import *
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_email(email):
    password = '147fg85fg'
    sender = 'testing820mail@gmail.com'
    receiver = email
    port = 465
    confirmation_code = random.randint(1000, 10000)

    email_message = MIMEMultipart("alternative")
    email_message["Subject"] = "Email verification"
    email_message["From"] = sender
    email_message["To"] = receiver

    body = """\
    This message is sent automatically. Do not reply to this message.
    Your verification code is {0}. Write this number in the application.
    Do not send this code to anybody!""".format(confirmation_code)

    mime_obj = MIMEText(body, "plain")
    email_message.attach(mime_obj)

    # Create a secure SSL context
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', port, context=context) as server:
        server.login('testing820mail@gmail.com', password)
        server.sendmail(sender, receiver, email_message.as_string())
    return confirmation_code


def check_confirmation_code(valid_code, input_code):
    try:
        if int(valid_code) == int(input_code):
            return True
        else:
            return False
    except:
        return False


root = Tk()
root.title('Text Editor')
root.geometry('800x500')

email_confirmed = 0

password_code = StringVar()


def new_file():
    my_text.delete('1.0', END)

    root.title('New File - Text Editor')
    status_bar.config(text='New File       ')


def connect():
    global password_code
    global email_confirmed

    def validate_passcode1(pass_code):
        global password_code
        global email_confirmed

        check = check_confirmation_code(password_code, pass_code.get())

        if check:
            email_confirmed = 2
        else:
            email_confirmed = 0

        print(email_confirmed)
        pass_window.destroy()

    def validate_email(email):

        def validate_passcode(pass_code):
            global password_code
            global email_confirmed

            check = check_confirmation_code(password_code, pass_code.get())

            if check:
                email_confirmed = 2
            else:
                email_confirmed = 0

            print(email_confirmed)
            password_window.destroy()

        global password_code
        global email_confirmed

        email_confirmed = 1
        password_code = send_email(email.get())

        connect_window.destroy()

        password_window = Tk()
        password_window.title('Email Confirmation')

        password_label = Label(password_window, text='Code:').grid(row=0, column=0)
        pass_code = StringVar(password_window)
        password_entry = Entry(password_window, textvariable=pass_code, width=50).grid(row=0, column=1)

        validate_passcode = partial(validate_passcode, pass_code)

        submit = Button(password_window, text='Submit', command=validate_passcode).grid(row=2, column=0)

        password_window.mainloop()

    if email_confirmed == 0:

        connect_window = Tk()
        connect_window.title('Email Confirmation')

        email_label = Label(connect_window, text='Email:').grid(row=0, column=0)
        email = StringVar(connect_window)
        email_entry = Entry(connect_window, textvariable=email, width=50).grid(row=0, column=1)

        validate_email = partial(validate_email, email)

        submit = Button(connect_window, text='Submit', command=validate_email).grid(row=2, column=0)

        connect_window.mainloop()

    elif email_confirmed == 1:

        pass_window = Tk()
        pass_window.title('Email Confirmation')

        pass_label = Label(pass_window, text='Code:').grid(row=0, column=0)
        pass_code = StringVar(pass_window)
        pass_entry = Entry(pass_window, textvariable=pass_code, width=50).grid(row=0, column=1)

        validate_passcode1 = partial(validate_passcode1, pass_code)

        submit = Button(pass_window, text='Submit', command=validate_passcode1).grid(row=2, column=0)

        pass_window.mainloop()


def check_status():
    global email_confirmed

    if email_confirmed == 0:
        my_text.delete('1.0', END)
        my_text.insert(END, 'UPS! Not confirmed email!')

    elif email_confirmed == 1:
        my_text.delete('1.0', END)
        my_text.insert(END, 'Email confirmation is pending!')

    elif email_confirmed == 2:
        my_text.delete('1.0', END)
        my_text.insert(END, 'YEY! Email confirmed!')


# Create Main Frame
my_frame = Frame(root)
my_frame.pack(pady=5)

# Create out Scrollbar For the Text Box
text_scroll = Scrollbar(my_frame)
text_scroll.pack(side=RIGHT, fill=Y)

# Create Text Box
my_text = Text(my_frame, width=97, height=25,
               font=('Helvetica', 16), selectbackground='yellow',
               selectforeground='black', undo=True,
               yscrollcommand=text_scroll.set)
my_text.pack()

# Configure out Scrollbar
text_scroll.config(command=my_text.yview)

# Create Menu
my_menu = Menu(root)
root.config(menu=my_menu)

# Add File Menu
file_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label='File', menu=file_menu)
file_menu.add_command(label='New', command=new_file)
file_menu.add_command(label='Confirm email', command=connect)
file_menu.add_command(label='Check email status', command=check_status)
file_menu.add_separator()
file_menu.add_command(label='Exit', command=root.quit)

# Add Status Bar to Bottom
status_bar = Label(root, text='Ready     ', anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=5)
root.mainloop()
