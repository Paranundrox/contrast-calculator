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
            entry = tk.Entry(gui, width = 5)
            entry.insert('insert', defaultHex[(2*i+1):(2*i+3)])
            entry.grid(sticky='S', row=3, column=(i))
            entries.append(entry)
        return(entries)

    def drawText(hexcode):
        lightMode = tk.Label(gui, height=1, width=15, background=light, foreground = hexcode, anchor='center', padx=1, pady=1, text='text in light mode')
        lightMode.grid(row = 5, column = 0)

        darkMode = tk.Label(gui, height=1, width=15, background=dark, foreground = hexcode, anchor='center', padx=1, pady=1, text='text in dark mode')
        darkMode.grid(row = 5, column = 1)

        amoledMode = tk.Label(gui, height=1, width=15, background=amoled, foreground = hexcode, anchor='center', padx=1, pady=1, text='text in amoled mode')
        amoledMode.grid(row = 5, column = 2)

        lightModeContrast = tk.Label(gui, height=1, width=15, background=light, foreground = '#000000', anchor='center', padx=1, pady=1, text='{0:,.2f}'.format(contrast(hexcode, light)))
        lightModeContrast.grid(row = 6, column = 0)
    
        darkModeContrast = tk.Label(gui, height=1, width=15, background=light, foreground = '#000000', anchor='center', padx=1, pady=1, text='{0:,.2f}'.format(contrast(hexcode, dark)))
        darkModeContrast.grid(row = 6, column = 1)
    
        amoledModeContrast = tk.Label(gui, height=1, width=15, background=light, foreground = '#000000', anchor='center', padx=1, pady=1, text='{0:,.2f}'.format(contrast(hexcode, amoled)))
        amoledModeContrast.grid(row = 6, column = 2)

    def calculate():
        elements = ['#', entries[0].get(), entries[1].get(), entries[2].get()]
        combinedHex = ''.join(elements)

        drawText(combinedHex)

    def updateEntries(hexcode):
        for i, entry in enumerate(entries):
            entry.delete('0', 'end')
            entry.insert('insert', hexcode[(2*i+1):(2*i+3)])
        


    def randomize(entries):
        defaultHex = random.choice(contrastPass)
        drawText(defaultHex)
        updateEntries(defaultHex)


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
    gui.geometry('400x200')

    entries = drawEntries()
    drawText(defaultHex)

    calculateButton = tk.Button(gui, text='Calculate', fg='black', bg='white', command=lambda:calculate(), height=1, width=15)
    calculateButton.grid(sticky='S', row=4, column=1)

    randomizeButton = tk.Button(gui, text='Randomize', fg='black', bg='white', command=lambda:randomize(entries), height=1, width=15)
    randomizeButton.grid(sticky='S', row=4, column=0)
    gui.mainloop()