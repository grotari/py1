import tkinter as tk
from tkinter import filedialog
import PyPDF2
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import string
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import codecs
import numpy as np
import pandas as pd
import csv
import os


# nltk.download('punkt')
# nltk.download('stopwords')

class Application(tk.Frame):
    """ BookShelf App provides a platform for data scientists aimed at empirical text analysis
    input files are to found in input folder
    output images and texts are placed in output folder """

    def __init__(self, master, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.grid()
        self.root = master
        self.list_books = []
        self.page_content = ''
        self.text_box = None

        canvas = tk.Canvas(self.root, width=600, height=300)
        canvas.grid(columnspan=3, rowspan=3, padx=20)

        logo = Image.open('input/icon/icon2.png')
        logo = logo.resize((275, 121), Image.ANTIALIAS)
        logo = ImageTk.PhotoImage(logo)  # convert pillow image into TK image
        logo_label = tk.Label(image=logo)  # place the logo into a logo widget
        logo_label.image = logo
        logo_label.grid(column=1, row=1)

        label = tk.Label(self.root, text="Search the book", font=('Cambria', 25))
        label.grid(column=1, row=2, sticky='nsew')

        self.select_menu()
        select_book_menu = tk.OptionMenu(self.root, select_var, *self.list_books, command=self.select_book)
        select_book_menu.grid(row=3, column=1, sticky='nsew')

        # Create a new button Frame
        button_frame = tk.Frame(self.root, padx=20)
        button_frame.grid(row=4, column=2)

        browse_btn = tk.Button(button_frame, textvariable=browse_text, activeforeground="#D0A83A",
                               command=self.open_file)
        browse_btn.grid(sticky='nsew')
        get_text_button = tk.Button(button_frame, text='Save File', activeforeground="#D0A83A",
                                    command=self.save_txt)
        get_text_button.grid(sticky='nsew')
        clear_button = tk.Button(button_frame, text='Clear Text', activeforeground="red", command=self.clear_text)
        clear_button.grid(sticky='nsew')
        wordcloud_button = tk.Button(button_frame, text='WordCloud', activeforeground="#D0A83A",
                                     command=self.wordcloud_create)
        wordcloud_button.grid(sticky='nsew')
        stats_button = tk.Button(button_frame, text="Stats", activeforeground="#D0A83A", command=self.stats)
        stats_button.grid(sticky='nsew')
        emo_tokens_button = tk.Button(button_frame, text='Fit', activeforeground="#D0A83A", command=self.emo_w_tokens)
        emo_tokens_button.grid(sticky='nsew')
        emo_dens_button = tk.Button(button_frame, text='Scatter', activeforeground="#D0A83A", command=self.emo_dens)
        emo_dens_button.grid(sticky='nsew')
        button = tk.Button(button_frame, text="Quit", command=self.quit, activeforeground="red")
        button.grid(sticky='nsew')

        canvas2 = tk.Canvas(self.root, width=600, height=50)
        canvas2.grid(columnspan=3)

    def open_file(self):
        browse_text.set("loading...")
        file = filedialog.askopenfile(parent=self.root,
                                      initialdir="input/corpus",
                                      mode='rb', title="Choose a file",
                                      filetypes=(("Pdf files", "*.pdf"), ("All files", "*.*")))
        pdf_file_path.set(file)
        if file:
            read_pdf = PyPDF2.PdfFileReader(file)  # create a pdf reader object
            for i in range(0, read_pdf.numPages):
                pageObj = read_pdf.getPage(i)  # create a page object
                self.page_content = self.page_content + pageObj.extractText()  # extracting text from page
                self.display_text()
            return self.page_content

    def display_text(self):
        browse_text.set("Browse")
        self.text_box = tk.Text(self.root, height=10, width=50, padx=15, pady=15, wrap="word", font=("Arial", 14))
        self.text_box.insert(1.0, self.page_content)
        self.text_box.tag_configure("left", justify="left", spacing2=10)
        self.text_box.tag_add("left", 1.0, "end")
        self.text_box.grid(column=1, row=4, sticky='nsew')
        s = tk.Scrollbar(self.root, orient=tk.VERTICAL, command=self.text_box.yview)
        s.grid(column=2, row=4, sticky='nsw')
        self.text_box['yscrollcommand'] = s.set

    def select_menu(self):
        select_var.set("Select book")
        self.list_books = ['Die Wassernixe von Jacob und Wilhelm Grimm',
                           'The old Man and his Grandson by J. and W. Grimm, transl. M. Hunt',
                           'The Master Cat by Charles Perrault',
                           'The Raven by Giambattista Basile']

    def select_book(self, value=None):
        if value == 'Die Wassernixe von Jacob und Wilhelm Grimm':
            print("You selected: Grimm, Jacob und Wilhelm Grimm. \x1B[3mDie Wassernixe\x1B[0m. Kinder- und "
                  "Hausmärchen, \n7. Aufl. Bd. 2. Göttingen, 1857, S. 451.")
            file = ("input/corpus/die-wassernixe.txt")
        elif value == 'The old Man and his Grandson by J. and W. Grimm, transl. M. Hunt':
            print("You selected: Grimm, Jacob, Alfred W. Hunt, and Wilhelm Grimm. \x1B[3mThe old Man and his "
                  "Grandson\x1B[0m. \nGrimm's Household Tales: With the Author's Notes; trans. from the German and "
                  "\nEdited by Margaret Hunt; with an Introd. by Andrew Lang. Detroit: Singing Tree Press, 1968.")
            file = ('input/corpus/the-old-man-and-his-grandson.txt')
        elif value == 'The Master Cat by Charles Perrault':
            print("You selected: Charles Perrault. \x1B[3mThe Master Cat\x1B[0m. The Fairy Tales of Charles Perrault, "
                  "\net al., trans. by Robert Samber and J. E. Mansion, Illustrated by Harry Clarke, 2009.")
            file = ("input/corpus/master-cat.txt")
        elif value == 'The Raven by Giambattista Basile':
            print("You selected: Basile, Giambattista, Laura Ross, and Beni Montresor. \x1B[3mThe Raven\x1B[0m. Old "
                  "\nNeapolitan Fairy Tales. New York: Knopf, 1963.")
            file = ("input/corpus/raven.txt")
        with open(file, 'r', encoding='utf-8') as f:
            self.page_content = f.read()
            self.display_text()
            f.close()

    def save_txt(self):
        text_file = filedialog.asksaveasfilename(initialdir="output/texts", title="Save File",
                                                 filetypes=(("Text Files", "*.txt"), ("All Files", "*.*")))
        text_file = open(text_file, 'w', encoding="utf-8")
        text_file.write(self.text_box.get('1.0', 'end'))

    def clear_text(self):
        print(self.text_box)
        self.text_box.delete('1.0', tk.END)

    def wordcloud_create(self):
        data1 = self.page_content.translate(str.maketrans('', '', string.punctuation)).lower()  # remove punctuation
        data2 = " ".join(data1.split())  # remove additional whitespace from text

        stops = set(stopwords.words('english'))
        # stops = set(stopwords.words('german'))  # call the in-built German stopword list in NLTK

        # define word cloud layout
        wordcloud = WordCloud(width=750, height=750,
                              background_color='white',
                              max_words=300,
                              stopwords=stops,
                              min_font_size=12).generate(data2)

        # plot the WordCloud image
        plt.figure(figsize=(7.5, 7.5), facecolor=None)
        plt.imshow(wordcloud, interpolation="bilinear")  # image displayed more smoothly
        plt.axis("off")
        plt.tight_layout(pad=10)

        plt.show(block=False)
        wordcloud.to_file("output/img/wordcloud_frequencies.png")

    def stats(self):
        self.clear_text()
        dataframe = pd.read_csv('input/data_set/emo-python-project-eng-small.csv', delimiter=";")
        dataframe.drop(dataframe.columns[13], axis=1, inplace=True)
        self.text_box.insert(1.0, f"{(dataframe.isnull().values.any())} \n{(dataframe.describe().round(1))}")
        print(f"{(dataframe.isnull().values.any())} \n{(dataframe.describe().round(1))}")

    def emo_w_tokens(self):
        df = pd.read_csv('input/data_set/emo-python-project-eng-small.csv', delimiter=";")

        y = df.iloc[:, 11].values
        x = df.iloc[:, 12].values

        plt.style.use('seaborn')
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.scatter(x, y)
        ax.set_xlabel("Number of Tokens per Text")
        ax.set_ylabel("Number of Emotion Words per Text")
        ax.set_title("Emotion / Tokens")
        ax.tick_params(axis="both", which="minor", labelsize=10)
        plt.savefig('output/img/emotion_words_tokens.png')
        plt.show()

    def emo_dens(self):
        fig, ax1 = plt.subplots(figsize=(8.5, 6.5))
        ax1.set_title('Emotion Density of each text')
        ax1.set_ylabel("Frequency")

        b_emo_freq = np.array([1.33, 2.64, 1.06, 1.63, 2.40, 1.66, 2.57])
        b_emo = np.array(["Anger", "Anticipation", "Disgust", "Fear", "Joy", "Sadness", "Trust"])

        ax1.plot(b_emo, b_emo_freq, '--b', marker='o', markerfacecolor='w')

        for i, j in zip(b_emo, b_emo_freq):
            ax1.annotate(str(j), xy=(i, j), ha="center", color="b", textcoords="offset points", xytext=(0, 10))

        ax1.grid(which='major', color='green', linestyle='--', linewidth=0.5)
        ax1.set(ylim=(0.8, 3))

        ax1.legend(['Emotion Density'])
        plt.savefig('output/img/emotion_density_eng_texts.png')
        plt.show()

    def quit(self):
        self.root.quit()


root = tk.Tk()
pdf_file_path = tk.StringVar()
browse_text = tk.StringVar()
browse_text.set("Browse")
select_var = tk.StringVar()

app = Application(master=root)
app.master.title('BS')
app.select_menu()

app.mainloop()
