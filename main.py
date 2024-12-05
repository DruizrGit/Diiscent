import matplotlib as mpl
from matplotlib import pyplot as plt

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from PIL import Image, ImageTk
from matplotlib import rcParams
import sys
import tkinter as tk
from tkinter import ttk

from dicepool import AttackPool, DefensePool

mpl.use("TkAgg")
plt.style.use("ggplot")

rcParams.update({"figure.autolayout": True})

LARGE_FONT = ("Verdana", 12)


class WinMain(tk.Tk):

    def __init__(self, *args, **kwargs):

        # Inherit tk.Tk methods / properties
        tk.Tk.__init__(self, *args, **kwargs)

        # Aesthetic Properties
        self.height = 760
        self.width = 1000
        tk.Tk.wm_title(self, "Diiscent")
        if sys.platform.startswith("win"):
            tk.Tk.iconbitmap(self, bitmap="Images/descent_icon.ico")
        else:
            self.tk.call('wm', 'iconphoto', self._w, tk.PhotoImage(file="Images/descent_icon.png"))

        tk.Tk.geometry(self, str(self.width) + "x" + str(self.height))
        tk.Tk.resizable(self, width=False, height=False)  # Can't adjust window size

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Dictionary of Frames
        self.frames = {}

        # Initialize MainPage
        frame = MainPage(container, self)
        self.frames[MainPage] = frame
        frame.grid(row=0, column=0, sticky="nsew")

        # Initialize Program on StartPage
        self.show_frame(MainPage)

    def show_frame(self, container):

        # Raise Frame to the Top (Show Frame)
        frame = self.frames[container]
        frame.tkraise()


class MainPage(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)

        # Defining the geometry of the Canvas
        self.centerX = int(controller.width / 2)
        self.centerY = int(controller.height / 2)
        self.quarterY = int(controller.height / 4)
        self.canvas = tk.Canvas(self, width=controller.width, height=controller.height)
        self.canvas.pack()

        # Background Images
        self.woodland_image = ImageTk.PhotoImage(
            Image.open("Images/Woodland.jpg").resize(
                (controller.width, controller.height)
            )
        )
        self.dark_image = ImageTk.PhotoImage(
            Image.open("Images/DarkTheme.jpg").resize(
                (controller.width, controller.height)
            )
        )

        # Menubar
        self.theme_init = 0
        self.theme_mode = 0
        self.theme_var = tk.Variable()
        self.show_menubar(controller)

        # Defining colours and Loading Dice Images
        self.atk_colours = ["Red", "Blue", "Yellow", "Green"]
        self.def_colours = ["Black", "Grey", "Brown"]

        self.atk_dice_images = {}
        self.def_dice_images = {}

        self.dice_cube_images = {}

        self.event_keys = ["Heart", "Range", "Surge"]
        self.atk_colours = ["Red", "Yellow", "Blue", "Green"]

        # Attack and Defense Dice Pool States
        self.atk_state = {
            "Red": [0, []],
            "Blue": [0, []],
            "Yellow": [0, []],
            "Green": [0, []],
        }

        self.def_state = {"Black": [0, []], "Grey": [0, []], "Brown": [0, []]}

        self.heart_max = {"Red": 3, "Blue": 2, "Yellow": 2, "Green": 1}

        self.range_max = {"Red": 0, "Blue": 6, "Yellow": 2, "Green": 1}

        self.heart_min = {"Red": 1, "Blue": 1, "Yellow": 0, "Green": 0}

        self.range_min = {"Red": 0, "Blue": 2, "Yellow": 0, "Green": 0}

        self.attack_pool = 0
        self.defense_pool = 0

        die_dims = (30, 30)
        die_cube_dims = (18, 18)

        # Store Dice Images
        for colour in self.atk_colours:
            self.atk_dice_images[colour] = ImageTk.PhotoImage(
                Image.open("Images/Descent" + colour + "Dice.png").resize(die_dims)
            )
            if colour == "Red":
                self.dice_cube_images[colour] = ImageTk.PhotoImage(
                    Image.open("Images/" + colour + "Cube.png").resize((18, 18))
                )
            else:
                self.dice_cube_images[colour] = ImageTk.PhotoImage(
                    Image.open("Images/" + colour + "Cube.png").resize(die_cube_dims)
                )
        for colour in self.def_colours:
            self.def_dice_images[colour] = ImageTk.PhotoImage(
                Image.open("Images/Descent" + colour + "Dice.png").resize(die_dims)
            )
            if colour == "Brown":
                self.dice_cube_images[colour] = ImageTk.PhotoImage(
                    Image.open("Images/" + colour + "Cube.png").resize((22, 22))
                )
            else:
                self.dice_cube_images[colour] = ImageTk.PhotoImage(
                    Image.open("Images/" + colour + "Cube.png").resize(die_cube_dims)
                )

        # Die Locations
        die_length = 45

        self.atk_x = 90
        self.atk_y = 170
        self.atk_sep = die_length + 20

        self.def_x = 125
        self.def_y = 277
        self.def_sep = die_length + 20

        # Attack Dice Buttons
        self.blue_dice = ImageTk.PhotoImage(
            Image.open("Images/DescentBlueDice.png").resize((die_length, die_length))
        )
        blue_dice_button = tk.Button(
            self,
            image=self.blue_dice,
            bg="blue",
            command=lambda: self.update_atk_dice("Blue", False),
        )
        self.canvas.create_window(
            self.atk_x, self.atk_y, anchor=tk.NW, window=blue_dice_button
        )

        self.yellow_dice = ImageTk.PhotoImage(
            Image.open("Images/DescentYellowDice.png").resize((die_length, die_length))
        )
        yellow_dice_button = tk.Button(
            self,
            image=self.yellow_dice,
            bg="yellow",
            command=lambda: self.update_atk_dice("Yellow", False),
        )
        self.canvas.create_window(
            self.atk_x + self.atk_sep,
            self.atk_y,
            anchor=tk.NW,
            window=yellow_dice_button,
        )

        self.red_dice = ImageTk.PhotoImage(
            Image.open("Images/DescentRedDice.png").resize((die_length, die_length))
        )
        red_dice_button = tk.Button(
            self,
            image=self.red_dice,
            bg="red",
            command=lambda: self.update_atk_dice("Red", False),
        )
        self.canvas.create_window(
            self.atk_x + 2 * self.atk_sep,
            self.atk_y,
            anchor=tk.NW,
            window=red_dice_button,
        )

        self.green_dice = ImageTk.PhotoImage(
            Image.open("Images/DescentGreenDice.png").resize((die_length, die_length))
        )
        green_dice_button = tk.Button(
            self,
            image=self.green_dice,
            bg="green",
            command=lambda: self.update_atk_dice("Green", False),
        )
        self.canvas.create_window(
            self.atk_x + 3 * self.atk_sep,
            self.atk_y,
            anchor=tk.NW,
            window=green_dice_button,
        )

        # Defense Dice Buttons
        self.black_dice = ImageTk.PhotoImage(
            Image.open("Images/DescentBlackDice.png").resize((die_length, die_length))
        )
        black_dice_button = tk.Button(
            self,
            image=self.black_dice,
            bg="black",
            command=lambda: self.update_def_dice("Black", False),
        )
        self.canvas.create_window(
            self.def_x, self.def_y, anchor=tk.NW, window=black_dice_button
        )

        self.grey_dice = ImageTk.PhotoImage(
            Image.open("Images/DescentGreyDice.png").resize((die_length, die_length))
        )
        grey_dice_button = tk.Button(
            self,
            image=self.grey_dice,
            bg="grey",
            command=lambda: self.update_def_dice("Grey", False),
        )
        self.canvas.create_window(
            self.def_x + self.def_sep, self.def_y, anchor=tk.NW, window=grey_dice_button
        )

        self.brown_dice = ImageTk.PhotoImage(
            Image.open("Images/DescentBrownDice.png").resize((die_length, die_length))
        )
        brown_dice_button = tk.Button(
            self,
            image=self.brown_dice,
            bg="brown",
            command=lambda: self.update_def_dice("Brown", False),
        )
        self.canvas.create_window(
            self.def_x + 2 * self.def_sep,
            self.def_y,
            anchor=tk.NW,
            window=brown_dice_button,
        )

        # Roll (Plotting) Button
        self.roll_image = ImageTk.PhotoImage(Image.open("Images/Roll.png"))
        plot_button = tk.Button(
            self,
            image=self.roll_image,
            bg="black",
            takefocus=False,
            command=self.draw_figures,
        )
        self.canvas.create_window(110, 700, anchor=tk.NW, window=plot_button)

        # Reset Pool Button
        self.reset_image = ImageTk.PhotoImage(Image.open("Images/Reset.png"))
        self.reset_button = tk.Button(
            self,
            image=self.reset_image,
            bg="black",
            takefocus=False,
            command=self.clear_pool,
        )
        self.canvas.create_window(240, 700, anchor=tk.NW, window=self.reset_button)

        # Radio Buttons for Atk Figure Types
        self.fig_order_atk = tk.StringVar()

        self.greater_text = ImageTk.PhotoImage(Image.open("Images/Greater.png"))
        greater_check_atk = tk.Radiobutton(
            self,
            image=self.greater_text,
            bg="black",
            var=self.fig_order_atk,
            indicatoron=0,
            value="great",
        )

        self.equal_text = ImageTk.PhotoImage(Image.open("Images/Equal.png"))
        equal_check_atk = tk.Radiobutton(
            self,
            image=self.equal_text,
            bg="black",
            var=self.fig_order_atk,
            indicatoron=0,
            value="exact",
        )

        self.less_text = ImageTk.PhotoImage(Image.open("Images/Less.png"))
        lesser_check_atk = tk.Radiobutton(
            self,
            image=self.less_text,
            bg="black",
            var=self.fig_order_atk,
            indicatoron=0,
            value="less",
        )

        self.canvas.create_window(100, 440, anchor=tk.NW, window=greater_check_atk)
        self.canvas.create_window(100, 475, anchor=tk.NW, window=equal_check_atk)
        self.canvas.create_window(100, 510, anchor=tk.NW, window=lesser_check_atk)

        greater_check_atk.select()

        # Radio Buttons for Def Figure Types
        self.fig_order_def = tk.StringVar()

        greater_check_def = tk.Radiobutton(
            self,
            image=self.greater_text,
            bg="black",
            var=self.fig_order_def,
            indicatoron=0,
            value="great",
        )

        equal_check_def = tk.Radiobutton(
            self,
            image=self.equal_text,
            bg="black",
            var=self.fig_order_def,
            indicatoron=0,
            value="exact",
        )

        lesser_check_def = tk.Radiobutton(
            self,
            image=self.less_text,
            bg="black",
            var=self.fig_order_def,
            indicatoron=0,
            value="less",
        )

        self.canvas.create_window(310, 440, anchor=tk.NW, window=greater_check_def)
        self.canvas.create_window(310, 475, anchor=tk.NW, window=equal_check_def)
        self.canvas.create_window(310, 510, anchor=tk.NW, window=lesser_check_def)

        greater_check_def.select()

        # Hearts / Range Toggle Button
        self.kind_button_mode = 0

        icon_size = 40
        self.melee_icon = ImageTk.PhotoImage(
            Image.open("Images/MeleeIcon40px.png").resize((icon_size, icon_size))
        )
        self.range_icon = ImageTk.PhotoImage(
            Image.open("Images/RangeIcon40px.png").resize((icon_size, icon_size))
        )

        self.kind_button = tk.Button(
            self, image=self.melee_icon, command=self.toggle_dmg_range, border=0
        )
        self.canvas.create_window(360, 365, anchor=tk.NW, window=self.kind_button)

        # Little Figure Dice Frames
        self.atk_die_frame = tk.LabelFrame(self, borderwidth=0)
        self.canvas.create_window(950, 370, anchor=tk.NE, window=self.atk_die_frame)

        self.def_die_frame = tk.LabelFrame(self, borderwidth=0)
        self.canvas.create_window(950, 690, anchor=tk.NE, window=self.def_die_frame)

    def show_menubar(self, controller):

        self.menubar = tk.Menu(controller)

        self.viewtab = tk.Menu(self.menubar, tearoff=0)
        self.viewtab.add_checkbutton(
            label="Woodland Theme",
            onvalue=0,
            offvalue=0,
            var=self.theme_var,
            command=self.toggle_theme,
        )
        self.viewtab.add_checkbutton(
            label="Dark Theme",
            onvalue=1,
            offvalue=1,
            var=self.theme_var,
            command=self.toggle_theme,
        )
        self.viewtab.invoke(self.viewtab.index("Woodland Theme"))
        self.menubar.add_cascade(label="View", menu=self.viewtab)

        self.theme_init = 1

        self.helptab = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Help", menu=self.helptab)
        self.helptab.add_command(
            label="Dice Breakdown", command=lambda: self.show_dice_breakdown(controller)
        )

        controller.config(menu=self.menubar)

    def toggle_theme(self):

        prev_theme = self.theme_mode
        current_theme = int(self.theme_var.get())

        if self.theme_init == 1:
            if prev_theme == current_theme:
                pass
            elif current_theme == 0:
                self.canvas.create_image(0, 0, image=self.woodland_image, anchor=tk.NW)
            else:
                self.canvas.create_image(0, 0, image=self.dark_image, anchor=tk.NW)
        else:
            if current_theme == 0:
                self.canvas.create_image(0, 0, image=self.woodland_image, anchor=tk.NW)
            else:
                self.canvas.create_image(0, 0, image=self.dark_image, anchor=tk.NW)

        self.theme_mode = int(self.theme_var.get())

    def show_dice_breakdown(self, controller):

        win = tk.Toplevel(controller)
        win.title("Dice Breakdown")
        if sys.platform.startswith("win"):
            win.iconbitmap("Images/descent_icon.ico")
        else:
            win.iconphoto(True, tk.PhotoImage(file="Images/descent_icon.png"))

        win.resizable(width=False, height=False)

        self.dicebreakdown_image = ImageTk.PhotoImage(
            Image.open("Images/DiceBreakdown.png")
        )
        label = tk.Label(win, image=self.dicebreakdown_image)
        label.pack()

    def draw_figures(self):

        if self.total_atk() != 0:

            if self.kind_button_mode == 0:
                self.draw_atk_probs(kind="Heart", measure=self.fig_order_atk.get())
                self.clear_atk_graph_dice()
                self.draw_atk_graph_dice()
            else:
                self.draw_atk_probs(kind="Range", measure=self.fig_order_atk.get())
                self.clear_atk_graph_dice()
                self.draw_atk_graph_dice()

        if self.total_def() != 0:

            self.draw_def_probs(measure=self.fig_order_def.get())
            self.clear_def_graph_dice()
            self.draw_def_graph_dice()

    def text_size(self, bars, kind):
        """
        Function computes the text size for the the percentile text above the rectangulur
        bars in the figures as well as the text size for the x-tick labels.

        """
        if kind == "bar_text":
            if bars <= 4:
                return 11
            elif bars <= 7:
                return 10
            elif bars <= 10:
                return 9
            elif bars <= 13:
                return 8
            elif bars <= 17:
                return 7.5
            elif bars <= 21:
                return 6.5
            elif bars <= 24:
                return 6
            elif bars <= 28:
                return 5
            else:
                return 4
        else:
            if bars <= 20:
                return 8
            elif bars <= 25:
                return 7
            elif bars <= 30:
                return 6
            elif bars <= 35:
                return 5
            else:
                return 4

    def draw_atk_probs(self, kind="Heart", measure="great"):

        atk_pool = AttackPool()

        for colour in self.atk_colours:
            atk_pool.atk_state[colour] = self.atk_state[colour][0]

        graph_fig = Figure(figsize=(5, 3), dpi=100)
        graph = graph_fig.add_subplot(1, 1, 1)

        probs = []

        if measure == "exact":
            str_kind = "exactly"
        elif measure == "great":
            str_kind = "at least"
        else:
            str_kind = "less than"

        if kind == "Heart":

            maxh = atk_pool.max_heart()

            # Construct Values and Include Misses (if necessary)
            if atk_pool.atk_state["Blue"] != 0:
                probs.append(atk_pool.event_select("Miss")["Prob"] * 100)

                # Construct Values
                x_axis = [i for i in range(maxh + 2)]
                values = [i - 1 for i in range(maxh + 2)]
                values[0] = "><"
            else:
                x_axis = [i for i in range(maxh + 1)]
                values = [str(i) for i in range(maxh + 1)]

            for val in range(maxh + 1):
                probs.append(
                    atk_pool.event_select(heart_val=val, heart_measure=measure)["Prob"]
                    * 100
                )

            print(values)
            print(probs)

            bar = graph.bar(x=x_axis, height=probs)
            bars = len(bar)
            bar_text_size = self.text_size(bars, "bar_text")
            xtick_text_size = self.text_size(bars, "xticks")

            ind = 0

            for rect in bar:
                height = rect.get_height()
                graph.text(
                    rect.get_x() + rect.get_width() / 2,
                    height,
                    str(atk_pool.fraction_rounder(probs[ind])),
                    ha="center",
                    va="bottom",
                    size=bar_text_size,
                )
                ind += 1

            graph.set_xlabel("Hearts (x)")
            graph.set_ylabel("Probability (%)")
            graph.set_xticks(x_axis)
            graph.set_xticklabels(labels=values, size=xtick_text_size)
            graph.set_title(
                "Probability of Rolling " + str_kind + " x Hearts", y=1.08, size=12
            )
            graph.set_ylim(0, 100)

        else:

            maxr = atk_pool.max_range()

            if atk_pool.atk_state["Blue"] != 0:
                probs.append(atk_pool.event_select(heart_val="Miss")["Prob"] * 100)

                # Construct Values
                x_axis = [i for i in range(maxr + 2)]
                values = [i - 1 for i in range(maxr + 2)]
                values[0] = "><"
            else:
                x_axis = [i for i in range(maxr + 1)]
                values = [str(i) for i in range(maxr + 1)]

            for val in range(maxr + 1):
                probs.append(
                    atk_pool.event_select(range_val=val, range_measure=measure)["Prob"]
                    * 100
                )

            print(values)
            print(probs)

            bar = graph.bar(x=x_axis, height=probs)
            bars = len(bar)
            bar_text_size = self.text_size(bars, "bar_text")
            xtick_text_size = self.text_size(bars, "xticks")

            ind = 0

            for rect in bar:
                height = rect.get_height()
                graph.text(
                    rect.get_x() + rect.get_width() / 2,
                    height,
                    str(atk_pool.fraction_rounder(probs[ind])),
                    ha="center",
                    va="bottom",
                    size=bar_text_size,
                )
                ind += 1

            graph.set_xlabel("Range (x)")
            graph.set_ylabel("Probability (%)")
            graph.set_xticks(x_axis)
            graph.set_xticklabels(labels=values, size=xtick_text_size)
            graph.set_title(
                "Probability of Rolling " + str_kind + " x Range", y=1.08, size=12
            )
            graph.set_ylim(0, 100)

        figure_canvas = tk.Canvas(self.canvas, width=200, height=200)
        self.canvas.create_window(460, 100, anchor=tk.NW, window=figure_canvas)

        fig_canvas = FigureCanvasTkAgg(graph_fig, master=figure_canvas)
        fig_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        fig_canvas.draw()

    def draw_atk_graph_dice(self):

        counter = 0

        for colour in self.atk_colours:

            for die in range(self.atk_state[colour][0]):

                atk_die_label = tk.Label(
                    self.atk_die_frame, image=self.dice_cube_images[colour]
                )
                atk_die_label.grid(row=0, column=counter)
                counter += 1

    def clear_atk_graph_dice(self):

        for die in self.atk_die_frame.winfo_children():
            die.destroy()

    def draw_def_probs(self, measure="great"):

        def_pool = DefensePool()

        for colour in self.def_colours:
            def_pool.def_state[colour] = self.def_state[colour][0]

        graph_fig = Figure(figsize=(5, 3), dpi=100)
        graph = graph_fig.add_subplot(1, 1, 1)

        probs = []

        if measure == "exact":
            str_kind = "exactly"
        elif measure == "great":
            str_kind = "at least"
        else:
            str_kind = "less than"

        maxs = def_pool.max_shield()

        # Construct Values
        x_axis = [i for i in range(maxs + 1)]
        values = [str(i) for i in range(maxs + 1)]

        for val in range(maxs + 1):
            probs.append(
                def_pool.event_select(shield_val=val, shield_measure=measure)["Prob"]
                * 100
            )

        print(values)
        print(probs)

        bar = graph.bar(x=x_axis, height=probs)
        bars = len(bar)
        bar_text_size = self.text_size(bars, "bar_text")
        xtick_text_size = self.text_size(bars, "xticks")

        ind = 0

        for rect in bar:
            height = rect.get_height()
            graph.text(
                rect.get_x() + rect.get_width() / 2,
                height,
                str(def_pool.fraction_rounder(probs[ind])),
                ha="center",
                va="bottom",
                size=bar_text_size,
            )
            ind += 1

        graph.set_xlabel("Shields (x)")
        graph.set_ylabel("Probability (%)")
        graph.set_xticks(x_axis)
        graph.set_xticklabels(labels=values, size=xtick_text_size)
        graph.set_title(
            "Probability of Rolling " + str_kind + " x Shield", y=1.08, size=12
        )
        graph.set_ylim(0, 100)

        figure_canvas = tk.Canvas(self.canvas, width=200, height=200)
        self.canvas.create_window(460, 420, anchor=tk.NW, window=figure_canvas)

        fig_canvas = FigureCanvasTkAgg(graph_fig, master=figure_canvas)
        fig_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        fig_canvas.draw()

    def draw_def_graph_dice(self):

        counter = 0

        for colour in self.def_colours:

            for die in range(self.def_state[colour][0]):

                def_die_label = tk.Label(
                    self.def_die_frame, image=self.dice_cube_images[colour]
                )
                def_die_label.grid(row=0, column=counter)
                counter += 1

    def clear_def_graph_dice(self):

        for die in self.def_die_frame.winfo_children():
            die.destroy()

    def toggle_dmg_range(self):

        if self.kind_button_mode == 0:
            self.kind_button.configure(image=self.range_icon)
            self.kind_button_mode = 1
            self.draw_figures()
        else:
            self.kind_button.configure(image=self.melee_icon)
            self.kind_button_mode = 0
            self.draw_figures()

    def update_atk_dice(self, colour, delete):

        if delete:
            print("\n" + colour + "\n")
            self.atk_state[colour][0] -= 1
            print(self.total_atk())

            if self.total_atk() == 0:
                self.clear_atk_pool()
                self.attack_pool.destroy()
                return 0
        else:

            if self.total_atk() == 7:
                return 0
            else:
                self.atk_state[colour][0] += 1

                if self.total_atk() == 1:
                    self.create_atk_pool()
                else:
                    pass

        self.clear_atk_pool()
        self.create_atk_buttons()
        self.display_atk_pool()
        self.draw_atk_dice()

    def create_atk_pool(self):

        self.attack_pool = tk.LabelFrame(self)
        self.canvas.create_window(95, 590, anchor=tk.NW, window=self.attack_pool)

    def create_atk_buttons(self):

        for colour in self.atk_colours:

            for dice in range(self.atk_state[colour][0]):

                self.atk_state[colour][1].append(
                    tk.Button(
                        self.attack_pool,
                        image=self.atk_dice_images[colour],
                        padx=5,
                        pady=5,
                        bg=colour,
                        command=lambda colour=colour: self.update_atk_dice(
                            colour, True
                        ),
                    )
                )

            print(colour + ":" + str(self.atk_state[colour][1]))

    def draw_atk_dice(self):

        counter = 0
        print("\n")

        for colour in self.atk_colours:

            num_dice = self.atk_state[colour][0]
            print(colour + ":" + str(num_dice))

            for dice in range(num_dice):

                self.atk_state[colour][1][dice].grid(row=0, column=counter)
                counter += 1

        print("\n")

    def clear_atk_pool(self):

        for colour in self.atk_colours:

            for button in self.atk_state[colour][1]:
                button.destroy()

            self.atk_state[colour][1] = []

    def update_def_dice(self, colour, delete):

        if delete:
            print("\n" + colour + "\n")
            self.def_state[colour][0] -= 1
            print(self.total_def())

            if self.total_def() == 0:
                self.clear_def_pool()
                self.defense_pool.destroy()
                return 0
        else:

            # Max 7 Dice in Pool
            if self.total_def() == 7:
                return 0
            else:
                self.def_state[colour][0] += 1

                if self.total_def() == 1:
                    self.create_def_pool()
                else:
                    pass

        self.clear_def_pool()
        self.create_def_buttons()
        self.display_def_pool()
        self.draw_def_dice()

    def create_def_pool(self):

        self.defense_pool = tk.LabelFrame(self)
        self.canvas.create_window(95, 635, anchor=tk.NW, window=self.defense_pool)

    def create_def_buttons(self):

        for colour in self.def_colours:

            for dice in range(self.def_state[colour][0]):

                self.def_state[colour][1].append(
                    tk.Button(
                        self.defense_pool,
                        image=self.def_dice_images[colour],
                        bg=colour,
                        command=lambda colour=colour: self.update_def_dice(
                            colour, True
                        ),
                    )
                )

            print(colour + ":" + str(self.def_state[colour][1]))

    def draw_def_dice(self):

        counter = 0
        print("\n")

        for colour in self.def_colours:

            num_dice = self.def_state[colour][0]
            print(colour + ":" + str(num_dice))

            for dice in range(num_dice):

                self.def_state[colour][1][dice].grid(row=0, column=counter)
                counter += 1

        print("\n")

    def clear_def_pool(self):

        for colour in self.def_colours:

            for button in self.def_state[colour][1]:
                button.destroy()

            self.def_state[colour][1] = []

    def total_atk(self):

        total = 0
        for colour in self.atk_colours:
            total += self.atk_state[colour][0]

        return total

    def total_def(self):

        total = 0
        for colour in self.def_colours:
            total += self.def_state[colour][0]

        return total

    def clear_pool(self):

        # Clears the entire Atk and Def Dice Pool

        if self.total_atk() != 0:

            self.clear_atk_pool()

            for colour in self.atk_colours:
                self.atk_state[colour][0] = 0

            self.attack_pool.destroy()

        if self.total_def() != 0:

            self.clear_def_pool()

            for colour in self.def_colours:
                self.def_state[colour][0] = 0

            self.defense_pool.destroy()

    def display_atk_pool(self):

        print(self.attack_pool.winfo_children())

    def display_def_pool(self):

        print(self.defense_pool.winfo_children())


root = WinMain()
root.mainloop()
