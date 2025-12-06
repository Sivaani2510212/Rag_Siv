import tkinter as tk

# ============================================================
# CLEARS WINDOW: Removes Unnecessary Widgets to go to the next stage
# ============================================================
def clear_middle_screen():
    for widget in main_frame.winfo_children():
        widget.pack_forget()
        widget.place_forget()

# ============================================================
# VIRTUAL KEYBOARD: Creates a virtual usable keyboard
# ============================================================
def keyboard():
    global active_key_handler, keyboard_frame, key_buttons, row_frame

    keyboard_frame = tk.Frame(root,bg=theme["main_bg"])
    keyboard_frame.pack(side="bottom", pady=15)

    layout = ["1234567890", "QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"]

    for row in layout:
        row_frame = tk.Frame(keyboard_frame, bg=theme["main_bg"])
        row_frame.pack()
        for ch in row:
            btn = tk.Button(row_frame,text=ch,width=4,height=2,command=lambda ch=ch: active_key_handler(ch),fg="#000000")
            btn.pack(side="left", padx=3, pady=3)
            key_buttons[ch] = btn

    space_btn = tk.Button(keyboard_frame, text="SPACE",width=40, height=2,command=lambda: active_key_handler(" "),fg="#000000")
    space_btn.pack(pady=5)

        
# ============================================================
# RULES: Explains the game rules and points system
# ============================================================
def next_button_fn(event=None):        
    for w in rules_frame.winfo_children():      #All widgets under the rules frame is destroyed
        w.destroy()
    rules_frame.pack_forget()       #Rules frame is forgotten(not destroyed, to be repacked if game is restarted)
    main_frame.pack(side="top", fill="both", expand=True)       #Packed later
    players()
    keyboard()

def rules_fn():        #Displays rules with colour formatting for highlighted key words 
    global rules_frame

    for w in rules_frame.winfo_children():      #Clear previous widgets
        w.destroy()

    txt = tk.Text(rules_frame, font=("Arial", 20), wrap="word", bg=theme["rules_bg"],fg=theme["text_fg"],bd=0, height=17)
    txt.pack(padx=20, pady=20)

    txt.tag_configure("header1", foreground=theme["rules_header"], font=("Arial",40, "bold"),justify="center")
    txt.tag_configure("header2", foreground=theme["rules_header"], font=("Arial",24, "bold"))
    txt.tag_configure("colour1", font=("Arial", 20), foreground=theme["rules_colour1"])
    txt.tag_configure("colour2", font=("Arial", 20, "bold"), foreground=theme["rules_colour2"])
    txt.tag_configure("colour3", font=("Arial", 20, "bold"), foreground=theme["rules_colour3"])
    txt.tag_configure("colour4", font=("Arial", 20), foreground=theme["rules_colour4"])

    txt.insert("end","\n\n")
    txt.insert("end", "WELCOME TO HANGMAN\n\n", "header1")
    txt.insert("end","\n")
    txt.insert("end", "The aim of the game is to find the word with the least number of guesses.\n"
                      "You may either ")
    txt.insert("end", "guess a letter", "colour1")
    txt.insert("end", " or attempt the ")
    txt.insert("end", "full word.\n\n", "colour1")

    txt.insert("end", "Rules:\n", "header2")

    txt.insert("end", "1. Each round has a maximum of ")
    txt.insert("end", "50 points", "colour2")
    txt.insert("end", ", awarded only if the word is guessed in its ")
    txt.insert("end", "entireity", "colour4")
    txt.insert("end", " on the ")
    txt.insert("end", "first attempt.\n", "colour4")

    txt.insert("end", "2. Each letter guessed costs ")
    txt.insert("end", "1 point ", "colour3")
    txt.insert("end", "(if correct) and ")
    txt.insert("end", "3 points ", "colour3")
    txt.insert("end", "(if incorrect).\n")

    txt.insert("end", "3. Guessing the full word incorrectly results in a penalty of ")
    txt.insert("end", "7 points.\n", "colour3")

    txt.insert("end", "4. All deductions apply from a maximum of ")
    txt.insert("end", "40", "colour2")
    txt.insert("end", " (letter guesses) or ")
    txt.insert("end", "50", "colour2")
    txt.insert("end", " (word guesses only).\n")

    txt.insert("end"," All letters are shown as spaces whereas numbers and special characters are revealed.")

    txt.config(state="disabled")

    next_button = tk.Button(rules_frame, text="Next", font=("Arial", 20,"bold"), command=next_button_fn,bg=theme["button_bg"],fg=theme["button_fg"],width=8,height=1)
    next_button.pack()
    next_button.focus_set()
    root.bind("<Return>", next_button_fn)       #Allows enter to be an input and calls next_button_fn


# ============================================================
# PLAYER ENTRY: Gets number of players and their names
# ============================================================
def players(event=None):
    global player_label, player_entry, player_btn
    global name_entries, name_labels, num_players, active_key_handler

    name_entries.clear()
    num_players = None
    active_key_handler = on_key_press1      #Allows entry of virtual keyboard to player_entry 

    player_label = tk.Label(main_frame, text="Enter Number Of Players:", font=("Arial", 15,"bold"),bg=theme["main_bg"],fg=theme["text_fg"])
    player_label.pack(pady=20)

    player_entry = tk.Entry(main_frame,font=("Arial", 15),width=23)
    player_entry.pack(pady=5)
    player_entry.focus_set()        #Sets cursor to player_entry

    player_btn = tk.Button(main_frame, text="OK",font=("Arial", 12,"bold"),command=save_players,bg=theme["button_bg"],fg=theme["button_fg"],width=5,height=1)
    player_btn.pack(pady=5)
    root.bind("<Return>", save_players)        #Allows enter to be an input and calls save_players

def set_handler(h):
    global active_key_handler
    active_key_handler = h

def save_players(event=None):
    global num_players, name_entries, name_handlers, theme
    global player_entry, player_label, player_btn, active_key_handler, player_list,restart_game_btn, toggle_theme_btn
    global keyboard_frame, restarted

    if num_players is None:
        value = player_entry.get().strip()      #Gets the input of the number of players

        if not value.isdigit():
            invalid_entry = tk.Label(main_frame, text="Enter a valid number",font=("Arial", 20),bg=theme["main_bg"], fg=theme["error"])
            invalid_entry.pack(pady=10)
            invalid_entry.after(1000, lambda: invalid_entry.pack_forget())
            return

        num_players = int(value)

        if num_players == 0:      #Condition to dismiss number of players as 0
            invalid_entry = tk.Label(main_frame, text="Number of players cannot be 0",font=("Arial", 20),bg=theme["main_bg"], fg=theme["error"])
            player_entry.delete(0, tk.END)
            invalid_entry.pack(pady=10)
            invalid_entry.after(1000, lambda: invalid_entry.pack_forget())
            return

        if num_players == 1:        #Condition to dismiss number of players as 1
            show_msg("This Is Not A One Player Game. Go Get A Friend :(", colour=theme["error"])
            toggle_theme_btn.place_forget()
            keyboard_frame.destroy()
            player_label.destroy()
            player_entry.destroy()
            player_btn.destroy()
            root.after(3000, root.destroy)
            return

        player_label.pack_forget()
        player_entry.pack_forget()
        player_btn.pack_forget()        #Clears all entry fields and labels of players

        name_entries = []
        name_handlers = []

        for i in range(1, num_players + 1):        #Entries for getting name of players
            lbl = tk.Label(main_frame, text=f"Enter Name Of Player {i}:",font=("Arial", 15, "bold"),bg=theme["main_bg"], fg=theme["text_fg"])
            lbl.pack(pady=5)

            entry = tk.Entry(main_frame, width=40, font=("Arial", 15))
            entry.pack()

            if i == 1:      #Sets cursor to entry of first name
                entry.focus_set()

            handler = make_handler(entry)
            name_entries.append(entry)      #Appends the name to name list
            name_handlers.append(handler)

            entry.bind("<FocusIn>", lambda e, h=handler: set_handler(h))        

        active_key_handler = name_handlers[0]

        player_btn = tk.Button(main_frame, text="Confirm Players",font=("Arial", 15, "bold"),command=save_players,bg=theme["button_bg"], fg=theme["button_fg"],width=13, height=1)
        player_btn.pack(pady=15)
        root.bind("<Return>", save_players) #Allows enter to be an input and calls save_players
        return
    

    player_list.clear()

    for entry in name_entries:
        name = entry.get().strip()
        if name != "":
            points_storage[name] = []       #Adds names to dictionary to then store points
            player_list.append(name)        #Adds names to list to process the correct order of word giver and guesser

    if len(player_list) != num_players:        #Condition to catch error of not entering all players names
        error_lbl = tk.Label(main_frame,
                             text='Not all player names were entered\nIf you want to play with a different number of players than entered click on "Restart Game"',
                             font=("Arial", 20),bg=theme["main_bg"],fg=theme["error"])
        error_lbl.pack(pady=10)
        restart_game_btn.place(relx=0.0, rely=0.0, anchor="nw")
        restarted = True        #Allows restarting of game to then edit number of players
        error_lbl.after(1500, lambda: error_lbl.pack_forget())
        return

    clear_middle_screen()
    keyboard_frame.pack_forget()
    
    for entry in name_entries:
        entry.pack_forget()
    player_btn.pack_forget()        #Removes all buttons created 

    giver_index = 0
    guesser_index = (giver_index + 1) % len(player_list)        #Initiallizes giver and guesser index to start the game

    prestart()


# ============================================================
# CHANGE THEME: Allows user to change between light and dark mode
# ============================================================
def toggle_theme():         
    global theme

    if theme is light_theme:
        theme = dark_theme
    else:
        theme = light_theme

    root.config(bg=theme["main_bg"])
    main_frame.config(bg=theme["main_bg"])
    rules_frame.config(bg=theme["rules_bg"])        #Sets themes to frames

    toggle_theme_btn.config(bg=theme["button_bg"], fg=theme["button_fg"])       #Sets themes to toggle_theme_btn
    
    for widget in main_frame.winfo_children():        #Sets themes to widgets in main frame
        recolour_widget(widget)

    for widget in rules_frame.winfo_children():        #Sets themes to widgets in rules_frame
        recolour_widget(widget)

    if "keyboard_frame" in globals() and keyboard_frame.winfo_exists():        #Sets themes to keyboard frame 
        keyboard_frame.config(bg=theme["main_bg"])
        for row_frame in keyboard_frame.winfo_children():
            if keyboard_frame.winfo_children().index(row_frame)<4:
                row_frame.config(bg=theme["main_bg"])

    hangman_canvas.config(bg=theme["main_bg"])
    draw_gallows()
    draw_hangman(c)

    if rules_frame.winfo_ismapped():   
        rules_fn()      #Changes theme and reshows rules in new theme and continues throught the program

def recolour_widget(w):         #Checks the type of widget and assigns the respective colour
    if isinstance(w, tk.Label):
        w.config(bg=theme["main_bg"], fg=theme["text_fg"])
    elif isinstance(w, tk.Button):
        w.config(bg=theme["button_bg"], fg=theme["button_fg"])
    elif isinstance(w, tk.Entry):
        w.config(bg="#FFFFFF" if theme is light_theme else "#cfcfcf",fg=theme["text_fg"],insertbackground=theme["text_fg"])
    elif isinstance(w, tk.Frame):
        w.config(bg=theme["main_bg"])
    elif isinstance(w, tk.Text):
        w.config(bg=theme["rules_bg"], fg=theme["text_fg"])

# ============================================================
# KEY HANDLERS: Handles the location of entry of virtual keyboard
# ============================================================
def on_key_press1(ch):
    player_entry.insert(tk.END, ch)
def on_key_press2(ch, entry):
    entry.insert(tk.END, ch)
def on_key_press3(ch):
    wordinput.insert(tk.END, ch)
def on_key_press4(ch):
    guess_entry.insert(tk.END, ch)
def make_handler(entry):
    return lambda ch: on_key_press2(ch, entry)      #Allows entry of virtual keyboard to set_handler 

# ============================================================
# PRESTART: Prepares the game to be played
# ============================================================
def prestart(event=None):
    global label, wordinput, reveal_btn, start_btn, active_key_handler, word_visible,restart_game_btn,restarted

    clear_msg()
    keyboard()
    
    active_key_handler = on_key_press3      #Allows entry of virtual keyboard to wordinput 
    word_visible = False

    giver = player_list[giver_index]
    label = tk.Label(main_frame, text=f"{giver.title()}, Enter Word:", font=("Arial",20),bg=theme["main_bg"],fg=theme["text_fg"])
    label.pack()

    wordinput = tk.Entry(main_frame, width=40, font=("Arial",15), show="*")
    wordinput.pack()
    wordinput.focus_set()       #Sets cursor to entry of wordinput

    reveal_btn = tk.Button(main_frame, text="Show Word",font=("Arial", 15,"bold"),command=toggle_word,bg=theme["button_bg"],fg=theme["button_fg"])
    reveal_btn.pack(pady=10)        #Allows user to check if the word entered is correct

    start_btn = tk.Button(main_frame, text="Start",font=("Arial", 12,"bold"), command=start,bg=theme["button_bg"],fg=theme["button_fg"])
    start_btn.pack(pady=10)
    root.bind("<Return>", start)        #Allows enter to be an input and calls start

# ============================================================
# GAME START: Starts the game
# ============================================================
def start(event=None):
    global word, word_visible

    word = wordinput.get().upper() #Gets the word from the entry

    if word in words:       #Checks if the word has already been used 
        show_msg("Word has already been used and hence can't be played!", theme["error"])
        wordinput.delete(0, tk.END)
        return

    if word.strip() == "":      #Checks if the word is allowed- no characters
        show_msg("Word cannot be empty!", theme["error"])
        wordinput.delete(0, tk.END)
        return

    if not any(ch.isalpha() for ch in word):        #Checks if the word is allowed- no letters
        show_msg("Word must contain at least one alphabet!", theme["error"])
        wordinput.delete(0, tk.END)
        return

    words.append(word)      #Adds the word to the list of words used

    word_visible = False        

    clear_middle_screen()

    if c > 0:       #Allows guessing until chances run out
        guessing()
        disp_word.pack()
        display_word()

# ============================================================
# CHANGE VISIBILITY OF WORD: Change the visibility of entered word(visible or not)- password like
# ============================================================
def toggle_word():       
    global word_visible
    if word_visible:
        wordinput.config(show="*")
        reveal_btn.config(text="Show Word")
        word_visible = False
    else:
        wordinput.config(show="")
        reveal_btn.config(text="Hide Word")
        word_visible = True

# ============================================================
# GUESSING: Allows the guesser to guess letters or word
# ============================================================
def guessing(event=None):       
    global guess_label, guess_entry, submit_guess_btn, active_key_handler

    clear_middle_screen()

    active_key_handler = on_key_press4      #Allows entry of virtual keyboard to guess_label
    guesser = player_list[guesser_index]

    guess_label = tk.Label(main_frame, text=f"{guesser.title()}, Enter Guess:", font=("Arial",20),bg=theme["main_bg"],fg=theme["text_fg"])
    guess_label.pack()

    guess_entry = tk.Entry(main_frame, width=40, font=("Arial",15))
    guess_entry.pack()
    guess_entry.focus_set()        #Sets cursor to entry of guess_entry

    submit_guess_btn = tk.Button(main_frame, text="Submit Guess",font=("Arial", 12,"bold"),command=submit_guess,bg=theme["button_bg"],fg=theme["button_fg"])
    submit_guess_btn.pack(pady=10)
    root.bind("<Return>", submit_guess)        #Allows enter to be an input and calls submit_guess 
    hangman_canvas.pack(pady=10)
    draw_gallows()


# ============================================================
# SUBMIT GUESS: Submits the guess, checks and then processes it
# ============================================================
def submit_guess(event=None):       
    global l, word, c, guessed, next_btn, ww
    clear_msg()

    guessed = False
    guess = guess_entry.get().strip().upper()       #Gets guess from guess_entry
    if len(guess) == 1:

        if not guess.isalpha():         #Condition to catch non alphabetic guess
            show_msg("You are only allowed to guess letters","#ff0000")
            guess_entry.delete(0, tk.END)         #Sets cursor to start of guess_entry
            return

        if guess in l:         #Condition to catch letters already guessed
            show_msg("Letter Already Guessed","#ff0000")
            guess_entry.focus_set()
            guess_entry.delete(0, tk.END)         #Sets cursor to start of guess_entry
            return

        l.append(guess)         #Adds letter to guessed letters if it hasn't been guessed yet

        if guess in word:
            show_msg("The letter is in the word","#00ff00")
            key_buttons[guess].config(bg="#3ff251", state="disabled")         #Changes colour of letter to green in virtual keyboard
            guess_entry.delete(0, tk.END)
            if all(ch in l for ch in word if ch.isalpha()):         #Checks if the word is complete due to all letters being guessed
                show_msg("You've Guessed the Word!","#00ff00")
                guessed = True
                make_next_round_button()
                submit_guess_btn.config(state="disabled")
        else:
            show_msg("The letter is not in the word","#ff0000")
            key_buttons[guess].config(bg="#FF6B6B", state="disabled")         #Changes colour of letter to red in virtual keyboard
            draw_hangman(c - 1)
            c -= 1

    elif len(guess) == len(word):         #Checks words guessed
        if guess == word:         #If the word guessed is correct
            show_msg("You've Guessed the Word!","#00ff00")
            for i in word:
                if i.isalnum():
                    key_buttons[i].config(bg="#00ff00", state="disabled")        #Changes colour of letter to green in virtual keyboard
            guessed = True
            disp_word.pack()
            disp_word.config(text=word)
            make_next_round_button()
            submit_guess_btn.config(state="disabled")
            guess_entry.delete(0, tk.END)         #Sets cursor to start of guess_entry
            return

        else:         #If the word guessed is wrong
            show_msg("Sorry !. That's the wrong word","#ff0000")
            draw_hangman(c - 1)
            c -= 1
            ww+=1
    else:         #Condition for invalid guesses
        show_msg("Invalid Guess","#ff0000")

    guess_entry.delete(0, tk.END)         #Sets cursor to start of guess_entry
    display_word()         #Displays the current hangman stage

    if c == 0:         #Doesn't allow more guesses when chances run out
        show_msg(f"You haven't guessed the word. The word was {word}.","#ff0000")
        draw_hangman(0)
        make_next_round_button()
        submit_guess_btn.config(state="disabled")
        guess_entry.delete(0, tk.END)         #Sets cursor to start of guess_entry
        return


# ============================================================
# TEMP MESSAGE: Shows and Clears feedback messages
# ============================================================
feedback_msg = None

def show_msg(text, colour=None):         
    global feedback_msg, theme

    if colour is None:
        colour = theme["text_fg"]

    if feedback_msg is None:
        feedback_msg = tk.Label(main_frame, text=text, font=("Arial",20),bg=theme["main_bg"],fg=colour)
        feedback_msg.pack(pady=10)
    else:
        feedback_msg.config(text=text,fg=colour)

def clear_msg():          
    global feedback_msg
    if feedback_msg:
        feedback_msg.config(text="")


# ============================================================
# NEXT ROUND BUTTON: Creates a button to change word giver and guesser
# ============================================================
next_btn = None

def make_next_round_button():         
    global next_btn
    if next_btn:
        next_btn.pack_forget()
    next_btn = tk.Button(main_frame, text="Next Round", font=("Arial",12,"bold"),command=next_round,bg=theme["button_bg"],fg=theme["button_fg"])
    next_btn.pack()
    next_btn.focus_set()
    root.bind("<Return>", next_round)         #Allows enter to be an input and calls next_round


# ============================================================
# NEXT ROUND: Changes word giver and guesser and allots points
# ============================================================
def next_round(event=None):         
    global c, l, guessed, giver_index, guesser_index, ww
    global show_points_btn, end_game_btn, restart_game_btn, next_btn, feedback_msg

    clear_msg()
    clear_middle_screen()
    keyboard_frame.pack_forget()
    next_btn.pack_forget()
    draw_gallows()

    if guessed:         #Allots points as per formula
        if len(l) == 0 and ww == 0:
            points = 50
        elif len(l) == 0 and ww > 0:
            points = 50 - 7*ww
            points = max(1, points)
        else:
            points = 40 - (len(l)-(7-c)) - 3*(7-c) - 7*ww
            points = max(1, points)

    else:
        points = 0

    guesser = player_list[guesser_index]
    points_storage[guesser].append(points)         #Saves the points

    c = 7
    l = []
    ww = 0
    guessed = False
    feedback_msg = None         #Resets values required for guessing

    for btn in key_buttons.values():
        btn.config(bg="SystemButtonFace", state="normal")         #Resets the keyboard button colours
    giver_index = (giver_index + 1) % len(player_list)
    guesser_index = (giver_index + 1) % len(player_list)         #Updates the new word giver and guesser

    end_game_btn.place(relx=1.0, rely=0.0, anchor="ne")
    restart_game_btn.place(relx=0.0, rely=0.0, anchor="nw")         
    show_points_btn.place(relx=0.5, rely=1.0, anchor="s")        #Gives options to show points and end or restart game
    
    prestart()

# ============================================================
# DISPLAY WORD: Creates what is to be diplayed of the word to be displayed based on letters guessed
# ============================================================
def display_word():
    s = ""
    ls = word.split()

    for x in word:         #Creates the hidden word
        if x in l:
            s += x
        elif x.isspace():
            s += "  "
        elif x.isalpha()==False:
            s += x
        else:
            s += "_ "

    s += "   ("
    for i, k in enumerate(ls):         #Displays the length of the word(s)
        if i != len(ls) - 1:
            s += f"{len(k)}, "
        else:
            s += f"{len(k)})"

    disp_word.config(text=s,bg=theme["main_bg"],fg=theme["text_fg"])         #Displays the hidden word(s) and its lenght


# ============================================================
# SHOW POINTS TABLE: Shows the cummulative points
# ============================================================
def show_points(t=4000):
    global points_storage, show_points_btn, total_points, points_data

    round_counts = [len(v) for k, v in points_storage.items() if k != "Name"]         #Counts total number of rounds played

    if len(set(round_counts)) != 1:         #Condition to check for unequal number of rounds played(stopped mid round)
        min_rounds = min(round_counts)
        points_data = [["Name", "Points", "Total"]]
        for name, pts in points_storage.items():
            if name != "Name":
                total = sum(pts[:min_rounds])
                points_data.append([name, pts, total])

    else:         #Condition for equal number of rounds played
        points_data = [["Name", "Points", "Total"]]
        for name, pts in points_storage.items():
            if name != "Name":
                total = sum(pts)
                points_data.append([name, pts, total])

    header = points_data[0]
    rows = points_data[1:]

    rows_sorted = sorted(rows, key=lambda r: r[2], reverse=True)         #Sorts the points in decending order

    medals = ["🥇", "🥈", "🥉"]
    current_rank = 1
    last_score = None
    medal_list = []

    for i, row in enumerate(rows_sorted):
        score = row[2]
        if last_score is None or score != last_score:
            current_rank = i + 1
            last_score = score

        medal = medals[current_rank - 1] if current_rank <= 3 else ""
        medal_list.append(medal)

    points_data = [header] + rows_sorted

    bg_colors = []
    stripe1 = "#FAFAFA" if theme is light_theme else "#2A2A2A"
    stripe2 = "#F0F0F0" if theme is light_theme else "#1E1E1E"

    for i, row in enumerate(points_data[1:]):
        medal = medal_list[i]

        if medal == "🥇":
            bg = "#FFF2A1"
        elif medal == "🥈":
            bg = "#DDE5F7"
        elif medal == "🥉":
            bg = "#F7D7C4"
        else:
            bg = stripe1 if i % 2 == 0 else stripe2

        bg_colors.append(bg)

    table_frame = tk.Frame(main_frame, bg=theme["main_bg"])
    table_frame.pack(pady=20)

    tk.Label(table_frame, text="", bg=theme["main_bg"]).grid(row=0, column=0)

    for c_id, c_data in enumerate(points_data[0]):         #Header Row
        label = tk.Label(table_frame,text=str(c_data),font=("Arial",13,"bold"),padx=5, pady=5,relief="ridge",bg=theme["main_bg"],fg=theme["text_fg"])
        label.grid(row=0, column=c_id+1, sticky="nsew")
    for r_id, r_data in enumerate(points_data[1:], start=1):         #Players and points
        medal_lbl = tk.Label(table_frame,text=medal_list[r_id - 1],font=("Arial",14),bg=bg_colors[r_id - 1],fg=theme["text_fg"],padx=10)
        medal_lbl.grid(row=r_id, column=0, sticky="nsew")
        for c_id, c_data in enumerate(r_data):
            label = tk.Label(table_frame,text=str(c_data),font=("Arial",13),padx=5, pady=5,relief="groove",bg=bg_colors[r_id - 1],fg=theme["text_fg"])
            label.grid(row=r_id, column=c_id+1, sticky="nsew")

    table_frame.after(t, lambda: table_frame.pack_forget())         #Displays table


# ============================================================
# FINAL RESULTS: Displays the points and gets final total points(based on rounds played)
# ============================================================
def final_results(t=3000):         
    global total_points

    clear_middle_screen()
    if "keyboard_frame" in globals() and keyboard_frame.winfo_exists():         #Deletes the keyabord
        keyboard_frame.pack_forget()

    total_points = []
        
    show_points(t)

    total_points = [sum(points_storage[name]) for name in player_list]
    winning_points = max(total_points)
    winners = [player_list[i] for i, pts in enumerate(total_points) if pts == winning_points]         #Gets winning points and winners
    print(total_points,winning_points,winners)
    if winning_points == 0:         #Condition for winning_points is 0
        msg = "No players scored any points!"
    else:
        if len(winners) == 1:         #Condition for one winner
            msg = f"Winner is {winners[0].title()} with {winning_points} points!"
        else:         #Condition for many winners
            msg = "Winners: " + ", ".join(w.title() for w in winners) + f" with {winning_points} points each!"

    msg9 = tk.Label(main_frame, text=msg, font=("Arial",30), bg=theme["main_bg"], fg=theme["text_fg"])
    msg9.pack(pady=10)

    msg10 = tk.Label(main_frame, text="Thank you for playing !", font=("Arial",30), bg=theme["main_bg"], fg=theme["text_fg"])
    msg10.pack(pady=5)

# ============================================================
# END GAME: Option to end the game
# ============================================================
def end_game():
    toggle_theme_btn.place_forget()
    final_results(5000)
    root.after(5000, root.destroy)


# ============================================================
# RESTART ENTIRE GAME: Restarts the game from the first
# ============================================================
def restart_game():
    global restart_game_btn, restarted

    final_results(3000)

    def do_full_reset():        
        global feedback_msg, word_visible, name_entries, num_players
        global c, l, key_buttons, player_list, points_storage
        global giver_index, guesser_index, active_key_handler
        global keyboard_frame, next_btn, ww
        global main_frame, rules_frame, disp_word, hangman_canvas, restarted

        for w in root.winfo_children():         #Destroys all widgets in root
            if w is not toggle_theme_btn:
                try:
                    w.destroy()
                except:
                    pass

        feedback_msg = None
        word_visible = False
        name_entries = []
        num_players = None
        c = 7
        ww = 0
        l = []
        key_buttons = {}
        points_storage = {"Name": "Points"}
        player_list = []
        giver_index = 0
        guesser_index = 1
        active_key_handler = None
        next_btn = None
        restarted = False         #Resets all global variables

        #Resets all frames and main buttons
        main_frame = tk.Frame(root, bg=theme["main_bg"])
        rules_frame = tk.Frame(root, bg=theme["rules_bg"])
        disp_word = tk.Label(main_frame, text="", font=("Arial",20))
        hangman_canvas = tk.Canvas(main_frame, width=300, height=250,bg=theme["main_bg"], highlightthickness=0)
        show_points_btn = tk.Button(main_frame, text="Show Points", font=("Arial",12,"bold"),command=show_points, bg=theme["button_bg"], fg=theme["button_fg"])
        end_game_btn = tk.Button(main_frame, text="End Game", font=("Arial",12,"bold"),command=end_game, bg=theme["button_bg"], fg=theme["button_fg"])
        restart_game_btn = tk.Button(main_frame, text="Restart Game", font=("Arial",12,"bold"),command=restart_game, bg=theme["button_bg"], fg=theme["button_fg"])

        #Globalizes all frames and main buttons 
        globals()["main_frame"] = main_frame
        globals()["rules_frame"] = rules_frame
        globals()["disp_word"] = disp_word
        globals()["hangman_canvas"] = hangman_canvas
        globals()["show_points_btn"] = show_points_btn
        globals()["end_game_btn"] = end_game_btn
        globals()["restart_game_btn"] = restart_game_btn

        #Procedure to restart the game
        rules_frame.pack(side="top", fill="both", expand=True)
        toggle_theme_btn.lift()
        restart_game_btn.place_forget()  

        rules_fn()

    root.after(3000, do_full_reset)


# ============================================================
# DRAW THE GALLOWS & HANGMAN: draws the basic structure
# ============================================================
def draw_gallows():
    hangman_canvas.delete("all")         #Deletes pre-existing drawings
    colour = theme["hangman"]

    hangman_canvas.create_line(30, 220, 180, 220, width=5, fill=colour)
    hangman_canvas.create_line(60, 220, 60, 40, width=5, fill=colour)
    hangman_canvas.create_line(58, 40, 180, 40, width=5, fill=colour)
    hangman_canvas.create_line(180, 40, 180, 70, width=5, fill=colour)
    hangman_canvas.create_line(60, 80, 100, 40, width=5, fill=colour)

def draw_hangman(c):         #Draws the stage of the hangman based on number of wrong guesses
    hangman_canvas.delete("hangman")
    wrong = 7 - c
    colour = theme["hangman"]

    if wrong >= 1:
        hangman_canvas.create_oval(155, 70, 205, 120, width=3,outline=colour, tag="hangman")
    if wrong >= 2:
        hangman_canvas.create_line(180, 120, 180, 170, width=3,fill=colour, tag="hangman")
    if wrong >= 3:
        hangman_canvas.create_line(180, 135, 150, 155, width=3,fill=colour, tag="hangman")
    if wrong >= 4:
        hangman_canvas.create_line(180, 135, 210, 155, width=3,fill=colour, tag="hangman")
    if wrong >= 5:
        hangman_canvas.create_line(180, 170, 160, 205, width=3,fill=colour, tag="hangman")
    if wrong >= 6:
        hangman_canvas.create_line(180, 170, 200, 205, width=3,fill=colour, tag="hangman")
    if wrong == 7:
        hangman_canvas.create_line(155, 72, 205, 42, width=4,fill=theme["error"], tag="hangman")
        hangman_canvas.create_line(155, 42, 205, 72, width=4,fill=theme["error"], tag="hangman")


# ============================================================
# GLOBAL VARIABLES
# ============================================================
word_visible = False
name_entries = []
num_players = None
c = 7
ww=0
l = []
key_buttons = {}
points_storage = {"Name": "Points"}
player_list = []
giver_index = 0
guesser_index = 1
active_key_handler = None
restarted = False   # <---- FIX 1 (added)
light_theme={"main_bg":"#FDF6E3", "rules_bg":"#FFF7C2", "button_bg":"#F7C948","button_fg":"#333333" ,"text_fg":"#333333", "error":"#d60b0b","hangman":"#333333", "rules_header":"#FFA500", "rules_colour1":"#1E90FF", "rules_colour2":"#00AA44", "rules_colour3":"#CC0000", "rules_colour4":"#A020F0"}
dark_theme={"main_bg":"#1E1E1E","rules_bg":"#2A2A2A","button_bg":"#f0f0f0","button_fg":"#000000","text_fg":"#ffffff","error":"#FF4C4C","hangman":"#E0E0E0","rules_header":"#FFA500","rules_colour1":"#4DA6FF","rules_colour2":"#00CC66","rules_colour3":"#FF6666","rules_colour4":"#C586C0"}
theme=light_theme
words=[]

# ============================================================
# ROOT FRAME 
# ============================================================
root = tk.Tk()
root.after(10, lambda: root.state("zoomed"))  
root.title("Hangman")
root.config(bg=theme["main_bg"])

# ============================================================
# MAIN FRAME 
# ============================================================
main_frame = tk.Frame(root,bg=theme["main_bg"])

# ============================================================
# RULES FRAME
# ============================================================
rules_frame = tk.Frame(root,bg=theme["rules_bg"])
rules_frame.pack(side="top", fill="both", expand=True)

# ============================================================
# GLOBAL BUTTONS AND LABELS
# ============================================================
disp_word = tk.Label(main_frame, text="", font=("Arial",20))
hangman_canvas = tk.Canvas(main_frame, width=300, height=250,bg=theme["main_bg"],highlightthickness=0)
toggle_theme_btn=tk.Button(root,text="Change Theme",font=("Arial", 20,"bold"), command=toggle_theme,bg=theme["button_bg"],fg=theme["button_fg"],width=12,height=1)
toggle_theme_btn.place(relx=1.0, rely=1.0, anchor="se")
toggle_theme_btn.lift()
show_points_btn = tk.Button(main_frame, text="Show Points", font=("Arial",12,"bold"), command=show_points,bg=theme["button_bg"],fg=theme["button_fg"])
end_game_btn = tk.Button(main_frame, text="End Game", font=("Arial",20,"bold"), command=end_game,bg=theme["button_bg"],fg=theme["button_fg"],width=12,height=1)
restart_game_btn = tk.Button(main_frame, text="Restart Game", font=("Arial",20,"bold"), command=restart_game,bg=theme["button_bg"],fg=theme["button_fg"],width=12,height=1)

# ============================================================
# INIT UI
# ============================================================
rules_fn()
root.mainloop()

