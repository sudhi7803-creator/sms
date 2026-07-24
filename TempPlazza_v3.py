import streamlit as st
from datetime import datetime
import os
import json


# =====================================================
# APP INFORMATION
# =====================================================

COMPANY_NAME = "AJB - TAB"
CREATOR_NAME = "Sudhin@2026"


# =====================================================
# PAGE SETTINGS
# =====================================================

st.set_page_config(
    page_title="AJB - TAB",
    page_icon="🌡️",
    layout="wide"
)


# =====================================================
# FILE SETTINGS
# =====================================================

from pathlib import Path

BASE_FOLDER = Path(__file__).parent

STATE_FILE = BASE_FOLDER / "TempPlazza_state.json"


if not os.path.exists(BASE_FOLDER):
    os.makedirs(BASE_FOLDER)



# =====================================================
# SAVE / LOAD LOGIN MEMORY
# =====================================================

def load_state():

    if os.path.exists(STATE_FILE):

        with open(STATE_FILE, "r") as f:
            return json.load(f)

    return {
        "logged_in": False,
        "username": ""
    }



def save_state():

    data = {
        "logged_in": st.session_state.logged_in,
        "username": st.session_state.username
    }

    with open(STATE_FILE, "w") as f:
        json.dump(data, f, indent=4)



# =====================================================
# LOAD SESSION
# =====================================================

if "loaded" not in st.session_state:

    old = load_state()

    st.session_state.logged_in = old["logged_in"]

    st.session_state.username = old["username"]

    st.session_state.loaded = True



# =====================================================
# USER DATABASE
# =====================================================

if "users" not in st.session_state:

    st.session_state.users = {

        "admin": "admin@123"

    }



# =====================================================
# DESIGN
# =====================================================

st.markdown(
"""
<style>

h1 {
color:#1E5A96;
text-align:center;
}

.stButton button {

background:#1E5A96;
color:white;

}

</style>
""",
unsafe_allow_html=True
)



# =====================================================
# LOGIN PAGE
# =====================================================

if not st.session_state.logged_in:


    st.title(
        COMPANY_NAME
    )


    st.subheader(
        "Temperature Data Logger"
    )


    username = st.text_input(
        "Username"
    )


    password = st.text_input(
        "Password",
        type="password"
    )



    if st.button(
        "🔐 Login",
        key="login_button"
    ):


        if (
            username in st.session_state.users
            and
            st.session_state.users[username] == password
        ):


            st.session_state.logged_in = True

            st.session_state.username = username

            save_state()

            st.rerun()


        else:

            st.error(
                "Invalid username or password"
            )



    st.write(
        f"Created by {CREATOR_NAME}"
    )


    st.stop()



# =====================================================
# AFTER LOGIN
# =====================================================


st.success(
    f"Welcome {st.session_state.username}"
)



if st.button(
    "Logout",
    key="logout_button"
):

    st.session_state.logged_in = False

    st.session_state.username = ""

    save_state()

    st.rerun()



st.title(
    "TempPlazza Data Logger"
)


st.success(
    "Login system working successfully"
)# =====================================================
# PART 2 - EXCEL CONNECTION
# =====================================================

from openpyxl import load_workbook
from datetime import datetime, date


# =====================================================
# EXCEL SETTINGS
# =====================================================


LOCAL_FILE = BASE_FOLDER / "TempPlazza.xlsx"


# =====================================================
# PROJECT INFORMATION
# =====================================================

tower = st.text_input("Tower")
level = st.text_input("Level")


# Create Excel sheet name after getting inputs

if tower and level:
    TEMPLATE_SHEET = f"Level-{tower}-{level}"
else:
    TEMPLATE_SHEET = None
    

# =====================================================
# EXCEL FUNCTIONS
# =====================================================

def open_excel():

    wb = load_workbook(LOCAL_FILE)

    st.write("Excel file:")
    st.write(LOCAL_FILE)

    st.write("Available sheets:")
    st.write(wb.sheetnames)

    return wb

def get_sheet():

    st.write("DEBUG: get_sheet started")

    if TEMPLATE_SHEET is None:
        st.warning("Please enter Tower and Level first")
        st.stop()

    wb = open_excel()

    st.write("Looking for sheet:")
    st.write(TEMPLATE_SHEET)
    
    st.write("Available sheets:")
    st.write(wb.sheetnames)

    if TEMPLATE_SHEET not in wb.sheetnames:
        st.error(
            f"Level sheet '{TEMPLATE_SHEET}' not found in {LOCAL_FILE.name}"
        )
        st.stop()

    ws = wb[TEMPLATE_SHEET]

    return wb, ws

# =====================================================
# SYNC COPY FUNCTION
# =====================================================

OUTPUT_FOLDER = BASE_FOLDER / "TempPlazza_Output"


def create_sync_copy(tower, level):

    tower_folder = OUTPUT_FOLDER / tower

    tower_folder.mkdir(
        parents=True,
        exist_ok=True
    )

    filename = f"{tower}_Level_{level}.xlsx"

    output_file = tower_folder / filename

    shutil.copy(
        LOCAL_FILE,
        output_file
    )

    return output_file



# =====================================================
# PROJECT INFORMATION
# =====================================================


st.subheader(
    "Project Information"
)


if "tower" not in st.session_state:

    st.session_state.tower = ""


if "level" not in st.session_state:

    st.session_state.level = ""



col1, col2 = st.columns(2)


with col1:

    tower = st.text_input(
        "Tower / Podium",
        value=st.session_state.tower,
        key="tower_input"
    )


with col2:

    level = st.text_input(
        "Level",
        value=st.session_state.level,
        key="level_input"
    )



if st.button(
    "🔒 Lock Tower & Level",
    key="lock_tower_level"
):


    st.session_state.tower = tower

    st.session_state.level = level


    wb, ws = get_sheet()


    # Excel locations

    ws["G9"] = tower

    ws["G7"] = level


    wb.save(
        LOCAL_FILE
    )


    st.success(
        "Tower and Level saved to Excel"
    )



# =====================================================
# AMBIENT TEMPERATURE
# =====================================================


st.subheader(
    "Ambient Air Temperature"
)



col1, col2 = st.columns(2)



with col1:

    ambient_db = st.text_input(
        "Ambient DB",
        key="ambient_db"
    )


with col2:

    ambient_wb = st.text_input(
        "Ambient WB",
        key="ambient_wb"
    )



if st.button(
    "🔒 Lock Ambient Temperature",
    key="lock_ambient"
):


    wb, ws = get_sheet()


    # Excel locations

    ws["J17"] = ambient_db

    ws["N17"] = ambient_wb


    wb.save(
        LOCAL_FILE
    )


    st.success(
        "Ambient temperature updated"
    )   # =====================================================
# PART 3 - EQUIPMENT DATA ENTRY
# =====================================================


st.subheader(
    "Equipment Details"
)



# Current Excel row memory

if "excel_row" not in st.session_state:

    st.session_state.excel_row = 17



# Current page memory

if "page_number" not in st.session_state:

    st.session_state.page_number = 1




# =====================================================
# CREATE NEW PAGE
# =====================================================

def create_new_page():

    wb = open_excel()


    old_sheet = wb[TEMPLATE_SHEET]


    new_name = (
        f"PAGE_{st.session_state.page_number}"
    )


    if new_name not in wb.sheetnames:


        new_sheet = wb.copy_worksheet(
            old_sheet
        )


        new_sheet.title = new_name


    wb.save(
        LOCAL_FILE
    )



def get_active_sheet():

    wb = open_excel()


    sheet_name = (
        f"PAGE_{st.session_state.page_number}"
    )


    if sheet_name in wb.sheetnames:

        ws = wb[sheet_name]


    else:

        # first page uses template

        if st.session_state.page_number == 1:

            ws = wb[TEMPLATE_SHEET]

            ws.title = sheet_name


        else:

            create_new_page()

            wb = open_excel()

            ws = wb[sheet_name]


    return wb, ws




# =====================================================
# INPUT FORM
# =====================================================


col1, col2 = st.columns(2)


with col1:

    equipment_tag = st.text_input(
        "Equipment Tag",
        key="equipment_tag"
    )


    room = st.text_input(
        "Room",
        key="room"
    )


    set_point = st.text_input(
        "Thermostat Set Point °C",
        key="set_point"
    )


    design = st.text_input(
        "Design Temp / %RH",
        key="design"
    )



with col2:

    reading_time = st.text_input(
        "Reading Time",
        key="reading_time"
    )


    indoor_db = st.text_input(
        "Indoor DB",
        key="indoor_db"
    )


    indoor_wb = st.text_input(
        "Indoor WB",
        key="indoor_wb"
    )


    indoor_rh = st.text_input(
        "Indoor RH %",
        key="indoor_rh"
    )



remarks = st.text_input(
    "Remarks",
    key="remarks"
)




# =====================================================
# UPDATE EXCEL BUTTON
# =====================================================


if st.button(
    "💾 Update Equipment Data",
    key="update_equipment"
):


    wb, ws = get_active_sheet()


    row = st.session_state.excel_row



    # Write data

    ws[f"A{row}"] = equipment_tag

    ws[f"R{row}"] = room

    ws[f"V{row}"] = set_point

    ws[f"AB{row}"] = design

    ws[f"AJ{row}"] = reading_time

    ws[f"AN{row}"] = indoor_db

    ws[f"AR{row}"] = indoor_wb

    ws[f"AV{row}"] = indoor_rh

    ws[f"AZ{row}"] = remarks



    wb.save(
        LOCAL_FILE
    )



    st.success(
        f"Equipment saved in Row {row}"
    )



    # Move next row

    st.session_state.excel_row += 1



    # If row exceeds 33

    if st.session_state.excel_row > 33:


        st.session_state.page_number += 1


        st.session_state.excel_row = 17


        create_new_page()


        st.info(
            f"New page created: PAGE_{st.session_state.page_number}"
        )# =====================================================
# PART 4 - PDF REPORT GENERATION
# =====================================================


st.subheader(
    "PDF Report"
)



def create_pdf(data):


    pdf = FPDF()


    pdf.add_page()



    # -------------------------
    # Header
    # -------------------------

    pdf.set_fill_color(
        30,
        90,
        150
    )

    pdf.rect(
        0,
        0,
        210,
        35,
        "F"
    )


    pdf.set_text_color(
        255,
        255,
        255
    )


    pdf.set_font(
        "Arial",
        "B",
        18
    )


    pdf.cell(
        0,
        10,
        "AJB - TAB",
        ln=True,
        align="C"
    )


    pdf.set_font(
        "Arial",
        "B",
        12
    )


    pdf.cell(
        0,
        8,
        "Temperature Test Daily Report",
        ln=True,
        align="C"
    )



    pdf.set_text_color(
        0,
        0,
        0
    )


    pdf.ln(
        15
    )



    # -------------------------
    # Project Information
    # -------------------------

    pdf.set_font(
        "Arial",
        "B",
        12
    )


    pdf.cell(
        0,
        8,
        "Project Information",
        ln=True
    )



    pdf.set_font(
        "Arial",
        size=11
    )


    info = [

        ("Prepared By",
        st.session_state.username),

        ("Date",
        datetime.now().strftime(
            "%Y-%m-%d %H:%M"
        )),

        ("Tower",
        st.session_state.tower),

        ("Level",
        st.session_state.level),

        ("Page",
        str(st.session_state.page_number))

    ]



    for label,value in info:


        pdf.cell(
            50,
            8,
            label,
            border=1
        )


        pdf.cell(
            140,
            8,
            str(value),
            border=1
        )


        pdf.ln()



    pdf.ln(8)



    # -------------------------
    # Equipment Data
    # -------------------------

    pdf.set_font(
        "Arial",
        "B",
        12
    )


    pdf.cell(
        0,
        8,
        "Equipment Details",
        ln=True
    )


    pdf.set_font(
        "Arial",
        size=11
    )


    equipment = [

        ("Equipment Tag",
         data["tag"]),

        ("Room",
         data["room"]),

        ("Set Point",
         data["set_point"]),

        ("Design",
         data["design"]),

        ("Reading Time",
         data["time"]),

        ("Indoor DB",
         data["db"]),

        ("Indoor WB",
         data["wb"]),

        ("Indoor RH",
         data["rh"])

    ]



    for label,value in equipment:


        pdf.cell(
            55,
            8,
            label,
            border=1
        )


        pdf.cell(
            135,
            8,
            str(value),
            border=1
        )


        pdf.ln()



    pdf.ln(8)



    # -------------------------
    # Remarks
    # -------------------------

    pdf.set_font(
        "Arial",
        "B",
        12
    )


    pdf.cell(
        0,
        8,
        "Remarks",
        ln=True
    )


    pdf.set_font(
        "Arial",
        size=11
    )


    pdf.multi_cell(
        0,
        8,
        data["remarks"],
        border=1
    )



    # -------------------------
    # Footer
    # -------------------------

    pdf.set_y(
        -20
    )


    pdf.set_font(
        "Arial",
        "I",
        9
    )


    pdf.cell(
        0,
        10,
        "Generated by AJB - TAB Temperature Data Logger",
        align="C"
    )



    return pdf




# =====================================================
# STORE LAST ENTRY FOR PDF
# =====================================================

if "last_equipment" not in st.session_state:

    st.session_state.last_equipment = None




# =====================================================
# PDF INPUT BUTTON
# =====================================================


pdf_tag = st.text_input(
    "PDF Equipment Tag",
    key="pdf_tag"
)



if st.button(
    "📄 Generate PDF",
    key="generate_pdf"
):


    data = {

        "tag": pdf_tag,

        "room":
        st.session_state.get(
            "room",
            ""
        ),

        "set_point":
        st.session_state.get(
            "set_point",
            ""
        ),

        "design":
        st.session_state.get(
            "design",
            ""
        ),

        "time":
        st.session_state.get(
            "reading_time",
            ""
        ),

        "db":
        st.session_state.get(
            "indoor_db",
            ""
        ),

        "wb":
        st.session_state.get(
            "indoor_wb",
            ""
        ),

        "rh":
        st.session_state.get(
            "indoor_rh",
            ""
        ),

        "remarks":
        st.session_state.get(
            "remarks",
            ""
        )

    }



    pdf = create_pdf(
        data
    )


    pdf_output = pdf.output(
        dest="S"
    ).encode(
        "latin-1"
    )



    st.download_button(

        label="⬇️ Download AJB-TAB PDF",

        data=pdf_output,

        file_name=
        f"AJB_TAB_{pdf_tag}.pdf",

        mime=
        "application/pdf",

        key="pdf_download"

    )


    st.success(
        "PDF ready"
    )