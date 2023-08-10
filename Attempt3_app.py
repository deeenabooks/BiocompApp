from PyQt5.QtWidgets import (
    QApplication, QWidget, QTextEdit, QVBoxLayout, QPushButton, QStackedWidget,
    QLabel, QComboBox, QLineEdit, QDialog, QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox
)
from PyQt5.QtGui import QIcon, QPixmap, QPainter
from PyQt5.QtCore import Qt, QRectF , QSize
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import pdfkit
from jinja2 import Environment, FileSystemLoader
from PyQt5.QtWebEngineWidgets import QWebEngineView


import sys
import os
# Define your dictionaries for tests here
chemical_tests = {
        'extractables and leachables': [
        'Gas Chromatography (GC)',
        'Liquid Chromatography (LC)',
        'Mass Spectrometry (MS)',
        'Inductively Coupled Plasma Spectroscopy (ICP)',
        'Fourier Transform Infrared Spectroscopy (FTIR)',
        'Infrared Spectroscopy (IR)',
        'Mass Spectrometry',
        'Residual Solvents',
        'Atomic Absorption Spectroscopy (AAS)',
        'Inductively Coupled Plasma Spectroscopy (ICP)'
        ],
    'Bulk Material Characterization': [
        'Atomic Absorption Spectroscopy (AAS)',
        'Inductively Coupled Plasma Spectroscopy (ICP)',
        'Thermal Analysis',
        'Infrared Spectroscopy Analysis for Identity and Estimation of Gross Composition (Reflectance Spectroscopy, Transmission Spectroscopy)'
        ],
    'Surface Characterization': [
        'IR Reflectance Spectroscopy',
        'Scanning Electron Microscopy (SEM)'
        ]
        }

mechanical_tests = {
    'Tensile Test': 'Measures the behavior of materials under tensile load to determine its strength, stiffness, and ductility (stress, strain, yield deformation).',
    'Compression Test': 'Measures the behavior of materials under compressive load to determine its compressive strength, stiffness, and deformation.',
    'Torsion Test': 'Measures the behavior of materials under torsional load (angular) to determine its torsional strength, stiffness, and ductility.',
    'Fatigue Test': 'Measures the behavior of materials under cyclic load applied at different angles to determine its fatigue strength and fatigue life.',
    'Fracture Test': 'Measures the required energy that will cause an already cracked material to fully break.',
    'Hardness Test': 'Measures the ability of materials to resist indentation, scratching, or deformation. There are different hardness tests, such as Brinell, Rockwell, and Vickers, which use different methods to measure hardness.',
    'Impact Test': 'Measures the behavior of materials under sudden impact or shock load to determine their impact strength and toughness.',
    'Creep Test': 'Also known as stress-relaxation test, it provides an idea of the behavior of the material under a constant stress.',
    'Nondestructive Testing': 'A set of testing that provides an assessment of the material\'s mechanical property without damaging the original material properties.'
    }

biological_testing_results = {
'Cytotoxicity': 'Measures the toxicity of the material to cells.',
'Sensitization': 'Measures the potential of the material to cause an allergic reaction.',
'Irritation or Intracutaneous Reactivity': 'Measures the potential of the material to cause irritation or inflammation.',
'Systemic Toxicity': 'Measures the potential of the material to cause toxicity to the body.',
'Pyrogenicity': 'Measures the potential of the material to cause fever.',
'Subchronic Toxicity':'Measures the potential of the material to cause toxicity to the body over a period of time.',
'Genotoxicity': 'Measures the potential of the material to cause damage to the genetic information within a cell.',
'Implantation': 'Measures the potential of the material to cause toxicity to the body over a period of time.',
'Hemocompatibility': 'Measures the potential of the material to cause an adverse reaction to blood.',
'Chronic Toxicity': 'Measures the potential of the material to cause toxicity to the body over a long period of time.',
'Caricinogenicity': 'Measures the potential of the material to cause cancer.',
}
        # Define the tests and their descriptions
def create_chemical_table(tests):
    table = QTableWidget(len(tests), 2)  # Change the number of columns to 2
    table.setHorizontalHeaderLabels(["Test", "Examples"])  # Set the column headings

    row_index = 0
    for test_title, test_description in tests.items():
        item_test = QTableWidgetItem(test_title)
        item_description = QTableWidgetItem("\n".join(test_description))  # Convert the list to a string

        # Set items in the appropriate cells
        table.setItem(row_index, 0, item_test)
        table.setItem(row_index, 1, item_description)

        # Increase the row height
        table.setRowHeight(row_index, 100)  # Adjust the value (e.g., 100) as needed

        row_index += 1

    # Auto-fit columns
        table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)  # Autofit both columns
        
    return table

def create_mechanical_table(tests):
    table = QTableWidget(len(tests), 2)  # Change the number of columns to 2
    table.setHorizontalHeaderLabels(["Test", "Description"])  # Set the column headings
    
    row_index = 0  # Initialize the row index
    for test_title, test_description in tests.items():
        item_test = QTableWidgetItem(test_title)
        item_description = QTableWidgetItem(test_description)  # Set the description directly
        
        # Set items in the appropriate cells
        table.setItem(row_index, 0, item_test)
        table.setItem(row_index, 1, item_description)
        
        # Ensure that the text is displayed horizontally
        item_test.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        item_description.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        
        row_index += 1  # Increment the row index
        
    # Auto-fit columns after adding all items
    table.resizeColumnsToContents()
    table.horizontalHeader().setStretchLastSection(True)  # Stretch the last column to fill remaining space
    
    # Adjust row height to fit the content
    for row_index in range(table.rowCount()):
        table.setRowHeight(row_index, table.rowHeight(row_index) + 10)  # Adjust the value (e.g., 10) as needed
        
    return table

def create_biological_table(tests):
    table = QTableWidget(len(tests), 2)  # Change the number of columns to 2
    table.setHorizontalHeaderLabels(["Test", "Description"])  # Set the column headings
    
    row_index = 0  # Initialize the row index
    for test_title, test_description in tests.items():
        item_test = QTableWidgetItem(test_title)
        item_description = QTableWidgetItem(test_description)  # Set the description directly
        
        # Set items in the appropriate cells
        table.setItem(row_index, 0, item_test)
        table.setItem(row_index, 1, item_description)
        
        # Set text alignment to display horizontally
        item_test.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        item_description.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        
        row_index += 1  # Increment the row index
        
    # Auto-fit columns after adding all items
    table.resizeColumnsToContents()
    table.horizontalHeader().setStretchLastSection(True)  # Stretch the last column to fill remaining space
    
    # Adjust row height to fit the content
    for row_index in range(table.rowCount()):
        table.setRowHeight(row_index, table.rowHeight(row_index) + 10)  # Adjust the value (e.g., 10) as needed
        
    return table

def render_html_template(user_name, implant_name, selected_test_2, selected_test_3, selected_test_4, results):
   
    with open("biocompatablity_template.html", "r") as template_file:
        template_content = template_file.read()
        template_file.close()
    html_content = Environment(loader=FileSystemLoader('.')).from_string(template_content).render(
    user_name=user_name,
    implant_name=implant_name,
    selected_test_2=selected_test_2,
    selected_test_3=selected_test_3,
    selected_test_4=selected_test_4,
    results=results
)

    return html_content


##main window
class TextEditDemo(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Biocompatibility Test Selector")
        self.resize(500, 500)

        self.stacked_widget = QStackedWidget()
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.stacked_widget)
        self.setLayout(self.layout)

        icon_path = "healthcare.png"  # Replace with the actual path to your PNG icon
        icon = QIcon(icon_path)
        self.setWindowIcon(icon)

        self.add_initial_page()
        self.implant_name = ""  # to store the current implant name
        self.result_history = []
        self.pdf_canvas = None
        self.pdf_generation_success_messages = []        
        
    def add_initial_page(self):
        initial_page = QWidget()
        layout = QVBoxLayout()

        self.textEdit = QTextEdit("Welcome to the Biocompatibility Test Selector\n\nwhere the process of biocompatibility testing is simplified.", readOnly=True)
        layout.addWidget(self.textEdit)
        disclaimer_label = QLabel()
        disclaimer_text = """
                Disclaimer:
                This is in support of Dana Haddadin Graduation project under the supervision of Dr. Walid Al-Zyoud.
                In order to complete the bachelor degree in biomedical engineering at the German Jordanian University.
                This is only a framework of suggested tests based on the open source information by ISO and FDA and TEUV.
                """
        disclaimer_label.setText(disclaimer_text)
        disclaimer_label.setObjectName("disclaimerLabel")  # Set object name for the label
        disclaimer_label.setStyleSheet("font-style: italic;")  # Set font style to italic
        layout.addWidget(disclaimer_label)

                # Add the "main flow chart" option
        btnMainFlowChart = QPushButton("Main Flow Chart")
        btnMainFlowChart.clicked.connect(self.show_main_flow_chart)
        layout.addWidget(btnMainFlowChart)

        btnNext = QPushButton("Next")
        btnNext.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold;")
        layout.addWidget(btnNext)

        initial_page.setLayout(layout)
        self.stacked_widget.addWidget(initial_page)

        # Connect the "Next" button click event to the btnNext_Clicked method
        btnNext.clicked.connect(self.btnNext_Clicked)
    def show_main_flow_chart(self):
                # Show the main flow chart image in a pop-up dialog with zoom-out capability
        image_path = "flow2.png"  # Replace with the actual path to your main flow chart image
        if os.path.exists(image_path):
            main_flow_chart_dialog = QDialog(self)
            main_flow_chart_dialog.setWindowTitle("Main Flow Chart")
            main_flow_chart_dialog.setWindowFlags(main_flow_chart_dialog.windowFlags() |  Qt.WindowMaximizeButtonHint)  # Add maximize button
            layout = QVBoxLayout(main_flow_chart_dialog)

            scene = QGraphicsScene()
            graphics_view = QGraphicsView(scene)
            layout.addWidget(graphics_view)

            image_label = QLabel()
            pixmap = QPixmap(image_path)
            if not pixmap.isNull():
                image_label.setPixmap(pixmap)
                scene.addPixmap(pixmap)

            # Set the initial zoom-out factor to 0.5 (you can adjust this value as needed)
            graphics_view.setRenderHint(QPainter.Antialiasing)
            graphics_view.setSceneRect(QRectF(pixmap.rect()))
            graphics_view.setDragMode(QGraphicsView.ScrollHandDrag)
            graphics_view.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
            graphics_view.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
            graphics_view.setRenderHint(QPainter.Antialiasing)

            btnClose = QPushButton("Close")
            btnClose.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold;")
            btnClose.clicked.connect(main_flow_chart_dialog.accept)
            layout.addWidget(btnClose)

            main_flow_chart_dialog.setLayout(layout)
            main_flow_chart_dialog.exec_()
        else:
            QMessageBox.warning(self, "Error", "Main flow chart image not found.")

    def btnNext_Clicked(self):
        question_window = self.add_question_window()
        if question_window.exec_() == QDialog.Accepted:
            # Dialog was accepted (Answer Now button was clicked)
            self.show_result_dialog()

    def add_question_window(self):
        
        question_window = QDialog(self)
        question_window.setWindowTitle("Biocompatibility Test Questions")
        question_window.setWindowFlags(question_window.windowFlags() |  Qt.WindowMaximizeButtonHint)  # Add maximize button
        layout = QVBoxLayout(question_window)
        
        layout.addWidget(QLabel("Please enter your name:"))
        self.user_name = QLineEdit()
        layout.addWidget(self.user_name)


        layout.addWidget(QLabel("Please enter the name of the implant:"))
        self.implant_name_input = QLineEdit()
        layout.addWidget(self.implant_name_input)

        layout.addWidget(QLabel("Question 1: How long will the implant be in the body?"))
        self.combo_box_2 = QComboBox()
        self.combo_box_2.addItems(["Select Option", "Less than 24 hours", "More than 24 hours but less than 30 days", "More than 30 days"])
        layout.addWidget(self.combo_box_2)

        layout.addWidget(QLabel("Question 2 : Is the implant in contact with bone or tissue?"))
        self.combo_box_3 = QComboBox()
        self.combo_box_3.addItems(["Select Option", "Yes", "No"])
        layout.addWidget(self.combo_box_3)

        layout.addWidget(QLabel("Question 3: Is the implant considered to be an orthopedic or dental implant?"))
        self.combo_box_4 = QComboBox()
        self.combo_box_4.addItems(["Select Option", "Yes", "No"])
        layout.addWidget(self.combo_box_4)

        btnsSubmit = QPushButton("Submit")
        btnsSubmit.clicked.connect(self.btnAnswerNow_Clicked)  # Connect to the correct method
        layout.addWidget(btnsSubmit)
        
        btnBack = QPushButton("Back")
        btnBack.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold;")
        btnBack.clicked.connect(question_window.reject)
        layout.addWidget(btnBack)

        question_window.setLayout(layout)
        return question_window
    
    
    def show_pdf_generation_success(self, pdf_file_name):
        success_message = f"PDF file successfully generated: {pdf_file_name}"
        QMessageBox.information(self, "Success", success_message)
        self.pdf_generation_success_messages.append(success_message)
        
    def generate_pdf(self, user_name, implant_name, selected_test_2, selected_test_3, selected_test_4, results):
        # Create a PDF file
        pdf_file_name = f"{implant_name}_biocompatibility_test.pdf"
        
        # Create a canvas
        pdf_canvas = canvas.Canvas(pdf_file_name, pagesize=letter)
        self.pdf_canvas = pdf_canvas

        # Render the HTML template
        html_content = render_html_template(
            user_name, implant_name, selected_test_2, selected_test_3, selected_test_4,
            "Orthopedic" if selected_test_4 == "Yes" else "Not Orthopedic",
            "Bone or Other Tissues" if selected_test_3 == "Yes" else "Blood", results
        )

        # Convert HTML to PDF and save
        pdfkit.from_string(html_content, pdf_file_name)

        # Save the PDF file
        pdf_canvas.save()

        self.show_pdf_generation_success(pdf_file_name)


    def btnAnswerNow_Clicked(self):
    # Process the answers here (e.g., getting the selected options from the drop-downs and implant name from the QLineEdit)
        user_name = self.user_name.text()
        implant_name = self.implant_name_input.text()
        selected_test_2 = self.combo_box_2.currentText()
        selected_test_3 = self.combo_box_3.currentText()
        selected_test_4 = self.combo_box_4.currentText()
        
        if selected_test_2 == "Select Option" or selected_test_3 == "Select Option" or selected_test_4 == "Select Option":
                    QMessageBox.warning(self, "Error", "Please answer all questions.")
        else:
                    result_combination = (selected_test_2, selected_test_3, selected_test_4)
                    results = self.result_mappings.get(result_combination, [])
                    
                    if not results:
                        QMessageBox.warning(self, "Error", "There is an error. Please revise your answers.")
                    else:
                        self.show_result_window(user_name,implant_name, results)
                        
            # Define the mappings of answer combinations to results with detailed descriptions
            # ... your result mappings ...
    def get_required_biological_tests(*test_names):
        required_tests = {test_name: biological_testing_results[test_name] for test_name in test_names}
        return required_tests
            
    result_mappings = { 
                    ("Less than 24 hours", "Yes", "Yes"): [
                        ("Chemical Testing", chemical_tests),
                        ("Biological Testing", get_required_biological_tests(
                            'Cytotoxicity', 'Sensitization', 'Irritation or Intracutaneous Reactivity',
                            'Systemic Toxicity', 'Pyrogenicity'
                                    )),
                        ("Mechanical Testing", mechanical_tests),],
                    
                        ("Less than 24 hours", "Yes", "No"): [
                        ("Chemical Testing", chemical_tests),
                        ("Biological Testing", get_required_biological_tests(
                            'Cytotoxicity', 'Sensitization', 'Irritation or Intracutaneous Reactivity',
                            'Systemic Toxicity', 'Pyrogenicity'
                                    )),
                        ],
                        ("Less than 24 hours", "No","No"): [
                            ("Chemical Testing", chemical_tests),
                        ("Biological Testing", get_required_biological_tests(
            
                            'Cytotoxicity', 'Sensitization', 'Irritation or Intracutaneous Reactivity',
                            'Systemic Toxicity', 'Pyrogenicity', 'Genotoxicity', 'Implantation', 'Hemocompatibility', 'Subchronic Toxicity', 'Chronic Toxicity'
                                    )),
                        ],
                        
                        ("More than 24 hours but less than 30 days", "Yes", "Yes"): [
                                ("Chemical Testing", chemical_tests),
                        ("Biological Testing", get_required_biological_tests(
                            'Cytotoxicity', 'Sensitization', 'Irritation or Intracutaneous Reactivity',
                            'Systemic Toxicity', 'Pyrogenicity', 'Genotoxicity', 'Implantation','Subchronic Toxicity'
                                    )),
                                ("Mechanical Testing", mechanical_tests),
                            ],
                            ("More than 24 hours but less than 30 days", "Yes", "No"): [
                            ("Chemical Testing", chemical_tests),
                        ("Biological Testing", get_required_biological_tests(
                            'Cytotoxicity', 'Sensitization', 'Irritation or Intracutaneous Reactivity',
                            'Systemic Toxicity', 'Pyrogenicity', 'Genotoxicity', 'Implantation','Subchronic Toxicity'
                                    )),
                            ],
                            ("More than 24 hours but less than 30 days", "No", "No"): [
                                ("Chemical Testing", chemical_tests),
                        ("Biological Testing", get_required_biological_tests(
            
                            'Cytotoxicity', 'Sensitization', 'Irritation or Intracutaneous Reactivity',
                            'Systemic Toxicity', 'Pyrogenicity', 'Genotoxicity', 'Implantation', 'Hemocompatibility', 'Subchronic Toxicity'
                                    )),
                                ],
                        ("More than 30 days", "Yes", "Yes"): [
                            ("Chemical Testing", chemical_tests),
                        ("Biological Testing", get_required_biological_tests(
                            'Cytotoxicity', 'Sensitization', 'Irritation or Intracutaneous Reactivity',
                            'Systemic Toxicity', 'Pyrogenicity', 'Genotoxicity', 'Implantation', 'Hemocompatibility', 'Subchronic Toxicity', 'Chronic Toxicity', 'Caricinogenicity'
                                    )),
                            ("Mechanical Testing", mechanical_tests),
                                ],
                        ("More than 30 days", "Yes", "No"): [   
                            ("Chemical Testing", chemical_tests),
                        ("Biological Testing", get_required_biological_tests(
                            'Cytotoxicity', 'Sensitization', 'Irritation or Intracutaneous Reactivity',
                            'Systemic Toxicity', 'Pyrogenicity', 'Genotoxicity', 'Implantation', 'Hemocompatibility', 'Subchronic Toxicity', 'Chronic Toxicity', 'Caricinogenicity'
                                    )),
                                ],
                            ("More than 30 days", "No", "No"): [
                                ("Chemical Testing", chemical_tests),
                        ("Biological Testing", get_required_biological_tests(
                            'Cytotoxicity', 'Sensitization', 'Irritation or Intracutaneous Reactivity',
                            'Systemic Toxicity', 'Pyrogenicity', 'Genotoxicity', 'Implantation', 'Hemocompatibility', 'Subchronic Toxicity', 'Chronic Toxicity', 'Caricinogenicity'
                                    )),
                                    ]
            
                
                                }       
        
         
        # Check if any question has not been answered
        
    def show_result_dialog(self):
    # Show the result in a new window or QMessageBox
        user_name = self.user_name.text()
        implant_name = self.implant_name_input.text()
        selected_test_2 = self.combo_box_2.currentText()
        selected_test_3 = self.combo_box_3.currentText()
        selected_test_4 = self.combo_box_4.currentText()
        
        if selected_test_2 == "Select Option" or selected_test_3 == "Select Option" or selected_test_4 == "Select Option":
            QMessageBox.warning(self, "Error", "Please answer all questions.")
    # Get the results based on the selected answers
        result_combination = (selected_test_2, selected_test_3, selected_test_4)
        results = self.result_mappings.get(result_combination, [])
        if not results:
            QMessageBox.warning(self, "Error", "There is an error. Please revise your answers.")
        else:
            self.show_result_window(user_name,implant_name, results)
                
    def show_result_window(self, user_name, implant_name, results):
        result_window = QDialog(self)
        result_window.setWindowTitle("Biocompatibility Test Results")
        result_window.setWindowFlags(result_window.windowFlags() | Qt.WindowMaximizeButtonHint)

        layout = QVBoxLayout(result_window)

        layout.addWidget(QLabel(f"User: {user_name}"))
        layout.addWidget(QLabel(f"Implant Name: {implant_name}"))

        for result_type, result_tests in results:
            table = None

            if result_type == "Chemical Testing":
                table = create_chemical_table(result_tests)
            elif result_type == "Mechanical Testing":
                table = create_mechanical_table(result_tests)
            elif result_type == "Biological Testing":
                table = create_biological_table(result_tests)

            if table:
                layout.addWidget(table)

        print_icon = QPushButton()
        print_icon.setIcon(QIcon("download.png"))
        print_icon.setIconSize(QSize(32, 32))
        print_icon.setToolTip("Download PDF")
        print_icon.clicked.connect(lambda: self.generate_and_show_pdf(
            user_name, implant_name, selected_test_2=None, selected_test_3=None, selected_test_4=None , results=results
        ))
        layout.addWidget(print_icon)

        btnClose = QPushButton("Close")
        btnClose.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold;")
        btnClose.clicked.connect(result_window.accept)
        layout.addWidget(btnClose)

        result_window.setLayout(layout)
        result_window.exec_()
    
    def show_pdf_preview(self, html_content):
        preview_dialog = QDialog(self)
        preview_dialog.setWindowTitle("PDF Preview")
        preview_dialog.setWindowFlags(preview_dialog.windowFlags() | Qt.WindowMaximizeButtonHint)
        
        layout = QVBoxLayout(preview_dialog)
        
        webview = QWebEngineView()
        webview.setHtml(html_content)
        layout.addWidget(webview)
        
        btnClose = QPushButton("Close")
        btnClose.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold;")
        btnClose.clicked.connect(preview_dialog.accept)
        layout.addWidget(btnClose)
        
        preview_dialog.setLayout(layout)
        preview_dialog.exec_()


    def generate_and_show_pdf(self, user_name, implant_name, selected_test_2, selected_test_3, selected_test_4, results):
        
        print(f"selected_test_2: {selected_test_2}")
        print(f"selected_test_3: {selected_test_3}")
        print(f"selected_test_4: {selected_test_4}")
#printing  is wrong " User Name: g

#Implant Name: ;o

#Duration: None

#Contact Type: None

#Orthopedic or Dental: None"   the answers for  selected  test 2  was less than 24 hour , selected test 3 was yes  and selected test 4 was yes ?  the logic of the conditons are not pbeing applied 
        
        pdf_content = render_html_template(
            user_name,
            implant_name,
            selected_test_2,
            selected_test_3,
            selected_test_4,
            results
        )        
        # Show HTML content preview in a popup dialog
        self.show_pdf_preview(pdf_content)
        
        # Optionally, you can proceed to generate the actual PDF here
        pdf_file_name = f"{implant_name}_biocompatibility_test.pdf"
        pdfkit.from_string(pdf_content, pdf_file_name)
        self.show_pdf_generation_success(pdf_file_name)
        

        
if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Create and show your main window or any other windows
    win = TextEditDemo()
    win.show()

    # Start the application event loop
    sys.exit(app.exec_())
