import tkinter as tk
import random

if __name__ == "__main__":

    def RGB(hexcode):
        linRGB = []
        SRGB = [int(hexcode[1:3], 16)/255, int(hexcode[3:5], 16)/255, int(hexcode[5:], 16)/255]
        for item in SRGB:
            if item <= 0.03928:
                linRGB.append(item/12.92)
            else: 
                linRGB.append(pow((((item + 0.055)/1.055)), 2.4))   
        return(linRGB)

    def lum(hexcode):
        linRGB = []
        linRGB = RGB(hexcode)
        Y = 0.2126*linRGB[0] + 0.7152*linRGB[1] + 0.0722*linRGB[2]
        return(Y)

    def contrast(A, B):
        lumA = lum(A)
        lumB = lum(B)
        if lumA > lumB:
            contrastOutput = (lumA+0.05)/(lumB+0.05)
        else: 
            contrastOutput = (lumB+0.05)/(lumA+0.05)
        return(contrastOutput)

    def drawEntries():
        entries = []
        for i in range(3):
            entry = tk.Entry(gui, width = 3)
            entry.insert('insert', defaultHex[(2*i+1):(2*i+3)])
            entry.grid(sticky='S', row=3, column=(5*i+1), columnspan = 3)
            entries.append(entry)
        return(entries)

    def drawText(hexcode):
        lightMode = tk.Label(gui, height=1, width=15, background=light, foreground = hexcode, anchor='center', padx=1, pady=1, text='text in light mode')
        lightMode.grid(row = 6, column = 0, columnspan = 5)

        darkMode = tk.Label(gui, height=1, width=15, background=dark, foreground = hexcode, anchor='center', padx=1, pady=1, text='text in dark mode')
        darkMode.grid(row = 6, column = 5, columnspan = 5)

        amoledMode = tk.Label(gui, height=1, width=15, background=amoled, foreground = hexcode, anchor='center', padx=1, pady=1, text='text in amoled mode')
        amoledMode.grid(row = 6, column = 10, columnspan = 5)

        lightModeContrast = tk.Label(gui, height=1, width=15, background=light, foreground = '#000000', anchor='center', padx=1, pady=1, text='{0:,.2f}'.format(contrast(hexcode, light)))
        lightModeContrast.grid(row = 7, column = 0, columnspan = 5)
    
        darkModeContrast = tk.Label(gui, height=1, width=15, background=light, foreground = '#000000', anchor='center', padx=1, pady=1, text='{0:,.2f}'.format(contrast(hexcode, dark)))
        darkModeContrast.grid(row = 7, column = 5, columnspan = 5)
    
        amoledModeContrast = tk.Label(gui, height=1, width=15, background=light, foreground = '#000000', anchor='center', padx=1, pady=1, text='{0:,.2f}'.format(contrast(hexcode, amoled)))
        amoledModeContrast.grid(row = 7, column = 10, columnspan = 5)

    def fillColor(hexcode):
        canvas = tk.Canvas(gui, width = 50, height = 50)
        canvas.grid(row = 4, column = 6, columnspan = 3)
        canvas.create_rectangle(0, 50, 50, 0, fill =hexcode)

    def calculate():
        elements = ['#', entries[0].get(), entries[1].get(), entries[2].get()]
        combinedHex = ''.join(elements)

        drawText(combinedHex)
        fillColor(combinedHex)

    def updateEntries(hexcode):
        for i, entry in enumerate(entries):
            entry.delete('0', 'end')
            entry.insert('insert', hexcode[(2*i+1):(2*i+3)])
        

    def randomize(entries):
        defaultHex = random.choice(contrastPass)
        drawText(defaultHex)
        fillColor(defaultHex)
        updateEntries(defaultHex)

    def increment(index):
        hexBit = hex(min(((int(entries[index].get(), 16))+1), 255))
        entries[index].delete('0', 'end')
        entries[index].insert('insert', hexBit[2:])
        calculate()
    
    def decrement(index):
        hexBit = hex(max(((int(entries[index].get(), 16))-1), 0))
        entries[index].delete('0', 'end')
        entries[index].insert('insert', hexBit[2:])
        calculate()
        


    chars = '0123456789ABCDEF'
    hex3list = []

    light = '#FFFFFF'
    dark = '#36393F'
    amoled = '#000000'

    for i in range (15):
        for j in range (15):
            for k in range(15):
                hextemp = [chars[i], chars[i], chars[j], chars[j], chars[k], chars[k]]
                hex3list.append('#'+''.join(hextemp))

    contrastPass = []
    for code in hex3list:
        if lum(code) >= 0.239 and lum(code) <= 0.279:
            contrastPass.append(code)

    defaultHex = random.choice(contrastPass)

    gui = tk.Tk()
    gui.configure(background='white')
    gui.title('Contrast Calculator')
    gui.geometry('360x150')

    gui.rowconfigure(0, weight = 0)

    entries = drawEntries()
    drawText(defaultHex)
    fillColor(defaultHex)

    calculateButton = tk.Button(gui, text='Calculate', fg='black', bg='white', command=lambda:calculate(), height=1, width=15)
    calculateButton.grid(sticky='S', row=5, column=8, columnspan = 5)

    randomizeButton = tk.Button(gui, text='Randomize', fg='black', bg='white', command=lambda:randomize(entries), height=1, width=15)
    randomizeButton.grid(sticky='S', row=5, column=2, columnspan = 5)

    increment1 = tk.Button(gui, text='+', fg='black', bg='white', command=lambda:increment(0), height=1, width=1)
    increment1.grid(sticky='W', row=3, column=0)
    increment2 = tk.Button(gui, text='+', fg='black', bg='white', command=lambda:increment(1), height=1, width=1)
    increment2.grid(sticky='W', row=3, column=5)
    increment3 = tk.Button(gui, text='+', fg='black', bg='white', command=lambda:increment(2), height=1, width=1)
    increment3.grid(sticky='W', row=3, column=10)

    decrement1 = tk.Button(gui, text='-', fg='black', bg='white', command=lambda:decrement(0), height=1, width=1)
    decrement1.grid(sticky='E', row=3, column=4)
    decrement2 = tk.Button(gui, text='-', fg='black', bg='white', command=lambda:decrement(1), height=1, width=1)
    decrement2.grid(sticky='E', row=3, column=9)
    decrement3 = tk.Button(gui, text='-', fg='black', bg='white', command=lambda:decrement(2), height=1, width=1)
    decrement3.grid(sticky='E', row=3, column=14)

    gui.mainloop()