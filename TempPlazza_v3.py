# =====================================================
# AJB - TAB TEMPPLAZZA DATA LOGGER
# SINGLE MODULE
# PART 1
# LOGIN + ADMIN + SIDEBAR + SETTINGS
# =====================================================


import streamlit as st
from pathlib import Path
from datetime import datetime
import json
import os


# =====================================================
# PAGE SETTINGS
# =====================================================

st.set_page_config(
    page_title="TempPlazza",
    page_icon="🌡️",
    layout="wide"
)



# =====================================================
# APPLICATION INFORMATION
# =====================================================

APP_NAME = "AJB - TAB TempPlazza"

ADMIN_USER = "admin"


BASE_FOLDER = Path(__file__).parent


REPORT_FOLDER = BASE_FOLDER / "Reports"

PDF_FOLDER = REPORT_FOLDER / "PDF"

EXCEL_FOLDER = REPORT_FOLDER / "Excel"


for folder in [
    REPORT_FOLDER,
    PDF_FOLDER,
    EXCEL_FOLDER
]:

    folder.mkdir(
        exist_ok=True
    )



USER_FILE = BASE_FOLDER / "users.json"



# =====================================================
# USER DATABASE
# =====================================================


def load_users():

    if USER_FILE.exists():

        with open(
            USER_FILE,
            "r"
        ) as f:

            return json.load(f)


    return {

        "admin":
        "admin@123"

    }




def save_users():

    with open(
        USER_FILE,
        "w"
    ) as f:

        json.dump(
            st.session_state.users,
            f,
            indent=4
        )





# =====================================================
# SESSION START
# =====================================================


if "users" not in st.session_state:

    st.session_state.users = load_users()



if "logged_in" not in st.session_state:

    st.session_state.logged_in = False



if "username" not in st.session_state:

    st.session_state.username = ""



if "pdf_ready" not in st.session_state:

    st.session_state.pdf_ready = None



if "excel_ready" not in st.session_state:

    st.session_state.excel_ready = None





# =====================================================
# DESIGN
# =====================================================


st.markdown(
"""
<style>


[data-testid="stSidebar"] {

background-color:#f5f7fa;

}


.card {

padding:20px;

border-radius:15px;

background:white;

box-shadow:0px 2px 8px #cccccc;

text-align:center;

}



button {

border-radius:10px !important;

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
        APP_NAME
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
        "🔐 Login"
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


            st.success(
                "Login Successful"
            )


            st.rerun()



        else:


            st.error(
                "Invalid Username or Password"
            )



    st.caption(
        "AJB - TAB TempPlazza"
    )



    st.stop()





# =====================================================
# SIDEBAR MENU
# =====================================================


with st.sidebar:


    st.title(
        "☰ TempPlazza Menu"
    )



    st.write(
        f"User : {st.session_state.username}"
    )



    st.divider()



    # ---------------------------------
    # Dashboard Menu
    # ---------------------------------


    if st.button(
        "📊 Dashboard"
    ):

        st.session_state.page = "dashboard"



    # ---------------------------------
    # Excel Download
    # ---------------------------------


    st.subheader(
        "Excel"
    )



    if st.session_state.excel_ready:


        st.download_button(

    label="⬇️ Download Excel",

    data=st.session_state.excel_ready,

    file_name="TempPlazza_Report.xlsx",

    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",

    key="sidebar_excel_download"
    
    )


    else:

        st.info(
            "Excel will appear after update"
        )





    # ---------------------------------
    # PDF
    # ---------------------------------


    st.subheader(
        "Reports"
    )



    if st.button(
        "📄 Generate PDF"
    ):


        st.session_state.make_pdf = True



    if st.session_state.pdf_ready:


        st.download_button(

    label="⬇️ Download PDF",

    data=st.session_state.pdf_ready,

    file_name="TempPlazza_Report.pdf",

    mime="application/pdf",

    key="sidebar_pdf_download"

)

# =====================================================
# MAIN APPLICATION START
# =====================================================


st.title(
    "TempPlazza Dashboard"
)


st.success(
    f"Welcome {st.session_state.username}"
)
# =====================================================
# PART 2
# MAIN WORKBOOK + SUMMARY WORKBOOK
# EQUIPMENT ENTRY MODULE
# =====================================================


from openpyxl import load_workbook
import shutil



# =====================================================
# FILE SETTINGS
# =====================================================


MASTER_FILE = BASE_FOLDER / "TempPlazza.xlsx"


SUMMARY_FILE = BASE_FOLDER / "TempPlazza_Summary.xlsx"



MAIN_OUTPUT = BASE_FOLDER / "Main_Report"


MAIN_OUTPUT.mkdir(
    exist_ok=True
)





# =====================================================
# SESSION VARIABLES
# =====================================================


if "tower" not in st.session_state:

    st.session_state.tower = ""



if "level" not in st.session_state:

    st.session_state.level = ""



if "main_row" not in st.session_state:

    st.session_state.main_row = 17



if "summary_row" not in st.session_state:

    st.session_state.summary_row = 2



if "main_page" not in st.session_state:

    st.session_state.main_page = 1






# =====================================================
# CREATE TOWER WORKBOOK
# =====================================================


def get_tower_file():

    tower_file = (
        MAIN_OUTPUT /
        f"{st.session_state.tower}.xlsx"
    )


    if not tower_file.exists():

        shutil.copy(
            MASTER_FILE,
            tower_file
        )


    return tower_file






# =====================================================
# OPEN MAIN WORKBOOK
# =====================================================


def open_main_excel():



    file = get_tower_file()


    return load_workbook(
        file
    )







# =====================================================
# CREATE LEVEL SHEET
# =====================================================


def get_level_sheet():



    wb = open_main_excel()


    level_name = st.session_state.level



    if level_name not in wb.sheetnames:



        source = wb.active


        ws = wb.copy_worksheet(
            source
        )


        ws.title = level_name




    return wb, wb[level_name]







# =====================================================
# CREATE NEXT LEVEL PAGE
# =====================================================


def create_main_next_page():



    wb = open_main_excel()



    new_name = (

        f"{st.session_state.level}"
        f"_Page_{st.session_state.main_page}"

    )



    if new_name not in wb.sheetnames:



        source = wb[
            st.session_state.level
        ]


        ws = wb.copy_worksheet(
            source
        )


        ws.title = new_name




    wb.save(
        get_tower_file()
    )






# =====================================================
# SUMMARY WORKBOOK
# =====================================================


def create_summary_file():



    if not SUMMARY_FILE.exists():



        wb = load_workbook(
            MASTER_FILE
        )


        ws = wb.active


        ws.title = "Summary"



        wb.save(
            SUMMARY_FILE
        )







def open_summary():



    create_summary_file()


    return load_workbook(
        SUMMARY_FILE
    )







# =====================================================
# PROJECT INFORMATION
# =====================================================


st.subheader(
    "Project Information"
)



c1,c2 = st.columns(2)



with c1:


    tower = st.text_input(
        "Tower / Podium"
    )



with c2:


    level = st.text_input(
        "Level"
    )






# =====================================================
# LOCK TOWER LEVEL
# =====================================================


if st.button(
    "🔒 Lock Tower & Level"
):



    st.session_state.tower = tower


    st.session_state.level = level



    st.session_state.main_row = 17


    st.session_state.main_page = 1




    wb,ws = get_level_sheet()



    ws["G9"] = tower


    ws["G7"] = level




    wb.save(
        get_tower_file()
    )



    st.success(
        "Tower and Level Locked"
    )






# =====================================================
# EQUIPMENT ENTRY FORM
# =====================================================


st.subheader(
    "Equipment Test Entry"
)




col1,col2 = st.columns(2)



with col1:



    equipment_tag = st.text_input(
        "Equipment Tag"
    )


    room = st.text_input(
        "Room"
    )


    set_point = st.text_input(
        "Set Point °C"
    )


    design = st.text_input(
        "Design Temp / RH"
    )




with col2:



    reading_time = st.text_input(
        "Reading Time"
    )


    indoor_db = st.text_input(
        "Indoor DB"
    )


    indoor_wb = st.text_input(
        "Indoor WB"
    )


    indoor_rh = st.text_input(
        "Indoor RH %"
    )




remarks = st.text_area(
    "Remarks / Issue / Delay"
)







# =====================================================
# SAVE EQUIPMENT
# =====================================================


if st.button(
    "💾 Save Equipment"
):



    if not st.session_state.tower:


        st.error(
            "Lock Tower and Level first"
        )


        st.stop()





    # -----------------------------
    # MAIN WORKBOOK
    # -----------------------------


    wb,ws = get_level_sheet()



    row = st.session_state.main_row



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
        get_tower_file()
    )






   # -----------------------------
# SUMMARY WORKBOOK
# -----------------------------


swb = open_summary()


# Check Summary sheet exists

if "Summary" not in swb.sheetnames:

    sws = swb.create_sheet(
        "Summary"
    )

else:

    sws = swb["Summary"]



srow = st.session_state.summary_row



sws[f"A{srow}"] = datetime.now().date()

sws[f"B{srow}"] = st.session_state.username

sws[f"C{srow}"] = st.session_state.tower

sws[f"D{srow}"] = st.session_state.level

sws[f"E{srow}"] = equipment_tag

sws[f"F{srow}"] = room

sws[f"G{srow}"] = set_point

sws[f"H{srow}"] = design

sws[f"I{srow}"] = reading_time

sws[f"J{srow}"] = indoor_db

sws[f"K{srow}"] = indoor_wb

sws[f"L{srow}"] = indoor_rh

sws[f"M{srow}"] = remarks



swb.save(
    SUMMARY_FILE
)



st.success(
    f"Saved Equipment Row {row}"
)



st.session_state.main_row += 1


st.session_state.summary_row += 1

    # MAIN WORKBOOK PAGE LIMIT

    if st.session_state.main_row > 33:



        st.session_state.main_page += 1


        st.session_state.main_row = 17


        create_main_next_page()



        st.info(
            "New Main Workbook Page Created"
        )






    # SUMMARY LIMIT 23


    if st.session_state.summary_row > 24:


        st.session_state.summary_row = 2


        st.info(
            "New Summary Sheet Required"
        )
# =====================================================
# PART 3
# DASHBOARD + SUMMARY PDF REPORT
# =====================================================


from fpdf import FPDF



REPORT_FOLDER = BASE_FOLDER / "Reports"

PDF_FOLDER = REPORT_FOLDER / "PDF"


PDF_FOLDER.mkdir(
    parents=True,
    exist_ok=True
)





# =====================================================
# DASHBOARD
# =====================================================


st.divider()


st.subheader(
    "📊 TempPlazza Dashboard"
)



total_equipment = (
    st.session_state.summary_row - 2
)



col1,col2,col3,col4 = st.columns(4)



with col1:

    st.metric(
        "Total Tested",
        total_equipment
    )



with col2:

    st.metric(
        "Current Tower",
        st.session_state.get(
            "tower",
            "-"
        )
    )



with col3:

    st.metric(
        "Current Level",
        st.session_state.get(
            "level",
            "-"
        )
    )



with col4:

    progress = min(
        total_equipment / 23,
        1.0
    )


    st.metric(
        "Summary Progress",
        f"{int(progress*100)}%"
    )



st.progress(
    progress
)








# =====================================================
# ADMIN PREPARED NAME
# =====================================================


if "prepared_name" not in st.session_state:


    st.session_state.prepared_name = ""





if (
    st.session_state.username == ADMIN_USER
):


    with st.expander(
        "Admin PDF Name Setting"
    ):



        st.session_state.prepared_name = st.text_input(

            "Enter Prepared By Name for PDF"

        )






def get_pdf_name():



    if (
        st.session_state.username == ADMIN_USER
        and
        st.session_state.prepared_name
    ):


        return st.session_state.prepared_name



    else:


        return "Authorized User"









# =====================================================
# PDF CLASS
# =====================================================


class SummaryPDF(FPDF):


    def header(self):


        self.set_font(
            "Arial",
            "B",
            16
        )


        self.cell(
            0,
            10,
            "AJB - TAB",
            ln=True,
            align="C"
        )


        self.set_font(
            "Arial",
            "",
            12
        )


        self.cell(
            0,
            8,
            "Temperature Test Summary Report",
            ln=True,
            align="C"
        )


        self.ln(5)





    def footer(self):


        self.set_y(-15)


        self.set_font(
            "Arial",
            "I",
            8
        )


        self.cell(
            0,
            10,
            "Generated by TempPlazza",
            align="C"
        )









# =====================================================
# CREATE SUMMARY PDF
# =====================================================


def create_summary_pdf():



    pdf = SummaryPDF()



    pdf.add_page()



    pdf.set_font(
        "Arial",
        size=11
    )



    pdf.cell(
        0,
        8,
        f"Project Tower : {st.session_state.tower}",
        ln=True
    )


    pdf.cell(
        0,
        8,
        f"Level : {st.session_state.level}",
        ln=True
    )


    pdf.cell(
        0,
        8,
        f"Date : {datetime.now().strftime('%Y-%m-%d')}",
        ln=True
    )


    pdf.cell(
        0,
        8,
        f"Prepared By : {get_pdf_name()}",
        ln=True
    )



    pdf.ln(5)





    pdf.set_font(
        "Arial",
        "B",
        10
    )


    headers = [

        "Tag",
        "Room",
        "SP",
        "DB",
        "WB",
        "RH"

    ]



    widths = [

        35,
        25,
        20,
        20,
        20,
        20

    ]



    for h,w in zip(headers,widths):

        pdf.cell(
            w,
            8,
            h,
            border=1
        )


    pdf.ln()



    pdf.set_font(
        "Arial",
        size=9
    )





    wb = load_workbook(
        SUMMARY_FILE
    )


    ws = wb["Summary"]





    for row in range(
        2,
        ws.max_row+1
    ):



        pdf.cell(
            35,
            8,
            str(ws[f"E{row}"].value),
            border=1
        )


        pdf.cell(
            25,
            8,
            str(ws[f"F{row}"].value),
            border=1
        )


        pdf.cell(
            20,
            8,
            str(ws[f"G{row}"].value),
            border=1
        )


        pdf.cell(
            20,
            8,
            str(ws[f"J{row}"].value),
            border=1
        )


        pdf.cell(
            20,
            8,
            str(ws[f"K{row}"].value),
            border=1
        )


        pdf.cell(
            20,
            8,
            str(ws[f"L{row}"].value),
            border=1
        )



        pdf.ln()






    pdf.ln(10)



    pdf.set_font(
        "Arial",
        "B",
        11
    )



    pdf.cell(
        0,
        8,
        "Issue / Delay / Remarks",
        ln=True
    )



    pdf.rect(
        10,
        pdf.get_y(),
        190,
        35
    )



    pdf.ln(40)



    return pdf







# =====================================================
# PDF BUTTON
# =====================================================


st.divider()


st.subheader(
    "📄 Reports"
)




issue_text = st.text_area(
    "Add Issue / Delay Details for Report"
)



if st.button(
    "Generate Summary PDF"
):


    pdf = create_summary_pdf()



    filename = (

        f"TempPlazza_Report_"
        f"{datetime.now().strftime('%Y%m%d')}.pdf"

    )



    path = PDF_FOLDER / filename



    pdf.output(
        path
    )



    with open(
        path,
        "rb"
    ) as file:



        st.download_button(

            "⬇️ Download PDF",

            data=file,

            file_name=filename,

            mime="application/pdf"

        )



    st.success(
        "Summary PDF Generated Successfully"
    )# =====================================================
# PART 4
# FINAL SIDEBAR MENU
# =====================================================


import io



# =====================================================
# CREATE EXCEL DOWNLOAD MEMORY
# =====================================================


def get_excel_download():



    if not st.session_state.get(
        "tower"
    ):

        return None



    file = get_tower_file()



    if file.exists():


        with open(
            file,
            "rb"
        ) as f:


            return f.read()



    return None






# =====================================================
# SIDEBAR MENU
# =====================================================


with st.sidebar:



    st.title(
        "☰ TempPlazza Menu"
    )



    st.divider()



    st.write(
        "👤 Logged User"
    )



    st.info(
        st.session_state.username
    )



    st.divider()






    # ==========================
    # DOWNLOAD EXCEL
    # ==========================


    st.subheader(
        "📂 Files"
    )



    excel_data = get_excel_download()



    if excel_data:



        st.download_button(

            label="⬇️ Download Main Excel",

            data=excel_data,

            file_name=f"{st.session_state.tower}.xlsx",

            mime=
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",

            key="side_excel_download"

        )


    else:


        st.warning(
            "Save equipment first"
        )







    # ==========================
    # SUMMARY PDF
    # ==========================



    if st.button(
        "📄 Generate Summary PDF",
        key="side_pdf"
    ):


        st.session_state.generate_report = True



        st.success(
            "Go to Reports section"
        )







    st.divider()







    # ==========================
    # ADMIN ONLY
    # ==========================


    if (

        st.session_state.username
        ==
        ADMIN_USER

    ):



        with st.expander(
            "🔐 Admin Panel"
        ):



            st.subheader(
                "User Management"
            )





            # ADD USER


            new_user = st.text_input(

                "Create Username",

                key="admin_new_user"

            )



            new_password = st.text_input(

                "Create Password",

                type="password",

                key="admin_new_password"

            )





            if st.button(

                "➕ Add User",

                key="admin_add"

            ):



                if new_user and new_password:



                    st.session_state.users[new_user] = new_password



                    st.success(
                        "User Created"
                    )



                else:


                    st.error(
                        "Enter username and password"
                    )







            # REMOVE USER



            remove_user = st.text_input(

                "Remove User",

                key="admin_remove"

            )




            if st.button(

                "❌ Remove User",

                key="admin_remove_button"

            ):



                if (

                    remove_user in st.session_state.users

                    and

                    remove_user != ADMIN_USER

                ):



                    del st.session_state.users[remove_user]



                    st.success(
                        "User Removed"
                    )


                else:


                    st.error(
                        "Cannot remove admin"
                    )







            # CHANGE PASSWORD



            change_user = st.text_input(

                "Change Password User",

                key="admin_change_user"

            )



            change_password = st.text_input(

                "New Password",

                type="password",

                key="admin_change_password"

            )





            if st.button(

                "🔑 Update Password",

                key="admin_password"

            ):



                if change_user in st.session_state.users:



                    st.session_state.users[
                        change_user
                    ] = change_password



                    st.success(
                        "Password Updated"
                    )


                else:


                    st.error(
                        "User not found"
                    )







    st.divider()






    # ==========================
    # LOGOUT
    # ==========================


    if st.button(

        "🚪 Logout",

        key="final_logout"

    ):



        st.session_state.logged_in = False


        st.session_state.username = ""



        save_state()



        st.rerun()