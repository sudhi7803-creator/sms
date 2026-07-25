# =====================================================
# AJB - TAB TEMPPLAZZA DATA LOGGER
# PART 1 - LOGIN + BASIC SETTINGS
# =====================================================


import streamlit as st
from datetime import datetime
from pathlib import Path
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
    page_title=COMPANY_NAME,
    page_icon="🌡️",
    layout="wide"
)



# =====================================================
# FOLDER SETTINGS
# =====================================================

BASE_FOLDER = Path(__file__).parent


STATE_FILE = BASE_FOLDER / "TempPlazza_state.json"



if not BASE_FOLDER.exists():

    BASE_FOLDER.mkdir()



# =====================================================
# LOAD LOGIN MEMORY
# =====================================================

def load_state():


    if STATE_FILE.exists():

        with open(
            STATE_FILE,
            "r"
        ) as file:

            return json.load(file)



    return {

        "logged_in": False,

        "username": ""

    }





# =====================================================
# SAVE LOGIN MEMORY
# =====================================================

def save_state():


    data = {

        "logged_in":
        st.session_state.logged_in,


        "username":
        st.session_state.username

    }


    with open(
        STATE_FILE,
        "w"
    ) as file:


        json.dump(
            data,
            file,
            indent=4
        )





# =====================================================
# SESSION INITIALIZATION
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


        "admin":
        "admin@123"


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

font-weight:bold;

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

            st.session_state.users[username]
            ==
            password

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
)


# =====================================================
# PART 2 - EXCEL CONNECTION MODULE
# =====================================================


from openpyxl import load_workbook
import shutil



# =====================================================
# EXCEL SETTINGS
# =====================================================


MASTER_FILE = BASE_FOLDER / "TempPlazza.xlsx"


OUTPUT_FOLDER = BASE_FOLDER / "TempPlazza_Output"


OUTPUT_FOLDER.mkdir(
    exist_ok=True
)




# =====================================================
# SESSION VARIABLES
# =====================================================


if "tower" not in st.session_state:

    st.session_state.tower = ""



if "level" not in st.session_state:

    st.session_state.level = ""



if "page_number" not in st.session_state:

    st.session_state.page_number = 1



if "excel_row" not in st.session_state:

    st.session_state.excel_row = 17





# =====================================================
# PROJECT INFORMATION
# =====================================================


st.subheader(
    "Project Information"
)



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





# =====================================================
# CREATE TOWER FILE
# =====================================================


def get_tower_file(tower_name):


    tower_file = (
        OUTPUT_FOLDER /
        f"{tower_name}.xlsx"
    )


    if not tower_file.exists():


        shutil.copy(
            MASTER_FILE,
            tower_file
        )



    return tower_file






# =====================================================
# OPEN EXCEL
# =====================================================


def open_excel():


    tower_file = get_tower_file(
        st.session_state.tower
    )


    wb = load_workbook(
        tower_file
    )


    return wb






# =====================================================
# CREATE LEVEL SHEET
# =====================================================


def get_sheet():


    wb = open_excel()


    level_name = st.session_state.level



    if level_name not in wb.sheetnames:


        source = wb.active


        new_sheet = wb.copy_worksheet(
            source
        )


        new_sheet.title = level_name




    ws = wb[level_name]



    return wb, ws






# =====================================================
# LOCK TOWER AND LEVEL
# =====================================================


if st.button(
    "🔒 Lock Tower & Level",
    key="lock_tower_level"
):


    st.session_state.tower = tower


    st.session_state.level = level


    st.session_state.page_number = 1


    st.session_state.excel_row = 17




    wb, ws = get_sheet()



    # Excel Header Update

    ws["G9"] = tower


    ws["G7"] = level





    tower_file = get_tower_file(
        tower
    )



    wb.save(
        tower_file
    )



    st.success(
        f"{tower}.xlsx created with sheet {level}"
    )







# =====================================================
# CREATE NEXT PAGE
# =====================================================


def create_new_page():


    wb = open_excel()



    base_sheet = st.session_state.level



    page = st.session_state.page_number



    new_sheet_name = (
        f"{base_sheet}_Page_{page}"
    )



    if new_sheet_name not in wb.sheetnames:


        source = wb[base_sheet]


        new_sheet = wb.copy_worksheet(
            source
        )


        new_sheet.title = new_sheet_name





    tower_file = get_tower_file(
        st.session_state.tower
    )



    wb.save(
        tower_file
    )







# =====================================================
# GET ACTIVE SHEET
# =====================================================


def get_active_sheet():


    wb = open_excel()



    if st.session_state.page_number == 1:


        ws = wb[
            st.session_state.level
        ]



    else:


        sheet_name = (

            f"{st.session_state.level}"
            f"_Page_{st.session_state.page_number}"

        )


        ws = wb[sheet_name]



    return wb, ws






# =====================================================
# EQUIPMENT INPUT FORM
# =====================================================


st.subheader(
    "Equipment Data"
)



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


    ws[f"A{row}"] = equipment_tag
    ws[f"R{row}"] = room
    ws[f"V{row}"] = set_point
    ws[f"AB{row}"] = design
    ws[f"AJ{row}"] = reading_time
    ws[f"AN{row}"] = indoor_db
    ws[f"AR{row}"] = indoor_wb
    ws[f"AV{row}"] = indoor_rh
    ws[f"AZ{row}"] = remarks



    tower_file = get_tower_file(
        st.session_state.tower
    )


    wb.save(
        tower_file
    )


    st.info(
        f"Saved File: {tower_file}"
    )


    st.success(
        f"Equipment saved in Row {row}"
    )


    st.session_state.excel_row += 1



    if st.session_state.excel_row > 33:

        st.session_state.page_number += 1

        st.session_state.excel_row = 17

        create_new_page()


        st.info(
            f"New page created: {st.session_state.page_number}"
        )
# =====================================================
# READ EQUIPMENT FROM EXCEL
# =====================================================

def get_equipment_from_excel(tag):

    wb, ws = get_active_sheet()


    for row in range(17,34):

        if ws[f"A{row}"].value == tag:

            return {

                "tag": ws[f"A{row}"].value,

                "room": ws[f"R{row}"].value,

                "set_point": ws[f"V{row}"].value,

                "design": ws[f"AB{row}"].value,

                "time": ws[f"AJ{row}"].value,

                "db": ws[f"AN{row}"].value,

                "wb": ws[f"AR{row}"].value,

                "rh": ws[f"AV{row}"].value,

                "remarks": ws[f"AZ{row}"].value

            }


    return None
# =====================================================
# PART 3 - PDF REPORT GENERATION MODULE
# =====================================================


from fpdf import FPDF




# =====================================================
# PDF CREATION FUNCTION
# =====================================================


def create_pdf(data):


    pdf = FPDF()



    pdf.add_page()



    # -------------------------
    # HEADER
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



    pdf.ln(15)




    # -------------------------
    # PROJECT INFORMATION
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

        (
            "Prepared By",
            st.session_state.username
        ),


        (
            "Date",
            datetime.now().strftime(
                "%Y-%m-%d %H:%M"
            )
        ),


        (
            "Tower",
            st.session_state.tower
        ),


        (
            "Level",
            st.session_state.level
        ),


        (
            "Page",
            str(st.session_state.page_number)
        )

    ]




    for label, value in info:


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
    # EQUIPMENT DETAILS
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


        (
            "Equipment Tag",
            data["tag"]
        ),


        (
            "Room",
            data["room"]
        ),


        (
            "Set Point",
            data["set_point"]
        ),


        (
            "Design",
            data["design"]
        ),


        (
            "Reading Time",
            data["time"]
        ),


        (
            "Indoor DB",
            data["db"]
        ),


        (
            "Indoor WB",
            data["wb"]
        ),


        (
            "Indoor RH",
            data["rh"]
        )

    ]




    for label, value in equipment:


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
    # REMARKS
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
    # FOOTER
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
# PDF REPORT SECTION
# =====================================================

st.subheader(
    "PDF Report"
)


pdf_tag = st.text_input(
    "PDF Equipment Tag",
    key="pdf_tag"
)


if st.button(
    "📄 Generate PDF",
    key="generate_pdf"
):

    data = get_equipment_from_excel(
    pdf_tag
)


if data is None:

    st.error(
        "Equipment tag not found in Excel"
    )

    st.stop()

    pdf = create_pdf(data)


    pdf_bytes = bytes(
    pdf.output(
        dest="S"
    )
    )


    st.download_button(
        label="⬇️ Download AJB-TAB PDF",

        data=pdf_bytes,

        file_name=f"AJB_TAB_{pdf_tag}.pdf",

        mime="application/pdf",

        key="pdf_download"
    )


    st.success(
        "PDF Generated Successfully"
    )# =====================================================
# DOWNLOAD EXCEL FILE
# =====================================================

st.subheader("Download Updated Excel")

if st.session_state.tower:

    excel_file = get_tower_file(
        st.session_state.tower
    )

    with open(excel_file, "rb") as f:

        st.download_button(
            label="⬇️ Download Updated Excel",
            data=f,
            file_name=f"{st.session_state.tower}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            key="download_excel"
        )