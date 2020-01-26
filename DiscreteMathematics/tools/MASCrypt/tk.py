import resources.operations as operation
# from os import getcwd
from tkinter import Tk, Menu, Scrollbar, END, IntVar, StringVar
from tkinter import Frame, Grid, Label, Entry, Text, Checkbutton, Button
from tkinter import messagebox as MessageBox
from tkinter.ttk import Combobox, Style

program_name = 'MASCrypt'
program_description = 'Modular Arithmetic Software for Cryptography'
lbl_width = 14
lbl_anchor = 'e'
lbl_sticky = 'e'
entry_sticky = 'we'
padx = 3
pady = 3
font = ('Courier New', 10)
bg_color = '#C9C9C9'
fg_color = '#000000'

# All available operations.
op_addition = ('Addition', '+')
op_substraction = ('Substraction', '-')
op_multiplication = ('Multiplication', 'x')
op_division = ('Division', '/')
op_square_root = ('Square root', '√')
op_primitive_root = ('Primitive root', '∝')
op_xor = ('XOR', 'XOR')
op_mod_inverse = ('Module inverse', 'Inv')
op_exponentation = ('Exponentation', 'a^b')
op_module = ('Module', 'mod')
op_gcd = ('GCD', 'GDC')
op_lcm = ('LCM', 'LCM')
op_primality = ('Primality', 'Prime')
op_factorization = ('Factorization', 'Fact')
op_discreteLogarithm = ('Discrete Logarithm', 'DLP')


def clear_all_entries():
    ''' Empty all entries.'''
    ops = [op1, op2, op3, mod, res]
    for op in ops:
        op.set('')
    op3_active.set(0)
    set_op3()
    mod_active.set(0)
    set_module()


def clear_all_widgets():
    ''' Clear all widgets in grid.'''
    clear_all_entries()
    widgets = [
        lbl_op1, ent_op1,
        lbl_op2, ent_op2,
        chk_op3, ent_op3,
        lbl_module, chk_module, ent_module,
        lbl_res, ent_res
    ]
    for widget in widgets:
        widget.grid_remove()


def set_base(event):
    clear_all_entries()

    b = cb_base.get()

    if b == cb_base_base2:
        base.set(2)
    elif b == cb_base_base10:
        base.set(10)
    elif b == cb_base_base16:
        base.set(16)

    print(f'base.get() = {base.get()}')


def set_module():
    if mod_active.get():
        ent_module.config(state='normal')
    else:
        ent_module.config(state='disabled')


def set_op3():
    if op3_active.get():
        ent_op3.config(state='normal')
    else:
        ent_op3.config(state='disabled')


def set_operation(selected_op):
    clear_all_widgets()

    lbl_op_title['text'] = selected_op

    # All operations include op1, res and btn_calculate widgets.
    lbl_op1.grid(
        row=1,
        column=0,
        padx=padx,
        pady=pady,
        sticky=lbl_sticky
    )
    ent_op1.grid(
        row=1,
        column=1,
        padx=padx,
        pady=pady,
        sticky=entry_sticky
    )

    lbl_res.grid(
        row=5,
        column=0,
        padx=padx,
        pady=pady,
        sticky=lbl_sticky
    )
    ent_res.grid(
        row=5,
        column=1,
        padx=padx,
        pady=pady,
        sticky=entry_sticky
    )

    # Operations that use op2 widgets.
    if selected_op in [
        op_addition[0],
        op_substraction[0],
        op_multiplication[0],
        op_division[0],
        op_xor[0],
        op_exponentation[0],
        op_gcd[0],
        op_lcm[0],
        op_discreteLogarithm[0]
    ]:
        lbl_op2.grid(
            row=2,
            column=0,
            padx=padx,
            pady=pady,
            sticky=lbl_sticky
        )
        ent_op2.grid(
            row=2,
            column=1,
            padx=padx,
            pady=pady,
            sticky=entry_sticky
        )

    # Operations that use op3 widgets.
    if selected_op in [
        op_gcd[0],
        op_lcm[0]
    ]:
        chk_op3.grid(
            row=3,
            column=0,
            padx=padx-1,
            sticky=lbl_sticky
        )
        ent_op3.grid(
            row=3,
            column=1,
            padx=padx,
            pady=pady,
            sticky=entry_sticky
        )

    # Base and Y widgets only for Discrete Logarithm operation.
    if selected_op == op_discreteLogarithm[0]:
        lbl_op1['text'] = 'Base'
        lbl_op2['text'] = 'Y'
    else:
        lbl_op1['text'] = 'First operator'
        lbl_op2['text'] = 'Second operator'

    # Operations that use module widgets.
    if selected_op in [
        op_addition[0],
        op_substraction[0],
        op_multiplication[0],
        op_exponentation[0],
        op_mod_inverse[0],
        op_module[0],
        op_discreteLogarithm[0]
    ]:
        if selected_op in [
            op_addition[0],
            op_substraction[0],
            op_multiplication[0],
            op_exponentation[0]
        ]:
            chk_module.grid(
                row=4,
                column=0,
                padx=padx-1,
                sticky=lbl_sticky
            )
        elif selected_op in [
            op_mod_inverse[0],
            op_module[0],
            op_discreteLogarithm[0]
        ]:
            lbl_module.grid(
                row=4,
                column=0,
                padx=padx,
                pady=pady,
                sticky=lbl_sticky
            )
            ent_module.config(state='normal')

        ent_module.grid(
            row=4,
            column=1,
            padx=padx,
            pady=pady,
            sticky=entry_sticky
        )

    oper.set(selected_op)

    print(f'oper.get() = {oper.get()}')


def calculate():
    items_with_error = []
    op = oper.get()
    if not base.get():
        items_with_error.append('Base')

    if not op:
        items_with_error.append('Operation')

    if len(items_with_error) != 0:
        MessageBox.showerror(
            title=f'Missing information:',
            message=f'You must select the following items:\
            \n\n{", ".join(items_with_error)}'
        )
        return

    if op == op_addition[0]:
        if mod_active.get():
            operation.addition(res, base, op1, op2, mod)
            txt_history.insert(
                END, f'{op1.get()} + {op2.get()} mod {mod.get()} = {res.get()}\n'
            )
        else:
            operation.addition(res, base, op1, op2)
            txt_history.insert(
                END, f'{op1.get()} + {op2.get()} = {res.get()}\n'
            )
    elif op == op_substraction[0]:
        if mod_active.get():
            operation.substraction(res, base, op1, op2, mod)
            txt_history.insert(
                END, f'{op1.get()} - {op2.get()} mod {mod.get()} = {res.get()}\n'
            )
        else:
            operation.substraction(res, base, op1, op2)
            txt_history.insert(
                END, f'{op1.get()} - {op2.get()} = {res.get()}\n'
            )
    elif op == op_multiplication[0]:
        if mod_active.get():
            operation.multiplication(res, base, op1, op2, mod)
            txt_history.insert(
                END, f'{op1.get()} x {op2.get()} mod {mod.get()} = {res.get()}\n'
            )
        else:
            operation.multiplication(res, base, op1, op2)
            txt_history.insert(
                END, f'{op1.get()} x {op2.get()} = {res.get()}\n'
            )
    elif op == op_division[0]:
        operation.division(res, base, op1, op2)
        txt_history.insert(
            END, f'{op1.get()}/{op2.get()} = {res.get()}\n'
        )
    elif op == op_square_root[0]:
        operation.square_root(res, base, op1)
        txt_history.insert(
            END, f'√{op1.get()} = {res.get()}\n'
        )
    elif op == op_primitive_root[0]:
        operation.primitive_root(res, base, op1)
        txt_history.insert(
            END, f'|∝|={len(eval(res.get()))}, {op1.get()} = {res.get()}\n'
        )
    elif op == op_xor[0]:
        operation.xor(res, base, op1, op2)
        txt_history.insert(
            END, f'{op1.get()} XOR {op2.get()} = {res.get()}\n'
        )
    elif op == op_mod_inverse[0]:
        operation.mod_inverse(res, base, op1, mod)
        txt_history.insert(
            END, f'inv({op1.get()}, {mod.get()}) = {res.get()}\n'
        )
    elif op == op_exponentation[0]:
        if mod_active.get():
            operation.exponentation(res, base, op1, op2, mod)
            txt_history.insert(
                END, f'{op1.get()}^{op2.get()} mod {mod.get()} = {res.get()}\n'
            )
        else:
            operation.exponentation(res, base, op1, op2)
            txt_history.insert(
                END, f'{op1.get()}^{op2.get()} = {res.get()}\n'
            )
    elif op == op_module[0]:
        operation.module(res, base, op1, mod)
        txt_history.insert(
            END, f'{op1.get()} mod {mod.get()} = {res.get()}\n'
        )
    elif op == op_gcd[0]:
        if op3_active.get():
            operation.gcd(res, base, op1, op2, op3)
            txt_history.insert(
                END, f'gdc({op1.get()}, {op2.get()}, {op3.get()}) = {res.get()}\n'
            )
        else:
            operation.gcd(res, base, op1, op2)
            txt_history.insert(
                END, f'gdc({op1.get()}, {op2.get()}) = {res.get()}\n'
            )
    elif op == op_lcm[0]:
        if op3_active.get():
            operation.lcm(res, base, op1, op2, op3)
            txt_history.insert(
                END, f'lcm({op1.get()}, {op2.get()}, {op3.get()}) = {res.get()}\n'
            )
        else:
            operation.lcm(res, base, op1, op2)
            txt_history.insert(
                END, f'lcm({op1.get()}, {op2.get()}) = {res.get()}\n'
            )
    elif op == op_primality[0]:
        operation.primality(res, base, op1)
        txt_history.insert(
            END, f'{op1.get()} {res.get().lower()}\n'
        )
    elif op == op_factorization[0]:
        operation.factorization(res, base, op1)
        txt_history.insert(
            END, f'{op1.get()} = {res.get()}\n'
        )
    elif op == op_discreteLogarithm[0]:
        operation.discreteLogarithm(res, base, op1, op2, mod)
        txt_history.insert(
            END, f'{op1.get()}^{res.get()} = {op2.get()} mod {mod.get()}\n'
        )

    txt_history.see(END)


def about():
    MessageBox.showinfo(f'About {program_name}', f'{program_description}')


root = Tk()
# root.geometry('650x250')
root.title(f'{program_name} - {program_description}')
root.resizable(1, 0)
# root.iconbitmap(f'@{getcwd()}/img/icon.xbm')

style = Style()
style.theme_create('custom_style',
                   parent='default',
                   settings={'TCombobox':
                             {'configure':
                              {'selectforeground': 'black',
                               'selectbackground': 'white'}
                              }
                             }
                   )
style.theme_use('custom_style')

menubar = Menu(root, bg=bg_color, fg=fg_color, borderwidth=1)
root.config(menu=menubar)

options_menu = Menu(menubar, tearoff=0)
options_menu.add_command(label='Configuration')
options_menu.add_separator()
options_menu.add_command(label='Exit', command=root.quit)

base = IntVar()
txt_history = StringVar()
oper = StringVar()
op1 = StringVar()
op2 = StringVar()
op3_active = IntVar()
op3 = StringVar()
mod_active = IntVar()
mod = StringVar()
res = StringVar()

base_list = [
    ('Base-2 (Binary)', 2),
    ('Base-10 (Decimal)', 10),
    ('Base-16 (Hexadecimal)', 16)
]

base_menu = Menu(menubar, tearoff=0)

for b in base_list:
    base_menu.add_command(
        label=f'{b[0]}', command=lambda b=b[1]: base.set(b)
    )

operation_list = [
    op_addition,
    op_substraction,
    op_multiplication,
    op_division,
    op_square_root,
    op_primitive_root,
    op_xor,
    op_mod_inverse,
    op_exponentation,
    op_module,
    op_gcd,
    op_lcm,
    op_primality,
    op_factorization,
    op_discreteLogarithm
]

operations_menu = Menu(menubar, tearoff=0)

for op in operation_list:
    operations_menu.add_command(
        label=f'{op[0]}', command=lambda op=op[0]: set_operation(op)
    )

help_menu = Menu(menubar, tearoff=0)
help_menu.add_command(label='View terms of use')
help_menu.add_command(label='View license')
help_menu.add_command(label='Documentation')
help_menu.add_separator()
help_menu.add_command(label=f'About {program_name}', command=about)

menubar.add_cascade(label='Options', menu=options_menu)
menubar.add_cascade(label='Base', menu=base_menu)
menubar.add_cascade(label='Operations', menu=operations_menu)
menubar.add_cascade(label='Help', menu=help_menu)

frm_L = Frame(
    root,
    bg=bg_color,
    bd=5
)
frm_L.pack(side='left', expand=True, fill='both')
frm_L.grid_propagate(False)
frm_L.grid_columnconfigure(1, weight=1)

frm_R = Frame(
    root,
    bg=bg_color,
    bd=5,
    width=150
)
frm_R.pack(side='right', expand=True, fill='both')
frm_R.grid_propagate(True)
frm_R.grid_columnconfigure(0, weight=1)
frm_R.grid_rowconfigure(1, weight=1)

frm_L1 = Frame(
    frm_L,
    bg=bg_color,
    bd=5,
    width=550,
    height=167
)
frm_L1.pack(expand=True, fill='both')
frm_L1.grid_propagate(False)
frm_L1.grid_columnconfigure(1, weight=1)

lbl_op_title = Label(
    frm_L1,
    anchor='center',
    text='Please, select an operation.',
    font='Helvetica 13 bold',
    width=lbl_width,
    bg=bg_color,
    fg=fg_color
)
lbl_op_title.grid(
    row=0,
    column=0,
    columnspan=2,
    padx=padx,
    pady=pady,
    sticky='we'
)

lbl_op1 = Label(
    frm_L1,
    anchor=lbl_anchor,
    text='First operator',
    width=lbl_width,
    bg=bg_color,
    fg=fg_color
)
ent_op1 = Entry(
    frm_L1,
    font=font,
    textvariable=op1
)

lbl_op2 = Label(
    frm_L1,
    anchor=lbl_anchor,
    text='Second operator',
    width=lbl_width,
    bg=bg_color,
    fg=fg_color
)
ent_op2 = Entry(
    frm_L1,
    font=font,
    textvariable=op2
)

chk_op3 = Checkbutton(
    frm_L1,
    anchor=lbl_anchor,
    text='Third operator',
    width=lbl_width-3,
    bg=bg_color,
    fg=fg_color,
    variable=op3_active,
    command=set_op3
)
ent_op3 = Entry(
    frm_L1,
    font=font,
    textvariable=op3
)

chk_module = Checkbutton(
    frm_L1,
    anchor=lbl_anchor,
    text='Module',
    width=lbl_width-3,
    bg=bg_color,
    fg=fg_color,
    variable=mod_active,
    command=set_module
)
lbl_module = Label(
    frm_L1,
    anchor=lbl_anchor,
    text='Module',
    width=lbl_width,
    bg=bg_color,
    fg=fg_color
)
ent_module = Entry(
    frm_L1,
    state='disabled',
    font=font,
    textvariable=mod
)

lbl_res = Label(
    frm_L1,
    anchor=lbl_anchor,
    text='Result',
    width=lbl_width,
    bg=bg_color,
    fg=fg_color
)
ent_res = Entry(
    frm_L1,
    font=font,
    textvariable=res,
    state='readonly',
    readonlybackground='white'
)

frm_L2 = Frame(
    frm_L,
    bg=bg_color,
    bd=5
)
frm_L2.pack(expand=True, fill='both')
frm_L2.grid_columnconfigure(1, weight=1)

btn_calculate = Button(
    frm_L2,
    text='Calculate',
    command=lambda: calculate()
)
btn_calculate.grid(row=0, column=0, padx=padx, pady=pady, sticky='w')

cb_base_default = '-- Select base --'
cb_base_base2 = 'Binary (Base-2)'
cb_base_base10 = 'Decimal (Base-10)'
cb_base_base16 = 'Hexadecimal (Base-16)'

cb_base = Combobox(frm_L2, state='readonly')
cb_base['values'] = [
    cb_base_default,
    cb_base_base2,
    cb_base_base10,
    cb_base_base16
]

cb_base.current(0)
cb_base.bind('<<ComboboxSelected>>', set_base)
cb_base.grid(row=0, column=1, padx=padx, pady=pady, sticky='w')

frm_L3 = Frame(
    frm_L,
    bg=bg_color,
    bd=5
)
frm_L3.pack(expand=True, fill='both')
frm_L3.grid_columnconfigure(1, weight=1)

# Grid for buttons
rows = 3
cols = 5
for i in range(rows):
    for x, o in enumerate(operation_list[cols*i:cols*(i+1)]):
        Grid.columnconfigure(frm_L3, x, weight=1)
        op_btn = Button(
            frm_L3,
            text=o[1],
            command=lambda o=o[0]: set_operation(o)
        )
        op_btn.grid(row=i, column=x, padx=padx, pady=pady, sticky='nsew')

lbl_history = Label(
    frm_R,
    anchor='center',
    text='History',
    width=lbl_width,
    bg=bg_color,
    fg=fg_color
)
lbl_history.grid(
    row=0,
    column=0,
    columnspan=2,
    padx=padx,
    pady=pady,
    sticky='n'
)

txt_history = Text(
    frm_R,
    font=font,
    state='normal',
    width=25,
    height=15
)
scrollb = Scrollbar(frm_R)
scrollb.config(command=txt_history.yview)
txt_history.config(yscrollcommand=scrollb.set)
scrollb.grid(row=1, column=1, pady=pady, sticky='nsew')
txt_history.grid(row=1, column=0, pady=pady, sticky='nsew')

btn_clear_history = Button(
    frm_R,
    text='Clear history',
    command=lambda: txt_history.delete('1.0', END)
)
btn_clear_history.grid(
    row=2,
    column=0,
    columnspan=2,
    padx=padx,
    pady=pady,
    sticky='nsew'
)

root.mainloop()
