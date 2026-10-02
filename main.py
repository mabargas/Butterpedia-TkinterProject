#Name: Mei Lan Bargas
#Course: ITEC 352

#the filedialog and askopenfile import will alow photos to be uploaded and added to the database
#pip install pillow to be able to do the upload as well
import tkinter
from tkinter import ttk, filedialog, messagebox
from tkinter.filedialog import askopenfile
import io
from PIL import Image, ImageTk
from objects import ButterflyLibraryMain


#Classification Lists
main_families = ["Nymphalidae", "Pieridae","Lycaenidae","Riodinidae","Hesperiidae","Papilionidae"]
nymph_subfamily = ["Nymphalinae", "Satyrinae", "Heliconiinae", "Danainae","Charaxinae", "Limenitidinae", "Morphinae", "Cyrestinae", "Biblidinae"]
pier_subfamily = ["Pierinae", "Coliadinae", "Dismorphiinae"]
lyc_subfamily = ["Lycaeninae", "Theclinae", "Polyommatinae", "Miletinae", "Poritiinae", "Liphyrinae"]
rio_subfamily = ["Riodininae", "Euselasiinae"]
hesper_subfamily = ["Hesperiinae", "Pyrginae", "Heteropterinae", "Euschemoniinae", "Coeliadinae", "Trapezitinae"]
papil_subfamily = ["Papilioninae", "Parnassiinae", "Baroniinae"]

global filename, img_bin
blmain = ButterflyLibraryMain()


class ButterpediaApp():
    #Method to Bind Combobox
    def sub_family_bind(e):
        if mainfam_combobox.get() == "Nymphalidae":
            subfam_combobox.configure(value = nymph_subfamily)
        if mainfam_combobox.get() == "Pieridae":
            subfam_combobox.configure(value = pier_subfamily)
        if mainfam_combobox.get() == "Lycaenidae":
            subfam_combobox.configure(value = lyc_subfamily)
        if mainfam_combobox.get() == "Riodinidae":
            subfam_combobox.configure(value = rio_subfamily)
        if mainfam_combobox.get() == "Hesperiidae":
            subfam_combobox.configure(value = hesper_subfamily)
        if mainfam_combobox.get() == "Papilionidae":
            subfam_combobox.configure(value = papil_subfamily)
    
    #Upload Image Method
    def upload_image():
        #filename and img_bin are beyond this function and apply to everything, like me assigning blmain to my objects.py class
        global filename, img_bin
        #Select file types with jpg and png
        file_types = [('All files', '*.*'), ('JPG', '*.jpg'), ('PNG', '.png')]
        #Uses the module diledialog and its method askopenfilename to open a user file and store it
        filename = filedialog.askopenfilename(filetypes = file_types)
        img_resize  = Image.open(filename)
        img_bin = img_resize.resize((80,80))
        #PhotoImage constructor converts img into a format for tkinter to display
        img_bin = ImageTk.PhotoImage(img_bin)
        #Puts the image in a label to show the user
        image_preview = tkinter.Label(image_label, image = img_bin)
        #Places the image above the Upload button
        image_preview.grid(row = 0, column = 0)
        
    #Validation to enter data and getting the data
    def enter_data():
        global filename, img_bin
        #Opens img_bin and reads it binary before it turns into a BLOB
        img_bin = open(filename, 'rb')
        accepted = accept_var.get()
        if accepted == "Accepted":
            name = name_entry.get()
            rarity = rarity_combobox.get()
            species_amt = species_amt_spinbox.get()
            mainfamily = mainfam_combobox.get()
            subfamily = subfam_combobox.get()
            color = color_combobox.get()
            wingpatterns = patterns_combobox.get()
            wingspan = wingspan_spinbox.get()
            metric = metric_combobox.get()
            img_bin = img_bin.read()
            location = loc_combobox.get()
            region = region_combobox.get()
            if name and rarity and species_amt and mainfamily and subfamily and color and wingpatterns and wingspan and metric and img_bin and location and region:
               blmain.add_butterflymain(name, rarity, species_amt, mainfamily, subfamily, color, 
                                                    wingpatterns, wingspan, metric, 
                                                    img_bin, location, region)
               tkinter.messagebox.showinfo("Butterfly Information", "Data Has Been Submitted")
            else:
                tkinter.messagebox.showwarning(title = "Warning: All Fields Not Filled Out", message = "Please Fill All of The Fields") 
                
                
        else:
            tkinter.messagebox.showwarning(title = "Warning: Please Check Confirmation Box",message="You have not confirmed all information is valid")  
    
    def mainshow_butterfly():
        butterflies = blmain.get_butterflies_main()
        #Store Images in a Dictionary
        main_tree.bfly_images = {}

        for butterfly in butterflies:
            #Fetch from database column 8
            img_bin = butterfly[8]

            #Convert into memory bytes, resize, and then convert into PhotoImage
            butterfly_img = Image.open(io.BytesIO(img_bin))
            butterfly_img = butterfly_img.resize((80,80))
            butterfly_img = ImageTk.PhotoImage(butterfly_img)

            #Insert Data Into Treeview
            #Insert the data into the treeview. '' means top row, 'end' means at the bottom of the tree view, text = '' means no text, iid is the database id column, values are my columns fetched from the database, and image is my butterfly images
            main_tree.insert('', 'end', text='', iid = butterfly[0],values = (butterfly[1], butterfly[2], butterfly[3], butterfly[4], butterfly[5], butterfly[6], butterfly[7]), image = butterfly_img)
            #Taking image associated with primary key, and storing it in my library so it can still be viewable
            main_tree.bfly_images[butterfly[0]] = butterfly_img
            
          
    def habshow_butterfly():
         #Store the method into a variable
         butterflies_hab = blmain.get_butterflies_hab()
         #Store the images into a dictionary
         hab_tree.bfly_hab_images = {}
         for butterfly in butterflies_hab:
            #Store the database index into a variable
            img_bin = butterfly[4]
            #Open the image and convert it into bytes
            butterflyh_img = Image.open(io.BytesIO(img_bin))
            #Resize it
            butterflyh_img = butterflyh_img.resize((80,80))
            #Turn the bytes into a format that tkinter can use
            butterflyh_img = ImageTk.PhotoImage(butterflyh_img)
            #Insert the data into the treeview. '' means top row, 'end' means at the bottom of the tree view, text = '' means no text, iid is the database id column, values are my columns fetched from the database, and image is my butterfly images
            hab_tree.insert('', 'end', text = '', iid = butterfly[0], values=(butterfly[1], butterfly[2], butterfly[3], butterfly[5], butterfly[6]), image = butterflyh_img)
            hab_tree.bfly_hab_images[butterfly[0]] = butterflyh_img
    
    def delete_butterfly_app():
        #Loop
        for butterfly_selection in main_tree.get_children():
            #Grab the tree selection
            butterfly_selection = main_tree.selection()
            #Stops the error for tuple index out of range
            if not butterfly_selection:
                return
            #Assign butterfly_id to the selection which has the column of 0 "the id"
            butterfly_id = butterfly_selection[0]
            #Delete from tree
            main_tree.delete(butterfly_id)
            #Delete from database
            blmain.delete_butterfly(butterfly_id)
        
        
    def refresh_butterfly_app():
        #If I don't have the delete loops, my image disappears for some reason
        #Loop to get children from my tree
        for butterfly_row in main_tree.get_children():
            #delete row
            main_tree.delete(butterfly_row)
            
        for habitat_row in hab_tree.get_children():
            hab_tree.delete(habitat_row)
        ButterpediaApp.mainshow_butterfly()
        ButterpediaApp.habshow_butterfly()
        

#________________________________________________________________________________________________________
#Main GUI Window
window = tkinter.Tk()
window.title("Butterpedia")
window.geometry("900x900")
window.resizable(0,0)

#Title
title_label = ttk.Label(window, text = "Welcome to the Butterpedia!", font = ("Poppins", 24, "bold"))
title_label.pack(pady= (20, 0))
desc_label = ttk.Label(window, text = "View and Add Butterflies to enjoy a library of Butterfly Information.", font = ("Poppins", 12))
desc_label.pack(pady= (0, 20))

#Notebook Tabs Frame Creation
tabs_frame = ttk.Notebook(window)
tabs_frame.pack()

#Adding the Frames
view_butterfly = ttk.Frame(tabs_frame)
view_habitat = ttk.Frame(tabs_frame)
add_butterfly = ttk.Frame(tabs_frame)

tabs_frame.add(view_butterfly, text = 'View Butterflies Main Information')
tabs_frame.add(view_habitat, text = 'View Butterflies Habitat')
tabs_frame.add(add_butterfly, text = 'Add Butterfly')

#Configuring the rows; rows are 0 for add_butterfly since it kept adding to much padding to the title
add_butterfly.rowconfigure(0, weight = 0)
add_butterfly.columnconfigure(0, weight = 1)

view_butterfly.rowconfigure(1, weight = 1)
view_butterfly.columnconfigure(0, weight = 1)

view_habitat.rowconfigure(1, weight = 1)
view_habitat.columnconfigure(0, weight = 1)

#Configuring Row Height
style = ttk.Style(window)
style.configure("Treeview", rowheight = 100)
style.configure("TNotebook.Tab", font = ("Poppins", 12))
style.map('TNotebook.Tab', foreground = [('selected', '#3700FF')])

#________________________________________________________________________________________________________
#View Main Butterfly Information Frame  View Main Butterfly Information Frame   View Main Butterfly Information Frame   View Main Butterfly Information Frame
#Refresh Butterflies
refresh_button = tkinter.Button(view_butterfly, text = "Refresh", width = 10,bg = "#3700FF",fg = "white", command = ButterpediaApp.refresh_butterfly_app)
refresh_button.grid(row = 0, column = 0, sticky = "w", padx = 10, pady = 10)

#Delete Butterflies
delete_button = tkinter.Button(view_butterfly, text = "Delete", width = 10, bg = "#FF7700",fg = "white",command = ButterpediaApp.delete_butterfly_app)
delete_button.grid(row = 0, column = 0, sticky = "w", padx = (100,0), pady = 10)

#View Butterflies Main Info Frame
main_tree_frame = tkinter.Frame(view_butterfly)
#Treeview Scrollbar
main_scrollbar = tkinter.Scrollbar(main_tree_frame)
main_scrollbar.pack(side = "right", fill = "y")

#Treeview
main_tree_frame.grid(row = 1, column= 0)
main_tree = ttk.Treeview(main_tree_frame, yscrollcommand=main_scrollbar.set)



main_tree['columns'] = ("Name", "Main Family", "Sub Family", "Color", 
"Wing Patterns", "Wingspan", "Metric")

#Create Columns
main_tree.column("#0", width = 100, anchor = 'center')
main_tree.column("Name", width = 120, anchor = 'center')
main_tree.column("Main Family", width = 90, anchor = 'center')
main_tree.column("Sub Family", width = 90, anchor = 'center')
main_tree.column("Color", width = 50, anchor = 'center')
main_tree.column("Wing Patterns", width = 100, anchor = 'center')
main_tree.column("Wingspan", width = 65, anchor = 'center')
main_tree.column("Metric", width = 45, anchor = 'center')

#Create Headings
main_tree.heading("#0", text = "Image")
main_tree.heading("Name", text = "Name")
main_tree.heading("Main Family", text = "Main Family")
main_tree.heading("Sub Family", text = "Sub Family")
main_tree.heading("Color", text = "Color")
main_tree.heading("Wing Patterns", text = "Wing Patterns")
main_tree.heading("Wingspan", text = "Wingspan")
main_tree.heading("Metric", text = "Metric")


main_tree.pack(fill="both", expand = True)
ButterpediaApp.mainshow_butterfly()

#________________________________________________________________________________________________________
#View Butterflies Habitat Frame     View Butterflies Habitat Frame      View Butterflies Habitat Frame

#View Butterflies Main Info Frame
hab_tree_frame = tkinter.Frame(view_habitat)
hab_tree_frame.grid(row = 1, column= 0, sticky = "nsew")

#Treeview Scrollbar
hab_scrollbar = tkinter.Scrollbar(hab_tree_frame)
hab_scrollbar.pack(side = "right", fill = "y")

hab_tree = ttk.Treeview(hab_tree_frame, yscrollcommand=hab_scrollbar.set)
hab_tree['columns'] = ("Name", "Rarity", "Genus Species #", "Location", 
"Region")

#Create Columns
hab_tree.column("#0", width = 100, anchor = 'center')
hab_tree.column("Name", width = 120, anchor = 'center')
hab_tree.column("Rarity", width = 100, anchor = 'center')
hab_tree.column("Genus Species #", width = 120, anchor = 'center')
hab_tree.column("Location", width = 80, anchor = 'center')
hab_tree.column("Region", width = 80, anchor = 'center')


#Create Headings
hab_tree.heading("#0", text = "Image")
hab_tree.heading("Name", text = "Name")
hab_tree.heading("Rarity", text = "Rarity")
hab_tree.heading("Genus Species #", text = "Genus Species #")
hab_tree.heading("Location", text = "Location")
hab_tree.heading("Region", text = "Region")


hab_tree.pack(fill="both", expand = True)
ButterpediaApp.habshow_butterfly()
#________________________________________________________________________________________________________
#Add Butterflies Frame      Add Butterflies Frame       Add Butterflies Frame       Add Butterflies Frame
ab_title_label = tkinter.Label(add_butterfly, text="Add Butterfly Information", font = ("Poppins", 20))
ab_title_label.grid(row = 0, column = 0, pady = (8,8))

#Add Name
name_frame = tkinter.Frame(add_butterfly)
name_frame.grid(row = 1, column = 0)

name_label = tkinter.LabelFrame(name_frame, text = "Butterfly Name", font = ("Poppins", 10, "bold"), labelanchor= "n")
name_label.grid(row = 0, column = 0)
name_entry = tkinter.Entry(name_label, width = 55)
name_entry.grid(row = 1, column =0)

#Add General Information: Classification, Est Population
pop_frame = tkinter.Frame(add_butterfly)
pop_frame.grid(row = 2, column = 0)

pop_label = tkinter.LabelFrame(pop_frame, text = "Population Information", font = ("Poppins", 10, "bold"), labelanchor= "n")
pop_label.grid(row = 0, column = 0)

rarity_label = tkinter.Label(pop_label, text = "Rarity", font = ("Poppins", 9))
rarity_label.grid(row = 0, column = 0)
rarity_combobox = ttk.Combobox(pop_label, values=["","Abundant", "Common", "Rare", "Extremely Rare", "Endangered"], state = "readonly")
rarity_combobox.grid(row = 1, column = 0)

species_amt_label = ttk.Label(pop_label, text = "Genus Species Amount", font = ("Poppins", 9))
species_amt_label.grid(row = 0, column = 1)
species_amt_spinbox = tkinter.Spinbox(pop_label, width = 8, from_=1, to=100000)
species_amt_spinbox.grid(row = 1, column = 1)

#Add Family Information
fam_frame = tkinter.Frame(add_butterfly)
fam_frame.grid(row = 3, column = 0)

fam_label = tkinter.LabelFrame(fam_frame, text = "Family Information", labelanchor= "n", font = ("Poppins", 10, "bold"))
fam_label.grid(row = 0, column = 0)

mainfam_label = tkinter.Label(fam_label, text = "Main Family", font = ("Poppins", 9))
mainfam_label.grid(row = 0, column = 0)
mainfam_combobox = ttk.Combobox(fam_label, values=["Nymphalidae","Pieridae", "Lycaenidae", "Riodinidae", "Hesperiidae", "Papilionidae"], state = "readonly")
mainfam_combobox.grid(row = 1, column = 0)

subfam_label = tkinter.Label(fam_label, text = "Sub Family", font = ("Poppins", 9))
subfam_label.grid(row = 0, column = 1)
subfam_combobox= ttk.Combobox(fam_label, values=[""], state = "readonly")
subfam_combobox.grid(row = 1, column = 1)
mainfam_combobox.bind("<<ComboboxSelected>>", ButterpediaApp.sub_family_bind)

#Add Appearance Information
appear_frame = tkinter.Frame(add_butterfly)
appear_frame.grid(row = 4, column = 0)

appear_label = tkinter.LabelFrame(appear_frame, text = "Appearance Information", labelanchor= "n", font = ("Poppins", 10, "bold"))
appear_label.grid(row = 0, column = 0)

color_label = tkinter.Label(appear_label, text = "Primary Color", font = ("Poppins", 9))
color_label.grid(row = 0, column = 0)
color_combobox = ttk.Combobox(appear_label, values=["", "Red", "Orange", "Yellow", "Green", "Blue", "Indigo","Blue",
                                                        "Pink", "White", "Brown", "Pink", "Black"], width = 8, state = "readonly")
color_combobox.grid(row = 1, column = 0)

patterns_label = tkinter.Label(appear_label, text = "Wing Patterns", font = ("Poppins", 9))
patterns_label.grid(row = 0, column = 1)
patterns_combobox= ttk.Combobox(appear_label, values = ["", "Spots", "Stripes", "Iridescent", "Gradient", "Opaque", "Chequered", "Black Veins", 
                                                            "Border Patterns", "Sunstreaks", "Colored Patches", "Colored Scales", "Spirals", "Ringlets", "Owl Eye Spots" ], width = 14, state = "readonly")
patterns_combobox.grid(row = 1, column = 1)

#Add Wingspan Information
wing_frame = tkinter.Frame(add_butterfly)
wing_frame.grid(row = 5, column = 0)

wing_label = tkinter.LabelFrame(wing_frame, text = "Wingspan Information", labelanchor= "n", font = ("Poppins", 10, "bold"))
wing_label.grid(row = 0, column = 0)

wingspan_label = tkinter.Label(wing_label, text = "Wingspan", font = ("Poppins", 9))
wingspan_label.grid(row = 0, column = 0)
wingspan_spinbox = ttk.Spinbox(wing_label, width = 10, from_=1, to=100)
wingspan_spinbox.grid(row = 1, column = 0, padx = 20)

metric_label = tkinter.Label(wing_label, text = "Metric", font = ("Poppins", 9))
metric_label.grid(row = 0, column = 1)
metric_combobox= ttk.Combobox(wing_label, values=["", "in", "cm"], width = 10, state = "readonly")
metric_combobox.grid(row = 1, column = 1)

#Add Habitat Information
habitat_frame = tkinter.Frame(add_butterfly)
habitat_frame.grid(row = 6, column = 0)

habitat_label = tkinter.LabelFrame(habitat_frame, text = "Habitat Information", labelanchor= "n", font = ("Poppins", 10, "bold"))
habitat_label.grid(row = 0, column = 0)

loc_label = tkinter.Label(habitat_label, text = "Geographical Location", font = ("Poppins", 9))
loc_label.grid(row = 0, column = 0)
loc_combobox = ttk.Combobox(habitat_label, values=["", "Tundra", "Forests", "Grasslands", "Deserts", "Mountains", "Coastal", "Caves"], width = 10, state = "readonly")
loc_combobox.grid(row = 1, column = 0)

region_label = tkinter.Label(habitat_label, text = "Region", font = ("Poppins", 9))
region_label.grid(row = 0, column = 1)
region_combobox= ttk.Combobox(habitat_label, values=["", "North America", "Asia", "Africa", "South America", "Anartica", "Europe", "Australia"], width = 15, state = "readonly")
region_combobox.grid(row = 1, column = 1)

#Upload an Image
image_frame = tkinter.Frame(add_butterfly)
image_frame.grid(row = 7, column = 0)

image_label = tkinter.LabelFrame(image_frame, text = "Upload Butterfly Image", labelanchor= "n", font = ("Poppins", 10, "bold"))
image_label.grid(row = 0, column = 1)

upload_button = tkinter.Button(image_label, text = "Upload Butterfly Image", command = lambda:ButterpediaApp.upload_image())
upload_button.grid(row = 1, column = 0, padx= 6)

#Accept Everything is as it should be
confirm_frame = tkinter.LabelFrame(add_butterfly, text = "Confirm All Information is Valid", labelanchor="n", font = ("Poppins", 10, "bold"))
confirm_frame.grid(row = 8, column = 0, padx = 10, pady = 10, sticky = "news")
accept_var = tkinter.StringVar(value = "Not Accepted")
confirm_check = tkinter.Checkbutton(confirm_frame, text = "I confirm that all information is valid",
                                    variable = accept_var, onvalue = "Accepted", offvalue="Not Accepted")
confirm_check.grid(row = 0, column = 0, sticky = "n")

#Submit Form
submit_button = tkinter.Button(add_butterfly, text="Submit Butterfly", bg = "#3700FF", fg = "white", command = ButterpediaApp.enter_data)
submit_button.grid(row = 9, column = 0, padx = 10)

#Padding The Input Boxes
for widget in name_label.winfo_children():
    widget.grid( padx = 30, pady = (2, 6))
    widget.columnconfigure(0, weight = 1)

for widget in pop_label.winfo_children():
    widget.grid(padx = 30, pady = (2, 6))
    widget.columnconfigure(0, weight = 1)

for widget in fam_label.winfo_children():
    widget.grid(padx = 28, pady = (2, 6))
    widget.columnconfigure(0, weight = 1)

for widget in appear_label.winfo_children():
    widget.grid(padx =53, pady = (2, 6))
    widget.columnconfigure(0, weight = 1)

for widget in wing_label.winfo_children():
    widget.grid(padx = 60, pady = (2, 6))
    widget.columnconfigure(0, weight = 1)

for widget in habitat_label.winfo_children():
    widget.grid(padx = 40, pady = (2, 6))
    widget.columnconfigure(0, weight = 1)

for widget in image_label.winfo_children():
    widget.grid(padx = 20, pady = (2, 6))
    widget.columnconfigure(0, weight = 1)


#Run Window Loop
window.mainloop()

